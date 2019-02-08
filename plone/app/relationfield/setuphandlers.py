# -*- coding: utf-8 -*-
from five.intid.intid import IntIds
from five.intid.site import addUtility
from z3c.relationfield.index import RelationCatalog
from z3c.relationfield.interfaces import IRelationValue
from zc.relation.interfaces import ICatalog
from zope.intid.interfaces import IIntIds

import BTrees


PLONE_RELATION_INDEXES = [
    {'element': IRelationValue['from_id']},
    {'element': IRelationValue['to_id']},
    {
        'element': IRelationValue['from_attribute'],
        'kwargs': {'btree': BTrees.family32.OI},
    },
]


def relation_catalog_factory():
    return RelationCatalog(indexes=PLONE_RELATION_INDEXES)


def add_relations(context):
    addUtility(
        context,
        ICatalog,
        relation_catalog_factory,
        ofs_name='relations',
        findroot=False,
    )


def add_intids(context):
    addUtility(context, IIntIds, IntIds, ofs_name='intids', findroot=False)


def installRelations(context):
    if context.readDataFile('install_relations.txt') is None:
        return
    portal = context.getSite()
    add_relations(portal)
    return 'Added relations utility.'
