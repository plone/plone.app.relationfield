from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import FunctionalTesting

import zope.interface
import zope.schema

from z3c.relationfield import RelationList
from z3c.relationfield.interfaces import IHasRelations
from persistent import Persistent


class IAddress(zope.interface.Interface):
    streetname = zope.schema.TextLine(title=u'Street name')
    city = zope.schema.TextLine(title=u'City')


@zope.interface.implementer(IAddress, IHasRelations)
class Address(Persistent):
    __name__ = u''
    streetname = u''
    city = u''

    def __init__(self, streetname, city):
        self.streetname = streetname
        self.city = city
        __name__ = '{streetname} - {city}'.format(**locals())


class IPerson(zope.interface.Interface):
    name = zope.schema.TextLine(
        title=u'Name',
        default=u'<no name>')
    phone = zope.schema.TextLine(
        title=u'Phone')
    addresses = RelationList(title=u'Addresses')


@zope.interface.implementer(IPerson, IHasRelations)
class Person(Persistent):
    name = u''

    def __init__(self, name):
        self.name = name


class PloneAppRelationfieldFixture(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import plone.app.relationfield
        self.loadZCML(package=plone.app.relationfield)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.relationfield:default')


FIXTURE = PloneAppRelationfieldFixture()
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name="plone.app.relationfield:Functional")
