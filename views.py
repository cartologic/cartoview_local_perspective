import json
import os
import re
from string import rstrip
from urlparse import urljoin

from django.http import HttpResponseRedirect
from django.shortcuts import render

from cartoview.app_manager.models import *
from forms import NewForm
from geonode import settings
from .models import *

dirname, filename = os.path.split(os.path.abspath(__file__))
APP_NAME = 'cartoview_local_perspective'
VIEW_TPL = "%s/index.html" % APP_NAME
NEW_EDIT_TPL = "%s/new.html" % APP_NAME

HELP_TPL = "%s/help.htm" % APP_NAME
CONFIG_TPL = "%s/config.js" % APP_NAME

# Regular expression for comments
comment_re = re.compile(
        '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
        re.DOTALL | re.MULTILINE
)

comments_exception = {'http://': 'HTTP_PLACE_HOLDER', 'https://': 'HTTPS_PLACE_HOLDER',
                      'location.protocol + "//': 'LOCATION_PLACE_HOLDER'}


def remove_json_comments(json_string):
    """ Parse a JSON file
        First remove comments and then use the json module package
        Comments look like :
            // ...
        or
            /*
            ...
            */
    """

    content = json_string  # ''.join(json_string)

    for key in comments_exception:
        content = content.replace(key, comments_exception[key])

    ## Looking for comments
    match = comment_re.search(content)
    while match:
        # single line comment
        content = content[:match.start()] + content[match.end():]
        match = comment_re.search(content)

    for key in comments_exception:
        content = content.replace(comments_exception[key], key)

    # Return json
    return content


def view(request, resource_id):
    localperspective_obj = LocalPerspective.objects.get(pk=resource_id)
    config_json = json.loads(remove_json_comments(localperspective_obj.config))
    config_json['webmap'] = str(localperspective_obj.web_map_id)
    config_json['title'] = localperspective_obj.title
    config_json['description'] = localperspective_obj.abstract
    config_json['sharinghost'] = rstrip(str(urljoin(settings.SITEURL, reverse("arcportal_home"))), '/')

    context = {'config_json': json.dumps(config_json)}
    return render(request, VIEW_TPL, context)


def save(request, map_form):
    if map_form.is_valid():
        localperspective_obj = map_form.save(commit=False)
        localperspective_obj.app = App.objects.get(name=APP_NAME)
        localperspective_obj.owner = request.user
        localperspective_obj.save()

        return HttpResponseRedirect(reverse('appinstance_detail', kwargs={'appinstanceid': localperspective_obj.pk}))
    else:
        context = {'map_form': map_form}
        return render(request, NEW_EDIT_TPL, context)


def new(request):
    if request.method == 'POST':
        map_form = NewForm(request.POST, prefix='map_form')
        return save(request, map_form)

    else:
        context = {'map_form': NewForm(prefix='map_form')}
        return render(request, NEW_EDIT_TPL, context)


def edit(request, resource_id):
    app_instance_obj = LocalPerspective.objects.get(pk=resource_id)
    if request.method == 'POST':
        map_form = NewForm(request.POST, prefix='map_form', instance=app_instance_obj)
        return save(request, map_form)

    else:
        context = {'map_form': NewForm(prefix='map_form', instance=app_instance_obj)}
        return render(request, NEW_EDIT_TPL, context)
