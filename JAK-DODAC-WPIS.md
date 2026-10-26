# Jak dodać wpis na bloga pochmurny.net

Instrukcja krok po kroku. Przykład: wpis „PHP2Shell, czyli Czarny Październik w internecie" z 26.10.2026.

## Co jest potrzebne

- Repozytorium `~/pochmurny.net` (GitHub: `gwolaniuk/pochmurny-blog`), branch `main`.
- Python 3 (skrypt `dodaj-wpis.py` korzysta tylko ze standardowej biblioteki).
- Działający `git push` (skrypt sam commituje i pushuje).

## Krok 1. Wymyśl tytuł i nazwę pliku

Tytuł idzie do nagłówka strony i do listy wpisów. Z niego skrypt robi nazwę pliku HTML (slug).

Przykład: tytuł `PHP2Shell, czyli Czarny Październik w internecie` → plik `wpis-php2shell-czyli-czarny-pazdziernik-w-internecie.html`.

Plik źródłowy nazwij z datą na początku, żeby wpisy sortowały się same:

```text
wpisy/2026-10-26-php2shell-czarny-pazdziernik.md
```

## Krok 2. Utwórz plik `.md` z nagłówkiem

Pierwsze cztery elementy są obowiązkowe. Bez nich skrypt przerwie pracę i wypisze, czego brakuje.

```markdown
# PHP2Shell, czyli Czarny Październik w internecie
data: 2026-10-26
tagi: bezpieczeństwo, php, internet
lead: Najgrubsza dziura w PHP od lat, wyścig z czasem o dobę i botnet, który czekał na okazję.

Treść wpisu zaczyna się tutaj.
```

Zasady dla nagłówka:

- `# Tytuł` — dokładnie jedna linia, pierwsza w pliku.
- `data:` — format `RRRR-MM-DD`. Na stronie pojawi się jako `DD.MM.RRRR`.
- `tagi:` — po przecinku, bez `#`. Na stronie wyświetlą się wielkimi literami jako pigułki.
- `lead:` — jedno zdanie, maksymalnie dwa. Idzie na listę wpisów i do meta description.

## Krok 3. Napisz treść w Markdownie

Obsługiwany jest ograniczony zestaw znaczników. Trzymaj się go, bo konwerter jest prosty i nie zna reszty.

| Element | Zapis | Efekt |
|---|---|---|
| Nagłówek sekcji | `## Tytuł sekcji` | `<h2>` |
| Podnagłówek | `### Tytuł` | `<h3>` |
| Akapit | zwykły tekst, oddzielony pustą linią | `<p>` |
| Lista punktowana | `- element` | `<ul><li>` |
| Cytat | `> tekst` | `<blockquote>` |
| Kod w linii | `` `session.upload_progress` `` | `<code>` |
| Blok kodu | trzy backticki przed i po | `<pre><code>` |
| Pogrubienie | `**tekst**` | `<strong>` |
| Link | `[opis](https://adres)` | `<a href>` |

Czego nie używać:

- Tabel Markdown — nie zostaną sformatowane. Zamień je na listę punktowaną (tak zrobiono z tabelą wersji PHP w przykładzie).
- Poziomej linii `---` — wyjdzie jako akapit z trzema myślnikami.
- Nagłówka `#` w treści — tytuł jest już ustawiony z pierwszej linii.
- Kursywy `*tekst*` — nie jest obsługiwana.

## Krok 4. Uruchom skrypt publikujący

```bash
cd ~/pochmurny.net
python3 dodaj-wpis.py wpisy/2026-10-26-php2shell-czarny-pazdziernik.md
```

Skrypt wykonuje pięć rzeczy:

1. Czyta tytuł, datę, tagi i lead.
2. Generuje `wpis-<slug>.html` z szablonu `wpis.html`: wstawia tytuł, opis, datę, tagi i treść.
3. Liczy czas czytania (200 słów na minutę, minimum 1 minuta).
4. Dodaje nowy wiersz **na górę** listy w `blog.html` i aktualizuje licznik wpisów.
5. Commituje zmiany (`wpis: <tytuł>`) i robi `git push`.

Przykładowy wynik:

```text
OK: wpis-php2shell-czyli-czarny-pazdziernik-w-internecie.html  (wierszy na blogu: 7)
zpushowane — blog zaktualizuje się na https://pochmurny.net/blog.html za ~1 min
```

## Krok 5. Sprawdź efekt

Po około minucie (tyle potrzebuje GitHub Pages na przebudowę) wejdź na:

```text
https://pochmurny.net/blog.html
https://pochmurny.net/wpis-<slug>.html
```

Na liście wpis powinien być pierwszy, z poprawną datą i tagami. W poście sprawdź nagłówki sekcji i to, czy nic nie zostało z surowym Markdownem (np. widoczne `**` albo `##`).

## Krok 6. Gdy coś pójdzie nie tak

**Skrypt przerwał pracę z komunikatem o brakującym polu.** Dodaj brakującą linię (`data:`, `tagi:` lub `lead:`) i uruchom ponownie.

**Wpis jest, ale lista wygląda dziwnie.** Skrypt zawsze dodaje wiersz na górę, więc drugie uruchomienie na tym samym pliku utworzy duplikat. Napraw to tak:

```bash
cd ~/pochmurny.net
git revert HEAD --no-edit   # cofa ostatni commit z publikacją
```

albo popraw `blog.html` ręcznie i zacommituj zmianę.

**Chcesz opublikować bez commita** (np. żeby najpierw obejrzeć efekt lokalnie):

```bash
python3 dodaj-wpis.py wpisy/plik.md --no-git
```

**Zmieniasz treść już opublikowanego wpisu.** Edytuj plik `.md`, usuń stary wiersz z `blog.html` i wygenerowany HTML, potem uruchom skrypt ponownie — albo prościej: popraw wygenerowany plik HTML i `.md`, a potem `git commit` i `git push` bez skryptu.

## Krok 7. Podsumowanie w pięciu linijkach

```bash
cd ~/pochmurny.net
nano wpisy/2026-10-26-moj-tytul.md      # tytuł, data, tagi, lead + treść
python3 dodaj-wpis.py wpisy/2026-10-26-moj-tytul.md
# czekaj ~1 min, sprawdź https://pochmurny.net/blog.html
```

Tyle. Reszta — HTML, lista wpisów, licznik, commit i push — dzieje się sama.
