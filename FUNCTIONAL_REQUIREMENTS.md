# Employee Manager — Wymagania aplikacji

## 1. Cel aplikacji

Aplikacja „Employee Manager” służy do zarządzania pracownikami poprzez:
- dodawanie pracowników,
- edycję danych pracownika,
- usuwanie pracowników,
- wyświetlanie listy pracowników,
- oznaczanie pracownika jako przebywającego na urlopie.

Aplikacja działa w modelu klient-serwer:
- backend: FastAPI,
- frontend: HTML + CSS + Vanilla JavaScript.

# 2. Funkcjonalności aplikacji

## 2.1 Zarządzanie pracownikami

Użytkownik powinien mieć możliwość:
- dodania nowego pracownika,
- edycji istniejącego pracownika,
- usunięcia pracownika,
- przeglądania listy pracowników,
- zresetowania wszystkich danych (usunięcia wszystkich pracowników jednym działaniem).

# 3. Model pracownika

## 3.1 Pola w żądaniu (request)

Treść żądania `POST`/`PUT` powinna zawierać następujące pola:

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| name | string | Tak | Imię i nazwisko pracownika |
| salary | integer | Tak | Wynagrodzenie |
| age | integer | Tak | Wiek pracownika |
| position | enum/string | Tak | Stanowisko pracownika |
| on_leave | boolean | Nie (domyślnie `false`) | Status urlopu |

## 3.2 Pole `id`

* jest generowane automatycznie przez backend przy dodaniu pracownika,
* nie powinno być wysyłane w treści żądania `POST`/`PUT` — jeśli zostanie przesłane, jest ignorowane,
* występuje wyłącznie w odpowiedzi API (`id` + pola z sekcji 3.1),
* jest unikalne i inkrementowane przy każdym nowo dodanym pracowniku,
* jest resetowane do wartości `1` po wywołaniu `POST /api/employees/reset`.

# 4. Walidacja danych

## 4.1 Pole Name

Pole `name`:
- musi być wymagane,
- minimalna długość: `1`,
- maksymalna długość: `50`,
- powinno akceptować:
  - litery,
  - cyfry,
  - pojedyncze spacje,
- nie powinno akceptować znaków specjalnych.

### Regex walidacyjny

```bash
^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż0-9]+(?: [A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż0-9]+)*$
```

## 4.2 Pole Salary

Pole `salary`:

* musi być typu integer,
* minimalna wartość: 1,
* maksymalna wartość: 200000.

## 4.3 Pole Age

Pole `age`:

* musi być typu integer,
* minimalna wartość: 18,
* maksymalna wartość: 65.

## 4.4 Pole Position

Pole `position`:

* musi być wymagane,
* powinno być wybierane wyłącznie z listy rozwijanej (dropdown),
* powinno obsługiwać wyłącznie następujące wartości:
    - Junior QA
    - Mid QA
    - Senior QA
    - QA Lead

## 4.5 Pole On Leave

Pole `on_leave`:

* powinno być typu boolean,
* powinno być prezentowane jako checkbox,
* domyślna wartość: false.

## 4.6 Pole Username (logowanie)

Pole `username` (formularz logowania, `POST /api/login`):
- musi być wymagane,
- minimalna długość: `1`,
- maksymalna długość: `10`,
- powinno akceptować:
  - litery (bez polskich znaków diakrytycznych),
  - cyfry,
- nie powinno akceptować spacji ani znaków specjalnych.

### Regex walidacyjny

```bash
^[A-Za-z0-9]{1,10}$
```

## 4.7 Pole Password (logowanie)

Pole `password` (formularz logowania, `POST /api/login`):
- musi być wymagane,
- minimalna długość: `1`,
- maksymalna długość: `20`,
- powinno akceptować:
  - litery (bez polskich znaków diakrytycznych),
  - cyfry,
  - znaki specjalne: `! @ # $ % ^ & * ( ) _ + - = [ ] { } | ; : , . < > ? / ~ \``,
- nie powinno akceptować spacji ani polskich znaków diakrytycznych.

### Regex walidacyjny

```bash
^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{}|;:,.<>?/~`]{1,20}$
```

# 5. UI aplikacji
## 5.1 Navbar

Navbar powinien zawierać:

* logo aplikacji,
* przycisk resetu danych (`Reset Data`),
* przycisk zmiany motywu.

## 5.2 Motyw aplikacji

Aplikacja powinna obsługiwać:
* dark mode,
* light mode.

Wybrany motyw powinien:
* być zapisywany w localStorage,
* być przywracany po odświeżeniu strony.

## 5.3 Modal potwierdzenia resetu danych

Kliknięcie przycisku `Reset Data` powinno:
* otwierać modal potwierdzenia (nie wykonywać resetu od razu),
* wyświetlać tytuł `Reset Data`,
* wyświetlać treść ostrzegawczą informującą, że operacja jest nieodwracalna,
* zawierać przycisk `Cancel` zamykający modal bez wykonania żadnej akcji,
* zawierać przycisk `Delete All` wywołujący reset danych i zamykający modal.

Modal:
* powinien być natywnym elementem HTML aplikacji (nie przeglądarkowym `confirm()`),
* powinien być spójny wizualnie z resztą UI (dark/light mode, rounded corners, accent color).

**Wszystkie modale w aplikacji (treść, przyciski) muszą być w języku angielskim.**

Po potwierdzeniu resetu (`Delete All`) aplikacja powinna:
* usunąć wszystkich pracowników,
* wyczyścić formularz dodawania/edycji — jeśli formularz był w trybie edycji, powinien wrócić do trybu `Add Employee`,
* odświeżyć tabelę pracowników (powinna zostać pusta).

# 6. Formularz pracownika
## 6.1 Formularz dodawania

Formularz powinien zawierać:

* pole `Name`,
* pole `Salary`,
* pole `Age`,
* dropdown `Position`,
* checkbox `On vacation`,
* przycisk `Add`.

## 6.2 Formularz edycji

Po kliknięciu przycisku `Edit`:

* formularz powinien zostać uzupełniony danymi pracownika,
* przycisk Add powinien zmienić się na Update,
* formularz powinien przejść w tryb edycji.

# 7. Dropdown stanowiska

Dropdown stanowiska:

* powinien posiadać placeholder: Select position,
* powinien uniemożliwiać wpisywanie własnych wartości,
* powinien pozwalać wyłącznie na wybór dostępnych opcji.

# 8. Checkbox urlopu

Checkbox:
* powinien umożliwiać oznaczenie pracownika jako będącego na urlopie,
* powinien być odznaczony domyślnie.

# 9. Tabela pracowników
## 9.1 Kolumny tabeli

Tabela powinna zawierać następujące kolumny:

| Kolumna | Opis |
|---|---|
| ID | Unikalny identyfikator pracownika |
| Name | Imię i nazwisko pracownika |
| Salary | Wynagrodzenie pracownika |
| Age | Wiek pracownika |
| Position | Stanowisko pracownika |
| Vacation | Status urlopu pracownika |
| Actions | Dostępne akcje |

## 9.2 Status urlopu

Kolumna `Vacation` powinna wyświetlać:

| Wartość | Znaczenie |
|---|---|
| ✅ | Pracownik przebywa na urlopie |
| ❌ | Pracownik nie przebywa na urlopie |


## 9.3 Akcje

Kolumna `Actions` powinna zawierać:

| Przycisk | Opis |
|---|---|
| Edit | Edycja danych pracownika |
| Delete | Usunięcie pracownika |

## 9.4 Stan pusty

Gdy lista pracowników jest pusta (np. po wywołaniu resetu lub przy pierwszym uruchomieniu):
* tabela nadal wyświetla nagłówki kolumn,
* `tbody` nie zawiera żadnych wierszy,
* aplikacja nie wyświetla obecnie dedykowanego komunikatu typu „Brak pracowników” — do rozważenia jako przyszłe usprawnienie UX.

# 10. Obsługa błędów

## 10.1 Kody statusu HTTP

| Scenariusz | Kod statusu | Treść odpowiedzi |
|---|---|---|
| Operacja zakończona sukcesem (`GET`, `POST`, `PUT`, `DELETE`, `POST /reset`) | 200 | Zaktualizowany zasób / lista / status |
| Niepoprawne dane wejściowe (`name`, `salary`, `age`, `position`) | 422 | `{"detail": [...]}` — lista błędów walidacji Pydantic |
| `PUT`/`DELETE` na nieistniejącym `id` | 404 | `{"detail": "Employee not found"}` |

## 10.2 Walidacja backendowa

Backend powinien zwracać błędy walidacyjne (422) dla:
- niepoprawnego `name`,
- niepoprawnego `salary`,
- niepoprawnego `age`,
- niepoprawnego `position`,
- niepoprawnego `username` lub `password` przy logowaniu (`POST /api/login`) — patrz 4.6, 4.7.

## 10.3 Nieznaleziony pracownik (404)

Endpointy `PUT /api/employees/{id}` oraz `DELETE /api/employees/{id}` powinny:
- zwracać kod `404`, jeśli pracownik o podanym `id` nie istnieje,
- zwracać treść `{"detail": "Employee not found"}`.

## 10.4 Error Box

Frontend powinien:
- wyświetlać komunikaty błędów,
- prezentować je w czerwonym kontenerze,
- ukrywać sekcję błędów przy poprawnym żądaniu.


# 11. Dokumentacja API (swagger)

http://127.0.0.1:8000/docs

# 12. Wymagania techniczne

## 12.1 Frontend

Frontend powinien:
- korzystać z:
  - HTML,
  - CSS,
  - Vanilla JavaScript,
- używać Fetch API do komunikacji z backendem,
- dynamicznie aktualizować tabelę bez przeładowania strony,
- obsługiwać localStorage do zapisywania motywu aplikacji,
- renderować dane pracowników dynamicznie w tabeli HTML.

## 12.2 Backend

Backend powinien:
- być napisany w FastAPI,
- wykorzystywać Pydantic do walidacji danych,
- przechowywać dane pracowników trwale w bazie SQLite (`db.py`) — dane
  przetrwają restart aplikacji; ścieżkę pliku bazy można nadpisać zmienną
  środowiskową `DB_PATH`,
- obsługiwać REST API,
- zwracać odpowiedzi w formacie JSON,
- posiadać endpoint healthcheck.

Tokeny sesji (`active_tokens`) pozostają wyłącznie w pamięci procesu — to
świadoma decyzja: token ma 10-minutowy TTL i nie powinien przetrwać
restartu serwera.

## 12.3 Walidacja danych

Walidacja danych powinna być realizowana:
- po stronie backendu przy użyciu Pydantic,
- po stronie frontendu poprzez ograniczenia pól formularza.

## 12.4 Obsługiwane endpointy

| Metoda HTTP | Endpoint | Opis | Kod sukcesu | Autoryzacja |
|---|---|---|---|---|
| GET | `/health` | Healthcheck API | 200 | Brak |
| POST | `/api/login` | Logowanie (`admin`/`admin`), zwraca bearer token ważny 10 minut | 200 (401 przy błędnych danych, 422 przy niepoprawnym formacie `username`/`password` — patrz 4.6, 4.7) | Brak |
| POST | `/api/logout` | Wylogowanie — unieważnia token po stronie serwera | 200 (401 bez tokenu) | Bearer |
| GET | `/api/employees` | Pobranie listy pracowników | 200 (401 bez tokenu) | Bearer |
| POST | `/api/employees` | Dodanie pracownika | 200 (401 bez tokenu) | Bearer |
| PUT | `/api/employees/{id}` | Aktualizacja pracownika | 200 (404 jeśli `id` nie istnieje, 401 bez tokenu) | Bearer |
| DELETE | `/api/employees/{id}` | Usunięcie pracownika | 200 (404 jeśli `id` nie istnieje, 401 bez tokenu) | Bearer |
| POST | `/api/employees/reset` | Usunięcie wszystkich pracowników i zresetowanie licznika ID | 200 (401 bez tokenu) | Bearer |

## 12.5 Autoryzacja

* Logowanie odbywa się na stronie `/login` (formularz username/password).
* Po poprawnym zalogowaniu token bearer jest zapisywany w `localStorage` przeglądarki i dołączany do każdego żądania API.
* Token wygasa po 10 minutach — kolejne żądania z wygasłym lub nieprawidłowym tokenem otrzymują `401`, a użytkownik jest przekierowywany na `/login`.
* Kliknięcie `Logout` wywołuje `POST /api/logout`, który unieważnia token po stronie serwera (usuwa go z magazynu tokenów), a dopiero potem czyści `localStorage` i przekierowuje na `/login`. Błąd sieci przy tym wywołaniu nie blokuje wylogowania lokalnego.
* Endpoint `/health` oraz `/api/login` nie wymagają autoryzacji.

# 13. Wymagania UX/UI

## 13.1 Responsywność

Interfejs użytkownika powinien:
- poprawnie działać na desktopie,
- poprawnie skalować się na mniejszych ekranach,
- obsługiwać zawijanie elementów formularza (`flex-wrap`).

## 13.2 Wygląd aplikacji

UI powinno:
- posiadać nowoczesny wygląd,
- wykorzystywać rounded corners,
- posiadać shadows,
- posiadać hover effects,
- wykorzystywać spójny accent color,
- obsługiwać dark mode i light mode.

## 13.3 Formularz

Formularz powinien:
- wyraźnie wskazywać tryb:
  - Add Employee,
  - Edit Employee,
- podświetlać tryb edycji,
- czyścić pola po poprawnym zapisaniu danych.

## 13.4 Tabela

Tabela powinna:
- posiadać hover effect dla wierszy,
- być czytelna wizualnie,
- posiadać wyróżniony nagłówek,
- wyświetlać dane w sposób centralnie wyrównany.

## 13.5 Obsługa błędów

Komunikaty błędów powinny:
- być widoczne dla użytkownika,
- posiadać czerwone obramowanie,
- posiadać czerwone tło,
- znikać po poprawnym wykonaniu operacji.

# 14. Przykładowy obiekt pracownika

```json
{
  "id": 1,
  "name": "Patryk",
  "salary": 15000,
  "age": 29,
  "position": "Senior QA",
  "on_leave": true
}