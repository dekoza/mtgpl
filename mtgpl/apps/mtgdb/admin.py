from django.contrib import admin

from .models import (
    Format, Legality, Block, Expansion, Artist, Rarity, CardSupertype, CardType, CardSubtype,
    CardColor, Card, Printing, Ruling
)


class MyAdminTemplate(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True


class ArtistAdmin(MyAdminTemplate):
    list_display = list_display_links = ('mtgjson_id',)
    search_fields = ('mtgjson_id',)

admin.site.register(Artist, ArtistAdmin)


class PrintingAdmin(MyAdminTemplate):
    search_fields = ('card__name',)

admin.site.register(Printing, PrintingAdmin)


class CardAdmin(MyAdminTemplate):
    search_fields = ('name',)
    raw_id_fields = ('front_side', 'rulings', )
    fieldsets = (
        (None, {
            'fields': ('name', 'text',)
        }),
        ('Basic info', {
            'fields': ('mana_cost', 'power', 'toughness', 'loyalty', ),
            'classes': ('collapse',),
        }),
        ('More details', {
            'fields': ('cmc', 'colors', 'hand_mod', 'life_mod', 'reserved', 'front_side',
                       'supertypes', 'types', 'subtypes', 'rulings'),
            'classes': ('collapse',),
        })
    )

admin.site.register(Card, CardAdmin)


admin.site.register((
    Format, Legality, Block, Expansion, Rarity, CardSupertype, CardType, CardSubtype,
    CardColor, Ruling
), MyAdminTemplate)

