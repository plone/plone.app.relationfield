# import unittest
# from zope.testing import doctest
# import zope.component.testing

# class UnitTestLayer:

#     @classmethod
#     def testTearDown(cls):
#         zope.component.testing.tearDown()

# def test_suite():

#     marshaler = doctest.DocFileSuite('marshaler.txt', optionflags=doctest.ELLIPSIS)
#     marshaler.layer = UnitTestLayer

#     return unittest.TestSuite((marshaler,))


from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.testing import layered
from plone.testing import z2


import doctest
import unittest


class PloneAppRelationFieldLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        import plone.app.dexterity
        self.loadZCML(name='meta.zcml', package=plone.app.dexterity)
        self.loadZCML(package=plone.app.dexterity)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.dexterity:testing')
        self.applyProfile(portal, 'plone.app.relationfield:default')


MY_PRODUCT_FIXTURE = PloneAppRelationFieldLayer()
MY_PRODUCT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MY_PRODUCT_FIXTURE,),
    name="PloneAppRelationFieldLayer:Integration")

optionflags = (doctest.ELLIPSIS |
              doctest.NORMALIZE_WHITESPACE)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('exportimport.txt', optionflags=optionflags),
                MY_PRODUCT_INTEGRATION_TESTING)
    ])

    return suite


if __name__ == '__main__':
    unittest.main(default='test_suite')
