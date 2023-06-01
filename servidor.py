import socket, cv2, pickle,struct,time
import pyshine as ps
import numpy as np

def remove_echo(audio ):
    
	sample_rate = 8000

    # Parámetros del algoritmo NMLS
	delay = int(0.05 * sample_rate)  # Retraso del eco en muestras
	mu = 0.1  # Factor de aprendizaje

    # Crear la señal de eco
	echo = np.zeros_like(audio)
	echo[delay:] = audio[:-delay]

    # Inicializar el filtro de cancelación de eco
	filter_length = int(0.1 * sample_rate)  # Longitud del filtro en muestras
	filter_coeffs = np.zeros(filter_length)

    # Aplicar el algoritmo NMLS para quitar el eco
	for i in range(filter_length, len(audio)):		
		x = audio[i:i-filter_length:-1, 1]
		y = np.dot(filter_coeffs, x)		
		e = echo[i] - y
		# print(e.flatten().shape)
		# print(type(mu)) 
		# print(x.shape)
		filter_coeffs += mu * x
		
    # Aplicar el filtro de cancelación de eco al audio original
	return np.convolve(audio[:,1], filter_coeffs, mode='same')

#  Definimos el modo de transmisión de audio como 'send'
mode =  'send'
name = 'SERVER TRANSMITTING AUDIO'
#  Capturamos el audio utilizando la función audioCapture y mostramos gráfico.
audio,context= ps.audioCapture(mode=mode)
ps.showPlot(context,name)

# Creamos un socket del servidor, establecen la dirección IP y el número de puerto
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.1.13'
port = 4980
backlog = 5
socket_address = (host_ip,port)
print('STARTING SERVER AT',socket_address,'...')
#  Enlazamos el socket a la dirección y se coloca en modo de escucha.
server_socket.bind(socket_address)
server_socket.listen(backlog)

while True:
	client_socket,addr = server_socket.accept()
	print('GOT CONNECTION FROM:',addr)
	if client_socket:
		conti=True
		while(conti):
			frame = audio.get()		
			filtered_frame = remove_echo(frame)
			# Serializamos el frame de audio filtrado utilizando
			a = pickle.dumps(filtered_frame )
			# Empaquetamos el tamaño de los datos serializados utilizando struct.pack
			message = struct.pack("Q",len(a))+a
			# Envíamos los datos al cliente a través del socke
			client_socket.sendall(message)

	else:
		break
#Se cierra el socket del cliente
client_socket.close()	
