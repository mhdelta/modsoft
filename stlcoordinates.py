import string
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import time
import serial
from progress.bar import Bar
from prettytable import PrettyTable
from bitstring import BitArray

fil = open('evaluaciones/1rectangulo-ascii.stl', 'r').read()
wordlist = fil.split()

# ESTE ARCHIVO EXTRAE LAS COORDENADAS X,Y DE UN ARCHIVO .STL
# SIN EMBARGO LA IMPRESORA NECESITA UN ORDEN PARA GRAFICAR LAS SUPERFICIES
# POR LO QUE SE UTILIZA LA HERRAMIENTA CONVEXHULL PARA ORGANIZAR LOS
# INDICES DE LOS VECTORES ALMACENANDO TODAS LAS COORDENADAS DE LOS TRIANGULOS
# .

x=0
contador_facetas=0
vertex=range(1000)
vertey=range(1000)



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
print "Cantidad de indices: ", len(hull_indices)


# These are the actual points.

valores = np.array(valores)
hull_valores=[]
for i in hull_indices:
	hull_valores.append(valores[i, :])
plt.plot(valores[:, 0], valores[:, 1], 'ko', markersize=10)
#plt.fill(hull_valores[:,0], hull_valores[:,1], fill=False, edgecolor='b')
plt.show()


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
    if (x2-x1)!=0:
        return float((y2-y1)/float(x2-x1))
    else:
        return y2-y1

pendientes = []



tabla_datos = PrettyTable()
tabla_datos.field_names = ["x1,y1","x2,y2","index","index^", "Pendiente"]
for i in range(0,len(hull_indices)-1):
     m=slope(intvertex[hull_indices[i]],intvertey[hull_indices[i]],intvertex[hull_indices[i+1]],intvertey[hull_indices[i+1]])
     tabla_datos.add_row([hull_valores[i], hull_valores[i+1], i, i+1, m])
     #print '(',intvertex[hull_indices[i]],',',intvertey[hull_indices[i]],')','(',intvertex[hull_indices[i+1]],',',intvertey[hull_indices[i+1]],')',i,i+1
     #print "m: ",slope(intvertex[hull_indices[i]],intvertey[hull_indices[i]],intvertex[hull_indices[i+1]],intvertey[hull_indices[i+1]])
     pendientes.append (m)

print tabla_datos

###########             ENVIO DE DATOS SERIAL               ####################

#5 DATOS PARA MANDAR:

# SE ENVIA UN "PAQUETE" POR CADA DOS COORDENADAS
#                             pos

#  BYTE_INFORMATIVO
#DIRX -,+    		                1 BIT 0                 0 -> -    1 -> +    
#DIRY -,+		                1 BIT 1                 0 -> -    1 -> +                  
#parte decimal de la pendiente	        6 BIT []

#BYTE_X
#pasos en xrange                        8 BIT

#BYTE_Y
#pasos en y por cada xrange             8 BIT

def check_bit(decimal, n):     # ojo recibe un @#$% decimal
    return ((decimal>>n)&1)



def BYTE_INFORMATIVO(indice): # CON ESTOS DOS DATOS PUEDO ENCONTRAR LOS 16 BITS PARA ENVIAR

    byte = []# ojo enviarle a esta funcion hull indices
    for i in range (8):
        byte.append(0)
    if (intvertex[hull_indices[indice]]-intvertex[hull_indices[indice + 1]] < 0):
        byte[0] = 1 #dir x

    if (intvertey[hull_indices[indice]]-intvertey[hull_indices[indice + 1]] < 0):
        byte[1] = 1 #dir y

    decimal = int((pendientes[indice]%1)*10) 
    if decimal == 0:
        byte[2]=0
        byte[3]=0
        byte[4]=0
        byte[5]=0
    elif decimal == 1:
        byte[2]=0
        byte[3]=0
        byte[4]=0
        byte[5]=1
    elif decimal == 2:
        byte[2]=0
        byte[3]=0
        byte[4]=1
        byte[5]=0
    elif decimal == 3:
        byte[2]=0
        byte[3]=0
        byte[4]=1
        byte[5]=1
    elif decimal == 4:
        byte[2]=0
        byte[3]=1
        byte[4]=0
        byte[5]=0
    elif decimal == 5:
        byte[2]=0
        byte[3]=1
        byte[4]=0
        byte[5]=1
    elif decimal == 6:
        byte[2]=0
        byte[3]=1
        byte[4]=1
        byte[5]=0
    elif decimal == 7:
        byte[2]=0
        byte[3]=1
        byte[4]=1
        byte[5]=1
    elif decimal == 8:
        byte[2]=1
        byte[3]=0
        byte[4]=0
        byte[5]=0
    elif decimal == 9:
        byte[2]=1
        byte[3]=0
        byte[4]=0
        byte[5]=1
        
    return byte

def BYTE_X(indice):
    byte=[]
    for i in range (8):
        byte.append(0)
    #   MOVIMIENTOS EN X
    deltax = abs((intvertex[hull_indices[indice]]-intvertex[hull_indices[indice + 1]]))
    bindeltax = int('{0:06b}'.format(deltax))

    for i in range (8):
        byte[i]=check_bit(deltax, i)

    return byte

    #miguel acuerdese que los pasos en el byte estan invertidos
        
def BYTE_Y(indice):
    byte=[]
    for i in range (8):
        byte.append(0)
    #   MOVIMIENTOS EN Y por cada x
    deltay = int(abs(pendientes[indice]))
    bindeltay = int('{0:06b}'.format(deltay))

    for i in range (deltay.bit_length()):
        byte[i]=check_bit(deltay, i)
    
    return byte




titulobyte=PrettyTable()
byte=PrettyTable()

titulobyte.field_names=["BYTES A ENVIAR"]
byte.field_names=["index","info", "data x", "data y"]
titulobyte.add_row([byte])



for i in range(len(hull_indices)-1):
    byte.add_row([i,BYTE_INFORMATIVO(i), BYTE_X(i), BYTE_Y(i)])

print titulobyte    

#######################  COMUNICACION SERIAL   #################################

port = 'COM2'
vserial0 = serial.Serial(port, baudrate=9600, bytesize=8, parity=serial.PARITY_NONE, stopbits=1)

def byte_hex(byte):
    bitlist=byte
    b = BitArray(bitlist)
    return hex(b.uint)[2:]    

for i in range(len(hull_indices)-1):
    vserial0.write(byte_hex(BYTE_INFORMATIVO(i)))
    vserial0.write(byte_hex(BYTE_X(i)))
    vserial0.write(byte_hex(BYTE_Y(i)))
    
    
    


