from setuptools import setup, find_packages
import os

version = '1.3.0'

setup(name='plone.app.relationfield',
      version=version,
      description="Plone support for z3c.relationfield",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='dexterity relations plone zc.relation',
      author='Alec Mitchell',
      author_email='apm13@columbia.edu',
      url='https://pypi.python.org/pypi/plone.app.relationfield',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.interface',
          'zope.component',
          'zope.schema',
          'zope.intid',
          'five.intid',
          'plone.app.intid',
          'z3c.form',
          'z3c.relationfield>=0.4.2',
          'z3c.formwidget.query',
          'plone.autoform',
          'plone.supermodel',
          'plone.app.vocabularies',
          'plone.schemaeditor>=1.3.5.dev0',
          'Products.CMFCore',
          'plone.rfc822',
      ],
      extras_require={'test': ['plone.app.testing', 'plone.app.dexterity']},
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
