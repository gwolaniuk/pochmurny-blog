# Authentik, SSO i jedna tożsamość na dwadzieścia usług
data: 2026-08-12
tagi: sso, self-hosted, security
lead: Jak przestać pamiętać dwadzieścia haseł i zacząć pamiętać jedno bardzo dobre.

## Problem: dwadzieścia usług, dwadzieścia haseł

Po latach samodzielnych hostowania lądujesz w punkcie, w którym masz managera haseł pełnego wpisów typu `admin@something: Zm3nH4slo2!` i nawyk logowania się osobno do każdego panelu. Każda usługa to osobny silnik sesji, osobna polityka haseł i — co gorsza — osobne konto, które trzeba wyłączyć, gdy ktoś odchodzi z projektu.

Rozwiązanie nazywa się SSO i od lat jest standardem w korporacjach. Nic nie stoi na przeszkodzie, żeby postawić je u siebie.

## Co wybrałem: Authentik

Postawiłem <a href="https://goauthentik.io" rel="nofollow">Authentik</a> — aplikację w stylu Keycloak/Dex, ale z sensownym UI i niskim progiem wejścia. Użytkownicy i grupy żyją w jednym miejscu (u mnie source of truth to LDAP do Proxmoxa/LDAP-a, ale może to być OIDC albo nawet lokalna baza).

Dwie ścieżki integracji:

- **OAuth2 / OIDC** — tam, gdzie aplikacja potrafi: Gitea, Nextcloud, Portainer, Grafana. Trzy zmienne środowiskowe i gotowe;
- **forward auth (`auth_request`)** — tam, gdzie nie potrafi: panel nginx-a, Proxmox, VictoriaMetrics. Nginx pyta Authentika o zgodę, a potem przepuszcza tylko z ważnym cookie.

```nginx
location / {
    auth_request /auth-verify;
    proxy_set_header X-Authentik-Username $upstream_http_x_authentik_username;
}
location = /auth-verify {
    proxy_pass http://authentik/outpost.goauthentik.io/auth/nginx;
    proxy_set_header X-Original-URL $scheme://$http_host$request_uri;
}
```

## Rzeczy, które bolą przy pierwszym montażu

- **Pierwsze konto zakłada się jednorazowim tokenem** z logów kontenera — łatwo o to zapomnieć, gdy stawiasz wszystko z pamięci;
- **flująca aplikacja po autoryzacji** — nie każda apka umie zrozumieć, że IDP zniknął. Błędy 401/500 w proxy zwykle znaczą „aplikacja dostała inny claim, niż się spodziewała";
- **konto break-glass** — lokalne konto administratora wyłączone na co dzień. Jeśli Authentik zdechnie w niedzielę o 23:00, bez niego nie wejdzesz nawet do panelu, żeby go włączyć;
- **wylogowanie globalne** — po wyłączeniu konta użytkownika sesje żyją do końca TTL. Włączcie krótkie TTL na aplikacjach, gdzie to ma znaczenie.

## Ile to dało

Jedno bardzo dobre hasło (długie, w managerze), jeden klucz sprzętowy FIDO2 zamiast dwudziestu kroków SMS i jedno miejsce, w którym wyłączam dostęp — jednym kliknięciem, nie telefonem do pięciu osób.

Minus jest jeden: po tygodniu z SSO irytujesz się przy każdej usłudze, która *nie* obsługuje logowania przez OIDC.

Konfiguracja i przykłady: <a href="https://github.com/gwolaniuk" rel="me">github.com/gwolaniuk</a>. Pytania: <a href="mailto:grzegorz@pochmurny.net">grzegorz@pochmurny.net</a>.
