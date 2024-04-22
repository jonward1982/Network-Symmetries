import OPPs

def GetAutomorphism(Si,Sj,G,pi,*args):
    '''Test for automorphism between (binary) states Si and Sj with graph G.
    Partition pi is orbit partition of vertices.
    Assume that vertices are labelled 0 to N-1 in G.'''

    if len(args)>0:
        verbose=args[0]
    else:
        verbose=True

    pit=[[u for u in cell if Si[u]==0] for cell in pi]+[[u for u in cell if Si[u]==1] for cell in pi]
    pib=[[u for u in cell if Sj[u]==0] for cell in pi]+[[u for u in cell if Sj[u]==1] for cell in pi]

    pit=[cell for cell in pit if len(cell)>0]
    pib=[cell for cell in pib if len(cell)>0]
    
    if verbose:
        print("\n_____________________")
        print("States:")
        print(Si)
        print(Sj)
        print("Partitions from states:")
        print(pit)
        print(pib)

    opp=OPPs.OrderedPartitionPair(pit,pib,G)

    perm=mapping(opp,verbose)

    return perm

class levelinformation(object):
    def __init__(self,opp,verbose):
        # Stored variables - set asside (roughly) right amount of memory:
        self.N=opp.G.N
        self.verbose=verbose
        self.levelpit=[[[-1 for i in range(opp.G.N)]]]*opp.G.N
        self.levelpib=[[[-1 for i in range(opp.G.N)]]]*opp.G.N
        self.levelcellind=[-1]*opp.G.N
        self.levelnodeind=[-1]*opp.G.N
        
        # Exit None flag
        self.returnnone=False
        
        # Set initial level, cell index and node index
        self.level=0
        for i,cell in enumerate(opp.t.pi):
            if len(cell)>1:
                break
        self.cellind=i
        self.nodeind=0
        
        # Set initial copy of current OPP partitions
        self.levelpit[self.level]=[[u for u in cell] for cell in opp.t.pi]
        self.levelpib[self.level]=[[u for u in cell] for cell in opp.b.pi]
        
    def resetlevel(self):
        if self.level>0:
            self.levelpit[self.level]=[[-1 for i in range(self.N)]]
            self.levelpib[self.level]=[[-1 for i in range(self.N)]]
            self.levelcellind[self.level]=-1
            self.levelnodeind[self.level]=-1
        else:
            print("!!!Trying to reset level 0 - something's gone wrong!!!")
    
    def nextnode_or_decreaselevel(self,opp):
        # New node/level
        stilllooking=True
        while stilllooking:
            if self.nodeind<len(opp.b.pi[self.cellind])-1:
                # Stay on same level and move on to the next vertex            
                self.nodeind+=1
                self.levelnodeind[self.level]=self.nodeind
                stilllooking=False
                if self.verbose:
                    print("Level {}. Next node is {}. OPP:".format(self.level,opp.b.pi[self.cellind][self.nodeind]))
                    print(opp)
            elif self.level>0:
                # Decrease level
                if self.verbose:
                    print("Decreasing level...")
                self.resetlevel()
                self.level-=1
                self.cellind=self.levelcellind[self.level]
                self.nodeind=self.levelnodeind[self.level]
                # This now continues the while loop and update nodeind as above
                # reset opp outside of this class
            else:
                # Have gotten to the last vertex in the level 0 cell
                if self.verbose:
                    print("Exhausted all possibilities.")
                # Exhausted all possibilities
                stilllooking=False
                self.returnnone=True
    
    def increaselevel(self,opp):
        # Only called when it is possible to increase level
        self.level+=1
        # Store the current OPP
        self.levelpit[self.level]=[[u for u in cell] for cell in opp.t.pi]
        self.levelpib[self.level]=[[u for u in cell] for cell in opp.b.pi]

        # Pick cell and vertex and store
        for i,cell in enumerate(opp.t.pi):
            if len(cell)>1:
                break

        self.cellind=i
        self.nodeind=0
        self.levelcellind[self.level]=self.cellind
        self.levelnodeind[self.level]=self.nodeind

    def create_opp(self,opp):
        # Reset the partition
        return OPPs.OrderedPartitionPair(self.levelpit[self.level],self.levelpib[self.level],opp.G)

def mapping(opp,verbose):
    
    if verbose:
        print("Starting mapping...")
    
    # Initial checking
    if not opp.IsRefined:
        opp.refine()
        if verbose:
            print("\nNeeds refining. Get:")        
            print(opp)
    
    if not opp.IsEquitable:
        if verbose:
            print("\nRefinement not equitable")
        return None

    if opp.IsUnit:
        perm=OPPs.GetPermutation(opp)
        if OPPs.IsAutomorphism(opp.G,perm):
            if verbose:
                print("\nFound automorphism")
                print(opp)
            return perm
            # If not an automorphism, then exit
        else:
            if verbose:
                print("Unit but not an automorphism - exiting")
            return None

    levelinfo=levelinformation(opp,verbose)
    
    count=0
    notdone=True
    
    # Main loop
    while notdone:
        # Safety count
        count+=1
        # Reset the partition
        opp=levelinfo.create_opp(opp)
        
        if verbose:
            print("\n*******************\n")
            print("Level {}, OPP:".format(levelinfo.level))
            print(opp)
        
        # Variables corresponding to the current cell and vertex
        u=opp.t.pi[levelinfo.cellind][0]
        v=opp.b.pi[levelinfo.cellind][levelinfo.nodeind]
        
        # Split the cell
        opp.split(u,v,levelinfo.cellind)
        if verbose:
            print("\nLevel {}. Mapping top vertex {} to bottom vertex {} in cell {}".format(levelinfo.level,u,v,levelinfo.cellind))
            print("Split OPP:")
            print(opp)
        
        # Refine if necessary
        if not opp.IsRefined:
            opp.refine()
            if verbose:
                print("\nNeeds refining. Get:")        
                print(opp)
        
        # Main tests.
        # (1) If unit, test if automorphism        
        if opp.IsUnit:
            perm=OPPs.GetPermutation(opp)
            if OPPs.IsAutomorphism(opp.G,perm):
                if verbose:
                    print("\nFound automorphism")
                    print(opp)
                return perm
            # If not an automorphism, then back track as far as necessary
            else:
                if verbose:
                    print("Unit but not an automorphism - backtrack")
                opp=levelinfo.create_opp(opp)
                levelinfo.nextnode_or_decreaselevel(opp)
                if levelinfo.returnnone:
                    return None

        elif opp.IsEquitable:
            # Since not unit, definitely not deepest level
            # To stop runaways, deepest possible level is N
            if levelinfo.level<opp.G.N:
                # Increase level
                if verbose:
                    print("Increasing level...")
                # Don't reset opp at new level
                # opp=levelinfo.create_opp(opp)
                levelinfo.increaselevel(opp)
                
        else:
            # Not equitable so choose a new vertex/go up a level
            opp=levelinfo.create_opp(opp)
            levelinfo.nextnode_or_decreaselevel(opp)
            
            if levelinfo.returnnone:
                # Exhausted all possibilities already printed
                return None  
            
            if verbose:
                print("Reset OPP, choose new vertex or go up a level")            
            
        
        if count>opp.G.N+1:
            print("Maximum loop count reached - check what's happening")
            return None
    
    print("While loop finished - check why")
    return None
