# -*- coding: utf-8 -*-
from plone.schemaeditor.fields import FieldFactory
from plone.schemaeditor.interfaces import IFieldEditFormSchema
from z3c.relationfield import interfaces
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.i18n import MessageFactory
from zope.interface import implementer
import pkg_resources

_ = MessageFactory('plone')

try:
    pkg_resources.get_distribution('plone.formwidget.contenttree')
except pkg_resources.DistributionNotFound:
    HAS_CONTENTTREE = False
else:
    HAS_CONTENTTREE = True

if HAS_CONTENTTREE:
    from plone.formwidget.contenttree import ObjPathSourceBinder


class IRelationFieldSettings(schema.interfaces.IField):

    allowedTargetTypes = schema.List(
        title=_(u'Types'),
        description=_(u'Allowed target types'),
        value_type=schema.Choice(
            title=_(u'Type'),
            vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes'
        ),
        required=False
    )


@adapter(interfaces.IRelationChoice)
@implementer(IFieldEditFormSchema)
def getRelationChoiceEditFormSchema(field):
    return IRelationFieldSettings


class RelationChoiceEditFormAdapter(object):

    def __init__(self, field):
        self.field = field

    def _read_allowedTargetTypes(self):
        field = self.field
        types = []
        if HAS_CONTENTTREE:
            filter_ = getattr(field.source, 'selectable_filter', None) or {}
            types.extend(filter_.criteria.get('portal_type') or [])
        return types

    def _write_allowedTargetTypes(self, value):
        field = self.field
        if HAS_CONTENTTREE:
            filter_ = getattr(field.source, 'selectable_filter', None) or {}
            filter_.criteria['portal_type'] = value

    allowedTargetTypes = property(_read_allowedTargetTypes,
                                  _write_allowedTargetTypes)


if HAS_CONTENTTREE:
    RelationChoiceFactory = FieldFactory(
        RelationChoice, _("Relation"),
        source=ObjPathSourceBinder()
    )


@adapter(interfaces.IRelationList)
@implementer(IFieldEditFormSchema)
def getRelationListEditFormSchema(field):
    return IRelationFieldSettings


class RelationListEditFormAdapter(object):

    def __init__(self, field):
        self.field = field

    def _read_allowedTargetTypes(self):
        field = self.field.value_type
        types = []
        if HAS_CONTENTTREE:
            filter_ = getattr(field.source, 'selectable_filter', None) or {}
            types.extend(filter_.criteria.get('portal_type') or [])
        return types

    def _write_allowedTargetTypes(self, value):
        field = self.field.value_type
        if HAS_CONTENTTREE:
            filter_ = getattr(field.source, 'selectable_filter', None) or {}
            filter_.criteria['portal_type'] = value

    allowedTargetTypes = property(_read_allowedTargetTypes,
                                  _write_allowedTargetTypes)


if HAS_CONTENTTREE:
    RelationListFactory = FieldFactory(
        RelationList, _("Relation List"),
        value_type=RelationChoice(title=_(u"Related"),
                                  source=ObjPathSourceBinder())
    )
