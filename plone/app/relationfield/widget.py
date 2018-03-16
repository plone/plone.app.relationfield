# -*- coding: utf-8 -*-
from z3c.form.datamanager import AttributeField
from z3c.form.datamanager import DictionaryField
from z3c.form.interfaces import NO_VALUE
from z3c.relationfield.interfaces import IRelation
from z3c.relationfield.interfaces import IRelationList
from z3c.relationfield.interfaces import IRelationValue
from z3c.relationfield.relation import RelationValue
from zope.component import adapter
from zope.component import getUtility
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from zope.security.interfaces import ForbiddenAttribute


@adapter(Interface, IRelation)
class RelationDataManager(AttributeField):
    """A data manager which uses the z3c.relationfield api to set
    relationships using a schema field."""

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
        if value is None:
            return super(RelationDataManager, self).set(None)

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


@adapter(dict, IRelation)
class RelationDictDataManager(DictionaryField):
    """A data manager which uses the z3c.relationfield api to set
    relationships using a schema field, for dict-like contexts."""

    def get(self):
        """Gets the target"""
        rel = None
        try:
            rel = super(RelationDictDataManager, self).get()
        except AttributeError:
            # Not set yet
            pass
        if rel is not None:
            if rel.isBroken():
                # XXX: should log or take action here
                return
            return rel.to_object

    def query(self, default=NO_VALUE):
        """See z3c.form.interfaces.IDataManager"""
        try:
            return self.get()
        except ForbiddenAttribute as e:
            raise e
        except AttributeError:
            if default == NO_VALUE:
                return super(RelationDictDataManager, self).query()
            else:
                return default

    def set(self, value):
        """Sets the relationship target"""
        if value is None:
            return super(RelationDictDataManager, self).set(None)

        current = None
        try:
            current = super(RelationDictDataManager, self).get()
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
            super(RelationDictDataManager, self).set(rel)


@adapter(Interface, IRelationList)
class RelationListDataManager(AttributeField):
    """A data manager which sets a list of relations"""

    def get(self):
        """Gets the target"""
        rel_list = []

        # Calling query() here will lead to infinite recursion!
        try:
            rel_list = super(RelationListDataManager, self).get()

        except AttributeError:
            rel_list = None

        if not rel_list:
            return []

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


@adapter(dict, IRelationList)
class RelationListDictDataManager(DictionaryField):
    """A data manager which sets a list of relations on dictionary"""

    def get(self):
        """Gets the target"""
        rel_list = []

        # Calling query() here will lead to infinite recursion!
        try:
            rel_list = super(RelationListDictDataManager, self).get()
        except AttributeError:
            rel_list = None

        if not rel_list:
            return []

        resolved_list = []
        for rel in rel_list:
            if rel.isBroken():
                # XXX: should log or take action here
                continue
            resolved_list.append(rel.to_object)
        return resolved_list

    def query(self, default=NO_VALUE):
        """See z3c.form.interfaces.IDataManager"""
        try:
            return self.get()
        except ForbiddenAttribute as e:
            raise e
        except AttributeError:
            return default

    def set(self, value):
        """Sets the relationship target"""
        value = value or []
        new_relationships = []
        intids = getUtility(IIntIds)
        for item in value:
            # otherwise create one
            to_id = intids.getId(item)
            new_relationships.append(RelationValue(to_id))
        super(RelationListDictDataManager, self).set(new_relationships)
