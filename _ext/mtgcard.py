# coding: utf-8
"""
### search:
msgid ":mtgtip:`(?<name>.*)`"
msgstr ".+"

### replace:
msgid ":mtgtip:`$1`"
msgstr ""

"""

from docutils import nodes


def old_mtgtip_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role to show a card in hovering tooltip

    At the moment you need to include the needed JavaScript in the template yourself.
    """

    if "<" in text and ">" in text:
        real_name, extras = text.split("<")
        shown = real_name
    else:
        real_name = shown = text.strip()

    keyval = real_name.replace(" ", "_")
    wrapped = (
        """<a class="nodec" keyname="name" keyvalue="%(keyval)s" onmouseover="OpenTip(event, this)" onclick="autoCardWindow(this); return false;" href="http://gatherer.wizards.com/Pages/Card/Details.aspx?name=%(text)s">%(text)s</a>"""
        % {"text": shown, "keyval": keyval, "real_name": real_name}
    )
    node = nodes.raw("", wrapped, format="html")
    return [node], []


def mtgtip_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role to show a card in hovering tooltip

    At the moment you need to include the needed JavaScript in the template yourself.
    """

    if "<" not in text:
        node = nodes.raw("", text, format="html")
        return [node], []

    card_name, extras = text.split("<")
    image_url, card_url, *_ = extras.split("|")
    card_url = card_url.split(">")[0]

    wrapped = f"""<a class="tooltip" href="{card_url}" target="_blank">{card_name}<span><img src="{image_url}"></span></a>"""

    node = nodes.raw("", wrapped, format="html")
    return [node], []


def mtgexp_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role to show expansion symbol.
    """

    wrapped = """<span class="ss ss-{text}"></span>""".format(text=text.lower())
    node = nodes.raw("", wrapped, format="html")
    return [node], []


def mtgrule_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role to link to Yawgatog's hyperlinked comprehensive rules guide.
    """

    anchor = text.split(",")[0].split(" ")[-1].replace(".", "")
    wrapped = "<a href='https://yawgatog.com/resources/magic-rules/#R{anchor}'>{text}</a>".format(
        text=text, anchor=anchor
    )
    node = nodes.raw("", wrapped, format="html")
    return [node], []


def setup(app):
    app.add_role("mtgtip", mtgtip_role)
    app.add_role("mtgexp", mtgexp_role)
    app.add_role("mtgrule", mtgrule_role)
