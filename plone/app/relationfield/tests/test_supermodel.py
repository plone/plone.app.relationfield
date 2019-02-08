# -*- coding: utf-8 -*-
from plone.app.relationfield.testing import FUNCTIONAL_WIDGETS_TESTING
from plone.testing import layered

import doctest
import os
import re
import six
import unittest


optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            got = re.sub("u'(.*?)'", "'\\1'", got)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [
            layered(
                doctest.DocFileSuite(
                    os.path.join(os.path.pardir, 'supermodel.txt'),
                    optionflags=optionflags,
                    checker=Py23DocChecker(),
                ),
                layer=FUNCTIONAL_WIDGETS_TESTING,
            )
        ]
    )
    return suite


if __name__ == '__main__':
    unittest.main(default='test_suite')
