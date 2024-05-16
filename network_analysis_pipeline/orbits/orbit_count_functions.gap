############################################
#
# Function to compute the number of state-space orbits
# rho using the OrbitsDomain function
# This constructs the full state-space so will not work for
# large n

rho_bin_orb_dom:=function(G,n)
# G is the group
# n is the number of vertices (the degree of the group)

local rho;

rho:=Length(OrbitsDomain(G,Tuples([0,1],n),Permuted));

return rho;

end;

############################################
#
# Function to compute the cycle number of a permutation of
# degree n

cyclenumber:=function(p,n)
# p is a permutation 
# n is the degree of the permutation

local cs,tot,m,x;

cs:=CycleStructurePerm(p);
m:=NrMovedPoints(p);

tot:=0;
for x in cs do
    if IsInt(x) then
       tot:=tot+x;
    fi;
od;

return tot+n-m;
end;

############################################
#
# Function to compute the number of state-space orbits
# rho using Polya Enumeration and the GAP function
# ConjugacyClasses.

rho_bin_polya:=function(G,N)
# G is the group
# N is the number of vertices (the degree of the group)

local cl,tot,c;

cl:=ConjugacyClasses(G);;
tot:=0;;
for c in cl do
    tot := tot + Size( c ) * 2 ^ cyclenumber( Representative( c ), N );;
od;

return tot/Order(G);
end;