from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.testing import layered

import doctest
import unittest


class PloneAppRelationFieldLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.dexterity
        self.loadZCML(name='meta.zcml', package=plone.app.dexterity)
        self.loadZCML(package=plone.app.dexterity)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.dexterity:testing')
        self.applyProfile(portal, 'plone.app.relationfield:default')


PARF_FIXTURE = PloneAppRelationFieldLayer()
PARF_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PARF_FIXTURE,),
    name="PloneAppRelationFieldLayer:Integration")

optionflags = (doctest.ELLIPSIS |
              doctest.NORMALIZE_WHITESPACE)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('exportimport.txt', optionflags=optionflags),
                PARF_INTEGRATION_TESTING)
    ])
    suite.addTests([
        layered(doctest.DocFileSuite('marshaler.txt', optionflags=optionflags),
                PARF_INTEGRATION_TESTING)
    ])

    return suite


if __name__ == '__main__':
    unittest.main(default='test_suite')
