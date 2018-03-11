### STRUKTURA TYPOWEGO PYTHONOWEGO PROJEKTU
##### na podstawie [`tablib`](https://github.com/kennethreitz/tablib) autorstwa Kennetha Reitza

```
/foo:
  |-----foo:
  |-----docs:
  |-----metapliki...
```

1. `/foo` - katalog główny projektu
2. `/foo/foo` - katalog kodu źródłowego (odpowiednik `src` w Javie)
3. `/foo/docs` - dokumentacja
4. `/foo/metapliki...` - różne dotatkowe pliki typu:
    * `.gitignore`
    * `README.md` i `LICENCE.md`
    * informujące o historii wersji, autorach, zaleceniach dla chcących dołączyć do projektu itp.
    * `setup.py` - plik, który zawiera logikę parsowania argumentów ze standard input oraz rzeczy związane z `setuptools`
    * pliki związane z publikacją projektu
    * `test_foo.py` - moduł testów

```
/foo:
  |-----foo:
         |------bar
         |------packages
         |------__init__.py
         |------pliki_zrodlowe...
```

1. `/foo/foo/bar` - pakiet modułów (lub innych pakietów) kodu źródłowego, najczęściej tworzony, gdy jeden z modułów znajdujących się w `/foo/foo/` rozrośnie się za bardzo i wymaga rozbicia na submoduły
2. `/foo/foo/packages` - zewnętrzne dependencje wbudowane w projekt
3. `__init__.py` - moduł inicjujący, którego obecność przed Pythonem 3.3 była konieczna, by dany katalog mógł być traktowany przez interpreter Pythona za pakiet. Teraz obecność tego modułu jest opcjonalna, ale może być konieczny do dokonywania specjalnych manipulacji np. typu modyfikacja namespace'u pakietu głównego `foo` tak by odsłaniał na zewnątrz tylko API projektu (czyli wyselekcjonowany podzbiór obiektów - tak właśnie jest przypadku `tablib`). Wszystko co pojawi się w namespac'ie tego modułu jest dodawane do namespece'u pakietu, w którym się znajduje (w związku z tym można np. wszystkie moduły pakietu zebrać w jednej zmiennej tak jak to robi `/tablib/tablib/formats/__init__.py`)
4. `pliki_zrodlowe...` - podstawowe moduły kodu źródłowego (w przypadku `tablib` są to tylko 2 moduły: `core.py` i `compat.py` - pierwszy z główną logiką, drugi zapewniający kompatybilność z Pythonem 2)

Przykład jak `/tablib/tablib/__init__.py` odsłania wybrane API:

```
""" Tablib. """

from tablib.core import (
    Databook, Dataset, detect_format, import_set, import_book,
    InvalidDatasetType, InvalidDimensions, UnsupportedFormat,
    __version__
)
```

w efekcie np. w module `/tablib/tablib/formats/_json.py` można importować bezpośrednio:

`import tablib`

zamiast

`import tablib.core`

#### [więcej](http://docs.python-guide.org/en/latest/writing/structure/)

**WAŻNE:** *aby zachować taką organizację importów jw., aplikacja musi być uruchamiana z poziomu katalogu głównego projektu*
