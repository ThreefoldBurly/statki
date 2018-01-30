## GUI

1. [ZROBIONE] <del>PlanszaGUI powinna być pochodną ttk.Frame i zawierać tylko obiekty klas ttk.Label i ttk.Button zorganizowane mniej więcej tak jak teraz. Wymiary ok. 25x30 pól.</del>

2. [ZROBIONE] <<del>W głównej ramce powinny znajdować się dwa obiekty PlanszaGUI - 1 dla własnych statków, drugi dla statków przeciwnika (jak w klasycznej grze)</del>

3. Na prawo od obu plansz powinna znajdować się ramka z widgetami kontrolującymi przebieg gry i zwracającymi informację o nim. Składająca się z 3 sekcji:
    * A.ramki ataku (układ minimum: 3 comboboksy: 1) wyboru statku, 2) wyboru salwy i 3) wyboru orientacji)
    * B.ramki floty (listy statków) - swojej i przeciwnika. Prawdopodobnie najlepszą implementacją będzie Treeview zamknięte w Notebooku
    * C.ramki ogólnej informacji o grze (która tura/runda, kto wygrywa (np. procent nietrafionych pól każdego gracza) oraz przycisk Koniec Rundy - najprostsza implementacja, wystarczy kilka etykiet i jeden przycisk

4. Na dole okna głównego powinna znajdować się ramka z polem tekstowym wypluwającym krótki opis kolejnych rund (jaki statek strzela gdzie i z jakim skutkiem + informacje o zatopieniu kolejnych statków)

5. Główne okno powinno być skalowalne ale jego powiększanie w dół powinno powiększać tylko ramkę dolną (albo głównie ramkę dolną oraz ramkę 3B (listę statków) z sekcji kontrolnej po prawo) a powiększanie w prawo tylko ramkę prawą.

6. Do powyższego należy dołożyć proste menu i 2 okna dialogowe:
    * A. rozpoczęcia gry z ustawieniami początkowymi (przy grze sieciowej inna dla gracza-gospodarza, inna dla gracza-gościa)
    * B. zakończenia gry z informacją podsumowującą jej przebieg i opcją wyjścia/restartu

7. [ZROBIONE] <<del>Pola statków na własnej planszy powinny mieć literowe oznaczenia rangi:

- T: kuter
- L: patrolowiec
- W: korweta
- F: fregata
- N: niszczyciel
- K: krążownik
- P: pancernik

Te oznaczenia powinny pojawiać się również na planszy przeciwnika, ale tylko na polach zatopionych statków</del>

8. Pola planszy (wszystkie: nieodkryte, wody, statków (niezatopionych i zatopionych), oddanych salw (trafień i pudeł)) powinny mieć tooltipy z informacjami, jednak pojawiające się tylko po określonym czasie bezruchu kursora (podobnie jak w Civ5).


