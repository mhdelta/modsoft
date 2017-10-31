# Software modulation fo sendind serial data using RS232 protocol.

Python implementation for transfor stl maps to 3 representative bytes and send them using RS232 protocol.

###STLcoordinates.py
 ESTE ARCHIVO EXTRAE LAS COORDENADAS X,Y DE UN ARCHIVO .STL
 SIN EMBARGO LA IMPRESORA NECESITA UN ORDEN PARA GRAFICAR LAS SUPERFICIES
 POR LO QUE SE UTILIZA LA HERRAMIENTA CONVEXHULL PARA ORGANIZAR LOS
 INDICES DE LOS VECTORES ALMACENANDO TODAS LAS COORDENADAS DE LOS TRIANGULOS

###             ENVIO DE DATOS SERIAL

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

putty for ssh if using Windows

## Authors

* **Miguel Angel Henao**
