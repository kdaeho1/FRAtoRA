import graphviz
import pydot
#import networkx as nx
import pygraphviz as pgv
import xml.etree.ElementTree as ET
#import matplotlib.pyplot as plt


graphs = pydot.graph_from_dot_file('file.dot')
# print(len(graphs))
# print(type(graphs))
graph = graphs[0]

#print(type(graph))
#graphs type list, graph type pydot.Dot
#graph successfully imported

#N = nx.MultiDiGraph()
#N = nx.nx_pydot.from_pydot(graph)
# a = N.number_of_edges()
# print(a)
# b = N.number_of_nodes()
# print(b)
# print(list(N.nodes))
# str = list(N.nodes)
# print(str)
#networkx graph created
#networkx edges = transitions, networkx nodes = statesimport graphviz
import pydot
#import networkx as nx
import pygraphviz as pgv
import xml.etree.ElementTree as ET
import xml.dom.minidom as md
#import matplotlib.pyplot as plt
import re


class Mapper:
    def __init__(self):
        self.regI = 4
        
    def read_file(self):
        self.graphs = pydot.graph_from_dot_file('file.dot')
        self.graph = self.graphs[0]
        self.edge = self.graph.get_edge_list()
        self.node = self.graph.get_node_list()

    def initialize(self):
        root = ET.Element('register-automaton', {})
        #register-atuomaton
        alphabet = ET.SubElement(root, 'alphabet', {})
        inputs = ET.SubElement(alphabet, 'inputs', {})
        symbol = ET.SubElement(inputs, 'symbol', {"name" : "ILoadRegisters"})
        symbol = ET.SubElement(inputs, 'symbol', {"name" : "IDummy"})
        symbol = ET.SubElement(inputs, 'symbol', {"name" : "IKnownInput"})
        param = ET.SubElement(symbol, 'param', {"type" : "int", "name":"p0"})
        param = ET.SubElement(symbol, 'param', {"type" : "int", "name":"p1"})
        symbol = ET.SubElement(inputs, 'symbol', {"name" : "IKnownOutput"})
        param = ET.SubElement(symbol, 'param', {"type" : "int", "name":"p0"})
        param = ET.SubElement(symbol, 'param', {"type" : "int", "name":"p1"})
        symbol = ET.SubElement(inputs, 'symbol', {"name" : "IFreshInput"})
        param = ET.SubElement(symbol, 'param', {"type" : "int", "name":"p0"})
        param = ET.SubElement(symbol, 'param', {"type" : "int", "name":"p1"})
        symbol = ET.SubElement(inputs, 'symbol', {"name" : "IFreshOutput"})
        param = ET.SubElement(symbol, 'param', {"type" : "int", "name":"p0"})
        param = ET.SubElement(symbol, 'param', {"type" : "int", "name":"p1"})
        outputs = ET.SubElement(alphabet, 'outputs', {})
        symbol = ET.SubElement(inputs, 'symbol', {"name" : "OFreshOutput"})
        param = ET.SubElement(symbol, 'param', {"type":"int", "name":"out"})
        symbol = ET.SubElement(outputs, 'symbol', {"name" : "OOK"})
        #alphabet

        constants = ET.SubElement(root, 'constants', {})
        constants.text = "const int zero = 0"
        #constants

        globals = ET.SubElement(root, 'globals', {})
        for i in range(self.regI):
            variable = ET.SubElement(globals, 'variable', {"type" : "int", "name" : "r" + str(i+1)})
            variable.text="0"
        variable = ET.SubElement(globals, 'variable',{"type" : "int", "name" : "x"})
        variable.text="0"
        variable = ET.SubElement(globals, 'variable',{"type" : "int", "name" : "y"})
        variable.text="0"
        #globals
        locations = ET.SubElement(root, 'locations', {})
        for i in self.node:
            parseStr = str(i).split("s")
            idStr = parseStr[1].split("[")
            location = ET.SubElement(locations, 'location', {"name" : "id" + idStr[0].strip()})
        #locations
        init = ET.SubElement(locations, 'location', {"name" : "id10000", "initial" : "true"})
        #initial location
        return root
        #return root node of mapper

    def load(self):
        transition = ET.SubElement(transitions, 'transition', {"from" : "id10000", "to" : "id0", "symbol" : "ILoadRegisters"})
        assignments = ET.SubElement(transition, 'assignments', {})
        for i in range(self.regI):
            assign = ET.SubElement(assignments, 'assign', {"to" : "r"+str(i+1)})
            assign.text = "0"
        transition = ET.SubElement(transitions, 'transition', {"from" : "id0", "to" : "id10000", "symbol" : "OOK"})


    def dummy(self):
        count = 0
        for i in range(len(self.node)):
            for j in self.edge :
                if i == int(str(j)[1]):
                    count = count + 1

            if count == 0:
                transition = ET.SubElement(transitions, 'transition', {"from" : "id"+str(i), "to" : "id"+str(i), "symbol" : "IDummy"})
            count = 0

    def freshInputTransition(self, source, target, first, second):
        transition = ET.SubElement(transitions, 'transition', {"from" : "id"+source, "to" : "id"+target, "symbol" : "IFreshInput", "params" : "x,y"})
        guard = ET.SubElement(transition, 'guard')
        guard.text = "x==r"+first
        assignments = ET.SubElement(transition, 'assignments', {})
        assign = ET.SubElement(assignments, 'assign', {"to" : "r"+second})
        assign.text = "y"
        transition = ET.SubElement(transitions, 'transition', {"from" : "id"+target, "to" : "id"+source, "symbol" : "OOK"})
    
    def freshOutputTransition(self, source, target, first, second):
        transition = ET.SubElement(transitions, 'transition', {"from" : "id"+source, "to" : "id"+target, "symbol" : "IFreshOutput", "params" : "x,y"})
        guard = ET.SubElement(transition, 'guard')
        guard.text = "x==r"+first
        assignments = ET.SubElement(transition, 'assignments', {})
        assign = ET.SubElement(assignments, 'assign', {"to" : "r"+second})
        assign.text = "y"
        transition = ET.SubElement(transitions, 'transition', {"from" : "id"+target, "to" : "id"+source, "symbol" : "OFreshOutput", "params" : "r"+second})

    def knownTransition(self, source, target, first, second):
        if first[-1] == "'":
            transition = ET.SubElement(transitions, 'transition', {"from" : "id"+source, "to" : "id"+target, "symbol" : "IKnownOutput", "params" : "x,y"})
        else:
            transition = ET.SubElement(transitions, 'transition', {"from" : "id"+source, "to" : "id"+target, "symbol" : "IKnownInput", "params" : "x,y"})
        guard = ET.SubElement(transition, 'guard')
        guard.text = "x==r"+first+" && y==r"+second
        transition = ET.SubElement(transitions, 'transition', {"from" : "id"+target, "to" : "id"+source, "symbol" : "OOK"})

    def findTransition(self, source, target, first, second):
        if second[-1]=="●":
            self.freshInputTransition(source, target, first, second.replace("●",""))
        elif second[-1]=="⊛":
            self.freshOutputTransition(source, target, first.replace("'",""), second.replace("⊛",""))
        else:
            self.knownTransition(source, target, first.replace("'",""), second)

    def traverse(self):
        # traverse transitions list
        for i in self.edge:
            parseStr = str(i).split("s")
            sourceStr = parseStr[1].split("->")
            sourceStr = sourceStr[0].strip()
            #get source id number
            targetStr = parseStr[2].split(" ")
            targetStr = targetStr[0]
            #get target id number
            labelStr = parseStr[2].split("[")
            #print(labelStr)
            labelStr = labelStr[1].split('"')
            labelStr = labelStr[1].split(' ')
            #get input registers#
            if(labelStr[0] != 'τ') :
                firstInput = labelStr[0]
                secondInput = labelStr[1]
                self.findTransition(sourceStr, targetStr, labelStr[0],labelStr[1])
            else:
                transition = ET.SubElement(transitions, 'transition', {"from" : "id"+sourceStr, "to" : "id"+targetStr, "symbol" : "IDummy"})
 

    def write(self):
        source_xml = md.parseString(ET.tostring(root)).toprettyxml(indent="\t",newl="\n")
        new_header = '<?xml version="1.0" encoding="UTF-8"?>\n'
        target_xml = re.sub(u"\<\?xml .+?>", new_header, source_xml)
        with open('model.xml','wb') as self.f:
            self.f.write(target_xml.encode('utf8'))
            self.f.close()


mapper = Mapper()
mapper.read_file()
root = mapper.initialize()
transitions = ET.SubElement(root, 'transitions', {})
mapper.load()
mapper.dummy()
mapper.traverse()
mapper.write()



edge = graph.get_edge_list()
node = graph.get_node_list()
#print(edge[3])
# #transitions and states successfully extracted

root = ET.Element('register-automaton', {})
xmlFile = ET.ElementTree(root)

alphabet = ET.SubElement(root, 'alphabet', {})
inputs = ET.SubElement(alphabet, 'inputs', {})
outputs = ET.SubElement(alphabet, 'outputs', {})

#where is input/output information found ????

constants = ET.SubElement(root, 'constants', {})
globals = ET.SubElement(root, 'globals', {})

locations = ET.SubElement(root, 'locations', {})

for i in node:
    parseStr = str(i).split("s")
#    print(parseStr)
    idStr = parseStr[1].split("[")
    location = ET.SubElement(locations, 'location', name = "id" + idStr[0].strip())

transitions = ET.SubElement(root, 'transitions')

# traverse transitions list to concatenate tree
for i in edge:
    parseStr = str(i).split("s")
    sourceStr = parseStr[1].split("->")
    sourceStr = sourceStr[0].strip()
    targetStr = parseStr[2].split(" ")
    targetStr = targetStr[0]
    labelStr = parseStr[2].split("[")
    labelStr = labelStr[1].split('"')
    labelStr = labelStr[1]


    if labelStr[-1] == "●" or "⊛":
        transition = ET.SubElement(transitions, 'transition')
        source = ET.SubElement(transition, 'source', ref = "id" + sourceStr)
        target = ET.SubElement(transition, 'target', ref = "id" + targetStr + "0")
        label_sync = ET.SubElement(transition, 'label', kind = "synchronization", x='0', y='0')
        if labelStr[-1] == "●":
            label_sync.text = "●"
        else :
            label_sync.text = "⊛"
        label_assign = ET.SubElement(transition, 'label', kind = "assignment", x='0', y='0')
        label_assign.text = "r" + labelStr[0] + "=x"

        transition = ET.SubElement(transitions, 'transition')
        source = ET.SubElement(transition, 'source', ref = "id" + targetStr + "0")
        target = ET.SubElement(transition, 'target', ref = "id" + targetStr)
        label_sync = ET.SubElement(transition, 'label', kind = "synchronization", x='0', y='0')
    elif labelStr == "τ":
        print("this is an internal process")
    else :
        transition = ET.SubElement(transitions, 'transition')
        source = ET.SubElement(transition, 'source', ref = "id" + sourceStr)
        target = ET.SubElement(transition, 'target', ref = "id" + targetStr + "0")
        label_guard = ET.SubElement(transition, 'label', kind = "guard", x='0', y='0')
        label_guard.text = "r" + labelstr[0] + "==x"
        label_sync = ET.SubElement(transition, 'label', kind = "synchronization", x='0', y='0')
        label_sync.text = "known"
        transition = ET.SubElement(transitions, 'transition')
        source = ET.SubElement(transition, 'source', ref = "id" + targetStr + "0")
        target = ET.SubElement(transition, 'target', ref = "id" + targetStr)
        label_sync = ET.SubElement(transition, 'label', kind = "synchronization", x='0', y='0')
    
    label_sync.text = "OOK"
    

    


xmlFile.write("ex.xml")

#nx.draw(N)
#plt.savefig("ex.png")



# for i in transition:
#     print(i)
# for i in state:
#     print(i)
#graph.write_png('output.png')

#the graph variable is a python list that can be moderated by pydot etc
