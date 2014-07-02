from plone.testing import Layer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import FunctionalTesting


class PloneAppRelationfieldFixture(Layer):
    defaultBases = (PLONE_FIXTURE,)


FIXTURE = PloneAppRelationfieldFixture()
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name="plone.app.relationfield:Functional")
