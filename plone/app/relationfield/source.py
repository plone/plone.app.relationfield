# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from z3c.formwidget.query.interfaces import IQuerySource
from zope.component import getUtility
from zope.interface import implementer
from zope.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IQuerySource)
class CMFContentSearchSource(object):
    def __init__(self, context):
        self.context = context
        self.intid_utility = getUtility(IIntIds)

    def __contains__(self, term):
        return self.intid_utility.queryId(term) is not None

    def __iter__(self):
        return [].__iter__()

    def __len__(self):
        return 0

    def getTerm(self, obj):
        return SimpleVocabulary.createTerm(
            obj, self.intid_utility.getId(obj), obj.Title()
        )

    def getTermByToken(self, value):
        return self.getTerm(self.intid_utility.getObject(int(value)))

    def search(self, query_string):
        catalog = getToolByName(self.context, 'portal_catalog')
        result = catalog(
            SearchableText='{0:s}*'.format(query_string), sort_limit=20
        )
        terms = []
        for brain in result:
            try:
                term = self.getTerm(brain.getObject())
            except KeyError:
                # An object without an intid in the catalog results
                continue
            terms.append(term)
        return terms
