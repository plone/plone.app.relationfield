# -*- coding: utf-8 -*-
from persistent import Persistent
from plone.app.relationfield import HAS_CONTENTTYPES
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from z3c.relationfield import RelationList
from z3c.relationfield.interfaces import IHasRelations
from zope.interface import implementer
from zope.interface import Interface

import zope.schema


if HAS_CONTENTTYPES:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE


class IAddress(Interface):
    streetname = zope.schema.TextLine(title=u'Street name')
    city = zope.schema.TextLine(title=u'City')


@implementer(IAddress, IHasRelations)
class Address(Persistent):
    __name__ = u''
    streetname = u''
    city = u''

    def __init__(self, streetname, city):
        self.streetname = streetname
        self.city = city
        __name__ = '{streetname} - {city}'.format(**locals())


class IPerson(zope.interface.Interface):
    name = zope.schema.TextLine(title=u'Name', default=u'<no name>')
    phone = zope.schema.TextLine(title=u'Phone')
    addresses = RelationList(title=u'Addresses')


@implementer(IPerson, IHasRelations)
class Person(Persistent):
    name = u''

    def __init__(self, name):
        self.name = name


class PloneAppRelationfieldFixture(PloneSandboxLayer):
    if HAS_CONTENTTYPES:
        defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)
    else:
        defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.relationfield

        self.loadZCML(package=plone.app.relationfield)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.relationfield:default')


FIXTURE = PloneAppRelationfieldFixture()
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='plone.app.relationfield:Functional'
)


class PloneAppRelationfieldContentTreeFixture(PloneSandboxLayer):

    if HAS_CONTENTTYPES:
        defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)
    else:
        defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)

        import plone.formwidget.contenttree

        self.loadZCML(package=plone.formwidget.contenttree)

        import plone.app.relationfield

        self.loadZCML(package=plone.app.relationfield)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.dexterity:default')
        self.applyProfile(portal, 'plone.formwidget.contenttree:default')
        self.applyProfile(portal, 'plone.app.relationfield:default')


CONTENTTREE_FIXTURE = PloneAppRelationfieldContentTreeFixture()

FUNCTIONAL_CONTENTTREE_TESTING = FunctionalTesting(
    bases=(CONTENTTREE_FIXTURE,),
    name='plone.app.relationfield.contenttree:Functional',
)


class PloneAppRelationfieldWidgetsFixture(PloneSandboxLayer):

    if HAS_CONTENTTYPES:
        defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)
    else:
        defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)

        import plone.app.widgets

        self.loadZCML(package=plone.app.widgets)

        import plone.app.relationfield

        self.loadZCML(package=plone.app.relationfield)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.dexterity:default')
        self.applyProfile(portal, 'plone.app.relationfield:default')


WIDGETS_FIXTURE = PloneAppRelationfieldWidgetsFixture()

FUNCTIONAL_WIDGETS_TESTING = FunctionalTesting(
    bases=(WIDGETS_FIXTURE,),
    name='plone.app.relationfield.contenttree:Functional',
)
