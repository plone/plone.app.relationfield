Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

3.0.3 (2023-06-01)
------------------

Bug fixes:


- Removed unneeded dependency on plone.app.dexterity.
  It remains a test dependency though.
  [maurits] (#1)


Internal:


- Update configuration files.
  [plone devs] (53dc5b4c)


3.0.2 (2023-04-15)
------------------

Internal:


- Update configuration files.
  [plone devs] (5623f8b3)


3.0.1 (2022-12-05)
------------------

Bug fixes:


- Remove deprecated ``plone.app.widgets`` code.
  [petschki] (#36)


3.0.0 (2022-11-30)
------------------

Bug fixes:


- Final release.
  [gforcada] (#600)


3.0.0b2 (2022-10-11)
--------------------

Bug fixes:


- Fix admin password in tests. [davisagli] (#35)


3.0.0b1 (2022-10-02)
--------------------

Bug fixes:


- Use longer password in tests. [davisagli] (#34)


3.0.0a1 (2021-08-04)
--------------------

Breaking changes:


- Update tests for Barceloneta LTS
  [petschki] (#32)


2.0.3 (2020-10-12)
------------------

Bug fixes:


- Update tests to fix updated schema cache.
  See https://github.com/plone/plone.dexterity/pull/137
  [@avoinea] (#30)


2.0.2 (2020-04-20)
------------------

Bug fixes:


- Minor packaging updates. (#1)


2.0.1 (2019-04-26)
------------------

Bug fixes:


- Added name "plone.relateditems" to behavior for further use of named behaviors. [iham] (#27)


2.0.0 (2019-02-13)
------------------

Breaking changes:


- Remove availability of interface indexes on relation catalog. Those broke if
  interfaces were removed. Plone itself never used those indexes. [jensens]
  (#26)


1.4.3 (2018-12-28)
------------------

Bug fixes:

- Remove installation of plone.app.widgets default profile in tests.
  In Plone 5.0/5.1 with plone.app.widgets >= 2.0, the profile is only a dummy profile for BBB.
  In Plone 5.2 will be removed.
  [jensens]


1.4.2 (2018-09-28)
------------------

Bug fixes:

- Change import of message factory from dx to non-deprecated way.
  [jensens]

- Fix tests in py3
  [pbauer]


1.4.1 (2018-06-19)
------------------

Bug fixes:

- Python 3 compatibility.
  [pbauer]


1.4.0 (2018-02-02)
------------------

New features:

- Related items behavior: show a "recently used" dropdown in the related items widget.
  The "recently used" dropdown is only available for Mockup 2.6.3+.
  [thet]

Bug fixes:

- Make doctests work with new testbrowser in Zope4
  [pbauer]


1.3.5 (2017-06-20)
------------------

Bug fixes:

- remove unittest2 dependency
  [kakshay21]


1.3.4 (2016-09-23)
------------------

New features:

- Support RelatedValues UUID lookup to validate with p.a.vocabularies
  [calvinhp]


1.3.3 (2016-04-25)
------------------

Fixes:

- cleanup: pep8, utf8 header, sorted imports, zca decorators, ...
  [jensens]


1.3.2 (2015-07-18)
------------------

- Fix test isolation problem.
  [gotcha, timo]


1.3.1 (2015-03-13)
------------------

- Integrate plone.app.widgets.
  [vangheem]

- Remove dependency on zope.app.intid.
  [davisagli]


1.3.0 (2014-11-01)
------------------

- Add schemaeditor support
  [smcmahon, datakurre]

- Added RelationListDictDataManager
  [jaroel, datakurre]


1.2.2 (2014-04-15)
------------------

- plone.rfc822 1.0.2 marshalls collections as ascii.
  [esteele]

- Remove the adaptation from this package and move it to plone.app.widgets.
  [frapell]

- Do not include demo by default.
  [frapell]

- Remove plone.formwidget.contenttree dependency.
  [frapell]

- Use the widget provided by plone.app.widgets.
  [frapell]


1.2.1 (2013-01-25)
------------------

- Update getSite import for compatibility with Plone 4.3.
  [davisagli]


1.2.0 (2012-09-21)
------------------

- changed handler for RelationChoiceHandler
  to plone.supermodel.exportimport.ChoiceHandler
  [gborelli]

- Monkey patch z3c.relationfield RelationValue, it is
  incompatible with Zope2/4 and can cause problems in some case.
  [do3cc]

1.1 (2011-07-02)
----------------

- Make sure the content tree widget profile is installed.
  [davisagli]

- Moved the 'related items' behavior here from plone.app.dexterity.
  [davisagli]

1.0 (2011-04-30)
----------------

- Make it possible to clear non-required RelationChoice fields.
  This closes http://code.google.com/p/dexterity/issues/detail?id=163
  [davisagli]

1.0b6 (2011-02-11)
------------------

- Create custom data manager for dictionaries.
  [dukebody]

1.0b5 (2010-02-22)
------------------

- Depend on plone.app.intid for intid utility installation and content
  registration.
  [alecm]

- Fix register_all_content_for_intids to register content in all
  Languages in LinguaPlone sites
  [csenger]

1.0b4 (2009-10-11)
------------------

- Add plone.rfc822 field marshaler.
  [optilude]

1.0b3 (2009-09-27)
------------------

- Fix IObjectPath utility's resolve() method signature. Thanks Hedley Roos.
  [optilude]

1.0b2 (2009-07-18)
------------------

- Add IObjectPath utility. This is required for broken relationships to work.
  Without it, deleting an object that has inbound relations will cause an
  error. Arguably, this isn't the ideal package for this, somewhat more
  general utility, but it can always be moved later as it's not imported
  anywhere.
  [optilude]

1.0b1 (2009-05-31)
------------------

- Made Archetypes support truly optional.
  [hannosch]

- Create glue package for adding z3c.relationfield support to Plone/Dexterity.
  [alecm]
