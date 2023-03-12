import graphviz as gph

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
        and returns None otherwise. Return path isn't necessarily optimal.

        Parameters: 
        -----------
        src: NodeType
            First end (node) of the edge
        dest: NodeType
            Second end (node) of the edge
        power: numeric (int or float)
            power of the agent
        """
        # recursive Deep First Search
        # does not return optimal path
        seen = {} # edge (a, b) : True
        def rec_path(position):
            if position == dest: 
                return [dest]

            neighbors = self.graph[position]
            # Moving to neighboors
            for n in neighbors:  # n = (node tag, power, dist)
                if (position, n[0]) not in seen:
                    seen[(position, n[0])] = True
                    seen[(n[0], position)] = True
                    if n[1] < power: # moving through only admissible paths
                        p = rec_path(n[0]) 
                        if not(p is None):
                            p.append(position) 
                            return p
        print(rec_path(src))
        return rec_path(src) #list had been constructed backwards because of recursion

        # Seance 1 Question 3:
        # TIME COMPLEXITY: 
        # n : number of nodes ; m : number of edges
        # checking if a node has been seen is O(1) in a dictionary
        # for each edge we check if the other end has been seen, each edge = 2 checks in total at most
        # Worst case scenario : each node is checked once, each edge is checked twice 
        # (e.g. graph having form 1 -- 2 -- ... -- n )
        # thus we have time complexity O(n + m) 
        #
        # SPACE COMPLEXITY:
        # max recursion depth is n
        # dictionary lenght is n
        # returned list has max length n if there's a path
        # thus we have space complexity O(n)



    def get_optimal_path_with_power(self, src, dest, power):
        """
        Returns the path from src to dest with given power
        and lowest distance if possible and returns None otherwise 

        Parameters: 
        -----------
        src: NodeType
            First end (node) of the edge
        dest: NodeType
            Second end (node) of the edge
        power: numeric (int or float)
            power of the agent
        
        Outputs:
        --------
        best_path: List
            A list which contains the optimal path ordered from source to destination
        """
        seen = {(n, False) for n in self.nodes}
        admissible_paths = [] # will contain tuples (ditance, path)

        def rec_path(d, position): #memorising distance by passing it to args
            neighbors = self.graph[position]

            if position == dest:
                return 0, [dest]

             # Moving to neighboors
            for n in neighbors:  # n : (node tag, power, dist)
                if not seen[n[0]]:
                    seen[n[0]] = True 
                    if n[1] < power: # moving through only admissible paths
                        result = rec_path(n[0], dest)
                        if not(result is None):
                            partial_d, p = rec_path(dest, n[0]) 
                            p.append(position) 
                            if position == src: # end of path, no recursion
                                admissible_paths.append(n[2] + partial_d, p)
                            else:
                                return n[2] + partial_d, p
        rec_path(src, 0)
        if admissible_paths:
            best_path = []
            dmin = admissible_paths[0][0]
            for d, path in admissible_paths:
                if d < dmin:
                    best_path = reversed(admissible_paths[1])
            return best_path
        # Same complexity O(n + m) but it's always worst case scenario
        # because to verifiy if we have the optimal path,
        # it's necessary to go through all nodes and all paths

    def connected_components(self): 
        """
        Returns the connected components in the form of a list of lists, 
        each one being a connected component    
        
        """
        seen = {n: False for n in self.nodes}
        #seen = [(n, False) for n in self.nodes]
        list_of_components = []
        for a in self.nodes:
            if not seen[a]:
                seen[a] = True
                connected_component = [a]
                # heap of nodes to add is just neighboors
                # because if they had been seen before, a would also have been seen
                print(self.graph)

                to_add = [] # remettre le zip
                for b in self.graph[a]:
                    to_add.append(b[0])
                while to_add:
                    b = to_add.pop()
                    connected_component.append(b)
                    seen[b] = True
                    for b_neighboor in self.graph[b]: #list(zip(*self.graph[b])[0]):
                        if not seen[b_neighboor[0]]:
                            # have to check if seen 
                            # (e.g. neighboor of b being neighboor of a already seen before)
                            to_add.append(b_neighboor[0])
                list_of_components.append(connected_component)
        # Complexity O(n) where n is the number of nodes
        print(list_of_components)
        return list_of_components


    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
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
        
        Outputs:
        --------
        """
        #Solution 1: djikstra with power >= 0, 
        #           has too great space complexity O(n^2)
        #           to memorize information about all nodes, isn't necessary
        #           but time complixity is optimal with O(mlog(m))
        #Solution 2: determine set of all possible powers in edges
        #           sorting it
        #           then doing dichotomic research with get_path_with_power 
        #           Complexity is O(m + mlog(m) + nlog(p)) = O((n+m)log(m)) also
        #           with n : number of nodes ; m : number of edges
        #                p : number of distinct powers, p = O(m)
        
        powers = []
        for n in self.nodes :
            print(self.graph[n])
            edges_power = zip(self.graph[n])[2] #zip(*self.graph[n[0]])[2]
            for p in edges_power:
                powers.append(p)
        powers = list(set(powers)).sort()
        # Dichotomic research
        i = 0
        j = len(powers)-1
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
        # assert len(nm) == 2 "wrong format of text file" test à implémenter 
        n = int(first_line[0])
        # assert isinstance(n, int) "wrong format of text file" test à implémenter
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
    '''Transform our initial graph as a graphviz friendly one
    and then print it. In addition, we are able to highlight a path upon the graph and "popup" will allow to manage
    if the render is automatically opened
    
    Parameters:
    -----------
    graph: Graph (class defined earlier)
        It's the graph we want to work on
    popup: bool
        Allow to control if the render in immediately opened (not so relevant on sspcloud but convenient on PC)
    path: list 
        A path that we want to highlight on the initial graph (as asked)
    eng: str
        Allow to change directly in the call the engine used to render the graph (more convenient than changing it into the function)
    col: str
        Allow to change the color of the highlight (just a cosmetic add)
    
    Outputs:
    dot: graphviz.graphs.Digraph
        It may be useful later but it's not essential
    '''


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
