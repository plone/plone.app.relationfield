# -*- coding: utf-8 -*-
from five.intid.intid import IntIds
from five.intid.site import addUtility
from z3c.relationfield.index import RelationCatalog
from zc.relation.interfaces import ICatalog
from zope.intid.interfaces import IIntIds


def add_relations(context):
    addUtility(context, ICatalog, RelationCatalog, ofs_name='relations',
               findroot=False)


def add_intids(context):
    addUtility(context, IIntIds, IntIds, ofs_name='intids',
               findroot=False)


def installRelations(context):
    if context.readDataFile('install_relations.txt') is None:
        return
    portal = context.getSite()
    add_relations(portal)
    return 'Added relations utility.'
