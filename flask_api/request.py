# coding: utf8
from __future__ import unicode_literals
from coreapi.negotiation import DefaultNegotiation
from coreapi import BaseRequest
from flask import Request
from flask_api.settings import default_settings
from werkzeug.datastructures import MultiDict


class APIRequest(BaseRequest, Request):
    parser_classes = default_settings.DEFAULT_PARSERS
    renderer_classes = default_settings.DEFAULT_RENDERERS
    negotiator_class = DefaultNegotiation
    empty_data_class = MultiDict

    @property
    def full_path(self):
        """
        Werzueg's full_path implementation always appends '?', even when the
        query string is empty.  Let's fix that.
        """
        if not self.query_string:
            return self.path
        return self.path + u'?' + self.query_string

    # CoreAPI integration points...

    def _get_method(self):
        return super(BaseRequest, self).method

    def _get_stream(self):
        return super(BaseRequest, self).stream

    def _get_content_type(self):
        return self.headers.get('Content-Type')

    def _get_content_length(self):
        return self.headers.get('Content-Length')

    def _get_accept(self):
        return self.headers.get('Accept')
