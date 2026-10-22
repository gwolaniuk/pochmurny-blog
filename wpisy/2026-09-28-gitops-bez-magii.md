# GitOps bez magii: jeden repo, jeden klaster
data: 2026-09-28
tagi: gitops, kubernetes
lead: Jak nie zamienić swojego pipeline'u w czarną skrzynkę i dlaczego „git push" to najlepszy panel administracyjny.

## Punkt wyjścia: panel, który zniknął

Przez lata zmiany na klastrze robiło się tam, gdzie aktualnie było — `kubectl edit` na produkcji, komuś w środku nocy, kto akurat miał konsolę. Działało, dopóki nie trzeba było odpowiedzieć na pytanie „co się zmieniło we wtorek o 21:14?". Nagle okazało się, że odpowiedź brzmi „nie wiem, trzeba spytać Pawła".

GitOps odwraca to: **repozytorium Git jest jedynym miejscem, gdzie deklarujesz stan klastra**, a proces automatyczny (u mnie Flux) pilnuje, żeby rzeczywistość dogoniła deklarację. Zmiana bez commita po prostu nie istnieje.

## Układ, który lubię: jedno repo, jedno drzewo

```text
clusters/
  prod/
    kustomization.yaml    # lista nakładek poniżej
    infrastructure/       # cert-manager, ingress, external-secrets
    apps/                 # gitea, grafana, authentik, ...
components/
  deployment.yaml         # powtarzalne szablony
```

Zamiast stu repo z „infrastructure-as-code" i osobnego z „app config" — jedno drzewo, jedno źródło prawdy. Nakładki (kustomize) zamiast helmowych wartości, których nikt nie umie później odtworzyć. Zero magii: `kustomize build` lokalnie daje dokładnie to, co trafi do klastra.

## Co to zmienia w praktyce

- **commit = zmiana na produkcji** — z opisem, autorem i review;
- **rollback to `git revert`**, nie „pamiętam, jak było";
- **diff w PR jest audytem** — każdy widzi, że zmieniamy limit pamięci, a nie tylko „ktoś coś poprawiał";
- **środowisko odtwarzalne** — nowy klaster = wystawienie tego samego drzewa, bez zbierania checklist z czatu.

Flux robi swoje: obserwuje repo, renderuje manifesty, **aplikuje różnice** i — co ważne — oznacza commit jako zweryfikowany dopiero, gdy zasoby są zdrowe. Sekcja `healthChecks` w Kustomization to najbardziej niedoceniany element: bez niej Flux uzna za sukces nawet deployment, który crash-loopuje.

## Gdzie ludzie się potykają

- **tajemnicze pole `lastAppliedConfiguration`** i nakładki, które „nie działają, bo coś nadpisuje" — porządek i sens nakładek trzeba ustalić raz, zanim zrobi się ich czterdzieści;
- **sekrety w repo** — nigdy. External Secrets Operator + Vault/SOPS; bez tego GitOps szybko staje się GitLeaks;
- **auto-sync na produkcji** bez bramki: u mnie auto-sync, ale zmiany idą tylko przez PR, a produkcja ogląda wyłącznie `main`;
- **paniczne wyłączanie kontrolera** przy awarii — jeśli GitOps zaboli, to znaczy, że diff powinien przejść przez głową, a nie przez szybki push.

Po roku: zero ręcznych zmian na klastrze, jedno miejsce, gdzie wszystko widać, i odpowiedź na pytanie „co i kiedy" w pięć sekund — `git log --oneline`.

Kod i manifesty: <a href="https://github.com/gwolaniuk" rel="me">github.com/gwolaniuk</a>. Wrażenia i kontrprzykłady: <a href="mailto:grzegorz@pochmurny.net">grzegorz@pochmurny.net</a>.
