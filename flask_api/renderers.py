# coding: utf8
from __future__ import unicode_literals
from coreapi import renderers
from flask import current_app, render_template, request
from flask.json import JSONEncoder
from flask.globals import _request_ctx_stack
import re


def dedent(content):
    """
    Remove leading indent from a block of text.
    Used when generating descriptions from docstrings.

    Note that python's `textwrap.dedent` doesn't quite cut it,
    as it fails to dedent multiline docstrings that include
    unindented text on the initial line.
    """
    whitespace_counts = [len(line) - len(line.lstrip(' '))
                         for line in content.splitlines()[1:] if line.lstrip()]

    # unindent the content if needed
    if whitespace_counts:
        whitespace_pattern = '^' + (' ' * min(whitespace_counts))
        content = re.sub(re.compile(whitespace_pattern, re.MULTILINE), '', content)

    return content.strip()


def convert_to_title(name):
    return name.replace('-', ' ').replace('_', ' ').capitalize()


# We don't need to make implementation changes to these clasees,
# but we make these importable from flask api.
BaseRenderer = renderers.BaseRenderer
HTMLRenderer = renderers.HTMLRenderer


class JSONRenderer(renderers.JSONRenderer):
    # Use Flask's default JSON encoder for a few extra tweaks.
    encoder_class = JSONEncoder


class BrowsableAPIRenderer(renderers.BrowsableAPIRenderer):
    media_type = 'text/html'
    handles_empty_responses = True

    def render_template(self, context, **options):
        adapter = _request_ctx_stack.top.url_adapter
        allowed_methods = adapter.allowed_methods()

        endpoint = request.url_rule.endpoint
        view_name = str(endpoint)
        view_description = current_app.view_functions[endpoint].__doc__
        if view_description is not None:
            view_description = dedent(view_description)

        from flask_api import __version__

        context.update({
            'allowed_methods': allowed_methods,
            'static_prefix': '/flask-api/static/',
            'view_name': convert_to_title(view_name),
            'view_description': view_description,
            'version': __version__
        })
        return render_template('base.html', **context)
