from scapy.all import TCP,IP,sr1,send,sniff

syn_segment = TCP(sport = 20123 ,dport=80, seq=123, flags='S')
syn_packet = IP(dst='www.google.com')/syn_segment
syn_ack_packet = sr1(syn_packet)
syn_ack_packet.show()
ack_segment = TCP(sport = 20123,dport=80,seq=124,flags= 'A')
ack_packet = IP(dst='www.google.com')/ack_segment
send(ack_packet)
#syn
sniff(timeout=1,prn=lambda x: x.show(),filter="tcp[tcpflags] == tcp-syn")
#syn and ack
sniff(timeout=1,prn=lambda x: x.show(),filter="tcp[tcpflags] == (tcp-syn|tcp-ack)")
#ack
sniff(timeout=1,prn=lambda x: x.show(),filter="(tcp[tcpflags] == tcp-ack ) and port 80")
#reset
sniff(timeout=1,prn=lambda x: x.show(),filter="tcp[tcpflags] == tcp-rst")