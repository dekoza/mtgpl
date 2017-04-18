from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField


class Language(models.Model):
    name = models.CharField(_('name'), max_length=30, unique=True)
    code = models.CharField(_('code'), max_length=5, unique=True)

    def __str__(self):
        return self.name


class CardTranslation(models.Model):
    card = models.ForeignKey('mtgdb.Card', verbose_name=_('card'), related_name='translations')
    lang = models.ForeignKey(Language, verbose_name=_('language'))
    name = models.CharField(_('translated name'), max_length=200)
    text = models.TextField(_('translated text'), blank=True)
    extra_context = JSONField(_('extra context'), default=dict, blank=True)

    class Meta:
        unique_together = ('card', 'lang')
        ordering = ('card__name', 'lang__code')

    def __str__(self):
        return "{lang.code}: {card.name}".format(card=self.card, lang=self.lang)


class RulingTranslation(models.Model):
    ruling = models.ForeignKey('mtgdb.Ruling', verbose_name=_('ruling'))
    lang = models.ForeignKey(Language, verbose_name=_('language'))
    text = models.TextField(_('translated text'), blank=True)
    extra_context = JSONField(_('extra context'), default=dict, blank=True)

    class Meta:
        unique_together = ('ruling', 'lang')

    def __str__(self):
        return self.translated_text


# Not exactly needed, kept for completion

class PrintingTranslation(models.Model):
    printing = models.ForeignKey('mtgdb.Printing', verbose_name=_('printing'))
    lang = models.ForeignKey(Language, verbose_name=_('language'))
    name = models.CharField(_('translated name'), max_length=200)
    multiverse_id = models.PositiveIntegerField(_('multiverse id'), null=True, blank=True)

    class Meta:
        unique_together = ('printing', 'lang')

    def __str__(self):
        return "{lang.code} {printing.expansion.code} {printing.card.name} - {trans}".format(**{
            'lang': self.lang,
            'printing': self.printing,
            'trans': self.translated_name,
        })
