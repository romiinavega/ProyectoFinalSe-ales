import pyaudio
import numpy as np
import wave

#Formato de audio de microfono
PROFUNDIDAD_BITS = pyaudio.paInt16
CANALES = 1
FRECUENCIA_MUESTREO = 44100
SEGUNDOS_GRABACION = 50

#Tamaño del chunk
CHUNK = 2048

window = np.blackman(CHUNK)

def analizar(stream):
    data = stream.read(CHUNK, exception_on_overflow=False)
    #"2048h"
    waveData = wave.struct.unpack("%dh"%(CHUNK), data)
    npData = np.array(waveData)

    dataEntrada = npData * window

    fftData = np.abs(np.fft.rfft(dataEntrada))

    indiceFrecuenciaDominante = fftData[1:].argmax() + 1

    #Cambio de indice a Hz
    y0,y1,y2 = np.log(fftData[indiceFrecuenciaDominante-1: indiceFrecuenciaDominante+2])
    x1 = ((y2 - y0) * 0.5) / (2 * y1 - y2 - y0)
    frecuenciaDominante = (indiceFrecuenciaDominante+x1)*FRECUENCIA_MUESTREO/CHUNK

    print("Frecuencia dominante:" + str(frecuenciaDominante) + "Hz", end='\r')

if __name__=="__main__":
    p = pyaudio.PyAudio()
    stream = p.open(format=PROFUNDIDAD_BITS, channels=CANALES, rate=FRECUENCIA_MUESTREO, input=True, frames_per_buffer=CHUNK)

    for i in range(0, int(FRECUENCIA_MUESTREO * SEGUNDOS_GRABACION / CHUNK)):
        analizar(stream)

    stream.stop_stream()
    stream.close()
    p.terminate()