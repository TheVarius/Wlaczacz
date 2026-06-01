import sys
import os
import pytest

# Dodajemy nadrzędny folder do ścieżki, żeby test widział plik discord_bot.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from discord_bot import wake_on_lan

def test_wake_on_lan_invalid_length():
    """Test sprawdza czy funkcja odrzuca adres MAC o błędnej długości"""
    # Za krótki adres
    assert wake_on_lan('34:5A:60:A4') == False
    
    # Za długi adres
    assert wake_on_lan('34:5A:60:A4:9E:F8:11') == False

def test_wake_on_lan_invalid_characters():
    """Test sprawdza czy funkcja rzuca False przy niepoprawnych znakach szesnastkowych"""
    assert wake_on_lan('XX:XX:XX:XX:XX:XX') == False

def test_wake_on_lan_success_and_mocked_socket(mocker):
    """
    Test sprawdza poprawne wyczyszczenie adresu MAC z dwukropków/myślników,
    skonstruowanie Magicznego Pakietu i wysłanie go. 
    Używamy 'mocker' żeby nie wysyłać prawdziwego prądu w sieć.
    """
    # Zastępujemy moduł 'socket' atrapą (mocker z pytest-mock)
    mock_socket = mocker.patch('socket.socket')
    mock_socket_instance = mock_socket.return_value.__enter__.return_value

    # Odpalamy funkcję na prawidłowym, testowym adresie
    mac_testowy = '11:22:33:44:55:66'
    wynik = wake_on_lan(mac_testowy)

    assert wynik == True

    # Sprawdzamy czy gniazdo zostało ustawione na BROADCAST
    import socket
    mock_socket_instance.setsockopt.assert_called_once_with(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Obliczamy jak powinien wyglądać wysłany pakiet:
    # 6 razy 'FF' (255) + 16 razy adres MAC
    expected_magic_packet = b'\xff' * 6 + bytes.fromhex('112233445566') * 16

    # Sprawdzamy, czy funkcja wysłała dokładnie taki pakiet pod dokładny adres i port 9
    mock_socket_instance.sendto.assert_called_once_with(expected_magic_packet, ('255.255.255.255', 9))

def test_wake_on_lan_dash_format(mocker):
    """Test sprawdza czy MAC w formacie z myślnikami zadziała poprawnie"""
    mocker.patch('socket.socket')
    assert wake_on_lan('11-22-33-44-55-66') == True
