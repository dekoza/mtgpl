from django.db import models
from django.utils.translation import gettext_lazy as _

COLORS = (
    ('white', _('White')),
    ('blue', _('Blue')),
    ('black', _('Black')),
    ('red', _('Red')),
    ('green', _('Green')),
)

LEGALITIES = (
    ('r', _('Restricted')),
    ('b', _('Banned')),
    ('c', _('Conditional')),
    ('l', _('Legal')),
)

BORDERS = (
    ('b', _('Black')),
    ('w', _('White')),
    ('s', _('Silver')),
    ('g', _('Gold')),
)


class Format(models.Model):
    name = models.CharField(_('name'), max_length=64, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Legality(models.Model):
    format = models.ForeignKey(Format, verbose_name=_('format'))
    card = models.ForeignKey('Card', verbose_name=_('card'), related_name='legality_statuses')
    status = models.CharField(_('status'), max_length=1, choices=LEGALITIES)
    condition = models.TextField(_('condition'), blank=True)

    def __str__(self):
        return "{card} is {status} in {format}".format(**{
            "card": self.card.name,
            "status": self.get_status_display(),
            "format": self.format.name
        })


class Block(models.Model):
    name = models.CharField(_('name'), max_length=64, unique=True)

    def __str__(self):
        return self.name


class Expansion(models.Model):
    name = models.CharField(_('name'), max_length=64, unique=True)
    code = models.CharField(_('code'), max_length=10, unique=True)
    symbol = models.ImageField(_('symbol'))
    release_date = models.DateField(_('release date'), null=True, blank=True)
    mkm_id = models.PositiveIntegerField(_('mkm id'), null=True, blank=True, db_index=True)
    block = models.ForeignKey(Block, null=True, blank=True)
    online_only = models.BooleanField(_('online only'), default=False)
    gatherer_code = models.CharField(_('gatherer code'), max_length=10, unique=True)
    mci_code = models.CharField(_('magiccards.info code'), max_length=10)
    exp_type = models.CharField(_('type'), max_length=16, blank=True)
    border = models.CharField(_('border'), max_length=1, blank=True, choices=BORDERS)

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return self.name


class Artist(models.Model):
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    mtgjson_id = models.CharField(_('mtgjson id'), max_length=100, db_index=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.mtgjson_id


class Rarity(models.Model):
    name = models.CharField(_('name'), max_length=20, db_index=True, unique=True)

    def __str__(self):
        return self.name


class CardSupertype(models.Model):
    name = models.CharField(_('name'), max_length=30, db_index=True, unique=True)

    def __str__(self):
        return self.name


class CardType(models.Model):
    name = models.CharField(_('name'), max_length=30, db_index=True, unique=True)

    def __str__(self):
        return self.name


class CardSubtype(models.Model):
    name = models.CharField(_('name'), max_length=30, db_index=True, unique=True)

    def __str__(self):
        return self.name


class CardColor(models.Model):
    name = models.CharField(_('name'), max_length=5, choices=COLORS, db_index=True, unique=True)

    def __str__(self):
        return self.name


class Ruling(models.Model):
    date = models.DateField(_('date'))
    hash = models.CharField(_('hash'), max_length=40, db_index=True)
    text = models.TextField(_('text'))

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.text


class Card(models.Model):
    name = models.CharField(_('name'), max_length=200, unique=True)
    mana_cost = models.CharField(_('mana cost'), max_length=100, blank=True)
    cmc = models.PositiveIntegerField(_('cmc'), default=0)
    colors = models.ManyToManyField(CardColor, verbose_name=_('colors'))
    supertypes = models.ManyToManyField(CardSupertype, verbose_name=_('supertypes'), blank=True)
    types = models.ManyToManyField(CardType, verbose_name=_('types'))
    subtypes = models.ManyToManyField(CardSubtype, verbose_name=_('subtypes'), blank=True)
    text = models.TextField(_('text'))
    power = models.CharField(_('power'), max_length=5, db_index=True, blank=True)
    toughness = models.CharField(_('toughness'), max_length=5, db_index=True, blank=True)
    loyalty = models.PositiveSmallIntegerField(_('loyalty'), null=True, blank=True, db_index=True)
    hand_mod = models.SmallIntegerField(_('hand modifier'), null=True, blank=True)
    life_mod = models.SmallIntegerField(_('life modifier'), null=True, blank=True)
    reserved = models.BooleanField(_('reserved'), default=False, help_text=_('Set to true if this card is reserved by Wizards Official Reprint Policy'))
    front_side = models.ForeignKey('Card', verbose_name=_('front side'), null=True, blank=True,
                                   related_name='other_sides')
    legality = models.ManyToManyField(Format, through=Legality, help_text=_('This field lists all formats that the card *could* be legal in along with its actual legality in that format.'))
    rulings = models.ManyToManyField(Ruling, blank=True)

    @property
    def type(self):
        return "{supertypes} {types} - {subtypes}".format(**dict(
            supertypes=" ".join(self.supertypes.all()),
            types=" ".join(self.types.all()),
            subtypes=" ".join(self.subtypes.all())))

    def __str__(self):
        return self.name


class Printing(models.Model):
    card = models.ForeignKey(Card, verbose_name=_('card'))
    expansion = models.ForeignKey(Expansion, verbose_name=_('expansion'))
    image = models.ImageField(_('image'), blank=True)
    artist = models.ForeignKey(Artist, verbose_name=_('artist'), related_name='painted_cards', null=True, blank=True)
    extra_artist = models.ForeignKey(Artist, verbose_name=_('extra artist'), related_name='painted_as_extra', null=True, blank=True)
    rarity = models.ForeignKey(Rarity, verbose_name=_('rarity'), null=True, blank=True)
    number = models.CharField(_('number'), max_length=5, db_index=True, blank=True)
    flavor = models.TextField(_('flavor'), blank=True)
    starter = models.BooleanField(_('starter'), default=False, help_text=_('Set to true if this card was only released as part of a core box set. These are technically part of the core sets and are tournament legal despite not being available in boosters.'))
    multiverese_id = models.PositiveIntegerField(_('multiverse id'), null=True, blank=True)
    timeshifted = models.BooleanField(_('timeshifted'), default=False)
    source = models.CharField(_('source'), max_length=256, blank=True)
    border = models.CharField(_('border'), max_length=1, blank=True, choices=BORDERS)
    layout = models.CharField(_('layout'), max_length=60, blank=True)

    class Meta:
        ordering = ['-expansion__release_date', 'number']

    def __str__(self):
        return "{} {}".format(self.expansion.code, self.card.name)
