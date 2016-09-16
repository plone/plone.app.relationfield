# -*- coding: utf-8 -*-
from Acquisition import aq_base
from zope.interface import implementer
from zope.component import adapter
from plone.uuid.interfaces import IUUID
from plone.uuid.interfaces import ATTRIBUTE_NAME
from z3c.relationfield.interfaces import IRelationValue


@implementer(IUUID)
@adapter(IRelationValue)
def rvUUID(context):
    """ Vocabulary validation via p.a.vocabularies CatalogSource
        requires the UUID of the target object to verify membership
    """
    return getattr(aq_base(context.to_object), ATTRIBUTE_NAME, None)
