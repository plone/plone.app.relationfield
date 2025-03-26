from pathlib import Path
from setuptools import find_packages
from setuptools import setup


version = "3.0.6"

long_description = (
    f"{Path('README.rst').read_text()}\n{Path('CHANGES.rst').read_text()}"
)

setup(
    name="plone.app.relationfield",
    version=version,
    description="Plone support for z3c.relationfield",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="dexterity relations plone zc.relation",
    author="Alec Mitchell",
    author_email="apm13@columbia.edu",
    url="https://pypi.org/project/plone.app.relationfield",
    license="GPL",
    packages=find_packages(),
    namespace_packages=["plone", "plone.app"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "plone.base",
        # Keep Products.CMFCore because z3c.dependencychecker does not yet
        # check transitive dependencies in our config.
        "Products.CMFCore",
        "five.intid",
        "plone.app.intid",
        "plone.app.vocabularies",
        "plone.app.z3cform",
        "plone.autoform",
        "plone.behavior",
        "plone.dexterity",
        "plone.rfc822",
        "plone.schemaeditor",
        "plone.supermodel",
        "plone.uuid",
        "z3c.form",
        "z3c.objpath",
        "z3c.formwidget.query",
        "z3c.relationfield",
        "zc.relation",
        "Zope",
        "zope.intid",
    ],
    extras_require={
        "test": [
            "plone.app.contenttypes[test]",
            "plone.app.testing",
            "plone.app.dexterity",
            "plone.formwidget.contenttree",
            "plone.testing",
        ]
    },
)
