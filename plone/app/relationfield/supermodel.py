# -*- coding: utf-8 -*-
from zope import schema
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList

from plone.supermodel.exportimport import BaseHandler
from plone.supermodel.utils import valueToElement

import pkg_resources

try:
    pkg_resources.get_distribution('plone.formwidget.contenttree')
except pkg_resources.DistributionNotFound:
    HAS_CONTENTTREE = False
else:
    HAS_CONTENTTREE = True

try:
    pkg_resources.get_distribution('plone.app.widgets')
except pkg_resources.DistributionNotFound:
    HAS_WIDGETS = False
else:
    HAS_WIDGETS = True

if HAS_CONTENTTREE:
    from plone.formwidget.contenttree import ObjPathSourceBinder


class RelationChoiceBaseHandler(BaseHandler):

    filteredAttributes = BaseHandler.filteredAttributes.copy()
    filteredAttributes.update({
        'allowedTargetTypes': 'w',
        'source': 'w',
        'vocabulary': 'w',
        'vocabularyName': 'rw'
    })

    def __init__(self, klass):
        super(RelationChoiceBaseHandler, self).__init__(klass)

        self.fieldAttributes['allowedTargetTypes'] = \
            schema.List(__name__='allowedTargetTypes',
                        title=u'Allowed target types',
                        value_type=schema.Text(title=u'Type'))

    def _constructField(self, attributes):
        allowedTargetTypes = attributes.get('allowedTargetTypes') or []
        if 'allowedTargetTypes' in attributes:
            del attributes['allowedTargetTypes']
        if HAS_CONTENTTREE:
            attributes['source'] = \
                ObjPathSourceBinder(portal_type=allowedTargetTypes)
        return super(RelationChoiceBaseHandler,
                     self)._constructField(attributes)

    def write(self, field, name, type, elementName='field'):
        element = super(RelationChoiceBaseHandler,
                        self).write(field, name, type, elementName)
        allowedTargetTypes = []
        if HAS_CONTENTTREE:
            filter_ = getattr(field.source, 'selectable_filter', None) or {}
            allowedTargetTypes.extend(
                filter_.criteria.get('portal_type') or [])

        attributeField = self.fieldAttributes['allowedTargetTypes']
        child = valueToElement(attributeField, allowedTargetTypes,
                               name='allowedTargetTypes', force=True)
        element.append(child)

        return element

RelationChoiceHandler = RelationChoiceBaseHandler(RelationChoice)
RelationListHandler = BaseHandler(RelationList)
