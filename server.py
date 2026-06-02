import socket

HOST = '0.0.0.0'
PORT = 9999

# Menyimpan daftar client yang terhubung (alamat tuple)
clients = {}  # {(ip, port): username}


def broadcast(server, message, exclude_addr):
    """Kirim pesan ke semua client kecuali pengirim"""
    for client_addr in clients:
        if client_addr != exclude_addr:
            try:
                server.sendto(message.encode('utf-8'), client_addr)
            except Exception as e:
                print(f"[SERVER] Gagal kirim ke {client_addr}: {e}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    print(f"[SERVER] UDP Chatroom Server berjalan di {HOST}:{PORT}")
    print("[SERVER] Menunggu client bergabung...\n")

    while True:
        try:
            data, addr = server.recvfrom(1024)
            message = data.decode('utf-8')

            # Jika pesan dimulai dengan /join, client baru bergabung
            if message.startswith("/join"):
                username = message.split(" ", 1)[1] if " " in message else f"{addr[0]}:{addr[1]}"
                clients[addr] = username
                print(f"[+] {username} ({addr[0]}:{addr[1]}) bergabung ke chatroom")

                # Kirim pesan selamat datang ke client yang baru join
                welcome = "Selamat Datang di Chatroom!"
                server.sendto(welcome.encode('utf-8'), addr)

                # Broadcast ke semua client bahwa ada yang bergabung
                join_msg = f"{addr[0]} * {addr[1]} > joined"
                broadcast(server, join_msg, addr)

            # Jika pesan /quit, client keluar
            elif message.startswith("/quit"):
                if addr in clients:
                    username = clients[addr]
                    print(f"[-] {username} ({addr[0]}:{addr[1]}) keluar dari chatroom")
                    quit_msg = f"{addr[0]} * {addr[1]} > left the chatroom"
                    del clients[addr]
                    broadcast(server, quit_msg, None)

            # Pesan biasa, broadcast ke semua client lain
            else:
                if addr not in clients:
                    # Auto-register jika belum join
                    clients[addr] = f"{addr[0]}:{addr[1]}"
                    print(f"[+] {addr[0]}:{addr[1]} auto-joined")

                print(f"[MSG] {addr[0]} * {addr[1]} > {message}")

                # Format pesan: IP * Port > pesan
                broadcast_msg = f"{addr[0]} * {addr[1]} > {message}"
                broadcast(server, broadcast_msg, addr)

        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
