from codemirror import *
from django import forms

from cartoview.app_manager.forms import AppInstanceForm
from config import config_template
from models import LocalPerspective


class NewForm(AppInstanceForm):
    class Meta(AppInstanceForm.Meta):
        model = LocalPerspective
        fields = AppInstanceForm.Meta.fields + ['config', 'web_map_id']

    web_map_id = forms.CharField(widget=forms.HiddenInput)
    config = CodeMirrorFormField(initial=config_template)
