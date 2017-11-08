from xml.dom import minidom
from operator import attrgetter
from random import randint
from time import perf_counter as pctime

import math
import copy
import sys
import os

soluciones = {
    'ga1':229884.00,
    'ga2':180117.00,
    'ga3':163403.00,
    'ga4':155795.00,
    'gb1':239077.00,
    'gb2':198045.00,
    'gb3':169368.00,
    'gc1':250557.00,
    'gc2':215019.00,
    'gc3':199344.00,
    'gc4':195365.00,
    'gd1':332533.00,
    'gd2':316711.00,
    'gd3':239482.00,
    'gd4':205834.00,
    'ge1':238880.00,
    'ge2':212262.00,
    'ge3':206658.00,
    'gf1':263175.00,
    'gf2':265214.00,
    'gf3':241487.00,
    'gf4':233861.00,
    'gg1':307272.00,
    'gg2':245441.00,
    'gg3':230170.00,
    'gg4':232646.00,
    'gg5':222025.00,
    'gg6':213457.00,
    'gh1':270525.00,
    'gh2':253366.00,
    'gh3':247449.00,
    'gh4':250221.00,
    'gh5':246121.00,
    'gh6':249136.00,
    'gi1':356381.00,
    'gi2':313917.00,
    'gi3':297318.00,
    'gi4':295988.00,
    'gi5':302708.00,
    'gj1':341984.00,
    'gj2':316308.00,
    'gj3':282535.00,
    'gj4':298184.00,
    'gk1':407939.00,
    'gk2':370840.00,
    'gk3':371322.00,
    'gk4':359642.00,
    'gl1':449271.00,
    'gl2':407445.00,
    'gl3':413806.00,
    'gl4':390247.00,
    'gl5':394576.00,
    'gm1':407072.00,
    'gm2':411132.00,
    'gm3':383448.00,
    'gm4':356311.00,
    'gn1':428328.00,
    'gn2':429521.00,
    'gn3':412220.00,
    'gn4':410694.00,
    'gn5':389349.00,
    'gn6':384461.00
}

demand_delivery_0 = []
demand_delivery = []
vehicule_capacity = 0


class Arch:

    def __init__(self,source,destination):
        self.source      = source
        self.destination = destination

class Node:

    def __init__(self,ide,typ,corX,corY,demand):
        self.ide  = ide
        self.typ  = typ
        self.corX = corX
        self.corY = corY
        self.demand = demand

    def __str__(self):

        return ("Id: %s Type: %s Cords: (%s,%s) Demand: %s") % (self.ide,self.typ,self.corX,self.corY,self.demand)

class Solution:
    def __init__(self, paths, deliveries, pickups, costs):
        self.paths = paths
        self.deliveries = deliveries
        self.pickups = pickups
        self.costs = costs

    def path_cost(self, path):
        distance = 0.0
        size = len(path)
        for i in range(0,size-1):
            distance += self.costs[path[i]][path[i+1]]
        return distance

    def cost(self):
        distance = 0.0
        for path in self.paths:
            distance += self.path_cost(path)
        return distance

    def neighbor_generator(self):
        index = 0
        for path in self.paths:
            if self.deliveries[index] > 1:
                stop = self.deliveries[index]
                for i in range(1,stop):
                    for j in range(i+1,stop+1):
                        n_paths = copy.deepcopy(self.paths) #neighbor paths
                        permuted_path = n_paths[index]
                        permuted_path[i], permuted_path[j]  = permuted_path[j], permuted_path[i]
                        yield Solution(n_paths, self.deliveries, self.pickups, self.costs)

            if self.pickups[index] > 1:
                stop2 = self.pickups[index]

                for i in range(stop + 1,stop + 1 + stop2):
                    for j in range (i+1,stop + 1 + stop2):
                        n_paths = copy.deepcopy(self.paths) #neighbor paths
                        permuted_path = n_paths[index]
                        permuted_path[i], permuted_path[j]  = permuted_path[j], permuted_path[i]
                        yield Solution(n_paths, self.deliveries, self.pickups, self.costs)

            index += 1

    def print_cost(self):
        print("Costo: "+str(self.cost()))

    def __str__(self):
        s = "Rutas:\n"
        for path in self.paths:
            s += "  "+str(path)+"\n"
        s += "\nCosto: "+str(self.cost())
        return s

#Funcion para obtener la distancia euclediana entre 2 nodos
def Distance(node1,node2):

    return math.sqrt((node1.corX - node2.corX)**2 + (node1.corY - node2.corY)**2)

def Parser(entryFile):

    doc      = minidom.parse(entryFile)
    nodes    = doc.getElementsByTagName('node') #Lista con los tipos del nodo
    cx       = doc.getElementsByTagName('cx') #Coordenada X del nodo
    cy       = doc.getElementsByTagName('cy') #Coordenada Y del nodo
    capacity = doc.getElementsByTagName('capacity') #Capacidad de cada vehiculo
    demand   = doc.getElementsByTagName('quantity') #Demanda de cada nodo

    nodesLength = len(nodes) #Tamano de la lista de nodos
    nodesList   = [] #Lista para guardar el resultado
    deliveryNodes = [] #Lista para obtener los identificadores de los nodos que son delivery
    pickUpNodes   = [] #Lista para obtener los identificadores de los nodos que son pickUp
    nodeDemand = 0 #Representa la demanda para el Nodo

    #El ID del nodo es un numero creciente a partir del 0
    for i in range(0,nodesLength):

        #Tipo 1 es para los delivery, Tipo 2 es para los pickUp
        typ = int(nodes[i].attributes['type'].value) #Obtenemos el tipo de cada Nodo
        if typ == 1:
            deliveryNodes.append(i)
        elif typ == 2:
            pickUpNodes.append(i)

        #Obtenemos las cordenadas (X,Y) del nodo i en el plano
        corX = float(cx[i].firstChild.nodeValue)
        corY = float(cy[i].firstChild.nodeValue)

        #El nodo 0 no tiene demanda, por lo que la lista de demand es de tamano nodesLength - 1
        if i > 0:
            nodeDemand = float(demand[i-1].firstChild.nodeValue)

        #Procedemos a crear la lista de los Nodos
        nodesList.append(Node(int(i),typ,corX,corY,nodeDemand))

    #Extraemos la capacidad de cada vehiculo
    vehiculeCapacity = float(capacity[0].firstChild.nodeValue)

    return (nodesList,deliveryNodes,pickUpNodes,vehiculeCapacity)

#Creamos el grafo con nodos y arcos
def GetGraph(entryFile):

    nodesList, deliveryNodes, pickUpNodes, vehiculeCapacity  = Parser(entryFile)

    global vehicule_capacity
    vehicule_capacity = vehiculeCapacity

    #Lista para obtener los arcos
    archsList = []

    #Matriz para guardar los costos de los arcos
    costMatrix = []

    #Realizamos un todos contra todos y vamos creando la matriz de costos
    #al igual que la creacion de los arcos
    for a in nodesList:
        costMatrix.append([])
        for b in nodesList:
            if a.ide == b.ide:
                costMatrix[a.ide].append(0)
                pass
            else:
                distance = Distance(a,b)
                archsList.append(Arch(a,b))
                costMatrix[a.ide].append(distance)


    return (nodesList,archsList,costMatrix,deliveryNodes,pickUpNodes,vehiculeCapacity)

#Algoritmo encargado de obtener la primera solucion
def generate_solution(entryFile):
    nodesList, archsList, costMatrix, deliveryNodes, pickUpNodes, vehiculeCapacity = GetGraph(entryFile)

    #Creamos la lista para verificar si un nodo ha sido visitado
    visitedNodes = [0] * len(nodesList)
    #Cada ruta siempre debe partir del origen, por lo que el origen siempre es visitado de primero
    visitedNodes[0] = 1

    #Variable para ir guardando las rutas
    paths = []
    #Variable para ir determinando a que set pertenece cada solucion
    sett = 0
    #Variable para llevar el registro del nodo se tratara expandir
    nodeToExpand = 0
    #Variables para hacer el chequeo de las listas de visitados
    deliveryLength,pickUpLength = len(deliveryNodes),len(pickUpNodes)

    #Variables para determinar cuantos nodos de cada tipo son usados en cada camino
    deliveryUsed,pickUpUsed = [],[]

    #Iniciamos el ciclo para construir todas las rutas
    while deliveryNodes or pickUpNodes:

        #Creamos la lista para cada camino
        paths.append([])
        paths[sett].append(0)
        global demand_delivery
        global demand_delivery_0
        demand_delivery.append([])

        #creamos las listas para asignar cuantos nodos de tipo delivery y pickUp son
        #usados en cada camino
        deliveryUsed.append([])
        deliveryUsed[sett] = 0
        pickUpUsed.append([])
        pickUpUsed[sett] = 0

        #Iniciamos la capacidad total del vehiculo ya que iniciaremos los delivery
        capacity = vehiculeCapacity
        #Inicializamos los flags para salirnos de los ciclos internos
        visitedAllDelivery,VisitedAllPickUp = False,False

        #Mientras hayan nodos de entrega
        if deliveryNodes:

            #Seteamos los nodos de delivery en no visitados para contruir Ruta
            for node in deliveryNodes:
                visitedNodes[node] = 0


            #Empezamos determiando hacia que nodo nos vamos a expander desde el origen
            for arch in archsList:

                id1 = arch.source.ide
                id2 = arch.destination.ide

                if id1 == 0 and id2 in deliveryNodes and visitedNodes[id2] == 0:

                    capacity -= arch.destination.demand
                    demand_delivery[sett].append(arch.destination.demand)
                    nodeToExpand = arch.destination
                    paths[sett].append(id2)
                    deliveryNodes.remove(id2)
                    deliveryUsed[sett] +=1
                    visitedNodes[id2] = 1
                    break


        #Empezamos a construir la ruta de los delivery hasta que no se pueda mas
        while capacity > 0 and deliveryNodes and not visitedAllDelivery:

            for arch in archsList:

                id1 = arch.source.ide
                id2 = arch.destination.ide

                if id1 == nodeToExpand.ide and id2 in deliveryNodes and visitedNodes[id2] == 0:

                    demand = arch.destination.demand
                    visitedNodes[id2] = 1

                    if (capacity - demand >= 0):

                        capacity -= demand
                        demand_delivery[sett].append(arch.destination.demand)
                        nodeToExpand = arch.destination
                        deliveryNodes.remove(id2)
                        deliveryUsed[sett] +=1
                        paths[sett].append(id2)
                        break

            #Debemos revisar si todos los nodos de delivery han sido visitado
            for i in range(1,deliveryLength+1):
                visitedAllDelivery = visitedNodes[i] == 1
                if not visitedAllDelivery:
                    break

        #Cada vez q vamos a realizar de expansion, seteamos las visitas en false
        if pickUpNodes:

            for node in pickUpNodes:
                visitedNodes[node] = 0

        #En caso de que no existan mas nodos delivery, nuestra nueva ruta debe comenzar desde
        #un nodo de tipo pick up
        if pickUpNodes and not deliveryNodes:

            for arch in archsList:

                id1 = arch.source.ide
                id2 = arch.destination.ide

                if id1 == 0 and visitedNodes[id2] == 0 and id2 in pickUpNodes:

                    capacity += arch.destination.demand
                    nodeToExpand = arch.destination
                    paths[sett].append(id2)
                    visitedNodes[id2] = 1
                    pickUpNodes.remove(id2)
                    pickUpUsed[sett] +=1
                    break

        #Empezamos la ruta de los pick up hasta que no se pueda mas
        while capacity < vehiculeCapacity and pickUpNodes and not VisitedAllPickUp:

            for arch in archsList:

                id1 = arch.source.ide
                id2 = arch.destination.ide

                if id1 == nodeToExpand.ide and id2 in pickUpNodes and visitedNodes[id2] == 0:
                    demand = arch.destination.demand
                    visitedNodes[id2] = 1

                    if (capacity + demand <= vehiculeCapacity):

                        capacity += demand
                        nodeToExpand = arch.destination
                        paths[sett].append(id2)
                        pickUpNodes.remove(id2)
                        pickUpUsed[sett] +=1
                        break

            #Debemos revisar si ya hemos agotado la opcion de pick ups para la ruta
            for i in range(deliveryLength+1,deliveryLength+pickUpLength+1):
                VisitedAllPickUp = visitedNodes[i] == 1
                if not VisitedAllPickUp:
                    break

        paths[sett].append(0)
        sett += 1

    demand_delivery_0 = copy.deepcopy(demand_delivery)

    return Solution(paths,deliveryUsed,pickUpUsed,costMatrix)

#Funcion para crear una vecindad a partir de una solucion inicial
#Si parameter es 0, se aplica la creacion de la vecindad completa
#en caso contrario, se va generando vecino a vecino
def CreateNeighborhood(solution):

    #lista para ir creando la vecindad
    neighbors = []

    #La variable index denota el camino de la ruta completa
    #que vamos a agarrar para permutar
    index = 0

    for path in solution.paths:

        #Revisamos si existen mas de 2 nodos de tipo delivery
        #en la ruta para permutar dicho camino
        if solution.deliveries[index] > 1:

            stop = solution.deliveries[index]
            '''se sabe que la posicion 0 siempre es el origen, asi que los delivery
            siempre iran a partir de la posicion 1 hasta efectivamente la posicion
            que dictamine el tamano de lista de deliverys usados para ese camino
            ejemplo: [0,d,d,d,d,d,d,p,p,p,0] hay 6 delivery por lo que se recorre
            de la posicion 1 hasta la posicion 6-1 = 5 ya que el ultimo elemento
            no permuta con los siguientes por ser pick ups'''
            for i in range(1,stop):

                for j in range(i+1,stop+1):

                    permutedPath  = copy.deepcopy(path)
                    neighbor = copy.deepcopy(solution.paths) #Mi vecino sera igual a mi path actual pero con una permutacion
                    temporal = permutedPath[i]
                    permutedPath[i]  = permutedPath[j]
                    permutedPath[j]  = temporal
                    neighbor[index]  = permutedPath #El camino que ando permutando es el que se cambia en la posicion index
                    neighbors.append(Solution(neighbor,solution.deliveries,solution.pickups,solution.costs))


        #Despues de haber permutado los delivery, emepzamos a ver
        #las posibles permutaciones de los pick up para expandir
        #la vecindad
        if solution.pickups[index] > 1:

            stop2 = solution.pickups[index]
            '''Los pickUp empiezan justamente despues de los delivery, por lo que el
            inicio para las permutaciones empieza a partir de la posicion donde 
            terminan los delivery + 1, al ser la ultima posicion 0 nuevamente, por
            ser el retorno al deposito, nos bastara evaluar en los 2 casos hasta la 
            longitud de los pickUp -1'''
            for i in range(stop + 1,stop + 1 + stop2):

                for j in range (i+1,stop + 1 + stop2):

                    permutedPath  = copy.deepcopy(path)
                    neighbor = copy.deepcopy(solution.paths)
                    temporal = permutedPath[i]
                    permutedPath[i]  = permutedPath[j]
                    permutedPath[j]  = temporal
                    neighbor[index]  = permutedPath
                    neighbors.append(Solution(neighbor,solution.deliveries,solution.pickups,solution.costs))

        index += 1

    return neighbors



def TabuSearch(solution):

    MAX_SIZE  = 10 #Variable para definir el maximo tamano de la lista taboo
    best_sol  = solution #Variable para encontrar la mejor solucion posible
    best_candidate = solution #variable para ir guardando los candidatos a mejor solucion
    best_cost  = best_sol.cost() #Variable que almacena el menor costo encontrado
    tabuList  = [] #lista taboo
    tabuList.append(best_sol)
    attempts = 0   #variable para designar cuantos intentos se pueden hacer para actualizar la mejor solucion
    sentinel = 400 #Variable para designar el maximo numero de iteraciones a realizar antes de salir del ciclo

    while(attempts <= 15 and sentinel > 0):


        #Para cada nuevo mejor candidato que vamos obteniendo, generamos su vecindad
        neighbors = CreateNeighborhood(best_candidate)
        index = randint(0,len(neighbors)-1)
        best_candidate = neighbors[index]#Elegimos un vecino aleatorio de la nueva vecindad para partir y decir
                                         #que sera el mejor candidato para sustituir la solucion final
        candidate_cost = best_candidate.cost()

        #Para cada vecino en la vecindad
        for neighbor in neighbors:

            neighbor_cost = neighbor.cost()

            #Si el nuevo vecino es un mejor candidato
            if not(neighbor.cost() in tabuList) and neighbor_cost < candidate_cost:

                best_candidate = neighbor
                candidate_cost = neighbor_cost

            #Verificamos si el nuevo candidato es el mas prometedor para ser solucion final
        if candidate_cost < best_cost:

            best_cost = candidate_cost
            best_sol  = best_candidate
               #En caso de haber encontrado una solucion aun mejor,
                #reiniciamos el numero de intentos antes de rendirnos
            attempts = 0

        tabuList.append(best_candidate.cost())

        if len(tabuList) > MAX_SIZE:
            tabuList.pop(0)

        #Aumentamos el # de intentos que hemos hecho para tratar de mejorar la solucion
        attempts += 1
        #
        sentinel -= 1

    #Devolvemos el mejor encontrado
    return best_sol

def disturbSolution(solution):

    index = 0
    disturbed = copy.deepcopy(solution)
    valid = False
    global demand_delivery
    global vehicule_capacity

    while not valid:
        #indices para saber sobre que ruta estamos trabajando
        i1 = randint(0,len(disturbed.paths)-1)
        i2 = randint(0,len(disturbed.paths)-1)
        while(i1 == i2):
            i2 = randint(0,len(disturbed.paths)-1)

        if(len(demand_delivery[i1]) < 1 or len(demand_delivery[i2]) < 1):
            continue

        #indices para saber sobre que nodo de la ruta estamos trabajando
        p1 = randint(1,disturbed.deliveries[i1])
        p2 = randint(1,disturbed.deliveries[i2])
        while(i1 == i2):
            p2 = randint(1,disturbed.deliveries[i2])

        delivs1 = copy.deepcopy(demand_delivery[i1])
        delivs2 = copy.deepcopy(demand_delivery[i2])

        #asignamos la alteracion en las listas sustitutas para saber si es valido
        delivs1[p1-1],delivs2[p2-1] = delivs2[p2-1],delivs1[p1-1]

        #si la modificacion es valida, procedemos a intercambiar
        global vehicule_capacity
        if (sum(delivs1) <= vehicule_capacity and sum(delivs2) <= vehicule_capacity):

            disturbed.paths[i1][p1],disturbed.paths[i2][p2] = disturbed.paths[i2][p2],disturbed.paths[i1][p1]
            demand_delivery[i1] = delivs1
            demand_delivery[i2] = delivs2
            valid = True

    return disturbed

def ILS(solution):

    attempts = 0
    iterator = 0
    MAX_ATTEMPT = 20
    MAX_ITERATION = 500
    best_sol = localSearch(solution,MAX_ATTEMPT)

    while(attempts < MAX_ATTEMPT and iterator < MAX_ITERATION):

        disturbed = disturbSolution(best_sol)
        candidate = localSearch(disturbed,MAX_ATTEMPT)

        if (candidate.cost() < best_sol.cost()):
            best_sol = candidate
            attempts = 0

        iterator += 1
        attempts += 1

    return best_sol



def firstBest(sol, neighborhood):    
    for neighbor in neighborhood:
        if neighbor.cost() < sol.cost():
            return neighbor
    return sol


def localSearch(ini_sol, max_it):
    sol = ini_sol
    iterations = 0
    while True:
        previous_cost = sol.cost()
        neighborhood = sol.neighbor_generator()
        sol = firstBest(sol, neighborhood)

        if sol.cost() == previous_cost:
            iterations += 1
            if iterations > max_it:
                break
    return sol


def main():
    instance  = "dataset/%s.xml" % (sys.argv[1])

    firt_time_begin = pctime()
    first_sol       = generate_solution(instance)
    first_time_end  = pctime() - firt_time_begin

    tabu_time_begin = pctime()
    tabu_sol        = TabuSearch(first_sol) 
    tabu_time_end   = pctime() - tabu_time_begin

    ils_time_begin = pctime()
    ils_sol = ILS(first_sol)
    ils_time_end = pctime() - ils_time_begin

    demand_delivery = copy.deepcopy(demand_delivery_0)
    ils2_time_begin = pctime()
    ils2_sol = ILS(first_sol)
    ils2_time_end = pctime() - ils2_time_begin

    demand_delivery = copy.deepcopy(demand_delivery_0)
    ils3_time_begin = pctime()
    ils3_sol = ILS(first_sol)
    ils3_time_end = pctime() - ils3_time_begin

    ils_final_sol = (ils_sol.cost() + ils2_sol.cost() + ils3_sol.cost()) / 3

    ils_final_time = (ils_time_end + ils2_time_end + ils3_time_end) / 3

    iniC = round(first_sol.cost(),2)
    tabC = round(tabu_sol.cost(),2)
    tabT = round(tabu_time_end,2)
    ilsC = round(ils_final_sol,2)
    ilsT = round(ils_final_time,2)
    mejC = round(soluciones[sys.argv[1]],2)

    if (sys.argv[1] == "ga1"):
        print("Inicial - Tabu - Ils Promedio - Optimo conocido - Tiempo Tabu - Tiempo Ils")

    print("%s - %s - %s - %s - %s - %s" % (iniC,tabC,ilsC,mejC,tabT,ilsT)) 





    '''print("Instancia %s:" % sys.argv[1])
    print("Distancia Solucion Inicial: %s Timepo de Inicial: %s" % (first_sol.cost(),first_time_end))
    print("Distancia Solucion Tabu:    %s Tiempo de Tabu:    %s" % (tabu_sol.cost(),tabu_time_end))
    print("Distancia Solucion ILS :    %s Tiempo de ILS :    %s" % (ils_final_sol,ils_final_time))
    print()'''




if __name__ == "__main__":
    main()
