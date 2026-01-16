import socket
import threading

from main import Peer

clientdata = open("clientdata.txt", "a")
serverlist = open("serverlist.txt", "a")
serverlistread = open("serverlist.txt", "r")

username = input("Enter your username: ")

question1 = input(
    'Would you like to join one you\'ve joined before or a new one (please type "old" or "new")? '
)

if question1 == "new":
    peer_host = input("Enter the host's IP address: ")
    serverlist.write(f"{peer_host}\n")
    peer_port = int(input("Enter the host's port number: "))
    serverlist.write(f"{peer_port}\n")
    serverlist.flush()
elif question1 == "old":
    with open("serverlist.txt", "r") as file:
        lines = file.readlines()

    if not lines:
        print("Server list file is empty, have you not connected to any servers yet?")
    else:
        for i in range(0, len(lines), 2):
            line1 = lines[i].rstrip("\n")
            line2 = lines[i + 1].rstrip("\n") if i + 1 < len(lines) else ""
            if line2:
                print(f"{(i // 2) + 1}: {line1}:{line2}")
            else:
                print(f"{(i // 2) + 1}: {line1}")

        # Ask user to pick one
        choice = int(input("\nEnter the number of the server to join: "))
        index = (choice - 1) * 2  # Convert back to line index
        peer_host = lines[index].rstrip("\n")
        peer_port = int(lines[index + 1].rstrip("\n"))
else:
    print("That isn't a valid option...")


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
        clientdata.write(f"{username}: {message}\n")
        clientdata.flush()
