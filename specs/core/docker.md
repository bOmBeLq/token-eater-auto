# Uruchamianie w Dockerze

## Wymagania

- Repozytorium ma zawierać wieloetapowy `Dockerfile` budujący i uruchamiający aplikację na .NET 10.
- Repozytorium ma zawierać plik `compose.yaml` uruchamiający aplikację i PostgreSQL.
- Dane PostgreSQL mają być zachowywane w wolumenie Dockera.
- Aplikacja ma oczekiwać na gotowość bazy danych i automatycznie zastosować migracje przy uruchomieniu.
- Ustawienia połączenia z bazą i SMTP mają być przekazywane przez konfigurację lub zmienne środowiskowe.
- Docker Compose ma uruchamiać Mailpit jako lokalny serwer SMTP i udostępniać jego interfejs webowy.
- `POSTGRES_PASSWORD` ma być wymagane i nie może mieć domyślnej wartości; brak zmiennej ma zatrzymać uruchomienie Docker Compose.
- Lokalne środowisko testowe ma zawierać plik `.env` ustawiający `POSTGRES_PASSWORD` na `gabi123`.
- Lokalne środowisko testowe ma udostępniać uruchomioną aplikację pod adresem `http://localhost:8080`.
