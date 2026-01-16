import socket
import threading

from main import Peer

username = input("Enter your username: ")

question1 = input("Do you want to host or join? ")

if question1.lower() == "host":
    host_ip = input("Enter the IP address to host on (0.0.0.0 for all interfaces): ")
    host_port = int(input("Enter the port number to host on: "))
    peer = Peer(host_ip, host_port)
    peer.start()

    print("\nServer running. Type messages to broadcast, or 'quit' to stop.\n")

    while True:
        message = input("> ")
        if message.lower() == "quit":
            print("Stopping server...")
            peer.stop()
            break
        elif message:
            peer.broadcast(f"{username}: {message}")

elif question1.lower() == "join":
    peer_host = input("Enter the host's IP address: ")
    peer_port = int(input("Enter the host's port number: "))

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((peer_host, peer_port))
    print(f"Connected to {peer_host}:{peer_port}")

    def listen():
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print("\nDisconnected from host.")
                    break
                print(f"\n{data.decode()}")
                print("> ", end="", flush=True)
            except:
                print("\nConnection lost.")
                break

    threading.Thread(target=listen, daemon=True).start()

    print("\nConnected. Type messages to send, or 'quit' to exit.\n")

    while True:
        message = input("> ")
        if message.lower() == "quit":
            conn.close()
            break
        elif message:
            conn.send(f"{username}: {message}".encode())

else:
    print("Invalid option. Please type 'host' or 'join'.")
