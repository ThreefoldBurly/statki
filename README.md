# statki

Gra w statki na planszy o arbitralnym rozmiarze.

Statki mają rangi:

- kuter (1 pole)
- patrolowiec (2-3 pola)
- korweta (4-6 pól)
- fregata (7-9 pól)
- niszczyciel (10-12 pól)
- krążownik (13-16 pól)
- pancernik (17-20 pól)

Każdy statek ma nazwę. Nazwa to taki detal, który robi klimat. Nawet w tak prostej grze jak statki. Dlatego poświęciłem trochę czasu, żeby program miał z czego wybierać. Jak na razie plik `nazwy-statkow.sti` zawiera 690 wymyślonych przeze mnie nazw. Trochę nad tym posiedziałem i myślę, że każdy, kto pracuje nad polską grą ze statkami (w jakiejkolwiek postaci - dajmy na to SF), mógłby na tym skorzystać. 

Statki mają dowolne kształty. Algorytm umieszcza je na planszy pole po polu, losując kierunek: *prawo*, *lewo*, *góra*, *dół*.

Logika umieszczania statków na planszy jest zakończona (w sumie ten sam algorytm mógłby służyć do rysowania map dla strategii 2D). Zaczynam pracę nad GUI (w Kivy).