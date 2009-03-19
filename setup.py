from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='plone.app.relationfield',
      version=version,
      description="Plone support for z3c.relationfield",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='dexterity relations plone zc.relation',
      author='Alec Mitchell',
      author_email='apm13@columbia.edu',
      url='http://code.google.com/p/dexterity',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'five.intid',
          'z3c.relationfield',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
