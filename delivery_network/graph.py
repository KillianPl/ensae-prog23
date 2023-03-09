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
        if node1 in self.graph:
            self.graphe[node1].append([])
            self.nb_nodes += 1
        if node2 in self.graph:
            self.graphe[node2].append([])
            self.nb_nodes += 1
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
        seen = {(n, False) for n in self.nodes}
        
        def rec_path(position):
            if position == dest: 
                return [dest]

            neighbors = self.graph[position]
             # Moving to neighboors
            for n in neighbors:  # n : (node tag, power, dist)
                if not seen[n[0]]:
                    seen[n[0]] = True 
                    if n[1] < power: # moving through only admissible paths
                        p = rec_path(n[0], dest) 
                        if not(p is None):
                            p.append(position) 
                            return p

        return rec_path(src)[::-1] #list had been constructed backwards because of recursion

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
        seen = {(n, False) for n in self.nodes}
        list_of_components = []
        for a in self.nodes:
            if not seen(a):
                seen[a] = True
                connected_component = [a]
                # heap of nodes to add is just neighboors
                # because if they had been seen before, a would also have been seen
                to_add = list(zip(*self.graph[a])[0])
                while to_add:
                    b = to_add.pop()
                    connected_component.append(b)
                    seen[b] = True

                    for b_neighboor in  list(zip(*self.graph[b])[0]):
                        if not seen[b_neighboor]:
                            # have to check if seen 
                            # (e.g. neighboor of b being neighboor of a already seen before)
                            to_add.append(b_neighboor)

                list_of_components.append(connected_component)
        # Complexity O(n) where n is the number of nodes
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
        for n in self.nodes:
            edges_power = zip(*self.graph[n[0]])[2]
            for p in edges_power:
                powers.append(p)
        powers = list(set(powers))).sort()
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
            

        def pmax(edges):
            """
            Returns the index of the edge with maximal power in the list edges 
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
        nm = graphe.readline().split(" ") #first line: number of nodes, number of edges
        # assert len(nm) == 2 "wrong format of text file"
        isinstance()
        n, m = map(int, nm)
        # assert isinstance(n, int) "wrong format of text fiile"
        G = Graph(list(range(n))) # initialization of graph
        G.nb_edges = m 

        E = graphe.readlines() 
        for edge in E: #filling G with specified edges
            ar =list(map(int, edge.split("-")))
            if len(ar) == 4: # distance specified
                G.add_edge(G, ar[0], ar[1], ar[2], ar[3])
            elif len(ar) == 3: # not specified
                G.add_edge(ar[0], ar[1], ar[2])
        graphe.close()
        return G


def graph_render(graph, popup = False):
    '''Transform our initial graph as a graphviz friendly one
    and then print it. In addition, "popup" will allow to control
    if the render is automatically opened'''

    dot = gph.Digraph('Initial_graph', comment='Initial graph')

    for i in graph.nodes():
        dot.nodes(str(i))
    
    viewed = []
    for k in graph.keys():
        for n in graph[k]:
            if n not in viewed:
                dot.edge(str(k),str(n))
            viewed.append(n)
        viewed.append(k)

    dot.render().replace('\\', '/', view=popup)
    return dot


def path_render(graph, path, popup=False):
    '''Will build a graphviz graph and highlight a defined path upon'''

    dot = gph.Digraph('Highlighted_graph', comment='Initial graph with path highlighted')

    for i in graph.nodes():
        if i in path:
            dot.nodes(str(i), color = 'green')
        else:
            dot.nodes(str(i))
    
    viewed = []
    for k in graph.keys():
        for n in graph[k]:
            if n not in viewed:
                if k and n in path:
                    dot.edge(str(k),str(n),color='green')
                else:  
                    dot.edge(str(k),str(n))
            viewed.append(n)
        viewed.append(k)

    dot.render().replace('\\', '/', view=popup)

