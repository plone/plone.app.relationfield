# -*- coding: utf-8 -*-
from plone.app.relationfield import HAS_CONTENTTREE
from plone.schemaeditor.fields import FieldFactory
from plone.schemaeditor.interfaces import IFieldEditFormSchema
from z3c.relationfield import interfaces
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.i18n import MessageFactory
from zope.interface import implementer

_ = MessageFactory('plone')

if HAS_CONTENTTREE:
    from plone.formwidget.contenttree import ObjPathSourceBinder


class IRelationFieldSettings(schema.interfaces.IField):

    portal_type = schema.Set(
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

    def _read_portal_type(self):
        field = self.field
        types = []

        if HAS_CONTENTTREE:
            filter_ = getattr(field.source, 'selectable_filter', None) or {}
            types.extend(filter_.criteria.get('portal_type') or [])

        return types

    def _write_portal_type(self, value):
        field = self.field

        if HAS_CONTENTTREE:
            filter_ = getattr(field.source, 'selectable_filter', None) or {}
            if value:
                filter_.criteria['portal_type'] = value
            elif 'portal_type' in filter_.criteria:
                del filter_.criteria['portal_type']

    portal_type = property(_read_portal_type,
                           _write_portal_type)


if HAS_CONTENTTREE:
    RelationChoiceFactory = FieldFactory(
        RelationChoice, _('Relation Choice'),
        source=ObjPathSourceBinder()
    )


@adapter(interfaces.IRelationList)
@implementer(IFieldEditFormSchema)
def getRelationListEditFormSchema(field):
    return IRelationFieldSettings


class RelationListEditFormAdapter(object):

    def __init__(self, field):
        self.field = field

    def _read_portal_type(self):
        field = self.field.value_type
        types = []

        if HAS_CONTENTTREE:
            filter_ = getattr(field.source, 'selectable_filter', None) or {}
            types.extend(filter_.criteria.get('portal_type') or [])

        return set(types)

    def _write_portal_type(self, value):
        field = self.field.value_type

        if HAS_CONTENTTREE:
            filter_ = getattr(field.source, 'selectable_filter', None) or {}
            if value:
                filter_.criteria['portal_type'] = list(value)
            elif 'portal_type' in filter_.criteria:
                del filter_.criteria['portal_type']

    portal_type = property(_read_portal_type, _write_portal_type)


if HAS_CONTENTTREE:
    RelationListFactory = FieldFactory(
        RelationList, _('Relation List'),
        value_type=RelationChoice(title=_(u'Relation Choice'),
                                  source=ObjPathSourceBinder())
    )
