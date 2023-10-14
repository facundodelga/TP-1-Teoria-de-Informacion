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
        self.vector_estacionario = [0,0]
    
    def abrirArchivo(self):
        try:
            with open(self.filename,"rb") as f:
                file = f.read()
                
                for line in file:
                    binario = convertirABinario(line)
                    
                    bits = [int(bit) for bit in binario]
                    # print(bits)
                    
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
            
            return 0
        except:
            print("Error al abrir archivo")
            return -1
        
    
    #b) Determinar si el contenido del archivo filename.bin proviene de una fuente binaria de memoria nula o no nula y calcular su entropía.
    def nula(self):
        #Para ser memoria nula los elementos de la fila van a ser iguales
        return abs(self.M[0][0] - self.M[0][1]) < 0.001 and abs(self.M[1][0] - self.M[1][1]) < 0.001

    def entropiaMemoriaNula(self): 
        p0 = self.M[0][0]
        p1 = self.M[1][1] 
        
        if(p0 == 0 or p1 == 0):
            return 0
        return self.M[0][0] * math.log2(1 / self.M[0][0]) + self.M[1][1] * math.log2 (1 / self.M[1][1])

    def  entropiaMemoriaNoNula(self):
        entropia = 0
        termino1 = self.vector_estacionario[0] * (self.M[0][0] * math.log2(1 / self.M[0][0]) + (self.M[0][1] * math.log2(1 / self.M[0][1])))
        termino2 = self.vector_estacionario[1] * (self.M[1][0] * math.log2(1 / self.M[1][0]) + (self.M[1][1] * math.log2(1 / self.M[1][1])))
        
        entropia = termino1 + termino2 
        return entropia

    def calcularVectorEstacionario(self): 
        # Definir la matriz de probabilidad condicional (self.M)
        matriz_condicional = np.array(self.M)
            
        # Definir el vector de probabilidad inicial
        vector_inicial = np.array([0.5, 0.5]) 
        # Calcular el vector estacionario
        self.vector_estacionario = vector_inicial
        nuevo_vector_estacionario = np.array([])

        while (True):
            nuevo_vector_estacionario = matriz_condicional.dot(self.vector_estacionario)
            
            if np.allclose(nuevo_vector_estacionario, self.vector_estacionario):
                # Si el vector no cambia termina el ciclo
                break
            
            self.vector_estacionario = nuevo_vector_estacionario
            
        #self.vector_estacionario[0] = round(self.vector_estacionario[0],2)
        #self.vector_estacionario[1] = round(self.vector_estacionario[1],2)
        
        return self.vector_estacionario
    
            
    def calculaDicProbabilidadesCombinadas(self, probabilidades, n):
            #Caso de corte
            if n == 1:
                return {"0": probabilidades[0], "1": probabilidades[1]}
            #Caso de no corte
            fuenteAnterior = self.calculaDicProbabilidadesCombinadas(probabilidades, n - 1)
            fuenteActual = {} #Inicializa diccionario vacio
            
            # Actualiza el diccionario sumandole un orden de fuente
            for key in fuenteAnterior.keys():
                fuenteActual[key + "0"] = round(fuenteAnterior[key] * probabilidades[0],2)
                fuenteActual[key + "1"] = round(fuenteAnterior[key] * probabilidades[1],2)

            return fuenteActual


    def calculaEntropiaExtensionN(self,n):
        probabilidades=[self.M[0][0],self.M[1][1]]
        entropia=0
        
        #Se calcula el diccionario con las probabilidades combinadas segun el orden que se ingreso
        dicProbabilidadesCombinadas=self.calculaDicProbabilidadesCombinadas(probabilidades,n)
        print("El vector de probabilidades combinadas es:")
        print(dicProbabilidadesCombinadas)
        
        #Calculo de la entropia de la fuente extendida de orden n
        for key in dicProbabilidadesCombinadas:
            if(dicProbabilidadesCombinadas[key] != 0):
                entropia += dicProbabilidadesCombinadas[key] * math.log2(1/dicProbabilidadesCombinadas[key])
            
        #entropia = round(entropia,2)
        
        print("La entropia de la fuente extendida de orden " + str(n) + " es: " + str(entropia))
        
    def print_M(self):
        print("Matriz de probabilidades condicionales")
        print(self.M[0])
        print(self.M[1])

def convertirABinario(valor_byte):
    representacion_binaria = bin(valor_byte)[2:]

    # La representación binaria tenga 8 bits (rellenando con ceros a la izquierda si es necesario)
    representacion_binaria = representacion_binaria.zfill(8)
    
    return representacion_binaria

def main():
    filename = sys.argv[1]
    #filename = "tp1_sample0.bin"
    
    if(len(sys.argv) > 2):
        n = int(sys.argv[2])
    else:
        n=1

    arch = archivo(filename, n)

    if(arch.abrirArchivo() == 0):
        arch.print_M()
        
        if(arch.nula()):
            print("\nLa fuente tiene simbolos estadisticamente independientes (es de memoria nula)")
            print("\nLa entropia de la fuente es: " + str(round(arch.entropiaMemoriaNula(),2)))
            arch.calculaEntropiaExtensionN(n)
        else:
            print("\nLa fuente tiene simbolos estadisticamente dependientes (es de memoria no nula)")
            arch.calcularVectorEstacionario()
            print("\nLa entropia de la fuente es: " + str(round(arch.entropiaMemoriaNoNula(),2)))
            print("\nVector estacionario " + str(arch.calcularVectorEstacionario()))



if __name__ == "__main__":
    main()
