# Konta użytkowników

## Wymagania

- Użytkownik ma móc zarejestrować konto za pomocą adresu e-mail i hasła.
- Adres e-mail ma być unikalny i służyć jako nazwa użytkownika podczas logowania.
- Konto ma być przechowywane w bazie PostgreSQL.
- Logowanie ma tworzyć bezpieczną sesję opartą na ciasteczku uwierzytelniającym.
- Użytkownik ma móc się wylogować.
- Dostęp do panelu i profilu ma wymagać zalogowania.
- Użytkownik ma potwierdzić adres e-mail za pomocą jednorazowego odnośnika wysłanego przez SMTP, zanim będzie mógł się zalogować.
- Użytkownik ma móc zlecić reset hasła i ustawić nowe hasło przez jednorazowy odnośnik wysłany przez SMTP.
- Formularze mają wyświetlać błędy walidacji bez ujawniania, czy podany adres istnieje podczas resetowania hasła.
- Hasło ma mieć co najmniej 8 znaków oraz zawierać małą literę, wielką literę, cyfrę i znak niealfanumeryczny.
