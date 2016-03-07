# -*- coding: utf-8 -*-
from plone.app.relationfield.monkey import PATCHES

import pkg_resources


PATCHES


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_CONTENTTYPES = False
else:
    HAS_CONTENTTYPES = True
