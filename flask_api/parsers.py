# coding: utf8
from __future__ import unicode_literals
from coreapi import exceptions, parsers
from werkzeug import formparser, urls


BaseParser = parsers.BaseParser
JSONParser = parsers.JSONParser


class MultiPartParser(BaseParser):
    media_type = 'multipart/form-data'
    handles_file_uploads = True
    handles_form_data = True

    def parse(self, stream, media_type, **options):
        stream_factory = formparser.default_stream_factory
        multipart_parser = formparser.MultiPartParser(stream_factory)

        boundary = media_type.params.get('boundary')
        if boundary is None:
            msg = 'Multipart message missing boundary in Content-Type header'
            raise exceptions.ParseError(msg)
        boundary = boundary.encode('ascii')

        content_length = options['content_length']

        try:
            return multipart_parser.parse(stream, boundary, content_length)
        except ValueError as exc:
            msg = 'Multipart parse error - %s' % exc
            raise exceptions.ParseError(msg)


class URLEncodedParser(BaseParser):
    media_type = 'application/x-www-form-urlencoded'
    handles_form_data = True

    def parse(self, stream, media_type, **options):
        return urls.url_decode_stream(stream)
