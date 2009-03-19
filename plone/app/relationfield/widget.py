from zope.component import adapts, getUtility
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from z3c.relationfield.interfaces import (
    IRelation,
    IRelationValue,
    IRelationList,
    )
from z3c.relationfield.schema import RelationChoice, RelationList
from z3c.relationfield.relation import RelationValue
from z3c.form.datamanager import AttributeField

from plone.supermodel.exportimport import BaseHandler

class RelationDataManager(AttributeField):
    """A data manager which uses the z3c.relationfield api to set
    relationships using a schema field."""
    adapts(Interface, IRelation)

    def get(self):
        """Gets the target"""
        rel = None
        try:
            rel = super(RelationDataManager, self).get()
        except AttributeError:
            # Not set yet
            pass
        if rel is not None:
            if rel.isBroken():
                # XXX: should log or take action here
                return
            return rel.to_object

    def set(self, value):
        """Sets the relationship target"""
        current = None
        try:
            current = super(RelationDataManager, self).get()
        except AttributeError:
            pass
        intids = getUtility(IIntIds)
        to_id = intids.getId(value)
        if IRelationValue.providedBy(current):
            # If we already have a relation, just set the to_id
            current.to_id = to_id
        else:
            # otherwise create a relationship
            rel = RelationValue(to_id)
            super(RelationDataManager, self).set(rel)


class RelationListDataManager(AttributeField):
    """A data manager which sets a list of relations"""
    adapts(Interface, IRelationList)

    def get(self):
        """Gets the target"""
        rel_list = []
        try:
            rel_list = super(RelationListDataManager, self).get()
        except AttributeError:
            # Not yet set
            pass
        resolved_list = []
        for rel in rel_list:
            if rel.isBroken():
                # XXX: should log or take action here
                continue
            resolved_list.append(rel.to_object)
        return resolved_list

    def set(self, value):
        """Sets the relationship target"""
        value = value or []
        new_relationships = []
        intids = getUtility(IIntIds)
        for item in value:
            # otherwise create one
            to_id = intids.getId(item)
            new_relationships.append(RelationValue(to_id))
        super(RelationListDataManager, self).set(new_relationships)


# plone.supermodel schema import/export handlers

RelationChoiceHandler = BaseHandler(RelationChoice)
RelationListHandler = BaseHandler(RelationList)
