import string
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import time
import serial
from progress.bar import Bar

fil = open('ascii-hexagono.stl', 'r').read()
wordlist = fil.split()

# ESTE ARCHIVO EXTRAE LAS COORDENADAS X,Y DE UN ARCHIVO .STL
# SIN EMBARGO LA IMPRESORA NECESITA UN ORDEN PARA GRAFICAR LAS SUPERFICIES
# POR LO QUE SE UTILIZA LA HERRAMIENTA CONVEXHULL PARA ORGANIZAR LOS
# INDICES DE LOS VECTORES ALMACENANDO TODAS LAS COORDENADAS DE LOS TRIANGULOS
# .

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



hull_indices.append(hull_indices[0])

print "indices: " , hull_indices


# These are the actual points.

valores = np.array(valores)
hull_valores=[]
for i in hull_indices:
	hull_valores.append(valores[i, :])
plt.plot(valores[:, 0], valores[:, 1], 'ko', markersize=10)
#plt.fill(hull_valores[:,0], hull_valores[:,1], fill=False, edgecolor='b')
#plt.show()


bar = Bar('Processing', max=len(hull_indices), suffix='%(percent)d%%')
#for i in hull_indices:
#    time.sleep(0.4)
#    bar.next()
#bar.finish()
print "\n\n"
print "[X  Y]"
for i in hull_indices:
    print valores[i]
                                         

######################   PENDIENTE DE UNA LINEA DADA POR DOS PUNTOS ################

def slope(x1, y1, x2, y2):
    return float((y2-y1)/float(x2-x1))

pendientes = []



for i in range(0,len(hull_indices)-1):
     print 'datos>','(',intvertex[hull_indices[i]],',',intvertey[hull_indices[i]],')','(',intvertex[hull_indices[i+1]],',',intvertey[hull_indices[i+1]],')','indice>',i,'mas `',i+1
     print slope(intvertex[hull_indices[i]],intvertey[hull_indices[i]],intvertex[hull_indices[i+1]],intvertey[hull_indices[i+1]]),"wait"
     pendientes.append (slope(intvertex[hull_indices[i]],intvertey[hull_indices[i]],intvertex[hull_indices[i+1]],intvertey[hull_indices[i+1]]))
plt.show()    


###########             ENVIO DE DATOS SERIAL               ####################

#5 DATOS PARA MANDAR:

# SE ENVIA UN "BYTE" POR CADA DOS COORDENADAS

#DIRX -,+    		1 BIT   0 -> -    1 -> +
#DIRY -,+		1 BIT   0 -> -    1 -> +
#PASOS++ DE Y	(2-6)   2 BIT
#PASOSX			6 BIT
#PASOSY POR CADAX	6 BIT


reset = []    
def BYTE(indice, pendiente): # CON ESTOS DOS DATOS PUEDO ENCONTRAR LOS 16 BITS PARA ENVIAR  
    for i in range (15):
        reset.append (0)
        
    byte = bytearray(reset)# ojo enviarle a esta funcion hull indices

    if (intvertex[hull_indices[indice]]-intvertex[hull_indices[indice + 1]] < 0):
        byte[0] = 1

    


    
BYTE (0,0)
    
    



#######################  COMUNICACION SERIAL   #################################

port = 'COM2'
vserial0 = serial.Serial(port, baudrate=9600, bytesize=8, parity=serial.PARITY_NONE, stopbits=1)

vserial0.write("cls")  







