# -*- coding: utf-8 -*-
from plone.app.relationfield import HAS_CONTENTTREE
from plone.app.relationfield import HAS_WIDGETS
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.model import Fieldset
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import Interface
from zope.interface import alsoProvides

if HAS_CONTENTTREE and not HAS_WIDGETS:
    from plone.formwidget.contenttree import ObjPathSourceBinder

try:
    from plone.app.dexterity import MessageFactory as _
except ImportError:
    def MessageFactory(messageid, default=None):
        return unicode(default)
    _ = MessageFactory


class IRelatedItems(Interface):
    """Behavior interface to make a Dexterity type support related items.
    """

    if HAS_CONTENTTREE and not HAS_WIDGETS:

        relatedItems = RelationList(
            title=_(u'label_related_items', default=u'Related Items'),
            default=[],
            value_type=RelationChoice(
                title=u"Related",
                source=ObjPathSourceBinder()
            ),
            required=False
        )

    else:

        relatedItems = RelationList(
            title=_(u'label_related_items', default=u'Related Items'),
            default=[],
            value_type=RelationChoice(
                title=u"Related",
                vocabulary="plone.app.vocabularies.Catalog"
            ),
            required=False
        )

fieldset = Fieldset('categorization',
                    label=_(u'Categorization'), fields=['relatedItems'])
IRelatedItems.setTaggedValue(FIELDSETS_KEY, [fieldset])

alsoProvides(IRelatedItems, IFormFieldProvider)
