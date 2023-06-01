import socket,cv2, pickle,struct
import pyshine as ps

   
# Definimos el modo de recepción de audio como 'get'
mode =  'get'
name = 'CLIENT RECEIVING AUDIO'
#  Capturamos el audio utilizando la función audioCapture y mostramos gráfico.
audio,context = ps.audioCapture(mode=mode)
ps.showPlot(context,name)

# Creamos un socket del cliente, establecemos la dirección IP y el número de puerto.
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.1.13'
port = 4982
socket_address = (host_ip,port)
# Nos conectamos a la dirección y el puerto del servidor especificados.
client_socket.connect(socket_address) 
print("CLIENT CONNECTED TO",socket_address)
data = b""
# Calculo el tamaño del paquete que se utilizará para recibir los datos 
payload_size = struct.calcsize("Q")

while True:
	# Entra en un bucle mientras el tamaño de data sea menor que el tamaño del paquete.
	while len(data) < payload_size:
		packet = client_socket.recv(4*1024) # 4K de espacio de búffer de recepción.
		if not packet: break                # Si no se recibe ningún paquete, se sale del bucle
		data+=packet
	packed_msg_size = data[:payload_size]       # Obtenemos el tamaño del mensaje empaquetado a partir de data
	data = data[payload_size:]                  # Actualizamos data para excluir el tamaño del mensaje empaquetado
	tam = struct.unpack("Q",packed_msg_size)[0] # Desempaquetamos el tamaño del mensaje 
	
	while len(data) < tam:
		data += client_socket.recv(4*1024)
	frame_data = data[:tam] # Extraemos los datos del frame original
	data  = data[tam:]
	frame = pickle.loads(frame_data) # Carga el frame
	audio.put(frame) 
# Cerramos el socket del cliente
client_socket.close()


