import json
import socket
import threading

HISTORY_FILE = "hostdata.txt"


class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []
        self.peer_addresses = set()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lock = threading.Lock()
        self.messages = []  # In-memory message history
        self._load_history()

    def _load_history(self):
        """Load existing messages from file on startup"""
        try:
            with open(HISTORY_FILE, "r") as f:
                self.messages = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.messages = []

    def _save_message(self, message):
        """Save a message to history"""
        with self.lock:
            self.messages.append(message)
        with open(HISTORY_FILE, "a") as f:
            f.write(message + "\n")

    def _send_history(self, conn):
        """Send all past messages to a newly connected peer"""
        with self.lock:
            history = self.messages[:]
        for msg in history:
            try:
                conn.send(f"[HISTORY] {msg}\n".encode())
            except:
                break

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Listening on {self.host}:{self.port}")
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            try:
                conn, addr = self.socket.accept()
                print(f"\A person has connected!")
                print("> ", end="", flush=True)
                # Send history before adding to peers list
                self._send_history(conn)
                threading.Thread(
                    target=self.handle_peer, args=(conn,), daemon=True
                ).start()
            except (OSError, ConnectionAbortedError):
                break

    def handle_peer(self, conn):
        with self.lock:
            if conn not in self.peers:
                self.peers.append(conn)
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()

                print(f"\n{message}")
                print("> ", end="", flush=True)

                # Save to history
                self._save_message(message)

                # Relay to all OTHER peers
                self.relay(message, exclude=conn)
            except:
                break
        with self.lock:
            if conn in self.peers:
                self.peers.remove(conn)
        conn.close()

    def relay(self, message, exclude=None):
        """Send a message to all peers except the one who sent it"""
        with self.lock:
            peers_copy = self.peers[:]
        for peer in peers_copy:
            if peer != exclude:
                try:
                    peer.send(message.encode())
                except:
                    with self.lock:
                        if peer in self.peers:
                            self.peers.remove(peer)

    def broadcast(self, message):
        """Send a message to all peers (and save to history)"""
        self._save_message(message)
        with self.lock:
            peers_copy = self.peers[:]
        for peer in peers_copy:
            try:
                peer.send(message.encode())
            except:
                with self.lock:
                    if peer in self.peers:
                        self.peers.remove(peer)

    def stop(self):
        self.socket.close()
        print("Stopped listening")
