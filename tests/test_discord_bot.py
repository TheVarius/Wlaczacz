import sys
import os
import pytest

# Ogarnięcie poprawnej ścieżki żeby widziało bota
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from discord_bot import wake_on_lan

def test_wake_on_lan_invalid_length():
    # Za krótki mac
    assert wake_on_lan('34:5A:60:A4') == False
    
    # Za długi mac
    assert wake_on_lan('34:5A:60:A4:9E:F8:11') == False

def test_wake_on_lan_invalid_characters():
    # Zły mac
    assert wake_on_lan('XX:XX:XX:XX:XX:XX') == False

def test_wake_on_lan_success_and_mocked_socket(mocker):
    # Blokujemy wysyłanie pakietów żeby testować na sucho
    mock_socket = mocker.patch('socket.socket')
    mock_socket_instance = mock_socket.return_value.__enter__.return_value

    # Poprawny mac testowy
    mac_testowy = '11:22:33:44:55:66'
    wynik = wake_on_lan(mac_testowy)

    assert wynik == True

    import socket
    mock_socket_instance.setsockopt.assert_called_once_with(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Taki ma być pakiet
    expected_magic_packet = b'\xff' * 6 + bytes.fromhex('112233445566') * 16

    # Sprawdzamy czy poszło na port 9
    mock_socket_instance.sendto.assert_called_once_with(expected_magic_packet, ('255.255.255.255', 9))

def test_wake_on_lan_dash_format(mocker):
    # Testujemy format z myślnikami
    mocker.patch('socket.socket')
    assert wake_on_lan('11-22-33-44-55-66') == True
