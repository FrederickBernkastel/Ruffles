"""
    README
    Avoid reloading modules in Spyder
        Go to Tools -> Preferences -> Python Interpreter; uncheck UMR
    Dependencies
        csv
        datetime
        numpy
    Requirements
        POS.py file
        .csv file with processed articles
"""
"""
    Constants definition
"""
DEBUG = False
FILE_NAME = "Search Data.csv"
FILE_ENCODING = "UTF-8-sig"
RECENT_DAYS = 30
DATA_NUM_OF_COLS = 5
STARTING_ENERGY = 10000
THRESHOLD = 1
DEGREE_INCREMENT = .1

"""
    Search
"""
import POS
import csv
import numpy as np
from datetime import date
"""
    Notes
    adj_l links to (weight,Node)
    node_d links to {key:Node}
"""
class Node:
    def __init__(self,key,dateCreated, isDocument):
        self.adj_l = []
        self.key = key
        self.dateCreated = dateCreated
        self.isDocument = isDocument
        
    def isSingleton(self):
        return not self.isDocument and len(self.adj_l)==1
    
    def update(self,adjNode,weight):
        self.adj_l.append((weight,adjNode))
        
    def __str__(self):
        return "Node %s"%(self.key) if self.isDocument else "Node %s"%(self.key[0])
    
class Graph:
    def __init__(
            self,
            dataNumOfCols = DATA_NUM_OF_COLS,
            recentDays = RECENT_DAYS
            ):
        self.node_d = {}
        self.dataNumOfCols = dataNumOfCols
        self.recentDays = recentDays
        
    # Creates graph of nodes
    def processNodes(self,csvFile,csvReader):
        # Extract weights for softmax
        self.art_weight_d = {}
        prev_art = ""
        curr_weight_l = []
        for row in csvReader:
            if row[3] != prev_art:
                if prev_art != "":
                    self.art_weight_d[prev_art] = np.sum(np.exp(curr_weight_l))
                curr_weight_l = [int(row[2])]
                prev_art = row[3]
            else:
                curr_weight_l.append(int(row[2]))
        self.art_weight_d[prev_art] = np.max(np.exp(curr_weight_l))
        
        csvFile.seek(0)
        for row in csvReader:
            self.__processNode(row)
            
        # Sorts all adjacent nodes for every node (for faster search traversal)
        self.__postProcessNodes()
        
        
        
    # Factory method to create / update a single Node
    def __processNode(self,row_l):
        if len(row_l) != self.dataNumOfCols:
            raise Exception("Unknown file format with wrong number of columns")
        word,tag,weight,link,dateCreated = row_l
        # pre-process data
        dateCreated = [int(item) for item in dateCreated.split("/")]
        dateCreated = date(dateCreated[2],dateCreated[1],dateCreated[0])
        
        # Check if dateCreated is recent
        if (dateCreated - date.today()).days > self.recentDays:
            return None
        
        # Reference node
        try:
            wordNode = self.node_d[(word,tag)]
        except:
            wordNode = Node((word,tag),dateCreated,isDocument = False)
            self.node_d[(word,tag)] = wordNode
        try:
            documentNode = self.node_d[link]
        except:
            documentNode = Node(link,dateCreated,isDocument = True)
            self.node_d[link] = documentNode
        weight = np.exp(int(weight)) / self.art_weight_d[documentNode.key]
        wordNode.update(documentNode,weight)
        documentNode.update(wordNode,weight)
        

    

        
    
    # Function to search graph using Contextual Network Search
    # This graph only returns the most likely known document, and additional checks on the content is required
    # If there are two equally likely documents, one is returned at random
    """
        his_set = (Node1,Node2)
        energy_dic = {Node1:energy_val,..}
    """
    def search(self, 
               searchStr, 
               Es = STARTING_ENERGY, 
               threshold = THRESHOLD, 
               degreeIncrement = DEGREE_INCREMENT
               ):
        search_tags = POS.POS(searchStr)
        self.energy_dic = {}
        self.threshold = threshold
        self.degreeIncrement = degreeIncrement
        
        for (word,tag),multiplier in search_tags.items():
            try:
                start_node = self.node_d[(word,tag)]
            except:
                # Continues if word,tag combination is unknown
                continue
            self.multiplier = multiplier
            self.his_set=set([])
            self.__energize(Es,start_node)
        return max(self.energy_dic, key=self.energy_dic.get)
    
    # Function to update energy graph for a single word
    def __energize(self,energy, curr_node,degree=1):
        print("%s %.5f"%(curr_node,energy))
        if curr_node.isDocument:
            try:
                self.energy_dic[curr_node] += energy * self.multiplier
            except:
                self.energy_dic[curr_node] = energy * self.multiplier

        # degree reduces weight with distance
        energy /= degree
        degree += self.degreeIncrement
        self.his_set.add(curr_node)
        
        for weight, adj_node in curr_node.adj_l:
            if adj_node in self.his_set or adj_node.isSingleton():
                continue
            weighted_energy = weight * energy
            if weighted_energy < self.threshold:
                break
            self.__energize(weighted_energy,adj_node,degree)
                           
    """
procedure energize(energy E, node nk){
        energy(Nk) := energy(nk) + E
        E' := E / degree of nk
        if (E' > T) {
                for each node Nj in Nk:
                    E'' := E' * Ejk
                    energize(E'',Nj)
        }
}
Nk          Set of all neghibour nodes of nk
T           Constant threshold value
energy      Data structure holding energy values

     """
    # Sorts adjacent nodes based on their weight
    def __postProcessNodes(self):
        for node in self.node_d.values():
            node.adj_l.sort(key=lambda x:x[0],reverse=True)
            
    def __str__(self):
        out_str = []
        for node in self.node_d.values():
            out_str.append(node.key if node.isDocument else "%s %s"%(node.key[0],node.key[1]))
            #out_str.append("\tis Singleton" if node.isSingleton() else "\tnot Singleton")
            out_str.append("\tis Document" if node.isDocument else "\tnot Document")
            out_str.append("\tAdjacent Nodes:")
            for weight,adj_node in node.adj_l:
                out_str.append("\t\t%s \n\t\t\t%.5f"%(adj_node.key,weight))
        
        return "\n".join(out_str)
        
        
def load_csv(f = FILE_NAME,enc = FILE_ENCODING):
    with open(f, encoding = enc) as csvFile:
        csvReader = csv.reader(csvFile)
        graph = Graph()
        graph.processNodes(csvFile,csvReader)
    if DEBUG:
        print(graph)
    return graph
        


    

g = load_csv()
print("returned " + str(g.search("fox hunting brown hens")))










