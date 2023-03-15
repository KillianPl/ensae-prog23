import graphviz as gph
from time import perf_counter
import numpy as np
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


    def get_optimal_path_with_power(self, src, dest, power):
        
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
        return None


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
        Returns path from src to dest with minimal power and the associated power when there is one
        Returns None otherwise

        Parameters:
        -----------
        src: NodeType
            The source node
        dest: NodeType
            The destination node
        
        Output: 
        --------
        tupple(list[Nodetype], float)  | NoneType
                    
        with
                path : list[Nodetype]
                    Sequence of nodes leading from src to dest through edges
                    whose power is less than that of the agent.

                power : float
                    Minimal power necessary to go from src to dest
        """
        #constructing list of distinct powers
        powers = [] 
        for n in self.nodes:
            for e in self.graph[n]:
                powers.append(e[1])

        powers = list(set(powers))
        powers.sort() #in place

        # Dichotomic research
        i = 0
        j = len(powers) - 1
        while i < j:
            if j == i+1:
                if self.get_path_with_power(src, dest, powers[i]) is None:
                    i = j
                else:
                    return self.get_path_with_power(src, dest, powers[i]), powers[i]

            if self.get_path_with_power(src, dest, powers[(i+j)//2]) is None:
                i = (i+j)//2
            else:
                j = (i+j)//2
        
        path = self.get_path_with_power(src, dest, powers[i])
        if not (path is None):
            return path, powers[i]

    def pmin(edges):
            """
            Returns the index of the edge with minimal power in the list edges 
            """


    def kruskal(self):
        """
        Returns the minimal covering tree of the graph.
        Construction uses Kruskal's algorithm.

        Output
        ---------
        G : Graph
        """
        # other idea is to create a subclass that inherits from Graph
        #Tree would have attribute parents and descendants

        # constructing list of (power, edge) without repetition
        edges_seen = {} #to check repetition
        edges = []
        for node_a in self.nodes:
            for edge in self.graph[node_a]: 
                node_b, p, d = edge
                if not ((node_a, node_b) in edges_seen):
                    edges_seen[(node_a, node_b)] = True
                    edges_seen[(node_b, node_a)] = True # to not add it again when on node_b
                    edges.append((node_a, node_b, p, d))
        # sorting in place on powers
        edges.sort(key= lambda a : a[2]) 

        #constructing covering tree 
        G = Graph(self.nodes)
        connected = {n: [n] for n in self.nodes} #to identify accessible nodes from n
        # using dictionary for O(1) check if two nodes are connected 
        for edge in edges:
            # loop invariant: connected[n] contains the connected component of node n at the end of each iteration
            node_a, node_b, p, d = edge
            if not (connected[node_b][0] == connected[node_a][0]):
                G.add_edge(node_a, node_b, p, d)
                for node_c in connected[node_b]: # none of the nodes connected to b were connected to a
                    connected[node_a].append(node_c)
                    connected[node_c] = connected[node_a] # pointers
                    # changing connected[a] will thus update it automatically 
                    # for all nodes in the connected component
                    
            if G.nb_edges() == G.nb_nodes()-1: # optionnal
                break # trees of size V have exactly V-1 edges : if it is reached, construction's over.
        return G
        
    def min_power_tree(self, src, dest):
        """
        Returns, if there is one, the only path from src to dest in a tree and the minimal
        power necessary to cross it.
        By construction of the minimal covering tree, the power is 
        the smallest one needed to go from src to dest
        It is assumed the function is being applied on a minimal covering tree,
        e.g. the output of the kruskal function
        

        Parameters: 
        -----------
        src: NodeType
            First end (node) of the edge
        dest: NodeType
            Second end (node) of the edge

        Output
        ----------
        tupple(list[NodeType], float) | NoneType
        
        with
                path : 
                    Sequence of nodes leading from src to dest through edges
                    whose power is less than that of the agent.

                power : float
                    Minimal power necessary to go from src to dest
        """
        # Recursive Deep First Search
        # unlike with a graph, we can just check nodes

        seen = {} # node : True
        def rec_path(position, min_p): #keeping track of the minimal power on the path
            if position == src:
                return [src], 0       
            #checking neighbors
            for edge in self.graph[position]:
                node_b, p, _ = edge
                if node_b not in seen:
                    seen[node_b] = True
                    result = rec_path(node_b, min(p, min_p))
                    if result is not None:
                            path, p_min = result # p_min <= p necessary
                            path.append(position)
                            return path, p_min
        return rec_path(dest, 0)

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
            ar = list(map(float, edge.split(" "))) # format : node_a, node_b, power, distance (optional)
            if len(ar) == 4: # distance specified
                 G.add_edge(int(ar[0]), int(ar[1]), ar[2], ar[3])
            elif len(ar) == 3: # not specified
                G.add_edge(int(ar[0]), int(ar[1]), ar[2], 1)
        graphe.close()
        return G



