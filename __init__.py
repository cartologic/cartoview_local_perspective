CARTOVIEW_VERSION = (1, 0, 0, 'final', 0)  # major.minor.build.release (PEP standard)

VERSION = (1, 0, 0, 'final', 0)  # major.minor.build.release (PEP standard)


def get_cartoview_version(*args, **kwargs):  # carto compatible version
    # Don't litter django/__init__.py with all the get_version stuff.
    # Only import if it's actually called.
    from django.utils.version import get_version
    return get_version(version=CARTOVIEW_VERSION)


def get_version(*args, **kwargs):
    # Don't litter django/__init__.py with all the get_version stuff.
    # Only import if it's actually called.
    from django.utils.version import get_version
    return get_version(version=VERSION)


urls_dict = {'admin': {'cartoview_local_perspective.new': 'Create new'},
             'admin': {'cartoview_local_perspective.new': 'Create new'},
             }
