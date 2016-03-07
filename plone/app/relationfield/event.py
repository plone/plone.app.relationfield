# -*- coding: utf-8 -*-
from plone.behavior.interfaces import IBehaviorAssignable
from z3c.relationfield.event import _setRelation
from z3c.relationfield.interfaces import IRelation
from z3c.relationfield.interfaces import IRelationList
from zope.schema import getFields


def extract_relations(obj):
    assignable = IBehaviorAssignable(obj, None)
    if assignable is None:
        return
    for behavior in assignable.enumerateBehaviors():
        if behavior.marker == behavior.interface:
            continue
        for name, field in getFields(behavior.interface).items():
            if IRelation.providedBy(field):
                try:
                    relation = getattr(behavior.interface(obj), name)
                except AttributeError:
                    continue
                yield behavior.interface, name, relation
            if IRelationList.providedBy(field):
                try:
                    rel_list = getattr(behavior.interface(obj), name)
                except AttributeError:
                    continue
                if rel_list is not None:
                    for relation in rel_list:
                        yield behavior.interface, name, relation


def update_behavior_relations(obj, event):
    """Re-register relations in behaviors
    """
    for behavior_interface, name, relation in extract_relations(obj):
        _setRelation(obj, name, relation)
