import time
import pandas as pd
from copy import deepcopy

n = input("Ingrese la cantidad de procesos que se llevaran a cabo: ")
n = int(n)

procesos = []

for i in range(n):
    a = int(input(f"Ti del proceso {i + 1}: "))
    b = int(input(f"Ingrese el t del proceso {i + 1}: "))
    process = {"ti":a , "t":b, "tf": 0, "T": 0, "E": 0, "I": 0, "complete": False}
    procesos.append(process)
    print("Agregado")


def fifo(pro):

    finished = 0
    currentTime = 0
    acumulador = 0
    acumuladorE = 0
    acumuladorI = 0
    wait = True

    while finished != len(pro):

        for elements in pro:
            initial = elements["ti"]
            t = elements["t"]
            T = elements["T"]
            I = elements["I"]
            if currentTime >= initial and elements["tf"] == 0:
                finished += 1
                elements["tf"] = currentTime + elements["t"]
                T = elements["tf"] - elements["ti"]
                elements["T"] = T
                acumulador += elements["T"]
                elements["E"] = T - t
                acumuladorE += elements["E"]
                I = t/T
                elements["I"] = I
                acumuladorI += elements["I"]
                wait = False
                currentTime += elements["t"]
                
        if wait:
            currentTime += 1
        
        left = []
        for element in pro:
            if element["tf"] == 0: left.append(element)
        
        if len(left) == 0: break
    
    promT = acumulador/n
    promE = acumuladorE/n
    promI = acumuladorI/n
    
    drawTable(pro)
    print("Promedio de T: ",f"{promT:.2f}")
    print("Promedio de E: ",f"{promE:.2f}")
    print("Promedio de I: ",f"{promI:.2f}")
    print("Clock final: " + str(currentTime))

def lifo(pro):
    rev = list(reversed(pro))
    fifo(rev)


def rr(pro):

    finished = 0
    currentTime = 0
    quantum = 4
    wait = True
    acumulador = 0
    acumuladorE = 0
    acumuladorI = 0

    while finished != len(pro):
        for elements in pro:
            test = elements["ti"]
            t = elements["t"]
            T = elements["T"]
            complete = elements["complete"]

            if currentTime >= test and complete == False:
                if elements["t"] > quantum:
                    currentTime += quantum
                    elements["t"] -= quantum
                    wait = False
                else:
                    finished += 1
                    elements["complete"] = True
                    elements["tf"] = currentTime + elements["t"]
                    T = elements["tf"] - elements["ti"]
                    elements["T"] = T
                    acumulador += elements["T"]
                    elements["E"] = T - t
                    acumuladorE += elements["E"]
                    elements["I"] = t/T
                    acumuladorI += elements["I"]
                    wait = False
                    currentTime += elements["t"]
            
            
            
        if wait:
            currentTime += 1
        
        left = []
        for element in pro:
            if element["tf"] == 0: left.append(element)
        
        if len(left) == 0: break
        
     
    promT = acumulador/n
    promE = acumuladorE/n
    promI = acumuladorI/n
    
    drawTable(pro)

    print("Promedio de T: "f"{promT:.2f}")
    print("Promedio de E: "f"{promE:.2f}")
    print("Promedio de I: "f"{promI:.2f}")
    print("Clock final: " + str(currentTime))

def drawTable(pro):
    tabla = pd.DataFrame(pro, columns=["ti", "t", "tf", "T", "E", "I"])
    print(tabla)

initialTime = time.time()

fifo(deepcopy(procesos))

times = time.time() - initialTime
print("Tiempo de ejecucion del proceso de fifo: " + str(f"{times:.7f}"))

initialTime2 = time.time()

lifo(deepcopy(procesos))

times2 = time.time() - initialTime2
print("Tiempo de ejecucion del proceso lifo: " + str(f"{times2:.7f}"))

initialTime3 = time.time()

rr(deepcopy(procesos))

times3 = time.time() - initialTime3
print("Tiempo de ejecucion del proceso round robin: " + str(f"{times3:.7f}"))

if times < times2 and times < times3:
    print("El proceso mas rapido fue lifo")
elif times2 < times and times2 < times3:
    print("El proceso mas rapido fue fifo")
elif times3 < times and times3 < times2:
    print("El proceso mas rapido fue Round Robin")