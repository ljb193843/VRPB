from xml.dom import minidom
from operator import attrgetter
from random import randint,choice
from time import time 

import math
import copy
import sys
import os

nodesList     = [] #Lista para guardar los nodos leidos
deliveryNodes = [] #Lista para obtener los identificadores de los nodos que son delivery
pickUpNodes   = []  #Lista para obtener los identificadores de los nodos que son pickUp
demandList    = [] #Lista para obtener las demandas de cada nodo
costMatrix    = [] #Matriz para guardar el costo de ir de un nodo a otro
vehiculeCapacity = 0 #Capacidad de los vehiculos
vehicules = 0 #Cantidad de Vehiculos



soluciones = {
    'GA1':229884.00,
    'GA2':180117.00,
    'GA3':163403.00,
    'GA4':155795.00,
    'GB1':239077.00,
    'GB2':198045.00,
    'GB3':169368.00,
    'GC1':250557.00,
    'GC2':215019.00,
    'GC3':199344.00,
    'GC4':195365.00,
    'GD1':332533.00,
    'GD2':316711.00,
    'GD3':239482.00,
    'GD4':205834.00,
    'GE1':238880.00,
    'GE2':212262.00,
    'GE3':206658.00,
    'GF1':263175.00,
    'GF2':265214.00,
    'GF3':241487.00,
    'GF4':233861.00,
    'GG1':307272.00,
    'GG2':245441.00,
    'GG3':230170.00,
    'GG4':232646.00,
    'GG5':222025.00,
    'GG6':213457.00,
    'GH1':270525.00,
    'GH2':253366.00,
    'GH3':247449.00,
    'GH4':250221.00,
    'GH5':246121.00,
    'GH6':249136.00,
    'GI1':356381.00,
    'GI2':313917.00,
    'GI3':297318.00,
    'GI4':295988.00,
    'GI5':302708.00,
    'GJ1':341984.00,
    'GJ2':316308.00,
    'GJ3':282535.00,
    'GJ4':298184.00,
    'GK1':407939.00,
    'GK2':370840.00,
    'GK3':371322.00,
    'GK4':359642.00,
    'GL1':449271.00,
    'GL2':407445.00,
    'GL3':413806.00,
    'GL4':390247.00,
    'GL5':394576.00,
    'GM1':407072.00,
    'GM2':411132.00,
    'GM3':383448.00,
    'GM4':356311.00,
    'GN1':428328.00,
    'GN2':429521.00,
    'GN3':412220.00,
    'GN4':410694.00,
    'GN5':389349.00,
    'GN6':384461.00
}

#Clase para albergar una solucion obtenida
class Solution:

    def __init__(self,routes,deliDemands,pickDemands,deliSize,pickSize):
        self.routes = routes #Rutas de la solucion
        self.deliDemands = deliDemands #Demanda de los nodos delivery para cada ruta
        self.pickDemands = pickDemands #Demanda de los nodos pickup para cada ruta
        self.deliSize = deliSize #Cantidad de nodos de tipo deliverie en la ruta
        self.pickSize = pickSize #Cantidad de nodos de tipo pick up en la ruta
        self.cost = 0 #Costo de la ruta

    #Funcion para obtener el costo de la ruta
    def getCost(self):

        def routeCost(route):
            global costMatrix
            cost = 0
            for i in range(0,len(route)-1):
                cost += costMatrix[route[i]][route[i+1]]
            return cost

        cost = 0
        for route in self.routes:
            cost += routeCost(route)
        return cost

    #Funcion para crear el iterador de la vecindad
    def generateNeighbor(self):

        global vehicules
        global vehiculeCapacity
        global demandList
        #tries = 0 #Variable para llevar el numero de intentos
        while True:

            n_routes = copy.deepcopy(self.routes)
            n_delDem = copy.deepcopy(self.deliDemands)
            n_picDem = copy.deepcopy(self.pickDemands)
            n_delSiz = copy.deepcopy(self.deliSize)
            n_picSiz = copy.deepcopy(self.pickSize)

            #variable para determinar si intercambiamos deliveries (1) o pickups (2)
            action = randint(1,2)

            #Caso para intercambiar deliveries
            if action == 1:
            	#Buscamos la primer ruta para el intercambio
            	r1_index = randint(0,vehicules-1)
            	#validamos que sea una ruta valida para intercambiar deliveries
            	while(self.deliSize[r1_index] == 0):
            		r1_index = randint(0,vehicules-1)
            	#Buscamos la segunda ruta para el intercambio
            	r2_index = r1_index
            	#Verificamos que sea una ruta valida y distinta de la primera ruta
            	while(r2_index == r1_index):
            		r2_index = randint(0,vehicules-1)
            		#validamos que sea una ruta valida para intercambiar deliveries
            		while(self.deliSize[r2_index] == 0):
            			r2_index = randint(0,vehicules-1)

            	#Seleccionamos el indice del nodo a intercambiar de la ruta 1
            	d1_index = randint(1,self.deliSize[r1_index])
            	#Seleccionamos el indice del nodo a intercambiar de la ruta 2
            	d2_index = randint(1,self.deliSize[r2_index])

            	#Obtenemos los identificadores de cada nodo para determinar su demanda
            	n1Id = n_routes[r1_index][d1_index]
            	n2Id = n_routes[r2_index][d2_index]

            	if ((n_delDem[r1_index] + demandList[n1Id] - demandList[n2Id] >= 0) and
            	(n_delDem[r2_index] + demandList[n2Id] - demandList[n1Id] >= 0)):

            		#Actualizamos la demanda de las rutas a intercambiar
            		n_delDem[r1_index] = n_delDem[r1_index] + demandList[n1Id] - demandList[n2Id]
            		n_delDem[r2_index] = n_delDem[r2_index] + demandList[n2Id] - demandList[n1Id]
            		#Realizamos el intercambio
            		n_routes[r1_index][d1_index],n_routes[r2_index][d2_index] = n_routes[r2_index][d2_index],n_routes[r1_index][d1_index]

            		yield Solution(n_routes,n_delDem,n_picDem,n_delSiz,n_picSiz)
            		tries = 0

            #Caso para intercambiar PickUps
            elif action == 2:

            	#Buscamos la primer ruta para el intercambio
            	r1_index = randint(0,vehicules-1)
            	#validamos que sea una ruta valida para intercambiar deliveries
            	while(self.pickSize[r1_index] == 0):
            		r1_index = randint(0,vehicules-1)
            	#Buscamos la segunda ruta para el intercambio
            	r2_index = r1_index
            	#Verificamos que sea una ruta valida y distinta de la primera ruta
            	while(r2_index == r1_index):
            		r2_index = randint(0,vehicules-1)
            		#validamos que sea una ruta valida para intercambiar deliveries
            		while(self.pickSize[r2_index] == 0):
            			r2_index = randint(0,vehicules-1)

            	#Determinamos los valores de inicio y fin los tramos de pickUp de las rotas en cuestion
            	beg_1 = self.deliSize[r1_index] + 1
            	end_1 = beg_1 + self.pickSize[r1_index] - 1
            	beg_2 = self.deliSize[r2_index] + 1
            	end_2 = beg_2 + self.pickSize[r2_index] - 1

            	#Seleccionamos el indice del nodo a intercambiar de la ruta 1
            	d1_index = randint(beg_1,end_1)
            	#Seleccionamos el indice del nodo a intercambiar de la ruta 2
            	d2_index = randint(beg_2,end_2)

            	#Obtenemos los identificadores de cada nodo para determinar su demanda
            	n1Id = n_routes[r1_index][d1_index]
            	n2Id = n_routes[r2_index][d2_index]

            	if ((n_picDem[r1_index] - demandList[n1Id] + demandList[n2Id] <= vehiculeCapacity) and
            	(n_picDem[r2_index] - demandList[n2Id] + demandList[n1Id] <= vehiculeCapacity)):

            		#Actualizamos la demanda de las rutas a intercambiar
            		n_picDem[r1_index] = n_picDem[r1_index] - demandList[n1Id] + demandList[n2Id]
            		n_picDem[r2_index] = n_picDem[r2_index] - demandList[n2Id] + demandList[n1Id]
            		#Realizamos el intercambio
            		n_routes[r1_index][d1_index],n_routes[r2_index][d2_index] = n_routes[r2_index][d2_index],n_routes[r1_index][d1_index]

            		yield Solution(n_routes,n_delDem,n_picDem,n_delSiz,n_picSiz)
            		tries = 0

            else:
            	pass

            #tries += 1



class Node:

    def __init__(self,ide,typ,corX,corY):
        self.ide  = ide
        self.typ  = typ
        self.corX = corX
        self.corY = corY

    def __str__(self):

        return ("Id: %s Type: %s Cords: (%s,%s)") % (self.ide,self.typ,self.corX,self.corY)

#Funcion para obtener la distancia euclediana entre 2 nodos
def Distance(node1,node2):

    return math.sqrt((node1.corX - node2.corX)**2 + (node1.corY - node2.corY)**2)

def parser(entryFile):

    doc      = minidom.parse(entryFile)
    nodes    = doc.getElementsByTagName('node') #Lista con los tipos del nodo
    cx       = doc.getElementsByTagName('cx') #Coordenada X del nodo
    cy       = doc.getElementsByTagName('cy') #Coordenada Y del nodo
    capacity = doc.getElementsByTagName('capacity') #Capacidad de cada vehiculo
    demand   = doc.getElementsByTagName('quantity') #Demanda de cada nodo
    vehicule = doc.getElementsByTagName('vehicle_profile')#Cantidad disponible de vehiculos

    nodesLength = len(nodes) #Tamano de la lista de nodos
    nodeDemand = 0 #Representa la demanda para el Nodo
    global nodesList
    global deliveryNodes
    global pickUpNodes
    global demandList
    global vehiculeCapacity
    global vehicules

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

        #Lista para guardar las demandas de los nodos
        demandList.append(nodeDemand)

        #Procedemos a crear la lista de los Nodos
        nodesList.append(Node(int(i),typ,corX,corY))

    #Extraemos la capacidad de cada vehiculo
    vehiculeCapacity = float(capacity[0].firstChild.nodeValue)

    vehicules = int(vehicule[0].attributes['number'].value)

    return

#Creamos el grafo con los costos asociados
def getCostMatrix():

    global costMatrix
    global nodesList
    #Realizamos un todos contra todos y vamos creando la matriz de costos
    #al igual que la creacion de los arcos
    for a in nodesList:
        costMatrix.append([])
        for b in nodesList:
            if a.ide == b.ide:
                costMatrix[a.ide].append(0)
            else:
                distance = Distance(a,b)
                costMatrix[a.ide].append(distance)
    return

#Algoritmo encargado de obtener la primera solucion
def getFirstSol():

    #Declaracion de las variables globales necesarias
    global vehicules
    global vehiculeCapacity
    global costMatrix
    global demandList
    global deliveryNodes
    global pickUpNodes
    global nodesList
    #Hacemos una copia de las listas de deliveries y pickups para generar
    #soluciones iniciales arbitrarias
    deliveries = copy.deepcopy(deliveryNodes)
    pickups    = copy.deepcopy(pickUpNodes)

    #Constante para los casos Borde de un posible ciclo infinito por ser insersiones aleatorias (poco probable)
    MAX_TRIES = 5000

    routes      = [] #Variable para almacenar las rutas generadas 
    delisInPath = [] #Variable para guardar la cantidad de deliveries en cada ruta
    picksInPath = [] #Variable para guardar la cantidad de pickUps en cada ruta
    deliDemands = [] #Variable para guardar la demanda de los deliveries en cada ruta
    pickDemands = [] #Variable para guardar la demanda de los pickups en cada ruta

    #Inicializamos cada uno de los caminos
    for i in range(0,vehicules):
        routes.append([0])
        delisInPath.append(0)
        picksInPath.append(0)
        deliDemands.append(vehiculeCapacity)
        pickDemands.append(0.0)

    #Varaible para determinar si se genera un loop infinito
    tries = 0
    while deliveries:

        #Elegimos una ruta arbitraria
        index  = randint(0,vehicules-1)
        #Escogemos un nodo arbitrario de tipo delivery
        nodeId = choice(deliveries)

        #En caso de que sea posible agregar el nodo a la ruta, se anhade y es eliminado de la 
        #lista de candidatos de deliveries
        if (deliDemands[index] - demandList[nodeId] >= 0):
            deliDemands[index] -= demandList[nodeId]
            routes[index].append(nodeId)
            delisInPath[index] += 1
            deliveries.remove(nodeId)
            tries = 0
        #cada vez que pasa el loop, se suma una al loop detector
        tries += 1

        #Manejo de casos borde
        if tries == MAX_TRIES:
            for node in deliveries:
                index = randint(0,vehicules-1)
                routes[index].append(node)
                delisInPath[index] +=1
            deliveries = []

    tries = 0
    #Debemos actualizar que hay todavia queda carga en el camion
    for i in range(0,vehicules):
    	pickDemands[i] = deliDemands[i]

    while pickups:

        #Elegimos una ruta arbitraria
        index  = randint(0,vehicules-1) 
        #Elegimos un nodo arbitrario
        nodeId = choice(pickups)

        #En caso de que sea posible agregar el nodo a la ruta, se anhade y es eliminado de la 
        #lista de candidatos de deliveries
        if (pickDemands[index] + demandList[nodeId] <= vehiculeCapacity):
            pickDemands[index] += demandList[nodeId]
            routes[index].append(nodeId)
            picksInPath[index] += 1
            pickups.remove(nodeId)
        #Si no podemos agregar mas a esa ruta, pasamos a la siguiente
        tries += 1

        #Manejos de casos bordes
        if tries == MAX_TRIES:
            for node in pickups:
                index = randint(0,vehicules-1)
                routes[index].append(node)
                picksInPath[index] += 1
            pickups = []

    #Una vez creadas las rutas, procedemos a incluir el retorno al origen
    for i in range(0,vehicules):
        routes[i].append(0)

    solution = Solution(routes,deliDemands,pickDemands,delisInPath,picksInPath)
    cost = round(solution.getCost(),2)
    solution.cost = cost

    return solution

#Definimos la obtencion del primer mejor en base a un nodo origen
def getFirstBest(sol):

    cost = sol.getCost()
    deadline = 0
    neighborhood = sol.generateNeighbor()
    for neighbor in neighborhood:
        if neighbor.getCost() < cost:
            return neighbor
        deadline +=1
        if deadline == 10000:
            return sol

#Implementacion de busqueda local con primer mejor
def localSearch(sol,max_tries):

    bestSol  = sol
    tries = 0
    while True:
        candidate = getFirstBest(bestSol)
        if candidate.getCost() < bestSol.getCost():
            bestSol = candidate
            tries = 0
        else:
            tries += 1
            if tries == max_tries:
                break

    return bestSol

def perturbate(sol):

	global demandList
	global vehicules
	global vehiculeCapacity

	perturbed = copy.deepcopy(sol)

	while True:
		#Vemos el porcentaje de peso, por lo general, permutar deliveries sale mejor que pick ups
		action = randint(1,10)
		#Le damos 70% de peso a los delivery
		if action in range(0,9):
			action = 1
		else:
			action = 2

		if action == 1:

        	#Ubicamos la primera ruta
			r1_index = randint(0,vehicules-1)
			while perturbed.deliSize[r1_index] == 0:
				r1_index = randint(0,vehicules-1)

			r2_index = r1_index
        	#	ubicamos la segunda ruta
			while(r2_index == r1_index):
				r2_index = randint(0,vehicules-1)
				#si la segunda ruta no tiene deliveries para intercambiar, seguimos buscando
				while perturbed.deliSize[r2_index] == 0:
					r2_index = randint(0,vehicules-1)

            #Calculamos el inicio y fin del subcamino de la ruta 1 que deseamos invertir
			p1_beg = randint(1,perturbed.deliSize[r1_index])
			p1_end = randint(p1_beg,perturbed.deliSize[r1_index])
            #Caso homologo al camino 1 pero para la ruta 2
			p2_beg = randint(1,perturbed.deliSize[r2_index])
			p2_end = randint(p2_beg,perturbed.deliSize[r2_index])

            #Separamos el camino en su primera parte -  el cuerpo que deseamos cambiar - el resto
			head1 = perturbed.routes[r1_index][0:p1_beg]
			subr1 = perturbed.routes[r1_index][p1_beg:p1_end+1]
			tail1 = perturbed.routes[r1_index][p1_end+1:]

            #Separamos el camino en su primera parte -  el cuerpo que deseamos cambiar - el resto
			head2 = perturbed.routes[r2_index][0:p2_beg]
			subr2 = perturbed.routes[r2_index][p2_beg:p2_end+1]
			tail2 = perturbed.routes[r2_index][p2_end+1:]

			#Calculamos la demanda que requiere el pedazo de la ruta 1 que desemos intercambiar
			subdemand1 = 0
			for node in subr1:
				subdemand1 += demandList[node]
            #Calculamos la demanda que requiere el pedazo de la ruta 2 que desemos intercambiar
			subdemand2 = 0
			for node in subr2:
				subdemand2 += demandList[node]
            #En caso de que el intercambio sea valido
			if ((perturbed.deliDemands[r1_index] + subdemand1 - subdemand2 >= 0) and (
            	perturbed.deliDemands[r2_index] + subdemand2 - subdemand1 >= 0)):

				perturbed.routes[r1_index],perturbed.routes[r2_index] = head1+subr2+tail1,head2+subr1+tail2
				perturbed.deliSize[r1_index] = perturbed.deliSize[r1_index] - len(subr1) + len(subr2)
				perturbed.deliSize[r2_index] = perturbed.deliSize[r2_index] - len(subr2) + len(subr1)
				perturbed.deliDemands[r1_index] = perturbed.deliDemands[r1_index] + subdemand1 - subdemand2
				perturbed.deliDemands[r2_index] = perturbed.deliDemands[r2_index] + subdemand2 - subdemand1

				return perturbed

		elif action == 2:
			#Ubicamos la primera ruta
			r1_index = randint(0,vehicules-1)
			while perturbed.pickSize[r1_index] == 0:
				r1_index = randint(0,vehicules-1)

			r2_index = r1_index
        	#	ubicamos la segunda ronda
			while(r2_index == r1_index):
				r2_index = randint(0,vehicules-1)
				#si la segunda ruta no tiene deliveries para intercambiar, seguimos buscando
				while perturbed.pickSize[r2_index] == 0:
					r2_index = randint(0,vehicules-1)

			#Calculamos el inicio y el fin de cada tramo de nodos de tipo pick up presentes en la ruta que se desea permutar
			beg_1  = perturbed.deliSize[r1_index] + 1
			end_1  = beg_1 + perturbed.pickSize[r1_index] - 1
			beg_2  = perturbed.deliSize[r2_index] + 1
			end_2  = beg_2 + perturbed.pickSize[r2_index] - 1 


            #Calculamos el inicio y fin del subcamino de la ruta 1 que deseamos invertir
			p1_beg = randint(beg_1,end_1)
			p1_end = randint(p1_beg,end_1)
            #Caso homologo al camino 1 pero para la ruta 2
			p2_beg = randint(beg_2,end_2)
			p2_end = randint(p2_beg,end_2)

            #Separamos el camino en su primera parte -  el cuerpo que deseamos cambiar - el resto
			head1 = perturbed.routes[r1_index][0:p1_beg]
			subr1 = perturbed.routes[r1_index][p1_beg:p1_end+1]
			tail1 = perturbed.routes[r1_index][p1_end+1:]

            #Separamos el camino en su primera parte -  el cuerpo que deseamos cambiar - el resto
			head2 = perturbed.routes[r2_index][0:p2_beg]
			subr2 = perturbed.routes[r2_index][p2_beg:p2_end+1]
			tail2 = perturbed.routes[r2_index][p2_end+1:]

			#Calculamos la demanda que requiere el pedazo de la ruta 1 que desemos intercambiar
			subdemand1 = 0
			for node in subr1:
				subdemand1 += demandList[node]
            #Calculamos la demanda que requiere el pedazo de la ruta 2 que desemos intercambiar
			subdemand2 = 0
			for node in subr2:
				subdemand2 += demandList[node]
            #En caso de que el intercambio sea valido
			if ((perturbed.pickDemands[r1_index] - subdemand1 + subdemand2 <= vehiculeCapacity) and (
            	perturbed.pickDemands[r2_index] - subdemand2 + subdemand1 <= vehiculeCapacity)):

				perturbed.routes[r1_index],perturbed.routes[r2_index] = head1+subr2+tail1,head2+subr1+tail2
				perturbed.pickSize[r1_index] = perturbed.pickSize[r1_index] - len(subr1) + len(subr2)
				perturbed.pickSize[r2_index] = perturbed.pickSize[r2_index] - len(subr2) + len(subr1)
				perturbed.pickDemands[r1_index] = perturbed.deliDemands[r1_index] - subdemand1 + subdemand2
				perturbed.pickDemands[r2_index] = perturbed.deliDemands[r2_index] - subdemand2 + subdemand1

				return perturbed

		else:
			pass

#Metaheuristica de busqueda local iterada
def ILS():

	tries = 0
	MAX_TRIES = 6
	sol = getFirstSol()
	bestSol = localSearch(sol,MAX_TRIES)

	while True:
		candidate = perturbate(bestSol)
		candidate = localSearch(candidate,15)
		if(candidate.getCost() < bestSol.getCost()):
			bestSol = candidate
			tries = 0
		else:
			tries +=1
			if (tries == MAX_TRIES):
				return bestSol
##############################################################################################################################################

#----------------------------------------------------------INICIO DE SECCION DE METAHEURISTICAS POBLACIONALES -------------------------------#

##############################################################################################################################################


#Funcion para transformar un conjunto de rutas en una ruta generalizada
def getSingleArray(sol):

	routes = copy.deepcopy(sol.routes)
	array = [0]
	for route in routes:
		array += route[1:]
	return array

#Funcion para obtener rutas de la forma en la que los deliveries estan antes q los pickup
def reorderRoute(route):

	global deliveryNodes
	global pickUpNodes
	deliSize = 0
	pickSize = 0

	size = len(route)#Delimitador para saber el tamano de la ruta
	ordered = [0]#Variable para obtener la ruta ya orenada (deliveries antes de pickups)
	pick = []

	#Para el rango que esta entre los delimitadores 0
	for node in route[1:size-1]:

		if node in deliveryNodes:
			ordered.append(node)
			deliSize += 1

		#Si no es delivery, significa que todavia no se puede anexar a la lista
		#hasta estar seguro de que no existen mas deliveries posteriorente
		else:
			pick.append(node)
			pickSize += 1
	#Al anexar todos los deliveries, se puede proceder a anexar los pickups
	for elem in pick:

		ordered.append(elem)
	#Agregamos el final de la ruta
	ordered.append(0)

	return(ordered,deliSize,pickSize)
#
#Funcion para realizar el cruze entre 2 padres
def crossover(father,mother):
	
	global deliveryNodes
	global pickUpNodes
	global vehicules

	#listas para ir llevar un control de que nodos estan disponibles para la ruta
	#Una vez que un nodo es agregado a la ruta, se procede
	deliveries = copy.deepcopy(deliveryNodes)
	pickups = copy.deepcopy(pickUpNodes)

	#decidimos quien sera el padre dominante (alfa) en el cruze
	action   = randint(1,2)
	routeLen = len(father) #El padre y la madre tienen la misma longitud, asi que es igual
							#determinar la longitud que tendra el hijo tomano cualquier padre 

	#alfa es el padre del cual se obtendra una subcadena y la longitud de los caminos
	#beta es el padre sumiso

	if action == 1:

		alfa = copy.deepcopy(father)
		beta = copy.deepcopy(mother)

	else:

		alfa = copy.deepcopy(mother)
		beta = copy.deepcopy(father)

	#arreglo para determinar si una posicion del hijo puede ser cambiada por alguien
	child_pos = [0]*routeLen

	child_pos[0] = 1          #Sabemos que los extremos siempre seran 0 ya que el origen y el destino son 
	child_pos[routeLen-1] = 1 #siempre el sumidero, por lo que sus posiciones son no variables

	child = [0]*routeLen #creamos el arreglo hijo, el cual sera el producto de la mezcla entre pares

	#Alberga las posiciones de los O's del nodo que se haya decidido como alfa
	indexes = []
	#creamos la lista de indices de delimitadores de ruta
	for i in range(1,routeLen-1):
		if alfa[i] == 0:
			indexes.append(i)

	#asignamos las posiciones de los delimitadores de rutas como no variables
	for index in indexes:
		child_pos[index] = 1

	#obtenemos los indices de las posiciones para obtener el subconjunto fijo que se heredara de alfa
	beg = randint(1,routeLen-1)
	end = randint(beg,routeLen-1)

	#obtenemos la subruta del croosover
	subAlfa = alfa[beg:end+1]

	child[beg:end+1] = subAlfa

	#Seteamos las posiciones de la subruta agregada como no variables
	for i in range(beg,end+1):
		child_pos[i] = 1

	#eliminamos estos nodos de de los deliveries y de los pickups para no usarlos en caso de que esten repetidos
	#en el otro padre
	for node in subAlfa:
		if node in deliveries:
			deliveries.remove(node)
		elif node in pickups:
			pickups.remove(node)
		else:
			pass
	#variable para guardar todas aquellas posiciones que no se lograron modificar en el intento de crossover
	negative_indexes = []

	#Tratamos de seleccionar si heredamos del padre alfa o del beta como primera opcion
	for index in range(1,routeLen-1):

		if child_pos[index] == 1:
			pass
		else:
			action = randint(1,2)
			#trato de copiar de alfa su posicion index
			if action == 1:

				if alfa[index] in deliveries:

					child[index] = alfa[index]
					deliveries.remove(alfa[index])
					child_pos[index] = 1

				elif alfa[index] in pickups:

					child[index] = alfa[index]
					pickups.remove(alfa[index])
					child_pos[index] = 1
				#En caso de que el nodo de la posicion index no se pueda ingresar del alfa,
				#probamos con el beta
				else:

					if beta[index] in deliveries:

						child[index] = beta[index]
						deliveries.remove(beta[index])
						child_pos[index] = 1

					elif beta[index] in pickups:

						child[index] = beta[index]
						pickups.remove(beta[index])
						child_pos[index] = 1

					else:
						#si esa posicion no se pudo ingresar de ningun padre, queda pendiente
						#para ser ocupada por algun nodo restante
						child[index] = -1
						negative_indexes.append(index)
			#Trararemos de copiar de beta primero
			elif action == 2:

				if beta[index] in deliveries:

					child[index] = beta[index]
					deliveries.remove(beta[index])
					child_pos[index] = 1

				elif beta[index] in pickups:

					child[index] = beta[index]
					pickups.remove(beta[index])
					child_pos[index] = 1
				#En caso de que el nodo de la posicion index no se pueda ingresar del beta,
				#probamos con el alfa
				else:

					if alfa[index] in deliveries:

						child[index] = alfa[index]
						deliveries.remove(alfa[index])
						child_pos[index] = 1

					elif alfa[index] in pickups:

						child[index] = alfa[index]
						pickups.remove(alfa[index])
						child_pos[index] = 1
					else:
						#si esa posicion no se pudo ingresar de ningun padre, queda pendiente
						#para ser ocupada por algun nodo restante
						child[index] = -1
						negative_indexes.append(index)
			else:
				pass

	#Una vez que se haya tratado de relizar el crossover, si quedan nodos por asignar
	#se realiza la asignacion en las posiciones vacantes de manera aleatoria
	while deliveries or pickups:

		for i in negative_indexes:
			#decidimos si escogemos para agarrar un delivery o un pick up
			action = randint(1,2)

			if action == 1:

				if deliveries and child_pos[i] == 0:

					nodeId = choice(deliveries)
					child[i] = nodeId
					deliveries.remove(nodeId)
					child_pos[i] = 1

			elif action == 2:

				if pickups and child_pos[i] == 0:

					nodeId = choice(pickups)
					child[i] = nodeId
					pickups.remove(nodeId)
					child_pos[i] = 1
	
	#una vez obtenido el crossover del singleArray, procedemos a generar una solucion de tipo
	#lista de listas y corregimos el oren de los nodos para la regla delivery antes que pickup
	#Agregamos la posicion del ultimo 0 para generar todos los caminos
	indexes.append(routeLen-1)
	routes = [] #Se utiliza para llevar las rutas obtenidas del single array
	deliSize = []#LLeva la cantidad de deliveries que hay presente en cada ruta
	pickSize = []#lleva la cantidad de picks que hay en cada ruta
	beg = 1
	end = 1
	for i in range(0,vehicules):

		#el final de cada ruta sera el control que llevamos en el arreglo indexes mas ariba
		end = indexes[i]
		routes.append([0]+child[beg:end+1])
		beg = end + 1
		routes[i],delis,picks = reorderRoute(routes[i])
		deliSize.append(delis)
		pickSize.append(picks)


	descendent = Solution(routes,[],[],deliSize,pickSize)
	cost = round(descendent.getCost(),2)
	descendent.cost = cost

	return descendent

#Funcion para obtener decendientes generados a traves de una poblacion
def descendentsPob(poblation):

	pob_size = len(poblation)
	descendents = []

	for i in range(0,pob_size):

		father_id = randint(0,pob_size-1)
		mother_id = randint(0,pob_size-1)
		while(father_id == mother_id):
			mother_id = randint(0,pob_size-1)

		father = getSingleArray(poblation[father_id])
		mother = getSingleArray(poblation[mother_id])
		descendents.append(crossover(father,mother))

	return descendents



#Funcion para generar la mutacion en una poblacion
def mutate(poblation):

	global vehicules

	mutated = copy.deepcopy(poblation)
	pob_size = len(poblation)

	i = 0
	for chromo in mutated:

		#decidimos si se debe o no mutar el chromosoma
		action = randint(1,2)

		#Es posible aplicar la mutacion
		if action == 1:

			r1_index = randint(0,vehicules-1)
			#Caso en el caso que se generan soluciones con alguna ruta vacia
			while not(chromo.routes[r1_index]) or len(chromo.routes[r1_index]) <= 2:
				r1_index = randint(0,vehicules-1)

			r2_index = randint(0,vehicules-1)
			#Caso en el caso que se generan soluciones con alguna ruta vacia
			while(r1_index == r2_index or len(chromo.routes[r2_index]) <= 2 ):
				r2_index = randint(0,vehicules-1)


			#Calculamos el inicio y el final de cada subruta que vamos a intercambiar en ambos caminos
			beg_1 = randint(1,len(chromo.routes[r1_index])-2)
			end_1 = randint(1,len(chromo.routes[r1_index])-2)

			if beg_1 > end_1:
				end_1,beg_1 = beg_1,end_1

			beg_2 = randint(1,len(chromo.routes[r2_index])-2)
			end_2 = randint(1,len(chromo.routes[r2_index])-2)

			if beg_2 > end_2:
				end_2,beg_2 = beg_2,end_2

			head1 = chromo.routes[r1_index][0:beg_1]
			midd1 = chromo.routes[r1_index][beg_1:end_1+1]
			tail1 = chromo.routes[r1_index][end_1+1:]

			head2 = chromo.routes[r2_index][0:beg_2]
			midd2 = chromo.routes[r2_index][beg_2:end_2+1]
			tail2 = chromo.routes[r2_index][end_2+1:]

			chromo.routes[r1_index] = head1+midd2+tail1
			chromo.routes[r2_index] = head2+midd1+tail2

			chromo.routes[r1_index],chromo.deliSize[r1_index],chromo.pickSize[r1_index] = reorderRoute(chromo.routes[r1_index])
			chromo.routes[r2_index],chromo.deliSize[r2_index],chromo.pickSize[r2_index] = reorderRoute(chromo.routes[r2_index])
			mutated[i] = chromo
			cost = mutated[i].getCost()
			mutated[i].cost = cost
			i+=1
		else:
			i+=1


	return mutated

#Funcion para determinar si una solucion es valida
def isValid(sol):

	global vehiculeCapacity
	global demandList

	valid = True
	i = 0
	for route in sol.routes:
		demand = 0
		for node in route[sol.deliSize[i]+1:]:
			demand += demandList[node]
		i+=1
		valid = demand <= vehiculeCapacity
		if not valid:
			break
	return valid

#META HEURISTICA DEL ALGORITMO GENETICO

def geneticAlgor(pob_size):

	poblation = []
	tries = 0
	MAX_TRIES = 2000

	upper_Bound = soluciones[sys.argv[1]]
	#Generamos la poblacion inicial
	for i in range(1,pob_size):
		poblation.append(getFirstSol())

	#Aplicacion de algoritmo de seleccion(solo los mejores candidatos son aceptables)
	poblation.sort(key=lambda x: x.cost)
	poblation = poblation[0:(len(poblation)//2)]

	best = poblation[0]

	while True:

		#Genera los nuevos hijos que seran parte de la poblacion
		descendents = descendentsPob(poblation)
		#Expandimos nuevamente la poblacion
		poblation += descendents
		#Generamos una mutacion aleatoria y probabilistica en la poblacion
		poblation = mutate(poblation)
		#Criterios de seleccion para la nueva poblacion
		poblation.sort(key=lambda x: x.cost)
		poblation = poblation[0:(len(poblation)//2)]

		if (poblation[0].cost < best.cost and isValid(poblation[0]) and upper_Bound < poblation[0].cost):

			best = poblation[0]
			tries = 0

		else:
			tries += 1
			if tries == MAX_TRIES:
				break

		if upper_Bound > poblation[0].cost:
			break

		else:
			pass

	return best

#Funcion para crear el contador de feromonas para cada posicion de la solucion en cuestion

#Funcion para reorganizar las hormigas en su mejor posicion
def antsBestPosition(sol):

	return localSearch(sol,5)


def createFeromoneCounter():

	global deliveryNodes
	global pickUpNodes

	totalNodes = [0]+deliveryNodes+pickUpNodes

	#es una lista de la forma [[0,0],[1,0],[2,0]...] donde el segundo elemento de cada tupla sigifica
	#la cantidad de veces que aparece el nodo (cuyo ID es el primer elemento de la tupla) en la posicon
	#actual en la que estemos revisando la solucion
	feromone_list = [0]*len(totalNodes)

	for i in range(0,len(feromone_list)):
		feromone_list[i] = [i,0]

	return feromone_list

#Funcion para obtener el costo de soluciones en forma de arreglo lineal
def getLinealCost(sol):

	global costMatrix

	cost = 0

	for i in range(0,len(sol)-1):

		orig = sol[i]
		dest = sol[i+1]
		cost += costMatrix[orig][dest]

	return [sol,cost]

#FUncion que se encarga de actualizar la cuenta de ocurrencias para cada posicion de la solucion
def actFeromoneCount(route,fer_count):

	#route es una solucion de la forma [0,1,2,3,0,6,7,8,19,11,0,..........,0]
	NODE = 0
	OCCURS = 1
	#fer cout es una lista del mismo tamano que la solucion en donde cada posicion de fer count
	#es una lista para cada posicion de la solucion en donde se almacenan las ocurrencias de todos
	#los nodos para esa posicion, de tal manera que se dese saber cual es la que tiene maor probabilidad
	#para ser asignada en el camino
	for i in range(1,len(route)-1):
		#Obtenemos el identiicador presente en la posicion actual de la ruta
		nodeId = route[i]
		fer_index = 0
		#Para la lista de ocurrencias de esa posicion, buscamos la que tiene como identificador el NODEID
		#y le sumamos 1 a sus ocurrencias
		for tuplet in fer_count[i]:
			if tuplet[NODE] == nodeId:
				tuplet[OCCURS] += 1
				fer_count[i][fer_index] = tuplet
				break
			fer_index += 1

	return fer_count

def createRouteFromFeromone(fer_count):

	global vehicules
	#Cantida de 0 internos que puede tener nuestra tupla
	routes = vehicules - 2
	NODE = 0
	#Fer_count tiene la misma longitu q una solucion, por lo que la solucion generada, sera e la misma logitud
	#de Fer_count
	sol_size = len(fer_count)
	sol = []

	for i in range(1,sol_size-1):

		for tuplet in fer_count[i]:

			if tuplet[NODE] != 0:

				if not(tuplet[NODE] in sol):
					sol.append(tuplet[NODE])
					break

			else:

				pass

	sol = getLinealCost(sol)

	return sol

#Algoritmo colonia de hormigas (paths_size es la cantidad de rutas q hacen las hormigas para esparcir las feromonas)
def antColony(paths_size):

	PATH = 0
	COST = 1
	OCCURS = 1
	best = 0
	tries = 0
	MAX_TRIES = 8

	while True:

		sols = []
		for i in range(0,paths_size):
			sols.append(getFirstSol())
			sols[i] = antsBestPosition(sols[i])
			sols[i] = getLinealCost(getSingleArray(sols[i]))

		#seleccionamos las mejores rutas iniciales para lograr un poco la optimizacion
		sols = sorted(sols,key=lambda x: x[COST])
		sols = sols[0:len(sols)//2]

		#Inicializamos nuestra mejor solucion
		if best == 0:
			best = sols[0]
		if sols[0][COST] < best[COST]:
			best = sols[0]



		#todas las soluciones tienen la misma longitud, por lo que la cadena de feromonas para cada posicion del arreglo,sera
		#del tamano que tenga cualquier solucion (por conveniencia se escoje la primera)
		chain_size = len(sols[0][PATH])

		#Es la lista de listas de feromonas que llevara cada posicion de nuestra solucion final
		#Si la solucion es por ejemplo [0,1,3,4,0,7,5,28,0,11,12,13,14,15,0,20,0] cada posicion desde ID 1 hasta ID 20
		#tendra su ocurrencias de feromonas gracias a feromone_occur[indice_de_la_posicion]
		feromone_occur = []
		#La posicion inicial y final de nuestra solucion no debe tener cadena de feromonas puesto que son posiciones
		#inmutables
		for i in range(0,chain_size):
			if i == 0 or (i == chain_size-1):
				feromone_occur.append([])
			else:
				feromone_occur.append(createFeromoneCounter())

		#Para cada solucion, procedemos a actualizar la linea de feromonas para cada posicion de la ruta
		for sol in sols:
			feromone_occur = actFeromoneCount(sol[PATH],feromone_occur)

		#Organizamos la lista de tuplas de cada posicion para determinar cuales obtuvieron mayor recurrencia en las feromonas
		i = 0
		for tupleList in feromone_occur:
			feromone_occur[i] = sorted(feromone_occur[i],key=lambda x: x[OCCURS],reverse=True)
			i+=1

		#Generamos el mejor camino posible creado por el rastro de feromonas
		candidate = createRouteFromFeromone(feromone_occur)
		
		if candidate[COST] < best[COST]:
			best = candidate
			tries = 0

		else:

			tries += 1
			if(tries == MAX_TRIES):
				break

	return best


def main():


	instance    = "dataset/%s.xml" % (sys.argv[1])
	bestKnown   = soluciones[sys.argv[1]]
	printOption = int(sys.argv[2])
	parser(instance)
	getCostMatrix()

	ils_sols = []
	ils_time = []
	ils_errs = []
	gen_sols = []
	gen_time = []
	gen_errs = []
	ant_sols = []
	ant_time = []
	ant_errs = []

	for i in range(0,1):

		t_start = time()
		ilSol = ILS()
		t_end = time()
		ils_sols.append(round(ilSol.getCost(),1))
		ils_time.append(t_end - t_start)
		error = ((bestKnown - ilSol.getCost())/bestKnown)*100
		ils_errs.append(abs(round(error,2)))

		t_start = time()
		geSol = geneticAlgor(100)
		t_end = time()
		gen_sols.append(geSol.cost)
		gen_time.append(t_end - t_start)
		error = ((bestKnown - geSol.cost)/bestKnown)*100
		gen_errs.append(abs(round(error,2)))

		t_start = time()
		atSol = antColony(10)
		t_end = time()
		ant_sols.append(atSol[1])
		ant_time.append(t_end - t_start)
		error = ((bestKnown - atSol[1])/bestKnown)*100
		ant_errs.append(abs(round(error,2)))



	ils_sols.sort(key=lambda x: x)
	best_ils = round(ils_sols[0],2)

	prom_tils = 0.0
	for t in ils_time:
		prom_tils += t
	prom_tils = round(prom_tils/len(ils_time),2)

	prom_eils = 0.0
	for e in ils_errs:
		prom_eils += e
	prom_eils  =  round(prom_eils/len(ils_errs),2)

	gen_sols.sort(key=lambda x: x)
	best_gen = round(gen_sols[0],2)

	prom_tgen = 0.0
	for t in gen_time:
		prom_tgen += t
	prom_tgen = round(prom_tgen/len(gen_time),2)

	prom_egen = 0.0
	for e in gen_errs:
		prom_egen += e
	prom_egen = round(prom_egen/len(gen_errs),2)

	ant_sols.sort(key=lambda x: x)
	best_ant = round(ant_sols[0],2)

	prom_tant = 0.0
	for t in ant_time:
		prom_tant += t
	prom_tant = round(prom_tant/len(ant_time),2)

	prom_eant = 0.0
	for e in ant_errs:
		prom_eant += e
	prom_eant = round(prom_eant/len(ant_errs),2)

	if printOption == 1:

		print("Instancia: %s" % (sys.argv[1]))
		print()
		print("Mejor Conocido:  %s" % bestKnown)
		print()
		print("Mejor ILS:       %s" % best_ils)
		print("Tiempo Promedio: %s segs" % prom_tils)
		print("Error Promedio:  %s " % prom_eils)
		print()
		print("Mejor Genetio:   %s" % best_gen)
		print("Tiempo Promedio: %s segs" % prom_tgen)
		print("Error Promedio:  %s" % prom_egen)
		print()
		print("Mejor Colonia:   %s" % best_ant)
		print("Tiempo Promedio: %s segs" % prom_tant)
		print("Error Promedio:  %s" % prom_eant)

	elif printOption == 2:

		print("Instancia: %s" % (sys.argv[1]))
		print()
		print("Resultados")
		print()
		print("Mejor Conocido     Mejor ILS        Tiempo         Error     Mejor GEN        Tiempo         Error")
		#Espaciacion (14 - 13 - 13 - 13 - 13 - 13 -13)
		print("%14.1f %13.1f %13.1f %13.1f %13.1f %13.1f %13.1f" % (bestKnown,best_ils,prom_tils,prom_eils,best_gen,prom_tgen,prom_egen))

	else:

		print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (bestKnown,best_ils,prom_tils,prom_eils,best_gen,prom_tgen,prom_egen,best_ant,prom_tant,prom_eant))





if __name__ == "__main__":
    main()
