import requests
import base64
import json
import os
from collatzCore import *
from CollatzMermaid import *
from InquirerPy import inquirer
from InquirerPy.base import Choice
from dataclasses import dataclass
import re 
import pandas as pd




#from jinja2 import Environment, FileSystemLoader

# Set up the environment
# The FileSystemLoader tells Jinja where to look for template files
#temp_env = Environment(loader=FileSystemLoader('Assets'))


@dataclass
class RegexEqual(str):
    string: str
    match: re.Match = None

    def __eq__(self, pattern):
        self.match = re.search(pattern, self.string)
        return self.match is not None
    
    def __getitem__(self, group):
        return self.match[group]



def interpret_input(s):
    itr = None
    match RegexEqual(s):
        case '^([0-9]*)$' as capture:
            print(f'number {capture[1]}')
            itr = [int(capture[1])]

        case '^([0-9]*)?-([0-9]*)$' as capture:
            print(f'range4-4 min:{capture[1] or 3} max:{capture[2]}')
            itr = range(int(capture[1] or 3), int(capture[2])+1)
        
        case r"^(\d+)(\s*\,\s*\d+)*$" as capture:
            print("list")
            
            itr = [int(n) for n in re.findall(r"\d+", capture[0])]
            
        case _:
            print('wrong, try again')
            raise SyntaxError("Wrong try again")
    
    return itr
    
def export_nodes_to_csv(g,fileName,sideInfos=None, determineColor=None):
    df = pd.DataFrame(index=g.nodes())
    
    df["MapFromOne"] = pd.Series(nx.get_node_attributes(g, "MapFromOne"))
    for info in sideInfos.keys():
        df[info] = pd.Series(nx.get_node_attributes(g, info))
    
    df["color"] = pd.Series(nx.get_node_attributes(g, "color"))
    df["distanceFromOne"] = pd.Series(nx.get_node_attributes(g, "distanceFromOne"))

    df= df.sort_index(ascending=True)
    
    os.makedirs('./graph_csvs', exist_ok=True)

    
    file_path = f'./graph_csvs/{fileName}.csv'

    df.to_csv(file_path)

    return file_path



    
    

EXPORT_OPTIONS = {
   
    "Mermaid Graph SVG": export_mermaid_to_svg,
    "Nodes CSV": export_nodes_to_csv,
    "Mermaid Graph File": export_mermaid_to_svg
    #  "Text File": None
}

DEFAULT_EXPORT_OPTIONS = ["Mermaid Graph SVG","Nodes CSV"]

def chooseExport(G, graphName,sideInfos=None, determineColor=None):
    """
    Docstring for chooseExport
    
    Each Export file must return a path to the file it created.

    :param G: Description
    :param graphName: Description
    :param sideInfos: Description
    :param determineColor: Description
    """

    fileName = graphName + f'({", ".join(sideInfos.keys()) if isinstance(sideInfos, dict) else ""})'

    selected = inquirer.checkbox(
        message="Choose methods to export the graph:",
        choices = [ Choice(k, enabled= (k in DEFAULT_EXPORT_OPTIONS)) for k in EXPORT_OPTIONS.keys()], 
        validate=lambda result: len(result) >= 1,
        invalid_message="should be at least 1 selection",
        instruction="(select at least 1)",
    ).execute()

    files_exported = {}
    print("Exporting To Files")
    for choise in selected:
        file_path = EXPORT_OPTIONS[choise](G, fileName, sideInfos, determineColor)
        if os.path.isfile(file_path):
            file_path = os.path.abspath(file_path)
            files_exported[choise] = file_path
            print(file_path)
    
    return files_exported


def run_user_ui(sideInfos=None, determineColor=None):
    prompt = input("Enter number/s: \n")
    user_numbers = interpret_input(prompt)
    G = generate_collatz(user_numbers,sideInfos=sideInfos, determineColor=determineColor)
    chooseExport(G, prompt,sideInfos=sideInfos, determineColor=determineColor)



# Alternative: Using Mermaid's kroki API



# Example usage
def main(): 
    try:
        #G = generate_collatz(user_numbers)
        run_user_ui({ "Mod6": lambda n, g: int(n)%6},lambda n,g: 'green' if n%2 else '')
        # export_nodes_to_csv(G,prompt,{"MapFromOne": lambda n, g: g.nodes[n].get("MapFromOne","")},lambda n,g: 'green' if n%2 else '')
    except SyntaxError:
        main()



if __name__ == "__main__":
    while True:
        main()
    
