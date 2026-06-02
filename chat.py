"""
UDP Chatroom Client
- Mengirim pesan ke server dan menerima broadcast dari client lain
- Menampilkan format: IP * Port > pesan
- Jalankan: python chat.py
"""

import socket
import threading
import sys

# Konfigurasi server - ubah sesuai IP server
SERVER_IP = '127.0.0.1'  # Ganti dengan IP server (misal: 192.168.1.1)
SERVER_PORT = 9999


def receive_messages(client_socket):
    """Thread untuk menerima pesan dari server secara terus-menerus"""
    while True:
        try:
            data, addr = client_socket.recvfrom(1024)
            message = data.decode('utf-8')
            print(f"\n{message}")
            print(">> ", end="", flush=True)
        except OSError:
            # Socket ditutup
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")
            break


def main():
    # Buat socket UDP
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Minta nama user
    username = input("Masukkan nama Anda: ").strip()
    if not username:
        username = "Anonymous"

    # Kirim pesan join ke server
    join_msg = f"/join {username}"
    client.sendto(join_msg.encode('utf-8'), (SERVER_IP, SERVER_PORT))

    # Tunggu pesan selamat datang
    try:
        data, addr = client.recvfrom(1024)
        welcome = data.decode('utf-8')
        print(f"\n{welcome}")
        print("-" * 40)
        print("Ketik pesan lalu tekan Enter untuk mengirim")
        print("Ketik /quit untuk keluar")
        print("-" * 40)
    except Exception as e:
        print(f"[ERROR] Tidak bisa terhubung ke server: {e}")
        client.close()
        return

    # Jalankan thread penerima pesan
    recv_thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
    recv_thread.start()

    # Loop untuk mengirim pesan
    while True:
        try:
            message = input(">> ")
            if message.strip() == "":
                continue

            if message.strip() == "/quit":
                client.sendto("/quit".encode('utf-8'), (SERVER_IP, SERVER_PORT))
                print("Keluar dari chatroom. Sampai jumpa!")
                break

            # Kirim pesan ke server
            client.sendto(message.encode('utf-8'), (SERVER_IP, SERVER_PORT))

        except KeyboardInterrupt:
            client.sendto("/quit".encode('utf-8'), (SERVER_IP, SERVER_PORT))
            print("\nKeluar dari chatroom. Sampai jumpa!")
            break

    client.close()


if __name__ == "__main__":
    main()
