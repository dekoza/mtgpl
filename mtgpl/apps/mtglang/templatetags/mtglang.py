from django import template
from ..models import Language

register = template.Library()


@register.simple_tag
def get_trans_lang(*args, **kwargs):
    return Language.objects.get(code="pl")


@register.simple_tag
def translate_card(card, lang, *args, **kwargs):
    try:
        return card.translations.get(lang=lang)
    except :
        return card


@register.filter
def mtgexp(qs):
    return qs.filter(exp_type__in=['expansion', 'core'])


@register.filter
def mtgextra(qs):
    return qs.exclude(exp_type__in=['expansion', 'core'])
