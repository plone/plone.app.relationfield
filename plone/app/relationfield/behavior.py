# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.model import Fieldset
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import alsoProvides
from plone.autoform import directives as form
from plone.supermodel import model
from plone.app.dexterity import MessageFactory as _
from plone.app.z3cform.widget import RelatedItemsFieldWidget


class IRelatedItems(model.Schema):
    """Behavior interface to make a Dexterity type support related items.
    """

    relatedItems = RelationList(
        title=_(u'label_related_items', default=u'Related Items'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False
    )
    form.widget('relatedItems', RelatedItemsFieldWidget,
                vocabulary='plone.app.vocabularies.Catalog')

fieldset = Fieldset('categorization',
                    label=_(u'Categorization'), fields=['relatedItems'])
IRelatedItems.setTaggedValue(FIELDSETS_KEY, [fieldset])

alsoProvides(IRelatedItems, IFormFieldProvider)
