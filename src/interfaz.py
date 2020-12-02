from tkinter import *

import pyaudio
import numpy as np
import wave

ventana = Tk()
ventana.title("Afinador de guitarra")
ventana.geometry("800x600")
bg_image = PhotoImage(file ="./imagenes/imagen.png")
x= Label (image = bg_image)
x.grid(row = 0, column = 0)

PROFUNDIDAD_BITS = pyaudio.paInt16
CANALES = 1
FRECUENCIA_MUESTREO = 44100

CHUNK = 2048
time= 1
window = np.blackman(CHUNK)


strFrecuencia= StringVar()
def sexta():

    PROFUNDIDAD_BITS = pyaudio.paInt16
    CANALES = 1
    FRECUENCIA_MUESTREO = 44100

    CHUNK = 2048
    time= 5
    window = np.blackman(CHUNK)


    def analizar(stream):
        data = stream.read(CHUNK, exception_on_overflow=False)
        waveData = wave.struct.unpack("%dh"%(CHUNK), data)  #sustituye / le da un formato de lectura
        npData = np.array(waveData)

        dataEntrada = npData * window

        fftData = np.abs(np.fft.rfft(dataEntrada)) #fourier con valor abs

        indiceFrecuenciaDominante= fftData[1:].argmax() + 1 #obtener indice de elemento con mas valor en la transformada, no es frecuencia, no esta en hz solo es el indice
        #para pasar indice a hz:
        y0,y1,y2 = np.log(fftData[indiceFrecuenciaDominante-1: indiceFrecuenciaDominante+2])
        x1=(y2-y0) *.5 / (2 * y1 -y2 -y0)

        frecuenciaDominante = (indiceFrecuenciaDominante + x1)* FRECUENCIA_MUESTREO/CHUNK


        if frecuenciaDominante> 320 and frecuenciaDominante < 340: #LA FRECUENCIA DE LA CUERDA MI RONDA LOS 350 hz
           Frecuencia = "cuerda afinada"
            
        elif frecuenciaDominante > 340: # Se validan 10 Hz arriba
           Frecuencia = "Aflojar cuerda"
            
        elif  frecuenciaDominante < 320: # Se validan 10 Hz abajo
           Frecuencia = "Apretar cuerda"
       #Este if valida el ruido sucio que pueda provocar el microfono para asi solo captar el de la  guitarra
        if frecuenciaDominante > 200 and frecuenciaDominante < 450: 
           strFrecuencia.set(Frecuencia +  " Frecuencia Hz " + str(int(frecuenciaDominante))  )
           # En esta linea larga lo unico que hice fue concatenar/Agregar La frecuencia que capta el microfono
            #Estaba en float (son muchos numeros) se convirtio a int (Son numeros enteros)
            #int() Funcion que convierte float a int
            #str() Funcion que convierte numeros a texto             
    if __name__ == "__main__":
        p = pyaudio.PyAudio()
        stream = p.open(format=PROFUNDIDAD_BITS, channels= CANALES, rate = FRECUENCIA_MUESTREO, input= True, frames_per_buffer=CHUNK) #lectura de bits- sensor del mic
        for i in range (0, int ((FRECUENCIA_MUESTREO * time) / CHUNK)):
            analizar(stream)

        stream.stop_stream()
        stream.close()
        p.terminate()
        

    
def cuerdas():
    btn6 = Button(ventana, text= "Mi, sexta cuerda", command= sexta).place(x=250, y= 150)
    '''
    btn3 = Button(ventana, text= "Sol", command= tercera).
    btn2 = Button(ventana, text= "Si", command= segunda).
    btn1 = Button(ventana, text= "Mi", command= primera).'''


btnInicio  = Button(ventana, text="Iniciar", command= cuerdas).place(x=350, y=100)
btnCerrar = Button(ventana,text = "cancelar",command = ventana.destroy).place(x=350, y=500)

lafrecuencia = Label(ventana, textvariable= strFrecuencia, width=30, background= '#f175f1').place(x=350, y=150)


ventana.mainloop()
