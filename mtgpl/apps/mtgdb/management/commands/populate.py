from django.core.management.base import BaseCommand
from json.decoder import JSONDecodeError

import arrow
import hashlib
from apps.mtgdb.models import (
    Expansion, Card, Printing, Rarity, CardColor, CardSubtype, CardSupertype, CardType, Artist,
    Block, Format, Legality,
    Ruling)
from apps.mtglang.models import Language, CardTranslation, PrintingTranslation


class Command(BaseCommand):
    help = 'Fills the database with data.'

    def add_arguments(self, parser):
        """Optional expansion argument ('LEA', 'DDD', etc)."""
        parser.add_argument('-e', '--expansion', nargs='?', help="Get only particular expansion's data.")

    def handle(self, *args, **options):
        exp = options['expansion']
        if exp:
            try:
                return self.populate_single_expansion(exp)
            except JSONDecodeError:
                self.stdout.write(f'{exp} is not an expansion.')
                return
        return self.populate_from_web()

    ##############################

    def populate_from_web(self, url='https://mtgjson.com/json/AllSetsArray-x.json'):
        import requests
        data = requests.get(url).json()
        for exp_data in data:
            self.populate_expansion(exp_data)
            self.populate_translations(exp_data)
            self.populate_rulings(exp_data)

    def populate_single_expansion(self, expansion):
        import requests
        url = f'https://mtgjson.com/json/{expansion}.json'
        exp_data = requests.get(url).json()
        self.populate_expansion(exp_data)
        self.populate_translations(exp_data)
        self.populate_rulings(exp_data)

    def populate_from_dict(self, data):
        # is this even needed?
        for exp_data in data.values():
            self.populate_expansion(exp_data)

    def populate_expansion(self, data):
        code = data['code']
        name = data['name']

        self.stdout.write(name)

        exp, created = Expansion.objects.get_or_create(name=name, code=code)
        exp.release_date = arrow.get(data.get('releaseDate')).date()
        exp.mkm_id = data.get('mkm_id')
        exp.gatherer_code = data.get('gatherer_code', code)
        exp.mci_code = data.get('magicCardsInfoCode', '')
        exp.exp_type = data.get('type', '')
        exp.border = data.get('border', ' ')[0].lower().strip()
        block_name = data.get('block')
        if block_name is not None:
            blk, blk_created = Block.objects.get_or_create(name=block_name)
            exp.block = blk

        exp.save()

        for card in data['cards']:
            self.populate_card(card, exp)
        self.stdout.write('')

    def populate_card(self, data, exp=None):
        new_printing = False
        name = data['name']

        self.stdout.write(name)

        card, new_card = Card.objects.get_or_create(name=name)
        card.text = data.get('text', '')
        card.reserved = data.get('reserved', False)

        if new_card:
            card.mana_cost = data.get('manaCost', '')
            card.cmc = data.get('cmc', 0)
            card.power = data.get('power', '')
            card.toughness = data.get('toughness', '')
            card.loyalty = data.get('loyalty')
            card.hand_mod = data.get('hand')
            card.life_mod = data.get('life')

            for color in data.get('colors', []):
                color, _c = CardColor.objects.get_or_create(name=color.lower())
                card.colors.add(color)

            for sutype in data.get('supertypes', []):
                st, _c = CardSupertype.objects.get_or_create(name=sutype)
                card.supertypes.add(st)

            for _type in data.get('types', []):
                tp, _c = CardType.objects.get_or_create(name=_type)
                card.types.add(tp)

        for subtp in data.get('subtypes', []):
            sbt, _c = CardSubtype.objects.get_or_create(name=subtp)
            card.subtypes.add(sbt)

        for lstatus in data.get('legalities', []):
            format_name = lstatus['format']
            status = lstatus['legality']
            format, _c = Format.objects.get_or_create(name=format_name)
            legality, _c = Legality.objects.get_or_create(format=format, card=card)
            legality.status = status[0].lower()
            legality.save()

        card.save()

        if exp is None:
            printings = data.get('printings')
            if printings and len(printings) == 1:
                exp_code = printings[0]
                exp = Expansion.objects.get(code=exp_code)

        if isinstance(exp, str):
            exp = Expansion.objects.get(code=exp)

        if isinstance(exp, Expansion):
            number = data.get('number', '')
            rar_name = data['rarity']
            artist_name = data['artist']
            version, new_printing = Printing.objects.get_or_create(card=card, expansion=exp, number=number)
            if new_printing:
                artist, _c = Artist.objects.get_or_create(mtgjson_id=artist_name)
                if _c:
                    split = artist_name.rsplit(maxsplit=1)
                    artist.first_name, artist.last_name = split if len(split) == 2 else ('', artist_name)
                    artist.save()
                rarity, _c = Rarity.objects.get_or_create(name=rar_name)
                version.artist = artist
                version.rarity = rarity
                version.flavor = data.get('flavor', '')
                version.starter = data.get('starter', False)
                version.multiverse_id = data.get('multiverseid', data.get('multiverseId'))
                version.number = data.get('number', '')
                version.timeshifted = data.get('timeshifted', False)
                version.source = data.get('source', '')

                version.layout = data.get('layout', '')

                if version.number and not version.number.isdecimal() and not version.number[-1] == 'a':
                    front_side_number = version.number[:-1] + 'a'
                    try:
                        front_side = Printing.objects.get(expansion=exp, number=front_side_number)
                        card.front_side = front_side.card
                        card.save()
                    except Printing.DoesNotExist:
                        pass

            version.border = data.get('border', exp.border)[:1]
            version.save()

        if new_card and new_printing:
            self.stdout.write('+', ending='')
        elif new_printing:
            self.stdout.write('-', ending='')
        else:
            self.stdout.write('.', ending='')

    def populate_translations(self, expdata):
        exp = Expansion.objects.get(code=expdata['code'])
        self.stdout.write(f'Populating translations for {exp.name}')
        for crd in expdata.get('cards', []):
            card = Card.objects.get(name=crd['name'])
            self.stdout.write('>', ending='')
            for trns in crd.get('foreignNames', []):
                laname = trns['language']
                lancode = laname[:2] + '_' + laname[-2:]
                lang, _lc = Language.objects.get_or_create(name=laname, defaults={'code': lancode})
                trans, _c = CardTranslation.objects.get_or_create(card=card, lang=lang, defaults={
                    'name': trns.get('name', ''),
                })
                printings = Printing.objects.filter(card=card, expansion=exp)
                for printing in printings:
                    ptrans, _pt = PrintingTranslation.objects.get_or_create(printing=printing, lang=lang, defaults={
                        'translated_name': trns.get('name', ''),
                        'multiverse_id': trns.get('multiverseid'),
                    })

                    if _pt:
                        self.stdout.write('+', ending='')
                    else:
                        self.stdout.write('.', ending='')
        self.stdout.write('')

    def populate_rulings(self, expdata):
        exp = Expansion.objects.get(code=expdata['code'])
        self.stdout.write(f'Populating rulings for {exp.name}')
        for crd in expdata.get('cards', []):
            card = Card.objects.get(name=crd['name'])
            self.stdout.write('>', ending='')
            for ruling in crd.get('rulings', []):
                text = ruling['text']
                date = arrow.get(ruling['date']).date()
                hash = hashlib.sha1(text.encode('utf-8')).hexdigest()
                rule, _c = Ruling.objects.get_or_create(hash=hash, defaults={
                    'text': text,
                    'date': date,
                })

                if rule not in card.rulings.all():
                    card.rulings.add(rule)
                    self.stdout.write('+', ending='')
                else:
                    self.stdout.write('.', ending='')

        self.stdout.write('')
