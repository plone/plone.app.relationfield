import unittest2 as unittest
from plone.app.relationfield.testing import FUNCTIONAL_TESTING
from plone.app.relationfield.testing import IPerson, Person
from plone.app.relationfield.testing import Address

from z3c.form.interfaces import IDataManager
from plone.app.relationfield.widget import RelationListDictDataManager
from zope.component import getUtility, getMultiAdapter
from zope.app.intid.interfaces import IIntIds
from z3c.relationfield.interfaces import IRelationValue


class RelationListDictDataManagerTest(unittest.TestCase):
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        intids = getUtility(IIntIds)

        self.person = portal.person = person = Person('Roel Bruggink')
        person.__parent__ = portal

        self.addresses = person.addresses = addresses = []
        for streetname in ['Jansbinnensingel', 'Willemsplein']:
            address = Address(streetname, 'Arnhem')
            addresses.append(address)

            # five.intids' register expect aq wrapped objects, but __parent__
            # works just fine.
            address.__parent__ = portal

            intids.register(address)

    def test_get_datamanger(self):
        dm = getMultiAdapter(({}, IPerson['addresses'], ), IDataManager)
        self.assertTrue(isinstance(dm, RelationListDictDataManager))

    def test_datamanager_get_empty(self):
        dm = RelationListDictDataManager({}, IPerson['addresses'])
        self.assertEqual(dm.get(), [])

    def test_datamanager_set_empty(self):
        dm = RelationListDictDataManager({}, IPerson['addresses'])
        dm.set([])
        self.assertEqual(dm.get(), [])

    def test_datamanager_set_nonempty(self):
        dm = RelationListDictDataManager({}, IPerson['addresses'])
        dm.set(self.person.addresses)
        self.assertEqual(dm.get(), self.person.addresses)

    def test_datamanager_should_contain_relationvalues(self):
        dm = RelationListDictDataManager({}, IPerson['addresses'])
        dm.set(self.person.addresses)

        storage = dm.data['addresses']
        self.assertNotEqual(storage, [])
        self.assertNotEqual(filter(IRelationValue.providedBy, storage), [])
