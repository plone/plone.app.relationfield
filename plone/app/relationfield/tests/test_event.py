from plone.app.relationfield.testing import FUNCTIONAL_TESTING
from plone.app.relationfield.tests.sample_behavior import ISampleItem
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.fti import register
from plone.dexterity.utils import addContentToContainer
from plone.dexterity.utils import createContent
from plone.dexterity.utils import createContentInContainer
from Products.CMFCore.utils import getToolByName
from z3c.relationfield.relation import RelationValue
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.event import notify
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent
import unittest2 as unittest


class TestRelationCatalogUpdater(unittest.TestCase):
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        super(TestRelationCatalogUpdater, self).setUp()
        self.portal = self.layer['portal']

        self.intids = getUtility(IIntIds)
        self.relation_catalog = getUtility(ICatalog)

        fti = DexterityFTI('SampleItem')
        fti.klass = 'plone.dexterity.content.Item'
        fti.behaviors = (
            'plone.app.relationfield.tests.sample_behavior.ISampleItem', )
        fti.schema = 'plone.app.relationfield.tests.sample_behavior.ISampleSchema'

        typestool = getToolByName(self.portal, 'portal_types')
        typestool._setObject('SampleItem', fti)
        register(fti)

        self.item_a = createContentInContainer(self.portal, 'SampleItem')
        self.item_c = createContentInContainer(self.portal, 'SampleItem')

        content = createContent('SampleItem')
        ISampleItem(content).relations = [RelationValue(
            self.intids.getId(self.item_a))]
        self.item_b = addContentToContainer(self.portal, content)

    def test_relation_is_added_to_zc_relation_catalog_when_added(self):
        relations = [rel for rel in self.relation_catalog.findRelations(
            {'to_id': self.intids.getId(self.item_a)})]

        self.assertEqual(1, len(relations))
        self.assertEqual(self.intids.getId(self.item_a), relations[0].to_id)
        self.assertEqual(self.intids.getId(self.item_b), relations[0].from_id)

    def test_relation_is_updated_when_editing(self):
        ISampleItem(self.item_b).relations = [RelationValue(
            self.intids.getId(self.item_c))]
        notify(ObjectModifiedEvent(self.item_b))

        relations = [rel for rel in self.relation_catalog.findRelations(
            {'to_id': self.intids.getId(self.item_c)})]

        self.assertEqual(1, len(relations))
        self.assertEqual(self.intids.getId(self.item_c), relations[0].to_id)
        self.assertEqual(self.intids.getId(self.item_b), relations[0].from_id)
