from CollatzCITEs import calculate_trajectory
from IPython.display import display, Math






def analyze_trajectory(l):

    d = calculate_trajectory(l)
    display(Math(d["latex"]))

