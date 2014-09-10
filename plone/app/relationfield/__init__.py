from plone.app.relationfield.monkey import PATCHES

PATCHES

import pkg_resources

try:
    pkg_resources.get_distribution('plone.formwidget.contenttree')
except pkg_resources.DistributionNotFound:
    HAS_CONTENTTREE = False
else:
    HAS_CONTENTTREE = True

try:
    pkg_resources.get_distribution('plone.app.widgets')
except pkg_resources.DistributionNotFound:
    HAS_WIDGETS = False
else:
    HAS_WIDGETS = True

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_CONTENTTYPES = False
else:
    HAS_CONTENTTYPES = True
