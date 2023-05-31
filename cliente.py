import socket,cv2, pickle,struct
import pyshine as ps

   
    
mode =  'get'
name = 'CLIENT RECEIVING AUDIO'
audio,context = ps.audioCapture(mode=mode)
ps.showPlot(context,name)

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.1.13'
port = 4982
socket_address = (host_ip,port)
client_socket.connect(socket_address) 
print("CLIENT CONNECTED TO",socket_address)
data = b""
payload_size = struct.calcsize("Q")

while True:
	while len(data) < payload_size:
		packet = client_socket.recv(4*1024) # 4K
		if not packet: break
		data+=packet
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	tam = struct.unpack("Q",packed_msg_size)[0]
	
	while len(data) < tam:
		data += client_socket.recv(4*1024)
	frame_data = data[:tam]
	data  = data[tam:]
	frame = pickle.loads(frame_data)
	audio.put(frame)

client_socket.close()


