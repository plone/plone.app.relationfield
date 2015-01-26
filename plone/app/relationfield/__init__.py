from plone.app.relationfield.monkey import PATCHES

PATCHES

import pkg_resources

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_CONTENTTYPES = False
else:
    HAS_CONTENTTYPES = True
