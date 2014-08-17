# -*- coding: utf-8 -*-
from plone.app.relationfield import HAS_CONTENTTREE
from plone.app.relationfield import HAS_WIDGETS
from plone.app.relationfield.testing import FUNCTIONAL_CONTENTTREE_TESTING
from plone.app.relationfield.testing import FUNCTIONAL_WIDGETS_TESTING
from plone.testing import layered
import doctest
import os
import unittest

optionflags = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    suite = unittest.TestSuite()
    if HAS_CONTENTTREE and not HAS_WIDGETS:
        suite.addTests([
            layered(doctest.DocFileSuite(
                    os.path.join(os.path.pardir,
                                 'supermodel_contenttree.txt'),
                    optionflags=optionflags),
                    FUNCTIONAL_CONTENTTREE_TESTING)
        ])
    elif HAS_WIDGETS:
        suite.addTests([
            layered(doctest.DocFileSuite(
                    os.path.join(os.path.pardir, 'supermodel.txt'),
                    optionflags=optionflags),
                    FUNCTIONAL_WIDGETS_TESTING)
        ])
    return suite


if __name__ == '__main__':
    unittest.main(default='test_suite')
