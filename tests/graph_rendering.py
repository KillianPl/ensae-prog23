import sys 

sys.path.append("delivery_network/")

from graph import Graph
import graphviz as gph


def graph_render(graph, popup = False, path=[], eng="sfdp", col="green"):
    """
    Vizualises of a graph and optionally a path in that graph.
    Result is printed or put in a new window.
    
    Parameters:
    -----------
    graph: Graph
        main object of class Graph 
    popup: bool
        Choose whether graphic rendering pops up in a new window or not
    path: list 
        Contains sequence of nodes forming a path from a source to a destination.
        It is assumed that the path is valid i.e. nodes and edges on that path exist.
    eng: str
        Choice of engine used to render the graph 
    col: str
        color of the highlighted path
    
    Output
    ----------
    dot: graphviz.graphs.Digraph
    """
    # Transforms graph as a graphviz friendly one
    # output is useless to us

    dot = gph.Digraph('Initial_graph', comment='Initial graph', engine=eng)

    for i in graph.nodes:
        if i in path:
            dot.node(str(i), color = col)
        else:
            dot.node(str(i))
    
    viewed = []
    
    for k in list(graph.graph.keys()):
        for n in graph.graph[k]:
            if n[0] not in viewed:
                if k and n[0] in path:
                    dot.edge(str(k),str(n[0]),color=col,dir="none")
                else:  
                    dot.edge(str(k),str(n[0]),dir="none")
            viewed.append(n[0])
        viewed.append(k)
    dot.render(view=popup).replace('\\', '/')
    print(type(dot))
    return dot

g = Graph.graph_from_file("input/network.00.in")

if __name__ == '__main__':
    graph_render(g)
