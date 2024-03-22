from scapy.all import IP,ICMP,sr1
import sys
import time

def traceroute(target):
    count = 1

    hops = {}

    while True:
        packet = IP(dst=target, ttl=count) / ICMP()

        start = time.time()
        reply = sr1(packet, verbose=0, timeout=5)
        end = time.time()

        
        if reply is None:
            break

        if reply.src == target:
            hops[reply.src] = end - start
            break
        
        
        
        hops[reply.src] = end - start
        count += 1

    print(f"Traceroute to {target}:")
    for key in hops.keys():
        print(f"{key} ({hops[key]:.3f} ms)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Wrong Usage\n Missing arguments")

    target = sys.argv[1]
    traceroute(target)