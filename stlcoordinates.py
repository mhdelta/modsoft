import string
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import time
import serial





fil = open('1rectangulo-ascii.stl', 'r').read()
wordlist = fil.split()

# ESTE ARCHIVO EXTRAE LAS COORDENADAS X,Y DE UN ARCHIVO .STL
# SIN EMBARGO LA IMPRESORA NECESITA UN ORDEN PARA GRAFICAR LAS SUPERFICIES
# POR LO QUE SE ESCRIBE LA PRIMERA COORDENADA DE CADA TRIANGULO, LUEGO LA 
# SEGUNDA Y DESPUES LA TERCERA, SUCESIVAMENTE HASTA LOS N TRIANGULOS QUE 
# FORMAN LA FIGURA.

x=0
contador_facetas=0
vertex=range(100)
vertey=range(100)


print "X","Y"
for i,j in enumerate(wordlist):	#hacer tuplas de palabras
    if j == "vertex":
    	print "("+wordlist[i+1]+","+wordlist[i+2]+")"
    	vertex[x]=wordlist[i+1] #Crea los vectores con las coordendas en orden descendente, tal y como esta en el texto ascii
    	vertey[x]=wordlist[i+2]
    	x += 1
    else: 
		if j == "facet":              #Cuantos triangulos tiene 
			contador_facetas += 1
	

	
print "contador facetas= ", contador_facetas
print "x= ",x		

print "\n","Organizadando de manera que se pueda imprimir:","\t"




intvertex=range(x)
intvertey=range(x)

for i in range (x):
	intvertex[i]=int (vertex[i])	#vctores almacenando las coordenadas como enteros
	intvertey[i]=int (vertey[i])


valores= zip(intvertex, intvertey)


# CREACION DE UN VECTOR CON EL ORDEN DE LOS INDICES MAS PROXIMOS, PARA GRAFICAR		

ch = ConvexHull(valores)

# Get the indices of the hull points.
hull_indices = list(ch.vertices)


print valores
print "indices: " , hull_indices
# These are the actual points.

valores = np.array(valores)
hull_valores=[]
for i in hull_indices:
	hull_valores.append(valores[i, :])
plt.plot(valores[:, 0], valores[:, 1], 'ko', markersize=10)
#plt.fill(hull_valores[:,0], hull_valores[:,1], fill=False, edgecolor='b')
#plt.show()



#   COMUNICACION SERIAL
port = 'COM2'
vserial0 = serial.Serial(port, baudrate=9600, bytesize=8, parity=serial.PARITY_EVEN, stopbits=1)

end=1
while end != "terminar":
    vserial0.write(chr(94))
    print chr(95)
    end=raw_input()





