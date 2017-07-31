# -*- coding: utf-8 -*-
# __author__ = "chao.fang"
from __future__ import unicode_literals, print_function, division
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.admin.widgets import AdminTextareaWidget
import copy
import json
from .utils import editor_settings


class EditorMdWidget(forms.Textarea):
    def __init__(self, attrs=None):
        params = attrs.copy()
        self.context = copy.deepcopy(editor_settings)
        self.context["width"] = params.pop("width")
        if isinstance(self.context["width"], float):
            self.context["width"] = '"{}%"'.format(self.context["width"] * 100)
        self.context["height"] = params.pop("height")
        if isinstance(self.context["height"], float):
            self.context["height"] = '"{}%"'.format(self.context["height"] * 100)
        self.context["toolbaricons"] = params.pop("toolbaricons", '[]')
        self.context["default"] = params.pop("default")
        self.context["imagepath"] = params.pop("imagepath")
        self.context["imageUploadURL"] = ''
        super(EditorMdWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = self.context["default"]
        self.context["markdown"] = value
        self.context["editor_id"] = "id_%s" % name.replace("-", "_")
        self.context["name"] = name
        return mark_safe(render_to_string('editor.md.html', self.context))

    class Media:
        # https://docs.djangoproject.com/en/1.11/topics/forms/media/
        js = ("js/jquery.min.js",
              "editor.md/editormd.min.js")
        css = {"all": ("editor.md/css/editormd.min.css",)}


class AdminEditorMdWidget(AdminTextareaWidget, EditorMdWidget):
    def __init__(self, **kwargs):
        super(AdminEditorMdWidget, self).__init__(**kwargs)