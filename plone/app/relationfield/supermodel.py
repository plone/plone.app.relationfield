# -*- coding: utf-8 -*-
from plone.app.vocabularies.catalog import CatalogSource
from plone.supermodel.exportimport import BaseHandler
from plone.supermodel.utils import valueToElement
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class RelationChoiceBaseHandler(BaseHandler):

    filteredAttributes = BaseHandler.filteredAttributes.copy()
    filteredAttributes.update(
        {
            'portal_type': 'w',
            'source': 'rw',
            'vocabulary': 'rw',
            'vocabularyName': 'rw',
        }
    )

    def __init__(self, klass):
        super(RelationChoiceBaseHandler, self).__init__(klass)

        self.fieldAttributes['portal_type'] = schema.List(
            __name__='portal_type',
            title=u'Allowed target types',
            value_type=schema.Text(title=u'Type'),
        )

    def _constructField(self, attributes):
        portal_type = (
            attributes.get('portal_type')
            or attributes.get('portal_types')
            or []
        )
        if 'portal_type' in attributes:
            del attributes['portal_type']

        if not portal_type:
            attributes['source'] = CatalogSource()
        else:
            attributes['source'] = CatalogSource(portal_type=portal_type)

        return super(RelationChoiceBaseHandler, self)._constructField(
            attributes
        )

    def write(self, field, name, type, elementName='field'):
        element = super(RelationChoiceBaseHandler, self).write(
            field, name, type, elementName
        )
        portal_type = []

        portal_type.extend(field.source.query.get('portal_type') or [])

        if portal_type:
            attributeField = self.fieldAttributes['portal_type']
            child = valueToElement(
                attributeField, portal_type, name='portal_type', force=True
            )
            element.append(child)

        return element


RelationChoiceHandler = RelationChoiceBaseHandler(RelationChoice)
RelationListHandler = BaseHandler(RelationList)
