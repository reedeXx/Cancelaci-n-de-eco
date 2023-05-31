import numpy as np
import soundfile as sf

def remove_echo(input_file, output_file):
    # Cargar el archivo de audio
    audio, sample_rate = sf.read(input_file)

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
        x = audio[i:i-filter_length:-1]
        y = np.dot(filter_coeffs, x)
        e = echo[i] - y
        filter_coeffs += mu * e * x

    # Aplicar el filtro de cancelación de eco al audio original
    filtered_audio = np.convolve(audio, filter_coeffs, mode='same')

    # Guardar el resultado en un nuevo archivo
    sf.write(output_file, filtered_audio, sample_rate)

# Uso del programa
input_file = 'signal.wav'
output_file = 'audio_output.wav'
remove_echo(input_file, output_file)
