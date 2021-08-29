# -*- coding: utf-8 -*-
import logging

import cssutils
from django import template
from django.template import Library
from inlinestyler.utils import inline_css

register = Library()

cssutils.log.setLevel(logging.CRITICAL)


@register.filter
def do_inline_css(parser, token):
    nodelist = parser.parse(("endinline_css",))
    parser.delete_first_token()
    return InlineCSSNode(nodelist)


class InlineCSSNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context).encode("ascii", "xmlcharrefreplace")
        return inline_css(output)


register.tag("inline_css", do_inline_css)
