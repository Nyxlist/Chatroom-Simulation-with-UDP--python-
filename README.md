# Chatroom Simulation Using UDP
Simulasi chatroom menggunakan UDP. Menggunakan satu Device, melalui terminal yang berbeda beda.

## Caranya

Langkah 1: Tambah virtual IP di adapter loopback (buka CMD sebagai Administrator):
```
netsh interface ip add address "Loopback" 192.168.1.11 255.255.255.0
netsh interface ip add address "Loopback" 192.168.1.12 255.255.255.0
netsh interface ip add address "Loopback" 192.168.1.13 255.255.255.0
```

Langkah 2: Jalankan server:
```
python server.py
```

Langkah 3: Buka 3 terminal berbeda, jalankan client dengan IP masing-masing:
```
:: Terminal 1 - Client 1
python chat.py 192.168.1.11 10005

:: Terminal 2 - Client 2
python chat.py 192.168.1.13 9973

:: Terminal 3 - Client 3
python chat.py 192.168.1.12 12501
```
