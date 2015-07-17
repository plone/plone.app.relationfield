# -*- coding: utf-8 -*-
import doctest
from unittest import TestSuite

from plone.testing import layered
from plone.testing.zca import ZCMLSandbox

import plone.app.relationfield.tests

ZCML_SANDBOX = ZCMLSandbox(
    filename='test_marshall.zcml',
    package=plone.app.relationfield.tests
)


def test_suite():
    suite = TestSuite()
    OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
    suite.addTest(layered(
        doctest.DocFileSuite(
            '../marshaler.rst',
            optionflags=OPTIONFLAGS,
            package="plone.app.relationfield.tests",
        ),
        layer=ZCML_SANDBOX)
    )
    return suite
