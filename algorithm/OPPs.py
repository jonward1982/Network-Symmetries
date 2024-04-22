class Graph(object):
    
    def __init__(self,alist):
        self.alist=[[u for u in neighbours] for neighbours in alist]
        self.V=set(range(len(self.alist)))
        self.N=len(self.V)
        self.E=set([frozenset([i,j]) for i,neighbours in enumerate(self.alist) for j in neighbours])
        self.d=[len(neighbours) for neighbours in self.alist]

class Partition(object):
    
    def __init__(self,pi,G):
        self.pi=pi
        self.G=G
        self.numberofcells=len(pi)
        self.cellsizes=[len(x) for x in pi]
        self.numberofelements=sum(self.cellsizes)
        self.IsRefined=None # getcelldegrees() replaces this
        self.celldegrees=self.getcelldegrees()
        if self.numberofcells==self.numberofelements:
            self.IsUnit=True
        else:
            self.IsUnit=False
        
        # IsRefined, IsUnit, cellsizes, celldegrees and numberofelements
        # should all be kept up to date by class functions.
        
    def __str__(self):
        return '[{}]'.format(' | '.join(map(lambda x: str(x).strip('[]'),self.pi)))
        # return "[%s]" % ' | '.join(map(lambda x: str(x).strip('[]'),self.pi))
        # return "[%s]" % ''.join('|'.join(map(str,cell)) for cell in self.pi)
        # return "[%s]" % '|'.join(.join(map(str,self.pi))+']'
        
    def degree(self,u,V):
        """Number of neighbours of u in V"""
        return len([x for x in self.G.alist[u] if x in V])
        
    def getcelldegrees(self):
        """Compute degrees of each cell to each other cell"""
        self.IsRefined=True # Only updates if false        
        degrees=[]
        for cell in self.pi:
            u=cell[0]
            celldegrees=[]
            for V in self.pi:                    
                celldegrees.append(self.degree(u,V))
            degrees.append(celldegrees)
            # Need to check whether same cell degrees for all vertices in cell, 
            # if not should indicate that it needs refinement. 
            # for u in cell:                
            for node in cell:
                nodedegrees=[]
                for V in self.pi:
                    nodedegrees.append(self.degree(node,V))
                if nodedegrees!=celldegrees:
                    self.IsRefined=False
                    break
        # self.celldegrees=degrees
        return degrees            
        
    def split(self,u,cell):
        # Split node u from cell
        # Convention: put target nodes after cell they were in
        if u in self.pi[cell]:
            if  len(self.pi[cell])>1:
                self.pi[cell].remove(u)
                self.pi=self.pi[:cell+1]+[[u]]+self.pi[cell+1:]
                # Updates
                self.numberofcells=len(self.pi)
                self.cellsizes=[len(x) for x in self.pi]
                self.celldegrees=self.getcelldegrees() # Sets IsRefined
                if self.numberofcells==self.numberofelements:
                    self.IsUnit=True
                else:
                    self.IsUnit=False
            else:
                print(self)
                print('Node {} is the only node in cell {}'.format(u,cell))
        else:
            print("Node {} not in cell {}".format(u,cell))
            
        
    def refine(self,alpha):
        """McKay's refinement algorithm"""
        
        # Largest vertex index
        N=max([max(x) for x in self.G.alist])+1
        # M=len(alpha)

        count1=0
        while len(alpha)>0 and len(self.pi)<N:
            W=alpha[0]
            alpha=alpha[1:]

            count2=0
            for X in self.pi:
                duW=[self.degree(u,W) for u in X]
                degs=set(duW)
                Xpartition=[[u for u in X if self.degree(u,W)==d] for d in degs]
                ind=self.pi.index(X)
                self.pi=self.pi[:ind]+Xpartition+self.pi[ind+1:]
                if X in alpha:
                    ind=alpha.index(X)
                    alpha=alpha[:ind]+Xpartition+alpha[ind+1:]                
                else:
                    cellsizes=[len(x) for x in Xpartition]
                    maxcellsize=max(cellsizes)
                    ind=cellsizes.index(maxcellsize)
                    alpha=alpha+Xpartition[:ind]+Xpartition[ind+1:]                
                count2+=1
                if count2>N:
                    print('Maxiumum iteration reached 2')
                    return
            count1+=1
            if count1>N:
                print('Maxiumum iteration reached 1')
                return
            
        # Keep all information up to date:
        self.IsRefined=True
        self.numberofcells=len(self.pi)
        self.cellsizes=[len(x) for x in self.pi]
        self.celldegrees=self.getcelldegrees()
        if self.numberofcells==self.numberofelements:
            self.IsUnit=True
        else:
            self.IsUnit=False

class OrderedPartitionPair(object):
    
    def __init__(self,pit,pib,G):
        # Ensures that this instance doesn't affect lists (of lists) pit and pib.
        self.t=Partition([[x for x in cell] for cell in pit],G)
        self.b=Partition([[x for x in cell] for cell in pib],G)
        self.G=G
        # self.numberofcells=[len(pit),len(pib)]
        # self.cellsizes=[[len(x) for x in pit],[len(x) for x in pib]]
        if self.t.numberofelements==self.b.numberofelements:
            self.numberofelements=self.t.numberofelements
        else:
            print('Number of elements not the same in top and bottom partitions!')        
        self.IsRefined=self.t.IsRefined and self.b.IsRefined
        self.IsIsomorphic=self.t.cellsizes==self.b.cellsizes
        self.IsUnit=self.t.IsUnit and self.b.IsUnit
        self.IsEquitable=self.IsIsomorphic and self.t.celldegrees==self.b.celldegrees    
        
    def __str__(self):
        st="[%s]" % ' | '.join(map(lambda x: str(x).strip('[]'),self.t.pi))
        sb="[%s]" % ' | '.join(map(lambda x: str(x).strip('[]'),self.b.pi))
        return st+'\n'+sb
        
    def split(self,ut,ub,cell):
        if ut in self.t.pi[cell] and ub in self.b.pi[cell]:
            self.t.split(ut,cell)
            self.b.split(ub,cell)
            
            # Updates
            self.IsRefined=self.t.IsRefined and self.b.IsRefined
            self.IsIsomorphic=self.t.cellsizes==self.b.cellsizes
            self.IsUnit=self.t.IsUnit and self.b.IsUnit
            self.IsEquitable=self.IsIsomorphic and self.t.celldegrees==self.b.celldegrees 
        else:
            if ub in self.b.pi[cell]:
                print('Node {} not in top cell {}'.format(ut,cell))
            else:
                print('Node {} not in top cell {}'.format(ub,cell))
    
    def refine(self):
        if not self.t.IsRefined:
            self.t.refine([[x for x in cell] for cell in self.t.pi])
        if not self.b.IsRefined:
            self.b.refine([[x for x in cell] for cell in self.b.pi])
        # Updates
        self.IsRefined=self.t.IsRefined and self.b.IsRefined
        self.IsIsomorphic=self.t.cellsizes==self.b.cellsizes
        self.IsUnit=self.t.IsUnit and self.b.IsUnit
        self.IsEquitable=self.IsIsomorphic and self.t.celldegrees==self.b.celldegrees

def GetPermutation(OPP):
    # Gets permutation from a Unit OPP
    # Assumes that vertices are labelled 0 to N-1
    if OPP.IsUnit:
        p=[-1]*OPP.numberofelements
        for i in range(OPP.t.numberofcells):
            p[OPP.t.pi[i][0]]=OPP.b.pi[i][0]
        if -1 in p:
            print('Ordered Partition Pair not formatted correctly:')
            print(OPP)
        return p
    else:
        print('Ordered Partition Pair is not unit')

def IsAutomorphism(G,p):
    # Take a graph G and a permutation p and test if p is an automorphism
    
    permutedE=set([frozenset([p[i],p[j]]) for i,neighbours in enumerate(G.alist) for j in neighbours])
    return G.E==permutedE
