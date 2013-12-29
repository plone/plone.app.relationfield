from plone.app.relationfield import RelationChoice, RelationList
from plone.supermodel.exportimport import BaseHandler
from plone.supermodel.utils import noNS, valueToElement, elementToValue
from zope.interface import Interface

import zope.schema


class RelationChoiceHandlerClass(BaseHandler):
    """Special handling for the RelationChoice field
       to cover the source attribute.
       We want to write it out as a dotted name.
    """

    filteredAttributes = BaseHandler.filteredAttributes.copy()
    filteredAttributes.update({'source': 'w', })

    def __init__(self, klass):
        super(RelationChoiceHandlerClass, self).__init__(klass)

        self.fieldAttributes['source'] = \
            zope.schema.Object(__name__='source', title=u"Source", schema=Interface)

    def write(self, field, name, type, elementName='field'):

        if field.source is not None:
            # The Choice field instantiates with both vocabulary and source
            # set to the same value. We want to be able to use the Choice
            # export handler, but avoid it writing out a vocabulary element.
            source = field.source
            field.vocabulary = None

        element = super(RelationChoiceHandlerClass, self).write(field, name, type, elementName)

        # write source
        if source is not None:
            attributeField = self.fieldAttributes['source']
            child = valueToElement(
                attributeField,
                "%s.%s" % (source.__module__, source.__name__),
                name='source',
                force=True
                )
            element.append(child)

        return element


RelationChoiceHandler = RelationChoiceHandlerClass(RelationChoice)
RelationListHandler = BaseHandler(RelationList)
