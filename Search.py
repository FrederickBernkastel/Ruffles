"""
    README
    Avoid reloading modules in Spyder
        Go to Tools -> Preferences -> Python Interpreter; uncheck UMR
    Dependencies
        csv
        datetime
    Requirements
        POS.py file
        .csv file with processed articles
"""
"""
    Constants definition
"""
DEBUG = True
FILE_NAME = "Search Data.csv"
FILE_ENCODING = "UTF-8-sig"
RECENT_DAYS = 30
DATA_NUM_OF_COLS = 5

"""
    Search
"""
import POS
import csv
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
    
class Graph:
    def __init__(self):
        self.node_d = {}
        
    # Creates graph of nodes
    def processNodes(self,csvReader):
        for row in csvReader:
            self.__processNode(row)
        # Sorts all adjacent nodes for every node, for faster search traversal
        self.__sortAllAdj()
        
    # Factory method to create / update a single Node
    def __processNode(self,row_l):
        if len(row_l) != DATA_NUM_OF_COLS:
            raise Exception("Unknown file format with wrong number of columns")
        word,tag,weight,link,dateCreated = row_l
        dateCreated = [int(item) for item in dateCreated.split("/")]
        dateCreated = date(dateCreated[2],dateCreated[1],dateCreated[0])
        # Check if dateCreated is recent
        if (dateCreated - date.today()).days > RECENT_DAYS:
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
        wordNode.update(documentNode,weight)
        documentNode.update(wordNode,weight)
        

    # Sorts adjacent nodes based on their weight
    def __sortAllAdj(self):
        for node in self.node_d.values():
            node.adj_l.sort(key=lambda x:x[0],reverse=True)
            
    def __str__(self):
        out_str = []
        for node in self.node_d.values():
            out_str.append(node.key if node.isDocument else "%s %s"%(node.key[0],node.key[1]))
            singleton_str = "\tis Singleton" if node.isSingleton() else "\tnot Singleton"
            out_str.append("%s"%(singleton_str))
            out_str.append("\tAdjacent Nodes:")
            for weight,adj_node in node.adj_l:
                out_str.append("\t\t%s \n\t\t\t%s"%(adj_node.key,weight))
        
        return "\n".join(out_str)
        
        
def load_csv(f=FILE_NAME):
    with open(f, encoding=FILE_ENCODING) as csvFile:
        csvReader = csv.reader(csvFile)
        graph = Graph()
        graph.processNodes(csvReader)
    if DEBUG:
        print(graph)
    return graph
        
#TODO: Search function
def search(searchStr, depth=4):
    search_tags = POS.POS(searchStr)
    
search("testing the test string tests")
load_csv()











