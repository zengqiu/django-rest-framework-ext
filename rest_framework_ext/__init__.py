from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution('djangorestframework-ext').version
except DistributionNotFound:
    pass
