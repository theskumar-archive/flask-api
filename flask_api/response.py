# coding: utf8
from __future__ import unicode_literals
from coreapi import BaseResponse
from flask import request, Response
from flask._compat import text_type, string_types


class APIResponse(BaseResponse, Response):
    def __init__(self, content=None, *args, **kwargs):
        super(APIResponse, self).__init__(None, *args, **kwargs)

        if isinstance(content, (list, dict, text_type, string_types)):
            self.render(content, request)
        elif isinstance(content, (bytes, bytearray)):
            self.set_data(content)
        else:
            self.response = content

    # CoreAPI integration points...

    def _get_headers(self):
        return self.headers

    def _get_status_code(self):
        return self.status_code

    def _set_status_code(self, status_code):
        self.status_code = status_code

    def _set_content(self, content):
        self.set_data(content)

    def _set_content_type(self, content_type):
        self.headers['Content-Type'] = content_type
