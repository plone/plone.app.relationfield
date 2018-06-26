# -*- coding: utf-8 -*-
from plone.rfc822.defaultfields import BaseFieldMarshaler
from z3c.relationfield import RelationValue

import six


class RelationFieldMarshaler(BaseFieldMarshaler):
    """Field marshaler for z3c.relationfield IRelation and IRelationChoice
    fields
    """

    ascii = True

    def encode(self, value, charset='utf-8', primary=False):
        if value is None:
            return None
        return str(value.to_id)

    def decode(
        self,
        value,
        message=None,
        charset='utf-8',
        contentType=None,
        primary=False,
    ):
        if isinstance(value, six.binary_type):
            value = value.decode(charset)
        try:
            toId = int(value)
        except TypeError as e:
            raise ValueError(e)
        return RelationValue(toId)
