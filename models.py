from django.db import models
from uuidfield import UUIDField

from cartoview.app_manager.models import AppInstance


# Create your models here.

class LocalPerspective(AppInstance):
    # note the related_name format to avoid conflicts between derived models
    web_map_id = UUIDField()
    config = models.TextField(null=True, blank=True)
