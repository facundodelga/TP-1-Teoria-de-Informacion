# Desarrollar un programa que pueda ser ejecutado por consola del siguiente modo:

# tpi1 filename.bin [N]

# Donde:

# tpi1 es el programa ejecutable
# filename.bin es un archivo binario
# N es un número natural (opcional)
# El programa debe realizar las siguientes acciones:

# Calcular las probabilidades condicionales del contenido del archivo filename.bin para el alfabeto binario.
# Determinar si el contenido del archivo filename.bin proviene de una fuente binaria de memoria nula o no nula y calcular su entropía.
# En el caso de ser una fuente de memoria nula, calcular las probabilidades y la entropía de la extensión de orden N.
# En el caso de ser una fuente de memoria no nula, obtener su vector estacionario.

import sys  # # Este import sirve para los argumentos de consola
import numpy as np # esta libreria intalenla poniendo en la consola pip install numpy es para hacer cuentas matematicas mas facil

class archivo:
    def __init__(self, filename, n):
        self.filename = filename
        self.n = n
        self.contenido = {} # esto lo puse asi para que quede como clave : valor, la clave es el caracter en ASCII y el valor va a ser las veces que se repite
    
    def abrirArchivo(self):
        with open(self.filename) as f:
            for lines in f:
                line = lines.rstrip().decode("ascii")
                if(line in self.contenido.keys()):
                    self.contenido[line] += 1
                else:
                    self.contenido.update({line : 1})


def main():
    filename = sys.argv[1]
    if(len(sys.argv) > 2):
        n = sys.argv[2]
    #print("filename: " + filename + " n: " + n)
    
    arch = archivo(filename, n)

if __name__ == "__main__":
    main()
