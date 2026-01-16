import sympy
import base64
import json
from fractions import Fraction
import os 
import networkx as nx
from networkx.readwrite import json_graph
import itertools






def incLast(l):
        if len(l) > 0:
            l[-1] = l[-1]+1
        return l

def addNumberToCollatzGraph(G, n,sideInfos=None, determineColor=None):
    
    sideInfos = sideInfos or {}

    def getFractionForm(n):
        
        next_num = 0
        fraction_form =  [0]
        distance_from_one = 0
        already_in_graph = n in G.nodes

        if n!=1:
            if n %2==1:
                next_num = 3*n+1
                distance_from_one, fraction_form = getFractionForm(next_num)
                fraction_form = fraction_form + [0]
            
            else:
                next_num = n//2
                distance_from_one, fraction_form = getFractionForm(next_num)
                fraction_form = incLast(fraction_form)
        
        # print(f'{n}: {fraction_form}')
        
            G.add_edge(n, next_num)
        
        if (not already_in_graph) or (n==1):
            for title, f in sideInfos.items():
                G.nodes[n][title] = f(n, G)
            
            G.nodes[n]["color"] = determineColor(n,G)
            G.nodes[n]["distanceFromOne"] = distance_from_one
            
        # if "MapFromOne" not in G.nodes[n]:
            G.nodes[n]["MapFromOne"] = fraction_form.copy() #Prevents the adding one to same list in memory as the privous one

        return distance_from_one + 1, fraction_form

    getFractionForm(n)
    #G.nodes[1]["MapFromOne"] =[]
    return G #, getFractionForm(n)

# Example usage


def generate_collatz(itr,sideInfos=None, determineColor=None):
    G = nx.DiGraph()
    G.add_node(1)

    for n in itr:
        addNumberToCollatzGraph(G,n,sideInfos=sideInfos, determineColor=determineColor)

    return G


        
    


