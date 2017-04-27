from django.test import TestCase
from django.utils.six import StringIO
from django.core.management import call_command
from unittest.mock import Mock
from apps.mtgdb.management.commands import populate


# Create your tests here.
class TestPopulateCommandHandling(TestCase):
    """Test whether handle() calls proper method, depending on expansion option."""

    def setUp(self):
        self.sut = populate.Command
        self.out = StringIO()
        self.sut.populate_from_web = Mock(return_value='From web')
        self.sut.populate_single_expansion = Mock(return_value='Single exp')

    def test_populate_cmd_handling_without_expansion(self):
        call_command('populate', stdout=self.out)
        self.assertIn('From web', self.out.getvalue())

    def test_populate_cmd_handling_with_expansion(self):
        call_command('populate', expansion='abc', stdout=self.out)
        self.assertIn('Single exp', self.out.getvalue())
