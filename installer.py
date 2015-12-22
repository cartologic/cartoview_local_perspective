info = {
    "title": "ESRI Local Perspective",
    "description": ''' Local Perspective is a configurable template for highlighting features from a web map based on a
                        user selected location or address. In addition to your data, you can include demographics,
                        lifestyle, live weather information and enable driving directions.''',
    "author": 'Cartologic',
    "tags": ['Maps'],
    "licence": 'BSD',
    "author_website": "http://www.cartologic.com",
    "single_instance": False
}

from django.contrib.contenttypes.models import ContentType


def install():
    pass


def uninstall():
    ContentType.objects.filter(app_label="cartoview_local_perspective").delete();
