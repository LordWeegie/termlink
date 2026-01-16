from main import Peer

host_ip = "0.0.0.0"  # This can be changed, but it should be a valid IP address
username = "Host"  # This can be changed
host_port = 8000  # You may also change this to any available port number
public = True  # If you would like this to be uploaded to the list of the servers on this website set this to True


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
