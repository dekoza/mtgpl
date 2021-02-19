Spolszczenie do gry Magic Arena
===============================

UWAGA: Tłumaczenie jest w wersji mocno rozwojowej. Bardzo dużo kart jest już przetłumaczonych,
ale dużo jeszcze brakuje. Proces przenoszenia tłumaczeń cały czas trwa. Pamiętaj też, że tłumaczenia
mogą zwierać błędy - czasem istotnie zmieniające sens kart. Dołożyliśmy wszelkich starań, żeby wyeliminować
takie przypadki, jednak mogą one występować i nie możesz mieć do nas o to pretensji. Ten projekt
jest całkowicie hobbystyczny. Przed graniem jakiegoś ważnego turnieju lepiej przełącz się na oficjalnie wspierany język.

Pobranie tłumaczenia
--------------------

1. Wejdź na `stronę, gdzie publikuję wydania <https://github.com/dekoza/mtgpl/releases/>`_.
2. Na samej górze jest najnowsza wersja. Dla ułatwienia dodaję do tytułu datę wydania.
3. Na samym dole danego wydania jest sekcja Assets, rozwiń ją.
4. Pobierz plik, którego nazwa zaczyna się od ``MTGA_DATA`` - tam są pliki używane przez grę.
5. Znajdź katalog instalacji gry na swoim komputerze. Domyślnie powinien to być ``C:\Program Files\Wizards of the Coast\MTGA\``
6. Wewnątrz znajduje się katalog ``MTGA_Data``. Skopiuj znajdujące się w nim katalogi ``Data`` oraz ``Loc`` w jakieś bezpieczne miejsce.
7. Rozpakuj pobrane archiwum. Jego struktura odzwierciedla zawartość powyższego katalogu ``MTGA_Data`` - przekopiuj pliki w odpowiednie miejsca nadpisując oryginalne plilki.
8. Uruchom grę. Wejdź do opcji (trybik na górze po prawej), wybierz Graphic. Rozwiń listę opcji "Locale" - w miejscu portugalskiego powinna być opcja ``Polski + English``,
   a w miejscu francuskiego – ``Pl + En (DEBUG)``. Pierwsza opcja jest dla normalnych graczy. Teksty, które nie zostały jeszcze przetłumaczone na polski będą się wyświetlać po angielsku
   (za wyjątkiem pierwszych kilku komunikatów tuż po uruchomieniu gry, których z jakichś powodów nie da się przetłumaczyć). Druga opcja jest przeznaczona dla osób chcących pomóc
   przy tłumaczeniu programu. Nieprzetłumaczone teksty są tam zastąpione identyfikatorami pozwalającymi szybko znaleźć dany tekst w plikach językowych.
9. Tak, nie ma (większości) polskich znaków. Niestety czcionka używana w grze zawiera póki co tylko litery "ł", "ó" oraz "ń". Pozostałe nie są w ogóle wyświetlane.
   Jeśli możesz, `wesprzyj prośbę dodania pozostałych polskich znaków <https://feedback.wizards.com/forums/918667-mtg-arena-bugs-product-suggestions/suggestions/42713978-please-add-more-diacritics-to-ingame-font>`_.
   Jak tylko czcionka zostanie uzupełniona, pliki zostaną zaktualizowane.
10. Miłej zabawy!

Sprawdzaj co jakiś czas stronę z punktu 1 - proces tłumaczenia będzie trwał dopóki wszystko nie zostanie przetłumaczone. Możesz więc spodziewać się
regularnych aktualizacji.

Przygotowuję program, który sam wykona wszystkie powyższe operacje, ale to jeszcze trochę potrwa - cierpliwości!

PS.
Mobilna wersja gry korzysta z tej samej struktury plików. Może się zatem okazać, że te same pliki zadziałają po przekopiowaniu ich na urządzenie mobilne.
Tak czy inaczej ta opcja też jest na tapecie i wkrótce pojawi się szczegółowa instrukcja spolszczenia wersji mobilnej.
