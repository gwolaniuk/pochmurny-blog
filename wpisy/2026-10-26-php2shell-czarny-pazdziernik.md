# PHP2Shell, czyli Czarny Październik w internecie
data: 2026-10-26
tagi: bezpieczeństwo, php, internet
lead: Najgrubsza dziura w PHP od lat, wyścig z czasem o dobę i botnet, który czekał na okazję. Opowieść dla ludzi, którzy nie programują — ale z Internetu korzystają.

Cześć!

Jeśli w ostatnich dniach ktoś z Twoich znajomych z branży IT chodził blady i mówił rzeczy typu „nie aktualizujesz PHP? to masz przejechane" — to nie była przesada. Mamy właśnie jeden z tych momentów, o których będzie się pisać w podręcznikach. Nazywa się to **PHP2Shell** i spokojnie mogę powiedzieć: to najgrubsza rzecz w PHP od lat, a może i w całej historii tego języka.

Usiądź wygodnie, bo historia jest naprawdę dobra: z wyciekiem, wyścigiem z czasem, botnetem i sztuczną inteligencją w roli głównej.

## Najpierw: czym w ogóle jest PHP?

Wyobraź sobie, że internet to ogromna biblioteka. Ty podchodzisz do lady i mówisz: „poproszę stronę z moim kontem". Nikt Ci jednak nie podaje książki — najpierw do akcji wkracza **bibliotekarz**, który biegnie między regałami, zbiera potrzebne kartki, skleja je w jeden dokument i dopiero wtedy podaje Ci go do przeczytania.

Tym bibliotekarzem jest właśnie PHP — język programowania działający na serwerze. Nie widzisz go, ale napędza około **70% stron w internecie**: WordPressa, Wikipedię, Drupala, Joomlę, sklepy, fora, blogi, panele logowania, strony urzędów. Jeśli jakaś strona ma logowanie, formularz kontaktowy albo „dodaj do koszyka" — bardzo prawdopodobnie stoi za tym PHP.

I tu jest pies pogrzebany: jeśli coś jest w tym bibliotekarzu zepsute, problem mają nie „jacyś programiści", tylko miliony zwykłych ludzi, którzy z tych stron korzystają.

## Co się zepsuło? Dwie dziury, jeden mechanizm

Podatności są dwie i obie mają CVSS **9.2 na 10**. Dla porównania: słynny Log4Shell z 2021 roku miał 10.0, więc jesteśmy o pół kroku od legendy.

- **CVE-2026-109618** — „korupcja przy braku pamięci". Kiedy PHP kończy mu się pamięć w trakcie obsługi żądania, zostawia po sobie na wpół zbudowane dane. Sprzątacz, który potem po nich chodzi, dostaje śmieci i... robi to, co one każą. Brzmi jak opis z filmu, ale to dosłownie tak działa.
- **CVE-2026-109619** — „martwe dane z poprzedniego gościa". PHP trzyma w pamięci resztki z poprzedniego żądania, mimo że pamięć została już zwolniona (to się nazywa `use-after-free`). Następny gość trafia na te resztki i może nimi sterować.

Efekt obu? **RCE — Remote Code Execution**, czyli zdalne wykonanie kodu. Mówiąc po ludzku: ktoś z drugiego końca świata wysyła na serwer odpowiednio spreparowaną wiadomość i serwer wykonuje jego polecenia. Bez logowania. Bez hasła. Bez niczego. A przy okazji może podejrzeć pamięć procesu, w której spokojnie leżą hasła, tokeny sesji, klucze API i certyfikaty **innych użytkowników**.

Najgorsze: to nie jest dziura w WordPressie ani w jakimś pluginie, którą załatasz aktualizacją wtyczki. To dziura **w samym silniku języka**. Nawet strona „Hello World" na świeżo postawionym PHP była podatna.

I wisienka na torcie: dotyczy **każdej wersji PHP od 5.4 wzwyż**, czyli praktycznie wszystkiego, co kiedykolwiek działało w sieci.

## Jak to odkryto? Tu zaczyna się sci-fi

Sierpień 2026. Zespół badawczy **Wiz** postanawia sprawdzić, czy da się znaleźć głęboko ukryte błędy w kodzie, który ludzie czytali przez dwadzieścia lat. I robi to nietypowo — z pomocą modeli AI (Wiz Atlas, Gemini 4 Argon, GPT-5.6 Sol).

19 sierpnia znajdują pierwszą dziurę. 20 sierpnia potwierdzają przejęcie serwera z Drupalem. 21 sierpnia — WordPress. 24 sierpnia zgłaszają wszystko zespołowi PHP. Ten potwierdza 21 września i zaczyna pracę nad poprawką. Wszystko idzie zgodnie ze sztuką, w tajemnicy, żeby hakerzy nie zdążyli.

I wtedy, 20 października, **wszystko się rozsypuje**. Identyfikatory CVE zaczynają krążyć po forach i mediach społecznościowych. Ktoś podaje błędną godzinę wydania poprawki i zmyśloną ocenę 10.0. Szczegółów technicznych na szczęście nie ma, ale jest jasny sygnał: „coś grubego w PHP, szykujcie się".

Zespół PHP robi rzecz bezprecedensową — **przyspiesza premierę o dzień**. Poprawki wychodzą 21 października o 13:40 UTC, zamiast 22 października. Cloudflare zdążył wdrożyć reguły ochronne o 3:02 w nocy, czyli dziewięć godzin przed łatką. Brzmi jak akcja z filmu o wyścigu zbrojeń? To był dokładnie taki wyścig.

## A teraz najciekawsze: co się działo w sieci

I tu wchodzimy w najbardziej nerdowski fragment tej historii, bo dane z sensorów są piękne w swoim przerażeniu.

**Ktoś próbował exploitować dziurę ZANIM ją opublikowano.** Amazon, przez swoją sieć honeypotów MadPot, zarejestrował próbę ataku **17 października** — cztery dni przed ujawnieniem i w trakcie embargo. Źródło: adres z sieci anonimizującej. Jak ktoś się o tym dowiedział, do dziś nie wiadomo. To trochę jakby ktoś zapukał do Twoich drzwi, zanim jeszcze kupiłeś mieszkanie.

**Skala skanowania jest absurdalna.** Laboratorium Delft Threat Intelligence (honeypoty + teleskop sieciowy) naliczyło od 21 do 26 października **ponad 41 tysięcy żądań eksploatacyjnych z 566 adresów IP, w 267 sieciach autonomicznych i 67 krajach**. 168 z tych adresów posłało nie tylko sondę, ale realny kod lub droppera. Najgorętsza godzina: 21 października, 21:00 UTC — **2 116 żądań w sześćdziesiąt minut**.

Fastly z kolei zobaczył do południa 22 października około **250 tysięcy żądań od narzędzi nazywających się „php2shell"**, z około 3 200 adresów IP. I tu ważny szczegół, który lubię: część tego ruchu to... obrońcy, którzy sami skanowali własne zasoby. W internecie naprawdę trudno odróżnić złego od dobrego, gdy obaj używają tych samych narzędzi.

**Ale — i to jest kluczowe — nikt publicznie nie potwierdził udanego włamania.** Sophos musiał publicznie skorygować własny raport: początkowo napisał, że widział udaną eksploatację u klienta, potem przyznał, że to były tylko skany i nieudane próby. CrowdStrike też nie widział sukcesu. Sansec zauważył, że krążące publicznie exploity **nie działały na domyślnych instalacjach** — wymagały specyficznej konfiguracji albo dodatkowych błędów w aplikacji. CISA do dziś **nie wpisała tych CVE do katalogu KEV** (sprawdziłem: katalog z 23 października, 1 756 wpisów, obu podatności brak).

Czyli: napastnicy walą drzwiami i oknami, ale większość z nich nie ma klucza. Na razie.

**A co z tym botnetem?** Sophos i Arctic Wolf zauważyli, że część ataków próbuje zainstalować **Potassium** — rozbudowaną mutację botnetu **Mirai**, który zamienia zhakowane serwery w armaty do ataków DDoS. Ten konkretny egzemplarz jest całkiem wyrafinowany: szyfruje swoją konfigurację algorytmem ChaCha20, ukrywa ruch jednym bajtem, a adresy serwerów dowodzenia potrafi rozwiązywać przez **Ethereum Name Service** (tak, blockchain jako DNS dla malware — cyberprzestępcy też lubią nowinki).

## Fabryka nieporozumień, czyli jak rodzi się panika

Tu muszę być z Tobą szczery, bo to najlepsza lekcja z całej tej historii.

23 października **Unit 42** (Palo Alto Networks) opublikowało głośny raport: atak na europejską instytucję rządową, w którym napastnik używał **agenta AI** do prowadzenia działań po włamaniu. W ciągu dwóch godzin miał dotrzeć do hashy haseł i sekretów MFA, postawić tunel NTLM do Active Directory i próbować eskalować do Domain Admina. Rozpoznano go po tym, że polecenia wysyłał w blokach z delimiterami — bo tak formatuje się prompty dla modeli językowych.

Dwa dni później Unit 42 **wycofało tę ocenę**. Przyznali, że nie potrafią potwierdzić, że wejście nastąpiło właśnie przez PHP2Shell. Włamanie było, ale przypisanie do tej konkretnej dziury — nie.

To jest bardzo ważne, bo pokazuje, jak wygląda rzeczywistość w pierwszych dniach po ujawnieniu luki: agencje, firmy i dziennikarze publikują ustalenia, które za 48 godzin trzeba prostować. **Czytaj komunikaty, ale sprawdzaj, kto je później skorygował.**

Równolegle rządy zaczęły działać: CISA w USA, NCSC w Wielkiej Brytanii, ENISA i Europol w UE, CERT-PH na Filipinach (26 października), Oracle, AWS, Microsoft, Google Cloud, cPanel. Część organizacji poszła na całość i **po prostu wyłączyła swoje strony** do czasu łatania. Epizod zyskał przez to nazwę „**Black October**" — i szczerze mówiąc, trudno się dziwić.

Skalę pokazują liczby: Censys doliczył się **34,4 miliona** usług PHP w wersjach potencjalnie podatnych. Unit 42 mówi o 22,6 miliona wystawionych instancji. To nie jest problem niszowy.

## Dobra wiadomość: jest łatka. Zła: nie ma wymówek

Poprawki wyszły 21 października:

- PHP 8.5 → **8.5.12**
- PHP 8.4 → **8.4.27**
- PHP 8.3 → **8.3.36**
- PHP 8.2 → **8.2.35**

Dla starszych wersji (7.4, 8.0, 8.1) PHP udostępniło minimalne backporty źródeł, a dostawcy hostingu i dystrybucje wydali własne paczki.

I tu najważniejsze zdanie z komunikatu PHP Foundation: **nie ma kompletnych obejść konfiguracyjnych**. Aktualizacja to jedyne pełne rozwiązanie. Można się wspomagać (WAF, limity pamięci, wyłączony `session.upload_progress`, na PHP 8.5 wyłączone `fatal_error_backtraces`), ale to plaster, nie operacja.

Dodatkowo 23 października pojawiła się trzecia dziura — **CVE-2026-115560** — na razie bez łatki, z obejściem `session.upload_progress.enabled = 0` w `php.ini` (i restart wszystkich workerów; `ini_set()` nie wystarczy).

A horyzont się nieco chmurzy: VulnCheck zbudował exploit na CVE-2026-109618, który **omija ASLR** (mechanizm losowego układania pamięci, teoretycznie utrudniający ataki) na x86-64 i działa nawet przy wyłączonym wyświetlaniu błędów. Na razie trzyma go dla klientów, ale to znak, że bariera wejścia powoli spada.

## Co to znaczy dla Ciebie, zwykłego człowieka?

Trzy rzeczy. Po kolei.

**1. Jeśli masz stronę, bloga albo sklep** — zapytaj hosting, czy PHP jest załatane. Nie „czy aktualizujecie", tylko konkretnie: „czy mam wersję 8.2.35 / 8.3.36 / 8.4.27 / 8.5.12 lub nowszą?".

**2. Jeśli korzystasz z cudzych stron** — nie masz nad tym kontroli, ale możesz ograniczyć szkody. Zmieniaj hasła tam, gdzie dostałeś ostrzeżenie. Używaj menedżera haseł, żeby wyciek z jednego serwisu nie ciągnął za sobą pozostałych. Włącz dwuskładnikowe logowanie wszędzie, gdzie się da — bo dane z pamięci serwera to często właśnie tokeny sesji i sekrety MFA.

**3. Jeśli widzisz w mediach „hakerzy przejęli pół internetu"** — weź głęboki oddech. Na dziś nie ma potwierdzonego, publicznie udokumentowanego przypadku udanego wykorzystania PHP2Shell do przejęcia serwera w realnym środowisku produkcyjnym. Są masowe próby, są nieudane ataki, jest botnet czekający na okazję. Ale to nie to samo co „już po wszystkim".

## Czego nas to uczy (i czemu jest fascynujące)

**Po pierwsze:** AI zmieniła reguły gry w wyszukiwaniu błędów. Dziura, która siedziała w PHP przez ponad dekadę i wymagała łańcucha tak skomplikowanego, że „na granicy ludzkich możliwości", została znaleziona przez modele w kilka dni. To dobra wiadomość dla obrońców — i zła, bo dokładnie te same modele pomagają potem budować exploity.

**Po drugie:** najsłabszym ogniwem nie jest kod, tylko **czas**. Wszystko rozsypało się nie dlatego, że poprawka była zła, ale dlatego, że identyfikatory CVE wyciekły dobę za wcześnie. Doba. W internecie doba to epoka.

**Po trzecie:** liczby nie kłamią, ale nagłówki owszem. 250 tysięcy żądań atakujących i zero potwierdzonych włamań to nie sprzeczność — to dowód, że „masowe skanowanie" i „masowa kompromitacja" to dwa zupełnie różne zjawiska. Nauczenie się odróżniania ich to dziś umiejętność na wagę złota, także dla ludzi spoza IT.

Mnie ta historia fascynuje, bo pokazuje internet takim, jaki jest naprawdę: kruchym, ale też zadziwiająco odpornym. Tysiące ludzi, których nie znasz, pracowało w nocy z 20 na 21 października nad łatką, którą Ty zainstalujesz jednym poleceniem i o której zapomnisz do przyszłego roku. To całkiem niezły powód, żeby mimo wszystko wierzyć w tę sieć.

A teraz idź sprawdzić, jaką masz wersję PHP. Serio.

> Źródła: PHP Foundation (komunikat z 21.10.2026), GitHub Security Advisory GHSA-6wmf-4rv5-p3rp, CISA, ENISA, NCSC-UK, CERT-PH, Wiz Research, Sophos, Unit 42 (brief zaktualizowany 25.10.2026), AWS Threat Intelligence, Fastly, Delft Threat Intelligence Lab, Censys, VulnCheck, Qualys, Rapid7.
