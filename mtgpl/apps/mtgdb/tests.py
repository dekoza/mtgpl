from django.test import TestCase
from django.utils.six import StringIO
from django.core.management import call_command
from unittest.mock import Mock

from apps.mtgdb.management.commands import populate
from apps.mtgdb.models import Expansion, Card, CardType, CardSubtype, CardColor


class TestPopulateCommandHandling(TestCase):
    """Tests whether handle() calls proper method, depending on expansion option."""

    def setUp(self):
        self.sut = populate.Command
        self.out = StringIO()
        self.sut.populate_from_web = Mock(return_value='Populate from web')
        self.sut.populate_single_expansion = Mock(return_value='Populate single exp')

    def test_populate_cmd_handling_without_expansion(self):
        call_command('populate', stdout=self.out)
        self.assertIn('Populate from web', self.out.getvalue())

    def test_populate_cmd_handling_with_expansion(self):
        call_command('populate', expansion='abc', stdout=self.out)
        self.assertIn('Populate single exp', self.out.getvalue())


class TestPopulatingDatabase(TestCase):
    """Tests populate_expansion() with example test data."""

    def setUp(self):
        self.sut = populate.Command()

        # TEST DATA BLOCK
        self.example_card_1 = {
            "artist": "Richard Thomas",
            "cmc": 5,
            "colorIdentity": ["U"],
            "colors": ["Blue"],
            "flavor": "These spirits of the air are winsome and wild, and cannot be truly contained. Only marginally intelligent, they often substitute whimsy for strategy, delighting in mischief and mayhem.",
            "id": "926234c2fe8863f49220a878346c4c5ca79b6046",
            "imageName": "air elemental",
            "layout": "normal",
            "legalities": [
                {
                    "format": "Commander",
                    "legality": "Legal"
                },
                {
                    "format": "Legacy",
                    "legality": "Legal"
                },
                {
                    "format": "Modern",
                    "legality": "Legal"
                },
                {
                    "format": "Vintage",
                    "legality": "Legal"
                }
            ],
            "manaCost": "{3}{U}{U}",
            "mciNumber": "47",
            "multiverseid": 94,
            "name": "Air Elemental",
            "originalText": "Flying",
            "originalType": "Summon \u2014 Elemental",
            "power": "4",
            "printings": [
                "LEA", "LEB", "2ED",
                "CED", "CEI", "3ED",
                "4ED", "5ED", "PO2",
                "6ED", "S99", "BRB",
                "BTD", "7ED", "8ED",
                "9ED", "10E", "DD2",
                "M10", "DPA", "ME4",
                "DD3_JVC"],
            "rarity": "Uncommon",
            "subtypes": [
                "Elemental"
            ],
            "text": "Flying",
            "toughness": "4",
            "type": "Creature \u2014 Elemental",
            "types": [
                "Creature"
            ]
        }
        self.example_card_2 = {
            "artist": "Mark Poole",
            "cmc": 1,
            "colorIdentity": [
                "U"
            ],
            "colors": [
                "Blue"
            ],
            "id": "aa74b7dc3b30b2e7559598f983543755e226811d",
            "imageName": "ancestral recall",
            "layout": "normal",
            "legalities": [
                {
                    "format": "Commander",
                    "legality": "Banned"
                },
                {
                    "format": "Legacy",
                    "legality": "Banned"
                },
                {
                    "format": "Vintage",
                    "legality": "Restricted"
                }
            ],
            "manaCost": "{U}",
            "mciNumber": "48",
            "multiverseid": 95,
            "name": "Ancestral Recall",
            "originalText": "Draw 3 cards or force opponent to draw 3 cards.",
            "originalType": "Instant",
            "printings": [
                "LEA", "LEB", "2ED",
                "CED", "CEI", "VMA"
            ],
            "rarity": "Rare",
            "reserved": True,
            "text": "Target player draws three cards.",
            "type": "Instant",
            "types": [
                "Instant"
            ]
        }
        self.single_exp = {
            'name': 'TestExp',
            'code': 'EXP',
            'gathererCode': 'exp',
            'oldCode': 'exp',
            'magicCardsInfoCode': 'exp',
            'releaseDate': '2000-01-01',
            'border': 'black',
            'type': 'core',
            'block': 'test',
            # 'onlineOnly', 'booster'
            'cards': [self.example_card_1]
        }
        self.multiple_exps = [
            {
                'name': 'TestExp',
                'code': 'EXP',
                'gathererCode': 'exp',
                'oldCode': 'exp',
                'magicCardsInfoCode': 'exp',
                'releaseDate': '2000-01-01',
                'border': 'black',
                'type': 'core',
                'block': 'test',
                'cards': [self.example_card_1]

            },
            {
                'name': 'TestExp2',
                'code': 'EXP2',
                'gathererCode': 'exp2',
                'oldCode': 'exp2',
                'magicCardsInfoCode': 'exp2',
                'releaseDate': '2000-01-02',
                'border': 'black',
                'type': 'core',
                'block': 'test',
                'cards': [self.example_card_1, self.example_card_2]
            }
        ]
        # END BLOCK

    def test_populating_single_expansion(self):
        self.sut.populate_expansion(self.single_exp)

        exp = Expansion.objects.get()
        self.assertEqual('TestExp', exp.name)
        self.assertEqual('test', exp.block.name)

        card = Card.objects.get()
        self.assertEqual('Air Elemental', card.name)

        c_type = CardType.objects.get()
        self.assertEqual('Creature', c_type.name)

        c_subtype = CardSubtype.objects.get()
        self.assertEqual('Elemental', c_subtype.name)

        c_color = CardColor.objects.get()
        self.assertEqual('blue', c_color.name)

        # def test_populating_multiple_expansions(self):
        #     for expansion in self.multiple_exps:
        #         populate.Command.populate_expansion(expansion)
