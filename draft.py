# -*- coding: utf-8 -*-
# Indiana pipelines map (1980):
# https://maps.indiana.edu/ArcGIS/rest/services/Infrastructure/Energy_Pipelines_Oil_Gas/MapServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json
class Node():
    def __init__(self, name):
        self.name = name
        self.adjList = {}
    
    def add_neighbor(self, neighbor, capacity):
        if isinstance(neighbor, Node):
            if neighbor not in self.adjList:
                self.adjList[neighbor] = capacity
                neighbor.adjList[self] = capacity
            else:
                return False
        
    def print_adjList(self):
        for neighbor in self.adjList.keys():
            print('\t-->', neighbor, '(' + str(self.adjList[neighbor]) + ')')
    
    def __str__(self):
        return self.name
    

class Graph():
    def __init__(self):
        self.nodes = []
        
    def add_node(self, node):
        if isinstance(node, Node):
            if node not in self.nodes:
                self.nodes.append(node)
                for neighbor in node.adjList:
                    self.nodes.append(neighbor)
            else:
                return False
    
    def print_nodes(self):
        for node in self.nodes:
            print(node)
            
    def print_graph(self):
        for node in self.nodes:
            print(node)
            node.print_adjList()
        
        
        
n1 = Node('a node')
n2 = Node('another node')
n3 = Node('a third node')
n1.add_neighbor(n2, 4)
n1.add_neighbor(n3, 5)

G = Graph()
G.add_node(n1)
G.print_nodes()
G.print_graph()
