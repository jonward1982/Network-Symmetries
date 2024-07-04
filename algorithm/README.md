## Basic use of orbit representatives

### Counting graph colourings

A graph or network $\Gamma$ is a set of vertices $V$ connected together by a set of edges $E$ (i.e. pairs of vertices). Given a finite set of colours $W$, a colouring of a graph asigns a colour to each vertex, so is a function from the set of vertices to the set of colours. The set of all colourings is $\Omega=W^V$, i.e. the set of all functions from the set of vertices to the set of colours.

A graph symmetry or automorphism $g$ is a permutation of the vertices that leaves the graph unchanged, i.e. for $u,v\in V$ we have $(u,v)\in E$ if and only if $(gu,gv)\in E$. The automorphism group $G$ of a graph is the set of all of the graph's automorphisms.

An automorphism can act on a graph colouring by moving the colours. More precisely we define the action of an automorophism $g\in G$ on a colouring $S\in\Omega$ so that for $v\in V$ we have $gS(gv)=S(v)$. 

We are interested in counting colourings that are equivalent under the action of the automorphim group, i.e. for $S_1,S_2\in\Omega$, there is a $g\in G$ such that $S_1=gS_2$.

In this notebook, we will look at some of the that I have developed to do this. 

We start by setting up a graph. There is a class in the `OPP` module for graphs, so we start by loading this module.

```python
import OPPs # Orbit Partition Pairs
```

A graph can be created by specifying an adjacency list. An adjacency list comprises of lists of the neighbours of each vertex. First let's create a path graph with three vertices

```python
# adjacency list
alist=[[1],[0,2],[1]] 
```

So vertex 0 is connected to vertex 1, vertex 1 is connect to vertex 0 and vertex 2, and vertex 2 is connect to vertex 1. We create an instance of this graph from the OPPs module

```python
Gpath=OPPs.Graph(alist)
```

The graph object has attributes corresponding to the adjacency list `alist`, the set of vertices `V`, the number of vertices `N`, the set of edges `E` and the degree of each vertex `d`. Edges are frozensets:

```python
Gpath.E
```

There is only one automorphism of this graph (other than the identity), which corresponds to permuting vertices 0 and 2.

In the `OrbitRepresentatives` module, I have written code to produce "orbit representatives" for the case where there are just two colours. The set of orbit representatives is a set of colourings $R\subset\Omega$ so that for any colouring $c\in\Omega$ there is a $g\in G$ and $r\in\Omega$ such that $c=gr$, but also for any $r_1,r_2\in R$ there is no $g\in G$ such that $r_1=gr_2$. The number of orbit representatives is the number of possible distinct colourings.

```python
import OrbitRepresentatives as ORs
```

The function `OrbitRepresentatives` in the `ORs` class produces the set of orbit representatives but it needs to be passed the orbit partition of vertices. For the 3-vertex path graph considered here, vertices 0 and 2 are in the same orbit, and 1 is in its own orbit. We encode that in python as a list of lists:

```python
pi=[[0,2],[1]]
```

We can now produce the set of orbit representatives for the path graph with the `OrbitRepresentatives`, setting the verbose argument to `True`:

```python
Reps,tests,successes=ORs.OrbitRepresentatives(Gpath,pi,True)
```

The set of orbit representatives is:

```python
Reps
```

The only other possible colourings are `[0,0,1]` (which gets mapped to `[1,0,0]` by the non-trivial permutation) and `[1,1,0]` (which gets mapped to `[0,1,1]` by the non-trivial permutation).
