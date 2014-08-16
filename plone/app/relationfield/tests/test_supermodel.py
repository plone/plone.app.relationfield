# -*- coding: utf-8 -*-
import os
import doctest
import unittest

from plone.testing import layered

from plone.app.relationfield.testing import FUNCTIONAL_DEXTERITY_TESTING

optionflags = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite(
                os.path.join(os.path.pardir, 'supermodel.txt'),
                optionflags=optionflags),
                FUNCTIONAL_DEXTERITY_TESTING)
    ])
    return suite


if __name__ == '__main__':
    unittest.main(default='test_suite')
