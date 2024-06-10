import Automorphisms
import math

def InfectionSet(S):
    '''
    Takes a state S (a list of 0's and 1's) and produces a list of states
    obtained by switching each 0 to a 1 in turn. 
    '''

    Ip=[]
    for i,u in enumerate(S):
        if u==0:
            cSu=[x for x in S]
            cSu[i]=1
            Ip.append(cSu)

    return Ip

def OrbitRepresentatives(G,pi,*args):
    '''
    Arguments: 
    graph G
    vertex partition pi
    *args - currently only expecting logical verbose
    '''
    
    # set verbose variable, default is True
    if len(args)>0:
        verbose=args[0]        
    else:
        verbose=True
    
    # Verbose message
    if verbose:
        print('Computing Orbit Representatives')
       
    # Counts of tests and successes at each level
    leveltests=[0]
    levelsuccesses=[0]
    
    # Initialise the orbit representatives
    Rm=[[0]*G.N]
    Reps=[[0]*G.N,[1]*G.N]
    # Loop to the floor of half the number of vertices
    for i in range(1,math.floor(G.N/2)+1):
        if verbose:
            print('\n^^^^^^^^^^^^^^^^^^^^')
            print('i={} infected nodes'.format(i))
        
        # Initialise the next level's orbit representatives
        Rp=[]
        
        # Counters
        lcount=0
        scount=0
        
        # Infection set of all orbit representatives in the previous level
        Ip=[]
        for S in Rm:
            IpS=InfectionSet(S)
            Ip=Ip+[S for S in IpS if S not in Ip]

        # Loop through infection set
        for s in Ip:
            NotInRp=True
            # Loop through next level's representatives and look for an automorphism
            for R in Rp:
                lcount+=1
                # Test for automorphism
                perm=Automorphisms.GetAutomorphism(s,R,G,pi,verbose)
                if verbose:
                    print('Permutation:')
                    print(perm)
                # If find automorphism, can stop looking for representative and don't need to add it
                if perm!=None:
                    scount+=1
                    NotInRp=False
                    break
            # If no automorphism, add to the next level's representatives
            if NotInRp:
                Rp.append(s)
    
        # Count infomation
        leveltests.append(lcount)
        levelsuccesses.append(scount)
        
        # Flip representatives found so far
        if i<G.N/2:
            Reps=Reps+Rp+[[1-x for x in state] for state in Rp]
        else:
            Reps=Reps+Rp
        # Update the level representatives
        Rm=Rp
    
    # Return orbit representatives and count data
    return Reps,leveltests,levelsuccesses

