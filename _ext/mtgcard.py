#coding: utf-8
from docutils import nodes

import re
import string


def mtgtip_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role to show a card in hovering tooltip
    
    At the moment you need to include the needed JavaScript in the template yourself.
    """
    
    if "<" in text and ">" in text:
        shown, real_name = text.split("<")
        real_name = real_name.split(">")[0]
    else:
        real_name = shown = text.strip()
    
    keyval = real_name.replace(" ", "_")
    wrapped = """<a class="nodec" keyname="name" keyvalue="%(keyval)s" onmouseover="OpenTip(event, this)" onclick="autoCardWindow(this); return false;" href="http://gatherer.wizards.com/Pages/Card/Details.aspx?name=%(text)s">%(text)s</a>""" % {'text': shown, 'keyval':keyval, 'real_name': real_name}
    node = nodes.raw('', wrapped, format='html')
    return [node], []

def setup(app):
    app.add_role('mtgtip', mtgtip_role)

