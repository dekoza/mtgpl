#coding: utf-8
from docutils import nodes

import re
import string


def mtgcard_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role to show a card in hovering tooltip
    
    At the moment you need to include the needed JavaScript in the template yourself.
    """
    
    keyval = text.replace(" ", "_")
    wrapped = """<a class="nodec" keyname="name" keyvalue="%(keyval)s" onmouseover="OpenTip(event, this)" onclick="autoCardWindow(this)" href="http://gatherer.wizards.com/Pages/Card/Details.aspx?name=%(text)s">%(text)s</a>""" % {'text': text, 'keyval':keyval}
    node = nodes.raw('', wrapped, format='html')
    return [node], []

def setup(app):
    app.add_role('mtgcard', mtgcard_role)

