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
import math
import numpy as np

class archivo:
    def __init__(self, filename, n):
        self.filename = filename
        self.n = n
        self.M = [[0,0],[0,0]]
    
    def abrirArchivo(self):
        with open(self.filename,"rb") as f:
            file = f.read()
            
            for line in file:
                binario = convertirABinario(line)
                
                bits = [int(bit) for bit in binario]
                print(bits)
                
                anterior = bits[0]
                bits.pop(0)

                for actual in bits:
                    self.M[anterior][actual] += 1
                    anterior = actual
        
        t0 = self.M[0][0] + self.M[1][0]  
        t1 = self.M[1][1] + self.M[0][1]
        
        # Probabilidad desde el estado 0
        self.M[0][0] /= t0  #p00
        self.M[0][0] = round(self.M[0][0],2)
        
        self.M[1][0] /= t0  #p10
        self.M[1][0] = round(self.M[1][0],2) 
        
        # Probabilidad desde el estado 1
        self.M[0][1] /= t1  #p01
        self.M[0][1] = round(self.M[0][1],2)
        
        self.M[1][1] /= t1  #p11
        self.M[1][1] = round(self.M[1][1],2)
        
        print(self.M)
        return 0
    
    #b) Determinar si el contenido del archivo filename.bin proviene de una fuente binaria de memoria nula o no nula y calcular su entropía.
    def nula(self):
        #Para ser memoria nula los elementos de la fila van a ser iguales
        return self.M[0][0] == self.M[0][1] and self.M[1][0] == self.M[1][1]

    def entropiaMemoriaNula(self): 
        #calculo de entropia para memoria nula
        return self.M[0][0] * math.log2(1 / self.M[0][0]) + self.M[1][1] * math.log2 (1 / self.M[1][1])

    def  entropiaMemoriaNoNula(self): 
        p00 = self.M[0][0]
        p10 = self.M[0][1]
        p01 = self.M[1][0]
        p11 = self.M[1][1]

        # if(p0 == 0 or p1 == 0):
        #     return 0

        return round(p00 * math.log2(1 / p00) + p01 * math.log2(1 / p01) + p10 * math.log2(1 / p10) + p11 * math.log2(1 / p11),2)

    def calcularVectorEstacionario(self): 
        # Definir la matriz de probabilidad condicional (self.M)
        matriz_condicional = np.array(self.M)
            
        # Definir el vector de probabilidad inicial
        vector_inicial = np.array([0.5, 0.5]) 
        
        # Calcular el vector estacionario
        vector_estacionario = vector_inicial
        nuevo_vector_estacionario = np.array([])
        while (True):
            nuevo_vector_estacionario = np.dot(vector_estacionario, matriz_condicional)
            if np.equal(nuevo_vector_estacionario, vector_estacionario):
                # Si el vector no cambia termina el ciclo
                break
            vector_estacionario = nuevo_vector_estacionario
        
        return vector_estacionario
    
    
    
    def calculaDicProbabilidadesCombinadas(self, probabilidades, n):
        if n == 1:
            return {"0": probabilidades[0], "1": probabilidades[1]}
        
        primera_parte = self.calculaDicProbabilidadesCombinadas(probabilidades, n - 1)
        # segunda_parte = primera_parte.copy()  # Copia el diccionario primera_parte
        
        # Actualiza la primera parte con "0"
        dict_aux = primera_parte.copy()
        for key in dict_aux.keys():
            primera_parte[key + "0"] = round(primera_parte[key] * probabilidades[0],2)
        
        for key in dict_aux.keys():
            primera_parte[key + "1"] = round(primera_parte[key] * probabilidades[1],2)
            
        # Actualiza la segunda parte con "1"
        # dict_aux = segunda_parte.copy()
        # for key in dict_aux.keys():
        #     segunda_parte[key + "1"] = round(segunda_parte[key] * probabilidades[1],2)
        
        return primera_parte


    def calculaEntropiaExtensionN(self,n):
        probabilidades=[self.M[0][0],self.M[1][1]]
        entropia = 0
        #Se calcula el diccionario con las probabilidades combinadas segun el orden que se ingreso
        dicProbabilidadesCombinadas=self.calculaDicProbabilidadesCombinadas(probabilidades,n)
        print("El vector de probabilidades combinadas es:")
        print(dicProbabilidadesCombinadas)
        #Calculo de la entropia de la fuente extendida de orden n
        for key in dicProbabilidadesCombinadas.keys():
            if(dicProbabilidadesCombinadas[key] != 0 and len(key) == n): 
                entropia += dicProbabilidadesCombinadas[key] * math.log2(1 / dicProbabilidadesCombinadas[key])
        print("La entropia de la fuente extendida de orden: %d es:" %n)
        print("Entropia: %f" % entropia)

def convertirABinario(valor_byte):
    representacion_binaria = bin(valor_byte)[2:]

    # La representación binaria tenga 8 bits (rellenando con ceros a la izquierda si es necesario)
    representacion_binaria = representacion_binaria.zfill(8)
    
    return representacion_binaria

def main():
    #filename = sys.argv[1]
    filename = "tp1_sample3.bin"
    n=3
    # if(len(sys.argv) > 2):
    #     n = sys.argv[2]
    # else
    #     n=1
    #print("filename: " + filename + " n: " + n)
    arch = archivo(filename, n)
    arch.abrirArchivo()
    print(str(arch.nula()))
    if(arch.nula()):
        print("La fuente tiene simbolos estadisticamente independientes (es de memoria nula)")
        print("La entropia de la fuente es: " + str(arch.entropiaMemoriaNula()))
        arch.calculaEntropiaExtensionN(n)
    else:
        print("La fuente tiene simbolos estadisticamente dependientes (es de memoria no nula)")
        print("La entropia de la fuente es: " + str(arch.entropiaMemoriaNoNula()))
    
    # input(" fin ")

if __name__ == "__main__":
    main()
