import socket
import pydub
from pydub import AudioSegment

# Load MP3 file using pydub
audio = AudioSegment.from_mp3("/Users/Idan/Downloads/Babalos - Snow Crystal [HQ] [music].mp3")
print("\n\n\n\n")
# Convert to raw data (16-bit signed PCM)
raw_data = audio.raw_data

# Set up the socket
server_ip = 'localhost'  # Change to receiver IP
server_port = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the receiver
sock.connect((server_ip, server_port))

# Send the raw audio data in chunks
chunk_size = 1024  # Adjust depending on your use case
for i in range(0, len(raw_data), chunk_size):
    sock.send(raw_data[i:i + chunk_size])

sock.close()
