import OPPs
import Automorphisms
#import Automorphisms_Recursion as Automorphisms
import math

def InfectionSet(S):

    Ip=[]
    for i,u in enumerate(S):
        if u==0:
            cSu=[x for x in S]
            cSu[i]=1
            Ip.append(cSu)

    return Ip

def OrbitRepresentatives(G,pi,*args):
    
    if len(args)>0:
        verbose=args[0]        
    else:
        verbose=True
    
    if verbose:
        print('Computing Orbit Representatives')
        
    leveltests=[0]
    levelsuccesses=[0]
    
    Rm=[[0]*G.N]
    Reps=[[0]*G.N,[1]*G.N]
    for i in range(1,math.floor(G.N/2)+1):
        if verbose:
            print('\n^^^^^^^^^^^^^^^^^^^^')
            print('i={} infected nodes'.format(i))
        Rp=[]
        lcount=0
        scount=0
        Ip=[]
        for S in Rm:
            IpS=InfectionSet(S)
            Ip=Ip+[S for S in IpS if S not in Ip]

        for s in Ip:
            NotInRp=True
            for R in Rp:
                lcount+=1
                perm=Automorphisms.GetAutomorphism(s,R,G,pi,verbose)
                if verbose:
                    print('Permutation:')
                    print(perm)
                if perm!=None:
                    scount+=1
                    NotInRp=False
                    break
                #fi;
            #od;
            if NotInRp:
                Rp.append(s)
            #fi;
        #od;
    
        leveltests.append(lcount)
        levelsuccesses.append(scount)
        if i<G.N/2:
            #print(Rp)
            #Reps.extend([Rp,[[1-x for x in state] for state in Rp]])
            Reps=Reps+Rp+[[1-x for x in state] for state in Rp]
        else:
            Reps=Reps+Rp
        #fi;
        Rm=Rp
    #od;
    
    return Reps,leveltests,levelsuccesses

