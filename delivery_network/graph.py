import graphviz as gph
from time import perf_counter

class Graph:
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes]) # n1 -> (n2, power_min, distance)
        self.nb_nodes = len(nodes)
        self.nb_edges = 0


    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output


    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        #checking if nodes are in the graph, adding them if not
        if node1 not in self.graph:
            self.graph[node1] = []
        if node2 not in self.graph:
            self.graph[node2] = []
        # edge addition
        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1

    
    def get_path_with_power(self, src, dest, power):
        """
        Returns an admissible path from src to dest with given power if possible
        and returns None otherwise. 
        Returned path isn't necessarily optimal in the sense of distance;

        Parameters: 
        -----------
        src: NodeType
            First end (node) of the edge
        dest: NodeType
            Second end (node) of the edge
        power: numeric (int or float)
            power of the agent

        Output
        ----------
        path : list[int]
            Sequence of nodes leading from src to dest through edges
            whose power is less than that of the agent.
        """
        # Deep First Search through recursion

        seen = {} # edge (a, b) : True

        def rec_path(position):
            if position == src: 
                return [src]

            neighbors = self.graph[position]
            # Moving to neighboors
            for n in neighbors:  # n = (node tag, power, dist)
                if (position, n[0]) not in seen:
                    seen[(position, n[0])] = True 
                    seen[(n[0], position)] = True 
                    if n[1] <= power: # moving through only admissible paths
                        p = rec_path(n[0]) 
                        if not(p is None):
                            p.append(position) 
                            return p
        path = rec_path(dest)
        return path


    # def get_optimal_path_with_power(self, src, dest, power):
    #     """
    #     Returns the path from src to dest with given power
    #     and with lowest distance if possible, and None otherwise.

    #     Parameters: 
    #     -----------
    #     src: NodeType
    #         First end (node) of the edge
    #     dest: NodeType
    #         Second end (node) of the edge
    #     power: numeric (int or float)
    #         power of the agent
        
    #     Outputs:
    #     --------
    #     best_path: List
    #         Sequence of nodes leading from src to dest through edges
    #         whose power is less than that of the agent and that 
    #         minimises distance traveled.
    #     """
    #     # Deep First Search through recursion
    #     seen = {} # format: edge (a, b) : True
    #     admissible_paths = [] 
        
    #     def rec_path(position, d): # keeping track of distance by passing it though args
    #         if position == src: 
    #             return [src], 0

    #         neighbors = self.graph[position]
    #         for n in neighbors:  # n = (node tag, power, dist)
    #             if (position, n[0]) not in seen:
    #                 seen[(position, n[0])] = True 
    #                 seen[(n[0], position)] = True 
    #                 if n[1] <= power: # moving through only admissible paths
    #                     p, d2 = rec_path(n[0], d +) 
    #                     if not(p is None):
    #                         p.append(position) 
    #                         return p
    #     path = rec_path(dest)

    #     return 
    #     seen = {(n, False) for n in self.nodes}
    #     admissible_paths = [] # will contain tuples (ditance, path)

    #     def rec_path(d, position): #memorising distance by passing it to args
    #         neighbors = self.graph[position]

    #         if position == dest:
    #             return 0, [dest]

    #          # Moving to neighboors
    #         for n in neighbors:  # n : (node tag, power, dist)
    #             if not seen[n[0]]:
    #                 seen[n[0]] = True 
    #                 if n[1] <= power: # moving through only admissible paths
    #                     result = rec_path(n[0], dest)
    #                     if not(result is None):
    #                         partial_d, p = rec_path(dest, n[0]) 
    #                         p.append(position) 
    #                         if position == src: # end of path, no recursion
    #                             admissible_paths.append(n[2] + partial_d, p)
    #                         else:
    #                             return n[2] + partial_d, p
    #     rec_path(src, 0)
    #     if admissible_paths:
    #         best_path = []
    #         dmin = admissible_paths[0][0]
    #         for d, path in admissible_paths:
    #             if d < dmin:
    #                 best_path = reversed(admissible_paths[1])
    #         return best_path

    def connected_components(self): 
        """
        Returns the connected components of the graph in the form 
        of a list of lists.  
        
        Output
        -----------
        list_of_components : list[list[int]]
            Each sublist represents a connected component.
            The sublist contains the tags of all nodes in the component
        """
        seen = {n: False for n in self.nodes} 
        list_of_components = []

        for a in self.nodes:
            if not seen[a]: # if a wasn't seen, a belongs to a yet unseen connected component
                seen[a] = True
                connected_component = [a] 

                to_add = []
                for b in self.graph[a]:# heap of nodes to add is just neighboors
                    to_add.append(b[0])
                    # not necessary to check if seen, as none of the nodes
                    # in this connected component were seen (a would've also been otherwise)
                
                while to_add:
                    b = to_add.pop()
                    connected_component.append(b)
                    seen[b] = True
                    for b_neighboor in self.graph[b]:
                        if not seen[b_neighboor[0]]:
                            # have to check if seen 
                            # (e.g. neighboor of b being neighboor of a already seen before)
                            to_add.append(b_neighboor[0])
                list_of_components.append(connected_component)
        return list_of_components


    def connected_components_set(self):
        """
        Returns the connected components of a graph 

        Output: 
        ----------
        Type set[frozenset[int]]
            set of connected component, 
            each being represented as a frozen set
        """
        return set(map(frozenset, self.connected_components()))

    def min_power(self, src, dest):
        """
        Returns path from src to dest with minimal power and the associated power 

        Parameters:
        -----------
        src: NodeType
            The source node
        dest: NodeType
            The destination node
        
        Output:
        --------
        """
        #Solution 1: djikstra with power >= 0, 
        #           has too great space complexity O(n^2)
        #           to memorize information about all nodes, isn't necessary
        #           but time complexity is optimal with O(mlog(m))
        #Solution 2: determine set of all possible powers in edges
        #           sorting it
        #           then doing dichotomic research with get_path_with_power 
        #           Complexity is O(m + mlog(m) + nlog(p)) = O((n+m)log(m)) also
        #           with n : number of nodes ; m : number of edges
        #                p : number of distinct powers, p = O(m)
        
        powers = []
        for n in self.nodes:
            for e in self.graph[n]:
                powers.append(e[1])

        powers = sorted(list(set(powers)))
        print(powers)
        # Dichotomic research
        i = 0
        j = len(powers) - 1
        while i < j:
            if j == i+1:
                if get_path_with_power(self, src, dest, powers[i]) is None:
                    i = j
                else:
                    return get_path_with_power(self, src, dest, powers[i]), powers[i]

            if get_path_with_power(self, src, dest, powers[(i+j)//2]) is None:
                i = (i+j)//2
            else:
                j = (i+j)//2
        
        answer = get_path_with_power(self, src, dest, powers[i])
        if not (answer is None):
            return answer, powers[i]        
            

    def pmin(edges):
            """
            Returns the index of the edge with minimal power in the list edges 
            """

    # no 'self' in args of method
    @staticmethod 
    def graph_from_file(filename):
        """
        Reads a text file and returns the graph as an object of the Graph class.
        The file should have the following format: 
            The first line of the file is 'n m'
            The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
            The nodes (node1, node2) should be named 1..n
            All values are integers.

        Parameters: 
        -----------
        filename: str
            The name of the file

        Outputs: 
        -----------
        G: Graph
            An object of the class Graph with the graph from file_name.
        """

        graphe = open(filename, "r")
        first_line = graphe.readline().split(" ") #first line: number of nodes, number of edges
        n = int(first_line[0])
        G = Graph(list(range(1, n+1))) #initialization of graph

        E = graphe.readlines() 
        for edge in E: #filling G with specified edges
            edge = ''.join(edge.splitlines()) 
            ar =list(map(int, edge.split(" ")))
            if len(ar) == 4: # distance specified
                 G.add_edge(ar[0], ar[1], ar[2], ar[3])
            elif len(ar) == 3: # not specified
                G.add_edge(ar[0], ar[1], ar[2])
        graphe.close()
        return G


def graph_render(graph, popup = False, path=[], eng="sfdp", col="green"):
    """
    Transform our initial graph as a graphviz friendly one
    and then print it. In addition, we are able to highlight a path upon the graph and "popup" will allow to manage
    if the render is automatically opened
    
    Parameters:
    -----------
    graph: Graph (class defined earlier)
        It's the graph we want to work on
    popup: bool
        Whether graphic result pops up
    path: list 
        contains
    eng: str
        Choice of engine used to render the graph 
    col: str
        color of the highlighted path
    
    Output
    ----------
    dot: graphviz.graphs.Digraph
    """
    # (Output may be useful later but it's not essential)

    dot = gph.Digraph('Initial_graph', comment='Initial graph',engine=eng)

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

def time_measure(function):
    """
    This function allows us to measure in an easier way our program's performances by printing the elapsed time during function's work

    Parameters:
    -----------
    function: function's output type
        It takes a format like "function_analysed(paramaeter1,parameter2,...)"
    
    Outputs:
    --------
    None
    """
    s = perf_counter()
    function()
    e = perf_counter()
    print(f"Your function was performed in{e-s}s")