class Graph(object):

    def __init__(self, alist):
        """
        Initialise a graph with an adjacency list

        Args:
        alist (list[list]): the adjacency list representing the graph

        Attributes:
        alist (list[list]): the adjacency list
        V (set): the set of vertices (nodes) in the graph
        N (int): the total number of vertices
        E (set): the set of edges (as frozensets of vertex pairs)
        d (list[int]): the degree (number of neighbors) for each vertex
        """

        # Initialise the adjacency list
        self.alist = [[u for u in neighbours] for neighbours in alist]
        # Set of vertices
        self.V = set(range(len(self.alist)))
        # Total number of vertices
        self.N = len(self.V)
        # Set of edges (represented as frozensets)
        self.E = set(
            [
                frozenset([i, j])
                for i, neighbours in enumerate(self.alist)
                for j in neighbours
            ]
        )
        # Degree of each vertex
        self.d = [len(neighbours) for neighbours in self.alist]


class Partition(object):

    def __init__(self, pi, G):
        """
        Initialise a Partition object

        Args:
        pi (list): a list of cells (each cell represented as a list of vertices)
        G: the graph associated with the partition.

        Attributes:
        pi (list): the list of cells
        G: the graph
        numberofcells (int): the total number of cells
        cellsizes (list): a list containing the size of each cell
        numberofelements (int): the total number of elements (vertices) in the partition
        IsRefined (bool): indicates whether the partition has been refined (None initially)
        celldegrees (list): stores the degrees of each cell to every other cell
        IsUnit (bool): true if the partition consists of single-element cells, False otherwise
        """
        self.pi = pi
        self.G = G
        self.numberofcells = len(pi)
        self.cellsizes = [len(x) for x in pi]
        self.numberofelements = sum(self.cellsizes)
        self.IsRefined = None  # getcelldegrees() replaces this
        self.celldegrees = self.getcelldegrees()
        if self.numberofcells == self.numberofelements:
            self.IsUnit = True
        else:
            self.IsUnit = False

        # IsRefined, IsUnit, cellsizes, celldegrees and numberofelements
        # should all be kept up to date by class functions.

    def __str__(self):
        """
        Return a string representation of the partition

        Example: [[0, 1] | [2, 3]]
        """
        return "[{}]".format(" | ".join(map(lambda x: str(x).strip("[]"), self.pi)))
        # return "[%s]" % ' | '.join(map(lambda x: str(x).strip('[]'),self.pi))
        # return "[%s]" % ''.join('|'.join(map(str,cell)) for cell in self.pi)
        # return "[%s]" % '|'.join(.join(map(str,self.pi))+']'

    def degree(self, u, V):
        """
        Calculate the number of neighbors of vertex u in cell V

        Args:
        u: vertex index
        V: cell (list of vertices)

        Returns:
        int: Number of neighbors.
        """
        return len([x for x in self.G.alist[u] if x in V])

    def getcelldegrees(self):
        """
        Compute the degrees of each cell with respect to every other cell

        Returns:
        list: a list of lists representing cell degrees
        """
        self.IsRefined = True  # Only updates if false
        degrees = []
        for cell in self.pi:
            u = cell[0]
            celldegrees = []
            for V in self.pi:
                celldegrees.append(self.degree(u, V))
            degrees.append(celldegrees)
            # Need to check whether same cell degrees for all vertices in cell,
            # if not should indicate that it needs refinement.
            # for u in cell:
            for node in cell:
                nodedegrees = []
                for V in self.pi:
                    nodedegrees.append(self.degree(node, V))
                if nodedegrees != celldegrees:
                    self.IsRefined = False
                    break
        # self.celldegrees=degrees
        return degrees

    def split(self, u, cell):
        """
        Split vertex u from the specified cell

        Args:
            u: vertex index
            cell: index of the cell to split

        Notes:
            Convention: put target nodes after the cell they were in
            Update the partition attributes
        """
        # Split node u from cell
        # Convention: put target nodes after cell they were in
        if u in self.pi[cell]:
            if len(self.pi[cell]) > 1:
                self.pi[cell].remove(u)
                self.pi = self.pi[: cell + 1] + [[u]] + self.pi[cell + 1 :]
                # Updates
                self.numberofcells = len(self.pi)
                self.cellsizes = [len(x) for x in self.pi]
                self.celldegrees = self.getcelldegrees()  # Sets IsRefined
                if self.numberofcells == self.numberofelements:
                    self.IsUnit = True
                else:
                    self.IsUnit = False
            else:
                print(self)
                print("Node {} is the only node in cell {}".format(u, cell))
        else:
            print("Node {} not in cell {}".format(u, cell))

    def refine(self, alpha):
        """
        McKay's refinement algorithm for partitioning

        Args:
            alpha (list): a list of cells (each cell represented as a list of vertices)

        Notes:
            Refine the partition by splitting cells based on vertex degrees
            Update partition attributes (IsRefined, numberofcells, cellsizes, celldegrees, IsUnit)
            Stop when either alpha is empty or the number of cells reaches N (largest vertex index + 1)
            Print a message if maximum iterations are reached

        Returns None
        """

        # Largest vertex index
        N = max([max(x) for x in self.G.alist]) + 1
        # M=len(alpha)

        count1 = 0
        while len(alpha) > 0 and len(self.pi) < N:
            W = alpha[0]
            alpha = alpha[1:]

            count2 = 0
            for X in self.pi:
                duW = [self.degree(u, W) for u in X]
                degs = set(duW)
                Xpartition = [[u for u in X if self.degree(u, W) == d] for d in degs]
                ind = self.pi.index(X)
                self.pi = self.pi[:ind] + Xpartition + self.pi[ind + 1 :]
                if X in alpha:
                    ind = alpha.index(X)
                    alpha = alpha[:ind] + Xpartition + alpha[ind + 1 :]
                else:
                    cellsizes = [len(x) for x in Xpartition]
                    maxcellsize = max(cellsizes)
                    ind = cellsizes.index(maxcellsize)
                    alpha = alpha + Xpartition[:ind] + Xpartition[ind + 1 :]
                count2 += 1
                if count2 > N:
                    print("Maxiumum iteration reached 2")
                    return
            count1 += 1
            if count1 > N:
                print("Maxiumum iteration reached 1")
                return

        # Keep all information up to date:
        self.IsRefined = True
        self.numberofcells = len(self.pi)
        self.cellsizes = [len(x) for x in self.pi]
        self.celldegrees = self.getcelldegrees()
        if self.numberofcells == self.numberofelements:
            self.IsUnit = True
        else:
            self.IsUnit = False


class OrderedPartitionPair(object):

    def __init__(self, pit, pib, G):
        """
        Initialise an OPP object

        Args:
            pit (list): a list of cells for the top partition
            pib (list): a list of cells for the bottom partition
            G: the graph associated with the partitions

        Attributes:
            t (Partition): the top partition
            b (Partition): the bottom partition
            G: the graph
            numberofelements (int): the total number of elements (vertices) in both partitions
            IsRefined (bool): True if both partitions are refined, False otherwise
            IsIsomorphic (bool): True if the partitions have the same cell sizes, False otherwise
            IsUnit (bool): True if both partitions consist of single-element cells, False otherwise
            IsEquitable (bool): True if the partitions are isomorphic and have equal cell degrees
        """
        # Ensures that this instance doesn't affect lists (of lists) pit and pib.
        self.t = Partition([[x for x in cell] for cell in pit], G)
        self.b = Partition([[x for x in cell] for cell in pib], G)
        self.G = G
        # self.numberofcells=[len(pit),len(pib)]
        # self.cellsizes=[[len(x) for x in pit],[len(x) for x in pib]]
        if self.t.numberofelements == self.b.numberofelements:
            self.numberofelements = self.t.numberofelements
        else:
            print("Number of elements not the same in top and bottom partitions!")
        self.IsRefined = self.t.IsRefined and self.b.IsRefined
        self.IsIsomorphic = self.t.cellsizes == self.b.cellsizes
        self.IsUnit = self.t.IsUnit and self.b.IsUnit
        self.IsEquitable = (
            self.IsIsomorphic and self.t.celldegrees == self.b.celldegrees
        )

    def __str__(self):
        """
        Return a string representation of the ordered partition pair

        Example: [[0, 1] | [2, 3]]\n[[4, 5] | [6, 7]]
        """
        st = "[%s]" % " | ".join(map(lambda x: str(x).strip("[]"), self.t.pi))
        sb = "[%s]" % " | ".join(map(lambda x: str(x).strip("[]"), self.b.pi))
        return st + "\n" + sb

    def split(self, ut, ub, cell):
        """
        Split vertices ut and ub from the specified cell

        Args:
            ut: vertex index in the top partition
            ub: vertex index in the bottom partition
            cell: index of the cell to split

        Notes:
            - Updates both partitions
            - Updates attributes (IsRefined, IsIsomorphic, IsUnit, IsEquitable)
        """
        if ut in self.t.pi[cell] and ub in self.b.pi[cell]:
            self.t.split(ut, cell)
            self.b.split(ub, cell)

            # Updates
            self.IsRefined = self.t.IsRefined and self.b.IsRefined
            self.IsIsomorphic = self.t.cellsizes == self.b.cellsizes
            self.IsUnit = self.t.IsUnit and self.b.IsUnit
            self.IsEquitable = (
                self.IsIsomorphic and self.t.celldegrees == self.b.celldegrees
            )
        else:
            if ub in self.b.pi[cell]:
                print("Node {} not in top cell {}".format(ut, cell))
            else:
                print("Node {} not in top cell {}".format(ub, cell))

    def refine(self):
        """
        Refine both partitions using McKay's refinement algorithm

        Notes:
            - Updates both partitions
            - Updates attributes (IsRefined, IsIsomorphic, IsUnit, IsEquitable)
        """
        if not self.t.IsRefined:
            self.t.refine([[x for x in cell] for cell in self.t.pi])
        if not self.b.IsRefined:
            self.b.refine([[x for x in cell] for cell in self.b.pi])
        # Updates
        self.IsRefined = self.t.IsRefined and self.b.IsRefined
        self.IsIsomorphic = self.t.cellsizes == self.b.cellsizes
        self.IsUnit = self.t.IsUnit and self.b.IsUnit
        self.IsEquitable = (
            self.IsIsomorphic and self.t.celldegrees == self.b.celldegrees
        )


def GetPermutation(OPP):
    """
    Get permutation from a Unit OPP
    Assume that vertices are labeled 0 to N-1
    """
    if OPP.IsUnit:
        # Initialise an array to store the permutation
        p = [-1] * OPP.numberofelements
        # Map elements from the first partition (OPP.t) to the second partition (OPP.b)
        for i in range(OPP.t.numberofcells):
            p[OPP.t.pi[i][0]] = OPP.b.pi[i][0]
        # Check if any element in the permutation remains unassigned
        if -1 in p:
            print("Ordered Partition Pair not formatted correctly:")
            print(OPP)
        return p
    else:
        print("Ordered Partition Pair is not unit")


def IsAutomorphism(G, p):
    # Take a graph G and a permutation p and test if p is an automorphism
    # Create a set of permuted edges based on the given permutation
    permutedE = set(
        [
            frozenset([p[i], p[j]])
            for i, neighbours in enumerate(G.alist)
            for j in neighbours
        ]
    )
    # Check if the permuted edges match the original edges of the graph
    return G.E == permutedE
