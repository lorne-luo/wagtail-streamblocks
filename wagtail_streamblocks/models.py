# -*- coding: utf-8 -*-

import os

from django.db import models

from django.utils.functional import lazy
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from .blocks import SUPER_STREAM_BLOCK


class BaseStreamContentPage(Page):
    content = StreamField(SUPER_STREAM_BLOCK, blank=True)
    custom_template = models.CharField(max_length=250, blank=False, null=False, choices=(),
                                       help_text='Please select a template for this page, default base template')

    def __init__(self, *args, **kwargs):
        super(BaseStreamContentPage, self).__init__(*args, **kwargs)
        self._meta.get_field('custom_template').choices = lazy(self.custom_template_choices, list)()

    def get_template(self, request, *args, **kwargs):
        if request.is_ajax() and self.ajax_template:
            return self.ajax_template
        return self.custom_template or super(BaseStreamContentPage, self).get_template(request, *args, **kwargs)

    class Meta:
        abstract = True

    def custom_template_choices(self):
        choices = []
        app_label = self._meta.app_label
        path = os.path.join(os.path.dirname(__file__), 'templates', app_label)
        for file in os.listdir(path):
            if file.endswith(".html"):
                template = "%s/%s" % (app_label, file)
                choices.append((template, template))
        return choices
