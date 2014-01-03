# Support for editing RelationChoice and RelationList fields
# via plone.schemaeditor.
#
# Goal, provide a schemaeditor interface that makes it easy
# to do the most common thing: browse for relations by
# portal type -- while having it still be possible to spec
# custom sources by editing XML.
#
# Support for supermodel ex/im in exportimport.py
#
# XXX: prevent edit if field is not the editable use case.

from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.app.relationfield.interfaces import IRelationChoiceSourceBinder
from plone.schemaeditor import SchemaEditorMessageFactory as _
from plone.schemaeditor.fields import FieldFactory
from plone.schemaeditor.fields import IFieldFactory
from plone.schemaeditor.interfaces import IFieldEditFormSchema
from z3c.relationfield.interfaces import IRelationChoice
from z3c.relationfield.interfaces import IRelationList
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.app.intid.interfaces import IIntIds
from zope.component import adapter
from zope.component import adapts
from zope.component import queryUtility
from zope.interface import implementer
from zope.interface import implements

import zope.component
import zope.interface
import zope.schema


class RelationObjPathSourceBinder(ObjPathSourceBinder):
    implements(IRelationChoiceSourceBinder)

    def __init__(self, portal_types=None):
        if portal_types:
            super(RelationObjPathSourceBinder, self).__init__(
                portal_type=portal_types,
                )
        else:
            super(RelationObjPathSourceBinder, self).__init__()

    def portal_types(self):
        return self.selectable_filter.criteria.get('portal_type')


# In order to appear in schemaeditor's list of addable/
# editable fields, we need to supply a FieldFactory
# as a utility.
#
# This requires a custom FieldFactory class so that we
# can override the available method so that we don't
# show the option when it doesn't make sense.
class RelationFieldFactory(FieldFactory):
    implements(IFieldFactory)

    def available(self):
        return queryUtility(IIntIds) is not None

    def editable(self, field):
        return IRelationChoiceSourceBinder.providedBy(field.source)


RelationChoiceFactory = RelationFieldFactory(
    RelationChoice,
    _(u'label_relationchoice_field', default=u'Relation Choice'),
    source=RelationObjPathSourceBinder(),
)


class RelationListFieldFactory(FieldFactory):
    implements(IFieldFactory)

    def available(self):
        return queryUtility(IIntIds) is not None

    def editable(self, field):
        return IRelationChoiceSourceBinder.providedBy(field.value_type.source)


RelationListFactory = RelationListFieldFactory(
    RelationList,
    _(u'label_relationlist_field', default=u'Relation List'),
)


# Specify an editing interface and an adapter that will return it.

class IEditableRelationChoice(zope.schema.interfaces.IField):
    """ Add editing of portal types
    """

    portal_types = zope.schema.Set(
        title=_(u"Target types to allow for relations"),
        value_type=zope.schema.Choice(
            vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
            ),
        )


@implementer(IFieldEditFormSchema)
@adapter(IRelationChoice)
def getRelationChoiceFieldSchema(field):
    return IEditableRelationChoice


class EditableRelationChoiceField(object):
    implements(IEditableRelationChoice)
    adapts(RelationChoice)

    def __init__(self, field):
        self.__dict__['field'] = field

    def __getattr__(self, name):
        if name == 'portal_types':
            source = self.field.source
            if IRelationChoiceSourceBinder.providedBy(source):
                return source.portal_types()
            return []
        return getattr(self.field, name)

    def __setattr__(self, name, value):
        if name == 'portal_types':
            return setattr(
                self.field,
                'vocabulary',
                RelationObjPathSourceBinder(portal_types=value)
                )
        return setattr(self.field, name, value)
