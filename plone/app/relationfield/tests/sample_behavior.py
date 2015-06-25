from plone.app.dexterity import MessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import alsoProvides
from zope.interface import Interface


class ISampleItemMarker(Interface):
    """Marker Interface
    """


class ISampleItem(model.Schema):

    relations = RelationList(
        title=_(u'label_related_items', default=u'Related Items'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False
    )

alsoProvides(ISampleItem, IFormFieldProvider)


class ISampleSchema(model.Schema):
    """Base schema for the sample item.
    """
