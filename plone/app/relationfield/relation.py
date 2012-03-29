#!/usr/bin/python
# -*- coding: utf-8 -*-
from z3c.relationfield.relation import RelationValue as ORelationValue, \
    _object, _path
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
from zc.relation.interfaces import ICatalog


class RelationValue(ORelationValue):
    plone_app_relation = True
    def __init__(self, to_id):
        self._from_id = None
        super(RelationValue, self).__init__(to_id)

    @property
    def from_object(self):
        if self.from_id:
            return _object(self._from_id)
        else:
            return None

    @from_object.setter
    def from_object(self, obj):
        if not obj:
            return
        intids = getUtility(IIntIds)
        if not intids.queryId(obj):
            intids.register(obj)
        self._from_id = intids.getId(obj)

    @property
    def from_id(self):
        return self._from_id

    @property
    def from_path(self):
        return _path(self.from_object)

def convert(relation):
    if getattr(relation, 'plone_app_relation', False):
        return
    def inner_convert(relation):
        if getattr(relation, 'plone_app_relation', False):
            return None
        new_relation = RelationValue(relation.to_id)
        new_relation.from_object = relation.from_object
        new_relation.__parent__ = relation.__parent__
        new_relation.from_attribute = relation.from_attribute
        return new_relation
    source = relation.from_object
    relations_from_source = getattr(source, relation.from_attribute)
    if isinstance(relations_from_source, list):
        setattr(source, relation.from_attribute, 
            [inner_convert(relation) or relation for relation in 
            relations_from_source])
    else:
        setattr(source, relation.from_attribute,
            inner_convert(relation) or relation)
    return source
