# Projekt: Zdalny Włączacz PC (Bot Discord)

[![Tests](https://github.com/TheVarius/Wlaczacz/actions/workflows/pytest.yml/badge.svg)](https://github.com/TheVarius/Wlaczacz/actions)

## Opis zadania

Ten projekt pozwala na zdalne włączanie i wyłączanie komputera (z Windowsem) za pomocą bota na Discordzie.

Aby to działało poprawnie, system jest podzielony na dwie części:

1. **Stary Xiaomi** – leży w domu, podłączony do Wi-Fi. Czeka na wiadomość z Discorda, a gdy ją dostanie, wysyła sygnał po WIFI do komputera, żeby go włączyć.
2. **Komputer** – nasłuchuje poleceń z DC, aby jak coś się wyłączyć.

Obie części reagują tylko i wyłącznie na wiadomości od Ciebie (weryfikują ID użytkownika z Discorda). Jeśli ktoś inny wpisze komendę, bot po prostu go zignoruje.

## Komendy

Bot reaguje na dwie komendy:

- **`!wlacz`** – Odbiera ją telefon. Sprawdza, czy to Ty, a następnie wysyła magiczny pakiet do komputera, żeby go włączyć.
- **`!wylacz`** – Odbiera ją komputer. Weryfikuje czy to Ty, a następnie go wyłącza.

## Opis implementacji i plików źródłowych

Projekt jest napisany w Pythonie i korzysta z biblioteki `discord.py` do obsługi bota.

**Główny folder:**

- `discord_bot.py` – skrypt uruchamiany na telefonie w Termuxie. Czeka na komendę włączenia, przygotowuje magiczny pakiet Wake-on-LAN i wysyła go w domowe WIFI.
- `discord_wylacz.py` – skrypt uruchamiany na głównym komputerze. Zajmuje się odbieraniem komendy wyłączającej.
- `requirements.txt` – lista zewnętrznych paczek, które trzeba zainstalować.
- `.env` – ukryty plik, w którym trzymane są tajne klucze.

**Folder `tests/`:**

- `test_discord_bot.py` – testy sprawdzające, czy kod nie ma błędów (obsługa adresów MAC, sygnał do wybudzania PC itp.).

**Folder `.github/workflows/`:**

- `pytest.yml` – konfiguracja GitHub Actions. Mówi GitHubowi, żeby za każdym razem, gdy wrzucisz nowy kod, automatycznie go przetestował.

## Jak to uruchomić?

1. Stwórz plik `.env` i wpisz w nim swoje prywatne klucze (wzór poniżej):

   ```
   DISCORD_TOKEN=Twój_Token
   AUTHORIZED_USER_ID=Twoje_ID
   PC_MAC_ADDRESS=Twój_Adres_MAC
   ```

2. Zainstaluj potrzebne biblioteki wpisując w terminalu (na komputerze jak i telefonie):

   ```bash
   pip install -r requirements.txt
   ```

3. Na starym telefonie w Termuxie odpal skrypt włączający:

   ```bash
   python discord_bot.py
   ```

4. Na komputerze odpal skrypt wyłączający:
   ```bash
   python discord_wylacz.py
   ```

## Plany na przyszłość

Projekt jest stale rozwijany. W zakładce **Issues** na GitHubie będę dodawał nowe pomysły.
