# -*- coding: utf-8 -*-
from plone.app.vocabularies.catalog import CatalogSource
from plone.schemaeditor.fields import FieldFactory
from plone.schemaeditor.interfaces import IFieldEditFormSchema
from plone.schemaeditor.interfaces import IFieldFactory
from z3c.relationfield import interfaces
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.component import queryUtility
from zope.i18n import MessageFactory
from zope.interface import implementer
from zope.intid.interfaces import IIntIds


_ = MessageFactory('plone')


@implementer(IFieldFactory)
class RelationFieldFactory(FieldFactory):
    def available(self):
        return queryUtility(IIntIds) is not None


class IRelationFieldSettings(schema.interfaces.IField):

    portal_type = schema.Set(
        title=_(u'Types'),
        description=_(u'Allowed target types'),
        value_type=schema.Choice(
            title=_(u'Type'),
            vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes',
        ),
        required=False,
    )


@adapter(interfaces.IRelationChoice)
@implementer(IFieldEditFormSchema)
def getRelationChoiceEditFormSchema(field):
    return IRelationFieldSettings


class RelationChoiceEditFormAdapter(object):
    def __init__(self, field):
        self.field = field

    @property
    def portal_type(self):
        field = self.field
        types = []
        types.extend(field.source.query.get('portal_type') or [])
        return types

    @portal_type.setter
    def portal_type(self, value):
        field = self.field
        if value:
            field.source.query['portal_type'] = list(value)
        elif 'portal_type' in field.source.query:
            del field.source.query['portal_type']


RelationChoiceFactory = RelationFieldFactory(
    RelationChoice, _('Relation Choice'), source=CatalogSource()
)


@adapter(interfaces.IRelationList)
@implementer(IFieldEditFormSchema)
def getRelationListEditFormSchema(field):
    return IRelationFieldSettings


class RelationListEditFormAdapter(object):
    def __init__(self, field):
        self.field = field

    @property
    def portal_type(self):
        field = self.field.value_type
        types = []
        types.extend(field.source.query.get('portal_type') or [])
        return set(types)

    @portal_type.setter
    def portal_type(self, value):
        field = self.field.value_type
        if value:
            field.source.query['portal_type'] = list(value)
        elif 'portal_type' in field.source.query:
            del field.source.query['portal_type']


RelationListFactory = RelationFieldFactory(
    RelationList,
    _('Relation List'),
    value_type=RelationChoice(
        title=_(u'Relation Choice'), source=CatalogSource()
    ),
)
