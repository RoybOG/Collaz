from ete3 import Tree, TextFace, TreeStyle, add_face_to_node
import networkx as nx
import os
import sympy
from fractions import Fraction
import os 
import networkx as nx
from dataclasses import dataclass
import re 
import itertools

@dataclass
class RegexEqual(str):
    string: str
    match: re.Match = None

    def __eq__(self, pattern):
        self.match = re.search(pattern, self.string)
        return self.match is not None
    
    def __getitem__(self, group):
        return self.match[group]
    


def collatz_sequence(n, max_tries=None):
    """
    Generator that yields the Collatz sequence starting from n.
    If max_tries is provided, will stop after that many iterations.
    """
    tries = 0
    current = n
    
    while current != 1:
        yield current
        
        if max_tries and tries >= max_tries:
            break
            
        if current % 2 == 0:
            current = current // 2
        else:
            current = 3 * current + 1
            
        tries += 1
    
    yield current  # Yield the final 1



# Example usage

def log_sequence(n, max_tries=None, ):
    os.makedirs('collatz_calcs', exist_ok=True)
    filename=f'collatz_calcs/collatz_log_for_{n}.csv'
    with open(filename, 'w') as f:
        # f.write(f"\nTesting {n} (max tries: {max_tries}):\n")
        
        formulaCalc = lambda i: (n+1)*((Fraction(3,2))**(i-1))-1
        n_path = list(collatz_sequence(n, max_tries=max_tries))
        
        # Log each number and its prime factorization
        last_four_multiple_index=0
        f.write(', '.join(['index','number','factorization','distance from power of 2','reminder mod 4', 'is peak'])+ '\n')
        for i,num in enumerate(n_path):
            factors = sympy.ntheory.factorint(num)
            fstr = ' * '.join([f'{k}^{v}' for k,v in factors.items()])
            #f.write(f'{num} = {factors}\n')
            factors.pop(2, None)
            distFromPowerOfTwo = sum(factors.values())
            f.write(', '.join([str(v) for v in [i,num, fstr, distFromPowerOfTwo, num%4, " peak" if num%4==0 else '']]) + '\n')
                    

        


def build_graph(itr):
    G = nx.DiGraph()
    def add_to_graph(num):
        for pair in itertools.pairwise(collatz_sequence(num)):
            G.add_edge(*pair)
            # Store both mod4 and mod6 values
            G.nodes[pair[0]]['mod6'] = pair[0] % 6


    for i in itr:
        if G.has_node(i):
            continue
        add_to_graph(i)
    
    return G




def interpret_input(s):
    itr = None
    match RegexEqual(s):
        case '^([0-9]*)$' as capture:
            print(f'number {capture[1]}')
            itr = [int(capture[1])]

        case '^([0-9]*)?\-([0-9]*)$' as capture:
            print(f'range4-4 min:{capture[1] or 3} max:{capture[2]}')
            itr = range(int(capture[1] or 3), int(capture[2])+1)
        
        case r"^(\d+)(\s*\,\s*\d+)*$" as capture:
            print("list")
            
            itr = [int(n) for n in re.findall(r"\d+", capture[0])]
            
        case _:
            print('wrong, try again')
            raise TypeError("Wrong try again")
    
    return build_graph(itr)
    




def nx_to_newick(G):
    """
    Converts a NetworkX tree/DAG (DiGraph) to a Newick string.

    Args:
        G (nx.DiGraph): The NetworkX graph (must be a tree or a DAG).
        root_node: The starting node (root) of the tree.
        
    Returns:
        str: The Newick formatted string.
    """
    root=1

    eteTree = Tree(name=1)

    def recur_to_ete(current_node_num, current_new_node):
        
        for child_num in G.predecessors(current_node_num):
            c = current_new_node.add_child(name=child_num) 
            recur_to_ete(child_num,c)

    recur_to_ete(1,eteTree)

    return eteTree


    
    # 1. Initialize the root node for the ETE tree

def dual_label_layout(node):
    """
    Layout function that adds the node's name (in blue) and a custom 
    property (mod6, in red) next to the node.
    """
    
    # --- Part 1: Display the Main Node Name ---
    
    # 1. Check if the node has a name to display
    if node.name:
        # Create a face for the node's main identifier
        name_face = TextFace(str(node.name), fsize=10, fgcolor="blue")
        
        # Add the main name face to the node (left-aligned)
        add_face_to_node(name_face, node, column=0, position="branch-right")

    # --- Part 2: Display the Custom Number (e.g., mod 6) ---
    
    # 2. Check if the node has the custom property (replace 'mod6' with your actual attribute)
    if hasattr(node, "mod6"):
        # Get the custom value
        mod_value = str(node.mod6)
        
        # Create a face for the custom number
        mod_face = TextFace(f' ({mod_value})', fsize=8, fgcolor="red")
        
        # Add the custom face immediately to the right of the name (column=1)
        add_face_to_node(mod_face, node, column=1, position="branch-right")

def get_tree_style_for_labels(ete_tree):
    # 1. Define the TreeStyle
    ts = TreeStyle()
    
    # Use the custom layout function
    ts.layout_fn = dual_label_layout 
    ts.branch_vertical_margin = 10
    # Set display options
    ts.show_branch_length = False
    ts.show_leaf_name = False # Disable default names so we control their placement
    ts.mode = "r" 

    return ts
    # 2. Show the tree
    


def drawGraph(G,prompt="t"):  
# --- Setup Example Data ---
# Create a tree (the names are the numbers)
    t = nx_to_newick(G)
    os.makedirs('./collatz_graph', exist_ok=True)
    filename=f'./collatz_graph/{prompt}.svg'
    # Traverse and assign the custom 'mod6' property to each node
    """"
    for node in t.traverse("levelorder"):
        try:
            # Assume node names are convertible to integers for the Collatz graph
            num = int(node.name)
            node.add_features(mod6=num % 6)
        except ValueError:
            # Handle cases where internal node names aren't numbers (e.g., empty or "I1")
            node.add_features(mod6='-') 
    """
    ts = get_tree_style_for_labels(t)
    t.render(filename,tree_style=ts)
    t.show(tree_style=ts)
    


if __name__ == "__main__":
    prompt = input("Enter number: \n") #'3-40' '3,9,15,21,33,39,27'#
    drawGraph(interpret_input(prompt),prompt)
    #nx_to_newick(G)