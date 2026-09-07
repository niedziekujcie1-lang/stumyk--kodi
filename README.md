# Strumyk / Strims24 — Kodi 21 Omega

Repozytorium zawiera framework wtyczki Kodi 21 Omega oraz automatyczny build GitHub Actions.

## Funkcje
- Kategorie sportowe: piłka nożna, koszykówka, siatkówka, tenis, sporty motorowe, sporty walki, hokej i inne sporty.
- Bezpośrednie odtwarzanie legalnych/licencjonowanych streamów HLS (`.m3u8`) i DASH (`.mpd`) podanych przez użytkownika.
- Osobne pozycje informacyjne dla stron Strumyk i Strims24.

## Ważne
Wtyczka nie omija DRM, logowania, paywalli ani innych zabezpieczeń i nie wyciąga chronionych lub nieautoryzowanych transmisji. Sekcja źródeł bezpośrednich jest przeznaczona do legalnych/licencjonowanych streamów, które użytkownik ma prawo odtwarzać.

## Konfiguracja streamów
Po instalacji otwórz **Ustawienia dodatku**. Dla każdej kategorii sportowej można podać nazwę oraz bezpośredni URL HLS/DASH. Puste pole oznacza brak źródła w tej kategorii.

## Instalacja z ZIP
Aktualna wersja wtyczki jest publikowana automatycznie przez GitHub Actions. ZIP ma nazwę `plugin.video.strumyk-0.1.3.zip`.

W Kodi wybierz **Dodatki → Zainstaluj z pliku ZIP** albo zainstaluj wtyczkę przez repozytorium Kodi.

## Repozytorium Kodi
Adres repozytorium:
`https://niedziekujcie1-lang.github.io/stumyk--kodi/`

Aktualna wersja repozytorium: `1.0.5`.

Pliki repozytorium są budowane automatycznie przez workflow w `.github/workflows/build.yml`.
