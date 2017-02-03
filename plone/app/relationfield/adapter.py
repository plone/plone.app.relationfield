# -*- coding: utf-8 -*-
from Acquisition import aq_base
from plone.uuid.interfaces import ATTRIBUTE_NAME
from plone.uuid.interfaces import IUUID
from z3c.relationfield.interfaces import IRelationValue
from zope.component import adapter
from zope.interface import implementer


@implementer(IUUID)
@adapter(IRelationValue)
def rvUUID(context):
    """ Vocabulary validation via p.a.vocabularies CatalogSource
        requires the UUID of the target object to verify membership
    """
    return getattr(aq_base(context.to_object), ATTRIBUTE_NAME, None)
