from collections import defaultdict

from django.views.generic import DetailView, ListView
from apps.mtgdb.models import Expansion, Card, Artist


class ExpansionList(ListView):
    model = Expansion
    context_object_name = 'expansion_list'

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     qs = qs.filter(exp_type__in=['expansion', 'core'])
    #     return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_exp'] = Expansion.objects.exclude(exp_type__in=['expansion', 'core'])
        return context


class ExpansionDetail(DetailView):
    model = Expansion
    context_object_name = 'expansion'
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['printed_cards'] = obj.printing_set.all()
        return context


class ArtistList(ListView):
    model = Artist
    context_object_name = 'artist_list'


class ArtistDetail(DetailView):
    model = Artist
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        # painted_cards = defaultdict(list)
        # for obj in obj.painted_cards.all():
        #     painted_cards[obj.card].append(obj)
        context['painted_cards'] = obj.painted_cards.all()
        return context
