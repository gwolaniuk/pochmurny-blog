# Poczta na własnym serwerze — i dlaczego już nie
data: 2026-09-15
tagi: mail, dns, devops
lead: SPF, DKIM, DMARC, reputacja IP i inne powody, dla których nawet uparty DevOps oddaje pocztę komuś innemu.

## To był dobry pomysł

Poczta na własnym serwerze brzmi jak naturalny next step, jeśli i tak masz serwer, DNS-y i paranoję dotyczącą danych. Postawiłem to więc porządnie, nie „na ślinę i modlitwę":

```text
MX      mail17.example.pl          ; tylko jeden MX, szybki i pewny
TXT     v=spf1 include:_spf.example.pl -all
TXT     _dmarc  v=DMARC1; p=quarantine; rua=mailto:dmarc@example.pl
DKIM    2048-bit, rotacja co kwartał
```

Na papierze wszystko się zgadzało: SPF -all, DKIM podpisujący poprawnie, DMARC z raportami na maila. Testy z sieci domowej przechodziły, testy z Gmaila przechodziły, konta lądowały w skrzynce odbiorcy.

## Gdzie to się zaczyna sypać

Problem nie leży w konfiguracji. Leży w tym, że **rynek ufa adresom IP, nie konfiguracji**:

- współdzielone IP z kimś, kto kiedyś wysłał śmieci — i twoje maile idą do spamu;
- nowy zakres dopiero co zarejestrowany — „podejrzany" z automatu;
- Forwardowanie na duży provider z DOMINującym SPFDKIM? Nie, gorzej: jeden serwer źle zarządzanej listy subskrypcyjnej i jedna skarga wystarczą, żeby reputacja spadła na tygodnie;
- weryfikacja przy każdym połączeniu — RBL-e, throttling, DMARC policy u odbiorcy, który wcale nie patrzy na twoje -all, tylko na swój scoring.

Najbardziej bolesny był raport DMARC: 98% wiadomości *udanych*, ale te 2% to nasze własne alerty systemowe, które lądowały u klientów w spamie, a my dowiadywaliśmy się o tym dzień później z telefonu.

## Koszt uczciwy

Utrzymywanie serwera SMTP to nie tylko „umieszczę kontener". To:

- monitoring kolejki i opóźnień (mail opóźniony o 40 minut to mail nieistniejący);
- oddzielna reputacja, z osobnymi narzędziami — Postmaster, SNDS, inboxy testowe;
- backup skrzynek, który weryfikujesz, jak każdy inny backup;
- eskalacje, gdy ktoś dostanie maila po swoim urlopie, bo spam został na serwerze.

Policzylem, ile godzin w miesiącu na to idzie, i porównałem z ceną profesjonalnego hostingu poczty. Wynik był jednoznaczny, choć nie satysfakcjonujący.

## Oddanie poczty nie jest porażką

Przeniosłem skrzynki na dostawcę, który ma to w DNA — z zachowaniem własnej domeny, po aliasach i z tym samym SPF/DKIM/DMARC, tylko podpisane przez kogoś, kto ma globalną reputację na własnej stronie. Sieć routingowa i backupy dalej są moje, poczta już nie.

Zostały mi z tego trzy wnioski:

- **własny serwer od SMTP** ma sens tylko wtedy, gdy mail jest celem samym w sobie, a nie produktem ubocznym;
- **aliasy na własnej domenie** są tym, co naprawdę kupujesz — przenieść je można w godzinę;
- **-all w SPF jest prawidłowy** niezależnie od tego, kto hostuje — i dalej trzeba na to uważać, bo kiedyś utknął u kogoś `+all`.

Kiedyś wrócę — pewnie przy innej domenie i innym podejściu. Do tego czasu poczta jest czyjaś, a ja piszę tu notki.

Historie wojenne: <a href="mailto:grzegorz@pochmurny.net">grzegorz@pochmurny.net</a>.
