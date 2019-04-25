# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '2.0.1'

setup(
    name='plone.app.relationfield',
    version=version,
    description='Plone support for z3c.relationfield',
    long_description=(
        open('README.rst').read() + '\n' + open('CHANGES.rst').read()
    ),
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 5.2',
        "License :: OSI Approved :: GNU General Public License (GPL)",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='dexterity relations plone zc.relation',
    author='Alec Mitchell',
    author_email='apm13@columbia.edu',
    url='https://pypi.org/project/plone.app.relationfield',
    license='GPL',
    packages=find_packages(),
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
        'z3c.relationfield>0.7.999',
        'z3c.formwidget.query',
        'plone.autoform',
        'plone.supermodel',
        'plone.app.vocabularies',
        'plone.schemaeditor>=1.3.5.dev0',
        'Products.CMFCore',
        'plone.rfc822',
        'plone.app.z3cform>=1.1.0.dev0',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.dexterity',
            'plone.app.robotframework',
        ]
    },
    entry_points="""
    # -*- Entry points: -*-
    """,
)
