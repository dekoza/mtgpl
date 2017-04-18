from django.contrib import admin
from .models import Language, CardTranslation, PrintingTranslation
from apps.mtgdb.admin import Card, CardAdmin


class PrintingTranslationAdmin(admin.ModelAdmin):
    raw_id_fields = ('printing',)
    search_fields = ('printing__card__name', 'translated_name', 'lang__code')

admin.site.register(PrintingTranslation, PrintingTranslationAdmin)


class CardTranslationAdmin(admin.ModelAdmin):
    raw_id_fields = ('card',)
    search_fields = ('card__name', 'translated_name', 'lang__code')

admin.site.register(CardTranslation, CardTranslationAdmin)


admin.site.register([Language, ])


admin.site.unregister(Card)


class TransInline(admin.TabularInline):
    model = CardTranslation
    max_num = 1

class ImprovedCardAdmin(CardAdmin):
    inlines = [TransInline]

admin.site.register(Card, ImprovedCardAdmin)
