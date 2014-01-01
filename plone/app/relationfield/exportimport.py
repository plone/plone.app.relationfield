from plone.app.relationfield import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.supermodel.exportimport import BaseHandler
from plone.supermodel.utils import noNS, valueToElement, elementToValue
from zope.interface import Interface
from zope.schema.interfaces import IContextSourceBinder

import zope.schema


class RelationChoiceHandlerClass(BaseHandler):
    """Special handling for the RelationChoice field
       to cover the source attribute.
       We want to write it out as a dotted name.
    """

    filteredAttributes = BaseHandler.filteredAttributes.copy()
    # we're never going to write a source to XML, and we'll have
    # a custom reader for portal_types
    filteredAttributes.update({
        'source': 'w',
        'vocabulary': 'w',
        'vocabularyName': 'w',
        'values': 'w',
        'portal_types': 'rw',
        })

    def __init__(self, klass):
        super(RelationChoiceHandlerClass, self).__init__(klass)

        self.fieldAttributes['source'] = \
            zope.schema.Object(__name__='source', title=u"Source", schema=Interface)

        self.fieldAttributes['portal_types'] = \
            zope.schema.Set(
                __name__='portal_types',
                title=u"Portal Types",
                value_type=zope.schema.TextLine(),
                )

    def _constructField(self, attributes):
        # In our override of read, we use the superclass' read before
        # looking for portal_types. It tries to construct the field,
        # so we need to make sure it doesn't fail if there's no
        # source or vocabulary attributes yet.
        if 'source' not in attributes and \
           'values' not in attributes and \
           'vocabulary' not in attributes and \
           'vocabularyName' not in attributes:
            attributes['source'] = ObjPathSourceBinder()
        return self.klass(**attributes)

    def read(self, element):
        field = super(RelationChoiceHandlerClass, self).read(element)

        for pc_element in element.iterchildren(
          '{http://namespaces.plone.org/supermodel/schema}portal_types'
          ):
            attributeField = self.fieldAttributes.get('portal_types', None)
            portal_types = self.readAttribute(pc_element, attributeField)
            if portal_types:
                portal_types = [s for s in portal_types]
                # setting vocabulary also sets source
                field.vocabulary = ObjPathSourceBinder(portal_type=portal_types)
            break

        return field

    def write(self, field, name, type, elementName='field'):

        # if field.source is not None:
        #     # The Choice field instantiates with both vocabulary and source
        #     # set to the same value. We want to be able to use the Choice
        #     # export handler, but avoid it writing out a vocabulary element.
        #     source = field.source
        #     field.vocabulary = None

        element = super(RelationChoiceHandlerClass, self).write(field, name, type, elementName)

        # write source
        # if source is not None:
        #     attributeField = self.fieldAttributes['source']
        #     child = valueToElement(
        #         attributeField,
        #         "%s.%s" % (source.__module__, source.__name__),
        #         name='source',
        #         force=True
        #         )
        #     element.append(child)

        portal_types_field = self.fieldAttributes['portal_types']
        source = field.source
        if IContextSourceBinder.providedBy(source):
            filter = getattr(source, 'selectable_filter', None)
            if filter is not None:
                criteria = filter.criteria
                portal_types = criteria.get('portal_type')
                if len(criteria.keys()) == 1 and \
                   portal_types is not None:
                    child = valueToElement(
                        portal_types_field,
                        portal_types,
                        name='portal_types',
                        force=True
                        )
                    element.append(child)

        return element


RelationChoiceHandler = RelationChoiceHandlerClass(RelationChoice)
# RelationListHandler = BaseHandler(RelationList)
