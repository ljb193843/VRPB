from xml.dom import minidom
from operator import attrgetter
from random import randint,choice
from time import perf_counter as pctime

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

#Clase para albergar una solucion obtenida
class Solution:

    def __init__(self,routes,deliDemands,pickDemands,deliSize,pickSize):
        self.routes = routes #Rutas de la solucion
        self.deliDemands = deliDemands #Demanda de los nodos delivery para cada ruta
        self.pickDemands = pickDemands #Demanda de los nodos pickup para cada ruta
        self.deliSize = deliSize #Cantidad de nodos de tipo deliverie en la ruta
        self.pickSize = pickSize #Cantidad de nodos de tipo pick up en la ruta

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
    for i in range(0,vehicules-1):
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

    return Solution(routes,deliDemands,pickDemands,delisInPath,picksInPath)

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

    global vehiculeCapacity
    global vehicules
    global demandList

    perturbed = copy.deepcopy(sol)

    while True:

        #Ubicamos de que ruta vamos a eliminar al nodo
        r1_index = randint(0,vehicules-1)
        while perturbed.deliSize[r1_index] == 0:
            r1_index = randint(0,vehicules-1)

        r2_index = r1_index
        #Ubicamos la ruta en la que se va a agregar el nodo
        while(r2_index == r1_index):
            r2_index = randint(0,vehicules-1)
            #si la segunda ruta no tiene deliveries para intercambiar, seguimos buscando
            while perturbed.deliSize[r2_index] == 0:
                r2_index = randint(0,vehicules-1)

        #Ubicamos la posicion del nodo que vamos a eliminar
        n1_index = randint(1,perturbed.deliSize[r1_index])
        #Obtenemos el identificador del nodo
        n1Id = perturbed.routes[r1_index][n1_index]

        #Si es factible la introduccion:
        if (perturbed.deliDemands[r2_index] - demandList[n1Id] >= 0):

            #Instrucciones para el camino a expandir
        	perturbed.deliDemands[r2_index] -= demandList[n1Id]
        	perturbed.deliSize[r2_index] += 1
        	aux1 = perturbed.routes[r2_index][0:perturbed.deliSize[r2_index]]
        	aux2 = perturbed.routes[r2_index][perturbed.deliSize[r2_index]:]
        	aux1.append(n1Id)
        	perturbed.routes[r2_index] = aux1+aux2
        	#Instrucciones para el camino a recortar
        	perturbed.routes[r1_index].remove(n1Id)
        	perturbed.deliSize[r1_index] -= 1

        	return perturbed

        #Una vez realizado el cambio, para cada ruta, procedemos a intercambiar o no 2 nodos
        '''for i in range(0,vehicules-1):

            delis  = perturbed.deliSize[i]
            picks  = perturbed.pickSize[i]
            alter1 = randint(0,1)
            alter2 = randint(0,1)
            #verificamos si es posible hacer un cambio en los delivery
            if delis >= 2 and alter1 == 1:
                d1_index = randint(1,delis)
                d2_index = randint(1,delis)
                while(d1_index == d2_index):
                    d2_index = randint(1,delis)
                perturbed.routes[i][d1_index],perturbed.routes[i][d2_index] = perturbed.routes[i][d2_index],perturbed.routes[i][d1_index]
            #verificamos si es posible hacer un cambio en los pickups
            if picks >= 2 and alter2 == 1:
                d1_index = randint(delis+1,delis+picks)
                d2_index = randint(delis+1,delis+picks)
                while(d1_index == d2_index):
                    d2_index = randint(delis+1,delis+picks)
                perturbed.routes[i][d1_index],perturbed.routes[i][d2_index] = perturbed.routes[i][d2_index],perturbed.routes[i][d1_index]'''

def perturbate2(sol):

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

        	#Ubicamos de que ruta vamos a eliminar al nodo
			r1_index = randint(0,vehicules-1)
			while perturbed.deliSize[r1_index] == 0:
				r1_index = randint(0,vehicules-1)

			r2_index = r1_index
        	#	bicamos la ruta en la que se va a agregar el nodo
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

				print("PERMUTE DELIVERIES")
				return perturbed

		elif action == 2:
			#Ubicamos de que ruta vamos a eliminar al nodo
			r1_index = randint(0,vehicules-1)
			while perturbed.pickSize[r1_index] == 0:
				r1_index = randint(0,vehicules-1)

			r2_index = r1_index
        	#	bicamos la ruta en la que se va a agregar el nodo
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

				print("PERMUTE PICKUPS")
				return perturbed

		else:
			pass




def ILS(sol):

    tries = 0
    MAX_TRIES = 6

    bestSol = localSearch(sol,MAX_TRIES)
    print("Resultado de busqueda local: %s" % (bestSol.getCost()))

    while True:
        candidate = perturbate2(bestSol)
        candidate = localSearch(candidate,15)
        if(candidate.getCost() < bestSol.getCost()):
            bestSol = candidate
            print(bestSol.getCost())
            tries = 0
        print(tries)
        tries += 1
        if (tries == MAX_TRIES):
            return bestSol




def main():
    instance  = "dataset/%s.xml" % (sys.argv[1])
    parser(instance)
    getCostMatrix()

    s0 = getFirstSol()
    print("Solucion Inicial")
    for route in s0.routes:
        print("Ruta: %s" % route)
    print("Costo: %s" % s0.getCost())

    sils = ILS(s0)
    print("Solucion ILS")
    for route in sils.routes:
        print("Ruta: %s" % route)
    print("Costo: %s" % sils.getCost())


if __name__ == "__main__":
    main()
