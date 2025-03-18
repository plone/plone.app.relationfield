# -*- coding: UTF-8 -*-
from plone.app.z3cform.converters import RelationChoiceRelatedItemsWidgetConverter
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.app.z3cform.widget import RelatedItemsWidget
from plone.autoform import directives
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from z3c.form.browser.text import TextWidget
from z3c.form.datamanager import AttributeField
from z3c.form.datamanager import DictionaryField
from z3c.form.interfaces import IDataConverter
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import ITextWidget
from z3c.form.interfaces import IWidget
from z3c.form.interfaces import NO_VALUE
from z3c.form.widget import FieldWidget
from z3c.relationfield.interfaces import IRelation
from z3c.relationfield.interfaces import IRelationChoice
from z3c.relationfield.interfaces import IRelationList
from z3c.relationfield.interfaces import IRelationValue
from z3c.relationfield.relation import RelationValue
from z3c.relationfield.schema import Relation
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zc.relation.interfaces import ICatalog
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from zope.schema import Choice
from zope.schema import Field
from zope.schema import List
from zope.schema._bootstrapfields import TextLine
from zope.schema.interfaces import IField
from zope.schema.interfaces import IList
from zope.security.interfaces import ForbiddenAttribute

import logging

log = logging.getLogger(__name__)


log.info("""

**************************

Backrelations are enabled!

**************************
""")


# Fields

class IBackRelation(IField):
    pass

class IBackRelationChoice(IBackRelation):
    pass

class IBackRelationList(IList):
    pass


@implementer(IBackRelation)
class BackRelation(Relation):
    pass


@implementer(IBackRelationChoice)
class BackRelationChoice(RelationChoice):
    pass


@implementer(IBackRelationList)
class BackRelationList(RelationList):
    pass



# Widget

class IBackRelatedItemsWidget(ITextWidget):
    pass


@implementer(IBackRelatedItemsWidget)
class BackRelatedItemsWidget(RelatedItemsWidget):
    pass


@adapter(IBackRelation, IPloneFormLayer)
@implementer(IFieldWidget)
def BackRelatedItemsFieldWidget(field, request, extra=None):
    if extra is not None:
        request = extra
    return FieldWidget(field, BackRelatedItemsWidget(request))


@adapter(IRelationChoice, IBackRelatedItemsWidget)
class BackRelationChoiceRelatedItemsWidgetConverter(RelationChoiceRelatedItemsWidgetConverter):

    def toWidgetValue(self, value):
        if not value:
            return self.field.missing_value
        return IUUID(value)

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        try:
            catalog = getToolByName(self.widget.context, 'portal_catalog')
        except AttributeError:
            catalog = getToolByName(getSite(), 'portal_catalog')

        res = catalog(UID=value)
        if res:
            return res[0].getObject()
        else:
            return self.field.missing_value


@adapter(Interface, IBackRelation)
class BackRelationDataManager(AttributeField):
    """Like RelationDataManager but as Backrel

    A data manager which uses the z3c.relationfield api to set
    backrelationships using a schema field."""

    def get(self):
        """Gets the source"""
        rel = None
        try:
            rel = super(BackRelationDataManager, self).get()
        except AttributeError:
            # Not set yet
            pass
        if rel is not None:
            if rel.isBroken():
                # XXX: should log or take action here
                return
            return rel.from_object

    def set(self, value):
        """Sets the relationship source"""
        if value is None:
            return super(BackRelationDataManager, self).set(None)

        current = None
        try:
            current = super(BackRelationDataManager, self).get()
        except AttributeError:
            pass
        intids = getUtility(IIntIds)
        # import pdb; pdb.set_trace()
        # to_id = intids.getId(self.context)
        to_id = intids.getId(value)
        if IRelationValue.providedBy(current):
            # If we already have a relation, just set the to_id
            current.to_id = to_id
        else:
            # otherwise create a relationship
            rel = RelationValue(to_id)
            super(BackRelationDataManager, self).set(rel)


@adapter(Interface, IBackRelationList)
class BackRelationListDataManager(AttributeField):
    """Like RelationListDataManager but as Backrel

    A data manager which sets a list of relations"""

    def get(self):
        """Gets the target"""
        rel_list = []

        # Calling query() here will lead to infinite recursion!
        try:
            rel_list = super(BackRelationListDataManager, self).get()

        except AttributeError:
            rel_list = None

        if not rel_list:
            return []

        resolved_list = []
        for rel in rel_list:
            if rel.isBroken():
                # XXX: should log or take action here
                continue
            resolved_list.append(rel.to_object)
        return resolved_list

    def set(self, value):
        """Sets the relationship target"""
        value = value or []
        new_relationships = []
        intids = getUtility(IIntIds)
        for item in value:
            # otherwise create one
            to_id = intids.getId(item)
            new_relationships.append(RelationValue(to_id))
        super(BackRelationListDataManager, self).set(new_relationships)


def _setRelation_patched(obj, name, value):
    """Set a relation on an object.

    Sets up various essential attributes on the relation.
    """
    # if the Relation is None, we're done
    if value is None:
        return
    is_backrelation = False
    intids = getUtility(IIntIds)

    # the current object (the one that was modified)
    this_obj = obj
    this_id = intids.getId(this_obj)

    # the other object (the one that this has a relation to or from)
    other_id = value.to_id
    other_obj = intids.getObject(other_id)

    # 1. Configure the RelationValue that was already set on the current object
    fti = getUtility(IDexterityFTI, name=obj.portal_type)
    field_and_schema = get_field_and_schema_for_fieldname(name, fti)
    if field_and_schema:
        field, schema = field_and_schema
        if isinstance(field, (BackRelation, BackRelationChoice, BackRelationList)):
            # 1.1. Set value as Backrelation
            is_backrelation = True
            _set_backrelation(obj, name, value)

        elif isinstance(field, (Relation, RelationChoice, RelationList)):
            # 1.2. Set value as Relation. This is the normal default in Plone
            from z3c.relationfield.event import _old__setRelation
            _old__setRelation(obj, name, value)

    # 2. Configure a new RelationValue on the other object if there is a equivalent field
    fti = getUtility(IDexterityFTI, name=other_obj.portal_type)
    field_and_schema = get_field_and_schema_for_fieldname(name, fti)
    rel = None
    if field_and_schema:
        field, schema = field_and_schema
        if is_backrelation and isinstance(field, (Relation, RelationChoice)):
            # 2.1.1 Set a Relation for the backrelation
            log.info('Set a Relation for the backrelation')
            rel = RelationValue(this_id)
            rel.__parent__ = other_obj
            # also set from_object to parent object
            rel.from_object = other_obj
            # and the attribute to the attribute name
            rel.from_attribute = name
            setattr(other_obj, name, rel)

        elif is_backrelation and isinstance(field, RelationList):
            # 2.1.2 Add a Relation to Relationlist for the Backrelation
            log.info('Add a Relation to Relationlist for the backrelation')
            rel = RelationValue(this_id)
            rel.__parent__ = other_obj
            # also set from_object to parent object
            rel.from_object = other_obj
            # and the attribute to the attribute name
            rel.from_attribute = name
            setattr(other_obj, name, [rel])

        elif not is_backrelation and isinstance(field, (BackRelation, BackRelationChoice)):
            # 2.2.1 Set a Backrelation for the relation
            log.info('Set a Backrelation for the relation')
            rel = RelationValue(other_id)
            rel.__parent__ = other_obj
            # also set from_object to parent object
            rel.from_object = this_obj
            # and the attribute to the attribute name
            rel.from_attribute = name
            setattr(other_obj, name, rel)

        elif not is_backrelation and isinstance(field, RelationList):
            # 2.2.2 Add a Relation for the backrelationlist
            log.info('Add a Backrelation to the Relationlist for the relation')
            rel = RelationValue(other_id)
            rel.__parent__ = other_obj
            # also set from_object to parent object
            rel.from_object = this_obj
            # and the attribute to the attribute name
            rel.from_attribute = name
            setattr(other_obj, name, [rel])

        else:
            # 2.3 Relations of the same type point at each other!
            log.warn('Warning: Backrelation points to backrelation or relation to relation')
        return


    if is_backrelation and not field_and_schema:
        log.warn('Warning: No Relationfield {} on {} for Backrelationfield on {}!'.format(
            name, other_obj.portal_type, obj.portal_type))

    if not is_backrelation and not field_and_schema:
        log.info('Info: No Backrelationfield {} on {} for Relationfield on {}!'.format(
            name, other_obj.portal_type, obj.portal_type))

    if rel:
        rel_id = intids.register(rel)
        # and index the relation with the catalog
        catalog.index_doc(rel_id, rel)

    return

# TODO
# Subscriber to remove backrelations if the relation was changed.


def get_field_and_schema_for_fieldname(field_id, fti):
    """Get field and its schema from a fti.
    """
    from plone.dexterity.utils import iterSchemataForType
    # Turn form.widgets.IDublinCore.title into title
    field_id = field_id.split('.')[-1]
    for schema in iterSchemataForType(fti):
        field = schema.get(field_id, None)
        if field is not None:
            return (field, schema)
