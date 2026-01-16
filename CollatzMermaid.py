import requests
import base64
import json
import os
from collatzCore import *
import re 


def generate_mermaid_link(graph_code):
    # Define the state object
    state = {
        "code": graph_code,
        "mermaid": {"theme": "default"},
        "updateEditor": True
    }
    
    # Convert to JSON string
    json_str = json.dumps(state)
    
    # Encode to Base64
    # Note: Use urlsafe_b64encode if you find padding issues, 
    # but standard b64 is usually fine for mermaid.live
    encoded = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    
    l = f"https://mermaid.live/view#base64:{encoded}"
    print("\n link to graph")
    print(l)
    print()

    return l



def generate_mermaid_code(g,sideInfos=None, determineColor=None):
    
    
    getNodeID = lambda nodeNum: f'n{str(nodeNum)}'


    def getNodeDetails(n):
        
        s = f'["`**{n}**'
        
        if sideInfos:
            s = s + f'\n**MapToOne**: {g.nodes[n].get("MapFromOne","")}'+ '\n'
            for title in sideInfos.keys():
                r =  g.nodes[n][title]
                if str(r):
                    s = s + f'\n**{title}**: {r}'



        s = s +'`"]'

        if determineColor:
           c = g.nodes[n]["color"]
           if c:
               s = s + f':::{c}'

        g.nodes[n]["detailedInCode"]=True
        return s

    getNodeText = lambda n: getNodeID(n)+ ("" if g.nodes[node].get("detailedInCode",False) else getNodeDetails(n))


    mermaid_code = """---
config:
   flowchart:
    nodeSpacing: 100
    rankSpacing: 120
---
flowchart TD
classDef red stroke:red,stroke-width: 3px;
classDef green stroke:green,stroke-width: 3px;
classDef blue stroke:blue,stroke-width: 3px;
"""
    mermaid_code =mermaid_code + f'\n{getNodeID(1)+getNodeDetails(1)}'


    for node in g: 
        print(f'{node}->{list(g.neighbors(node))}')
        for niehgbour in g.neighbors(node):
            mermaid_code += f'\n{getNodeText(node)}-->{getNodeText(niehgbour)}'

    return mermaid_code


def mermaid_to_svg_kroki(mermaid_code):
    """
    Alternative method using Kroki API.
    
    Args:
        mermaid_code (str): The Mermaid diagram code
        output_file (str, optional): Path to save the SVG file
        
    Returns:
        str: The SVG content
    """
    
    url = "https://kroki.io/mermaid/svg"
    
    headers = {
        'Content-Type': 'text/plain'
    }
    
    response = requests.post(url, data=mermaid_code, headers=headers)
    
    if response.status_code == 200:
        svg_content = response.text
        
        return svg_content
    else:
        raise Exception(f"API request failed with status code {response.status_code}")


def mermaid_to_svg(mermaid_code):
    """
    Convert Mermaid diagram code to SVG using Mermaid's online API.
    
    Args:
        mermaid_code (str): The Mermaid diagram code
        output_file (str, optional): Path to save the SVG file
        
    Returns:
        str: The SVG content
    """
    
    # Mermaid Ink API endpoint
    url = "https://mermaid.ink/svg/"
    
    # Encode the mermaid code to base64
    encoded = base64.urlsafe_b64encode(mermaid_code.encode('utf-8')).decode('ascii').rstrip('=')
    
    # Make the request
    response = requests.get(f"{url}{encoded}")
    
    if response.status_code == 200:
        svg_content = response.text
    
        
        return svg_content
    
    #Solve bug! why certain attributes dont appear to some numbers like 27?
    
    
    else:
        print(f"API request failed with status code {response.status_code}")
        print("Try Kroki")
        return mermaid_to_svg_kroki(mermaid_code)
        
        



def export_mermaid_to_svg(g,fileName,sideInfos=None, determineColor=None):
    
    
    mermaid_code = generate_mermaid_code(g,sideInfos, determineColor)
    
    os.makedirs('./mermaid_graphs', exist_ok=True)
    
    file_path = f'./mermaid_graphs/{fileName}'
    file_content = ''
    try:
        file_content = mermaid_to_svg(mermaid_code)
        file_path = file_path + ".svg"
        print(f"SVG saved to {file_path}")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)

    except Exception as e:
        
        print(e)
        print("failed generating svg, creating a defualt mmd file")
        file_path = export_mermaid_to_file(g, fileName, mermaid_code=mermaid_code)
        
    finally:

        return file_path
    

def export_mermaid_to_file(g,fileName,sideInfos=None, determineColor=None, mermaid_code = ''):
    
    
    mermaid_code = mermaid_code or generate_mermaid_code(g,sideInfos, determineColor)
    
    os.makedirs('./mermaid_graphs', exist_ok=True)
    
    file_path = f'./mermaid_graphs/{fileName}'    

    file_path = file_path + ".mmd"

    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(mermaid_code)

    # if not os.path.isfile(file_path): #If a graph file was created already, a link was appened too
    #     with open('./graphLinks.md', "a") as f:
    #         f.write(f"* [{fileName}]({generate_mermaid_link(mermaid_code)})\n") 
         
    return file_path

        

   
    






if __name__ == "__main__":
#   while True:
    #main()
    # Example Mermaid flowchart
    
    
    
    file_content = ''
    with open(r'C:\Users\itayb\Documents\vsProjects\MATH\Collatz\mermaid_graphs\1-50(Mod6).mmd', "r") as f:
        mermaid_code = f.read()
    
        
            # Get SVG content
            #       svg = mermaid_to_svg(mermaid_code)
        file_content = mermaid_to_svg(mermaid_code)
        file_path = "test.svg"
        print(f"SVG saved to {file_path}")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)
        print("SVG generated successfully!")


        
        