# statki

*Uwaga dla rekruterów: ten projekt jest po polsku, ponieważ chciałem dla odmiany napisać coś po polsku i przy okazji skorzystać z tej wygody niedodawania wszędzie `u`, którą daje Python 3. Tak naprawdę wolę kodować po angielsku :). W razie wątpliwości zapraszam [tutaj](https://github.com/tburly/warriors).*

---

Gra w Statki na planszy o arbitralnym rozmiarze z nieznacznie zmodyfikowanymi (czyt. *wzbogaconymi*) zasadami ([więcej](https://github.com/tburly/statki/blob/master/meta/zasady.md)).

Podstawowe różnice względem klasycznej wersji:

1. Statki mają rozmiar **od 1 do 20 pól**. Z tego wynika, że mogą na planszy przybierać dość ekstrawaganckie kształty (np. mogą mieć *dziurę* w środku). Podstawowa zasada umieszczania statków - to, że nie mogą się ze sobą stykać - jest zachowana.

2. Statki mają rangi zależne od rozmiaru:

* 1 pole:     *kuter* (`T`)
* 2-3 pola:   *patrolowiec* (`L`)
* 4-6 pól:    *korweta* (`W`)
* 7-9 pól:    *fregata* (`F`)
* 10-12 pól:  *niszczyciel* (`N`)
* 13-16 pól:  *krążownik* (`K`)
* 17-20 pól:  *pancernik* (`P`)

    które decydują o sile rażenia w trakcie rundy gracza. Uwaga: ta siła rażenia *zmienia się* w trakcie rozgrywki! (w wyniku wrogich trafień).

3. Różna siła rażenia sprowadza się do tego, że w przeciwieństwie do wersji klasycznej:

* pojedyńcza salwa statku może zostać oddana nie w jedno a **w 1-3 sąsiadujące (w poziomie i piona) pola przeciwnika**
* statek może strzelać **od 1 do 3 salwami w ciągu swojej rundy**

4. Każdy statek ma nazwę. Na pierwszy rzut oka może się to wydawać przesadą. Komu to potrzebne w tak prostej grze, prawda? Jak się jednak okazuje (i jak mam nadzieję przekonają się potencjalni gracze) nazwa to taki detal, który dodaje zabawie dodatkowego wymiaru. Przesadą może było wymyślenie aż **690 nazw**. No cóż, poniosło mnie, ale może ktoś jeszcze z tego skorzysta, bo zestaw jest ciekawy i myślę, że każdy, kto pracuje nad polską grą ze statkami/okrętami (w jakiejkolwiek postaci - dajmy na to SF) mógłby z niego skorzystać.

---

**statki** to WIP. Aktualnie zbudowałem większość interfejsu w Tkinterze, co dało efekty lepsze niż się spodziewałem. Teraz przechodzę do pracy nad AI przeciwnika (przynajmniej w jakiejś podstawowej formie) oraz implementacji bardziej zaawansowanych zasad gry (jak trafienia, które obniżają rzeczywistą rangę statku oraz premie dla statków za zatopienie statku przeciwnika). Bieżące rozwijanie programu robię w gałęzi [`develop`](https://github.com/tburly/statki/tree/develop), więc tam należy szukać najbardziej aktualnej wersji.

![Zrzut ekranu z 20180212](/meta/zrzut-ekranu_20180212.png "Zrzut ekranu z 20180212")

---

Ikona statku autorstwa [Macrovector - Freepik.com](https://www.freepik.com/free-vector/ship-icons-collectio_1036114.htm)
