from importlib.metadata import version, PackageNotFoundError


try:
    __version__ = version('djangorestframework-ext')
except PackageNotFoundError:
    pass
