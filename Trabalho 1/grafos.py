from collections import defaultdict
import sys

class UndirectedGraph:

    def __init__(self, vertex):
        self.vertex = vertex
        self.graph = defaultdict(list)
        self.time = 0

    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def __AP_Bridges_Mod(self, u, visited, parent, low, discovered, articulation_points, bridges):
        children = 0
        visited[u] = True
        discovered[u] = self.time
        low[u] = self.time
        self.time += 1

        for v in self.graph[u]:
            if visited[v] == False:
                parent[v] = u
                children += 1
                self.__AP_Bridges_Mod(v, visited, parent, low, discovered, articulation_points, bridges)
                low[u] = min(low[u], low[v])

                if parent[u] == -1 and children > 1:
                    if (u not in articulation_points):
                        articulation_points.append(u)
                
                if parent[u] != -1 and low[v] >= discovered[u]:
                    if (u not in articulation_points):
                        articulation_points.append(u)

                if low[v] > discovered[u]:
                    bridges.append([u, v])

            elif v != parent[u]:
                low[u] = min(low[u], discovered[v])

    def __AP_Bridges(self):
        visited = [False] * (self.vertex + 1)
        discovered = [int] * (self.vertex + 1)
        low = [int] * (self.vertex + 1)
        parent = [-1] * (self.vertex + 1)
        articulation_points = []
        bridges = []

        for i in range(self.vertex):
            if visited[i] == False:
                self.__AP_Bridges_Mod(i, visited, parent, low, discovered, articulation_points, bridges)

        return articulation_points, bridges

    def solve(self):
        articulation_points, bridges = self.__AP_Bridges()

        print("\nPontos de Articulação")
        for i in range(len(articulation_points)):
            print(articulation_points[i])
        
        print("\nPontes")
        for i in range(len(bridges)):
            print(bridges[i])

class DirectedGraph():

    def __init__(self, vertex):
        self.vertex = vertex
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def __DFSUtil(self, v, visited, stackTopological, index, sccList):
        visited[v] = True
        sccList[index].append(v)
        for i in self.graph[v]:
            if visited[i] == False:
                self.__DFSUtil(i, visited, stackTopological, index, sccList)
        stackTopological.append(v)
        
    def __DFSCycle(self, u, color):
        color[u] = "gray"
        
        for i in self.graph[u]:
            if color[i] == "gray":
                return True
            
            if color[i] == "white" and self.__DFSCycle(i, color) == True:
                return True

        color[u] = "black"
        return False

    def __fillOrder(self, v, visited, stack):
        visited[v] = True
        for i in self.graph[v]:
            if visited[i] == False:
                self.__fillOrder(i, visited, stack)
        stack = stack.append(v)

    def __getTranspose(self):
        g = DirectedGraph(self)

        for i in self.graph:
            for j in self.graph[i]:
                g.addEdge(j, i)
        return g

    def __isCyclic(self):
        color = ["white"] * (self.vertex + 1)
        for i in range(self.vertex):
            if color[i] == "white":
                if self.__DFSCycle(i, color) == True:
                    return True
        return False

    def __StronglyConnectedComponents(self):
        stack = []
        stackTopological = []
        sccList = defaultdict(list)
        visited = [False] * (self.vertex + 1)
        index = 0

        for i in range(self.vertex):
            if visited[i] == False:
                self.__fillOrder(i, visited, stack)

        gr = self.__getTranspose()
        visited = [False] * (self.vertex + 1)

        while stack:
            i = stack.pop()
            if visited[i] == False:
                gr.__DFSUtil(i, visited, stackTopological, index, sccList)
                index += 1
            
        if(self.__isCyclic() == True):
            return True, sccList, None
        else:
            return False, sccList, stackTopological
    
    def solve(self):
        cyclic, sccList, stackTopological = self.__StronglyConnectedComponents()
        print("Componentes Fortemente Conexos")
        for i in sccList:
            if (0 not in sccList[i]):
                print(sccList[i])
        if cyclic == True:   
            print("\nO grafo possui ciclo(s), portanto não é possível gerar uma ordenação topológica")
        else:
            print("\nExemplo de ordenação topológica")
            if 0 in stackTopological: stackTopological.remove(0)
            print(stackTopological)

if(len(sys.argv)) < 3:
    print("Número incorreto de argumentos")
    print("Modo de uso:")
    print("$ %s (--dig|--undig) nome_arquivo.txt" %(sys.argv[0]))
elif sys.argv[1] == "--dig":
    file = open(sys.argv[2], "r")
    infos = file.readline()
    infos = infos.split(" ")
    g = DirectedGraph(int(infos[0]))

    for line in file:
        args = line.split(" ")
        g.addEdge(int(args[0]), int(args[1]))
    g.solve()

elif sys.argv[1] == "--undig":
    file = open(sys.argv[2], "r")
    infos = file.readline()
    infos = infos.split(" ")
    g = UndirectedGraph(int(infos[0]))

    for line in file:
        args = line.split(" ")
        g.addEdge(int(args[0]), int(args[1]))
    g.solve()