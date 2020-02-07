from collections import defaultdict
from math import sqrt
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import sys

CONST_XYAXIS = -2
CONST_YXAXIS = 20
CONST_GRID_DIST = 2
fig = ax = None
labeled = False

class Graph:

    def __init__(self, vertex):
        self.vertex = vertex
        self.graph = []
        self.MST = [[] for i in range(vertex)]

    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])
    
    def addEdgeMST(self, u, v):
        self.MST[u].append(v)
        self.MST[v].append(u)
    
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])
    
    def union(self, parent, rank, x, y):
        x_r = self.find(parent, x)
        y_r = self.find(parent, y)

        if rank[x_r] < rank[y_r]:
            parent[x_r] = y_r
        elif rank[x_r] > rank[y_r]:
            parent[y_r] = x_r
        else:
            parent[y_r] = x_r
            rank[x_r] += 1
    
    def KruskalAlgorithm(self):
        result = []
        i = 0
        j = 0

        self.graph = sorted(self.graph, key = lambda item: item[2])
        parent = []
        rank = []

        for node in range (self.vertex):
            parent.append(node)
            rank.append(0)
        
        while j < self.vertex - 1:
            u, v, w = self.graph[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            if x != y:
                j += 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
        
        return result
    
    def DFSMod(self, temp, v, visited):
        visited[v] = True
        temp.append(v + 1)

        for i in self.MST[v]:
            if visited[i] == False:
                temp = self.DFSMod(temp, i, visited)
        
        return temp
    
    def connectComponents(self):
        visited = []
        connectedComponents = []
        for _ in range (self.vertex):
            visited.append(False)
        for v in range (self.vertex):
            if visited[v] == False:
                temp = []
                connectedComponents.append(self.DFSMod(temp, v, visited))
        return connectedComponents

def graphicalRepresentation(vertex_list, connectedComponents):
    global fig, ax
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    fig, ax = plt.subplots()
    fig.canvas.set_window_title('K-Clustering')
    ax.set_xlim([CONST_XYAXIS, CONST_YXAXIS])
    ax.set_ylim([CONST_XYAXIS, CONST_YXAXIS])
    ax.set_aspect('equal')

    major_ticks = np.arange(CONST_XYAXIS, CONST_YXAXIS + 1, CONST_GRID_DIST)
    minor_ticks = np.arange(CONST_XYAXIS, CONST_YXAXIS + 1, CONST_GRID_DIST)
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)
    ax.grid(which='both', alpha=0.4)

    for i in range (0, len(connectedComponents)):
        for j in range (0, len(connectedComponents[i])):
            # print(i, j)
            element = connectedComponents[i][j] - 1
            x = vertex_list[element][0]
            y = vertex_list[element][1]
            if labeled:
                ax.annotate(element + 1, xy=(x + 0.2, y + 0.2), fontsize=6)
            vertex = plt.Circle((x, y), 0.1, color=colors[i])  # Plota o centro
            ax.add_patch(vertex)

    fig.canvas.draw()

def distanceBetweenPoints(p1, p2):
    aux = p1[0] - p2[0]
    aux2 = p1[1] - p2[1]
    aux3 = (aux * aux) + (aux2 * aux2)
    return sqrt(aux3)

def main():
    global labeled
    if(len(sys.argv)) < 2:
        print("Número incorreto de argumentos")
        print("Modo de uso:")
        print("$ %s nome_arquivo.txt" % (sys.argv[0]))
    else:
        file = open(sys.argv[1], "r")
        infos = file.readline().split(" ")
        g = Graph(int(infos[0]))
        vertex_number = int(infos[0])
        k = int(infos[1])
        vertex = []

    for line in file:
        args = line.split(" ")
        vertex.append([int(args[0]), int(args[1])])

    for i in range(0, vertex_number):
        for j in range(i + 1, vertex_number):
            p1 = [vertex[i][0], vertex[i][1]]
            p2 = [vertex[j][0], vertex[j][1]]
            g.addEdge(i, j, distanceBetweenPoints(p1, p2))

    result = g.KruskalAlgorithm()
    print(result)
    for i in range (0, len(result)):
        print("Aresta: ", i + 1, "U => " , vertex[result[i][0]] , " - V => " , vertex[result[i][1]])
    for i in range(0, k-1):
        result.pop()

    for i in range (0, len(result)):
        g.addEdgeMST(result[i][0], result[i][1])

    cc = g.connectComponents()

    for i in range (len(cc)):
        cc[i].sort()
    cc.sort()

    if (len(sys.argv) == 2) or (sys.argv[2] == "-command_line"):
        # print(cc)
        ababa = 2
    elif sys.argv[2] == "-graphical":
        if (len(sys.argv) > 3) and (sys.argv[3] == "-labeled"):
            labeled = True
        graphicalRepresentation(vertex, cc)
    
        plt.xlabel('X Axis')
        plt.ylabel('Y Axis')
        plt.grid()
        plt.show()

if __name__ == '__main__':
    main()