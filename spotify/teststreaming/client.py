import socket
import sounddevice as sd
import numpy as np

# Set up the socket to receive data
server_ip = 'localhost'  # Your server IP
server_port = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((server_ip, server_port))
sock.listen(1)

# Wait for the sender to connect
print("Waiting for connection...")
conn, addr = sock.accept()
print(f"Connected by {addr}")

# Receive and play audio data
chunk_size = 1024  # Same as sender
sample_rate = 44100  # Standard sample rate (adjust if necessary)

# Create a buffer to hold received data
buffer = b''

try:
    while True:
        # Receive data in chunks
        data = conn.recv(chunk_size)
        if not data:
            break
        buffer += data
        
        # Convert buffer to numpy array (16-bit PCM)
        audio_data = np.frombuffer(buffer, dtype=np.int16)
        
        # Play the audio
        sd.play(audio_data, samplerate=sample_rate)
        sd.wait()  # Wait until sound finishes before playing next chunk

finally:
    conn.close()
    sock.close()
