from __future__ import absolute_import

import logging
import sys

from pip._vendor import pkg_resources
from pip._vendor.packaging import specifiers
from pip._vendor.packaging import version

logger = logging.getLogger(__name__)


def get_metadata(dist):
    if (isinstance(dist, pkg_resources.DistInfoDistribution) and
            dist.has_metadata('METADATA')):
        return dist.get_metadata('METADATA')
    elif dist.has_metadata('PKG-INFO'):
        return dist.get_metadata('PKG-INFO')


def check_requires_python(requires_python):
    if requires_python is None:
        # The package provides no information
        return True
    try:
        requires_python_specifier = specifiers.SpecifierSet(requires_python)
    except specifiers.InvalidSpecifier as e:
        logger.debug(
            "Package %s has an invalid Requires-Python entry - %s" % (
                 requires_python, e))
        return ValueError('Wrong Specifier')

    # We only use major.minor.micro
    python_version = version.parse('.'.join(map(str, sys.version_info[:3])))
    if python_version not in requires_python_specifier:
        return False
