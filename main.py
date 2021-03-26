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
#networkx edges = transitions, networkx nodes = states

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
