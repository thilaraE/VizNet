#!/usr/bin/env python3
#
# File:    changeStatisticsALAAMbipartite.py
# Author:  Alex Stivala
# Created: August 2022
#
"""Functions to compute change statistics for ALAAM on bipartite
(two-mode) graphs (undirected). Each function takes a BipartiteGraph G and
outcome vector A and returns the change statistic for changing outcome
of node i to 1.

These functions take as their first parameter the type (mode) of the
node, either MODE_A or MODE_B (defined in BipartiteGraph.py).  So that
these functions have the same signature as the structural statistics,
use functools.partial() to create a function with the (G, A, i)
signature, e.g. partial(changeBipartiteDensity, MODE_B).

The attribute statistics take also as their second parameter the name
of the attribute to use, used as the key in the relevant attribute
dictionary in the Graph object. As described in
changeStatisticsALAAM.py, functools.partial() is also used to create a
function wih the (G, A, i) signature. Similarly for functions that
take a setting network, as also described in changeStatisticsALAAM.py.

In the function documentation here, a node shown as an asterisk "*"
here, denotes a node of the specified mode with the outcome attribute,
and if shown as "@" is a node of the other mode with the outcome
attibute.

A node shown as an lowercase "o" here, denotes a node of the other
(non-reference) node with or without the attribute, and a node shown
as lowercase "x" is an actor of the reference mode with or without the
outcome attribute. In summary:


 Mode       Outcome variable       Symbol
 =  mode    0 or 1                 x
 =  mode    1                      *
 != mode    0 or 1                 o
 != mode    1                      @

(The symbols are chosen so that * is a bit like a 'filled' x, and @ is a
bit like a 'filled' o).

Note since the network is bipartite, only nodes of different modes can
have an edge between them, i.e. we can have *--o, *--@, x--o, and
x--@, but not *--*, *--x, o--o, or o--@.

So in the functions, a node denoted * is the node i, which has the
supplied (reference) mode and is being changed from 0 to 1 on the
outcome variable. (Note there may be more than one such node, in which
case they will be structurally equivalent). So all the functions will
return 0 if the mode of node i is not equal to the supplied reference
mode.

The use of the mode parameter and functools.partial() avoids having to
implement two versions of every funciton, one for each mode. E.g.
instead of having to define both changeBipartiteActivityA(G, A, i) and
changeBipartiteActivityB(G, A, i) which check that G.bipartite_node_mode(i) ==
MODE_A and G.bipartite_node_mode(i) == MODE_B, respectively, we just
have the single function changeBipartiteActivity(mode, G, A, i), which
we can use via partial(changeBipartiteActivity, MODE_A) or
partial(changeBipartiteActivity, MODE_B).

The function documentaiton also shows the MPNet name for the
statistic, with [mode] for the relevant mode.
E.g. partial(changeBipartiteDensity, MODE_A) means density for node
type A, DesnityXA in MPNet.


See

  G. Daraganova and G. Robins. Autologistic actor attribute models. In
  D. Lusher, J. Koskinen, and G. Robins, editors, Exponential Random
  Graph Models for Social Networks, chapter 9, pages 102-114. Cambridge
  University Press, New York, 2013.

  G. Robins, P. Pattison, and P. Elliott. Network models for social
  influence processes. Psychometrika, 66(2):161-189, 2001.

  Stivala, A. (2023). Overcoming near-degeneracy in the autologistic 
  actor attribute model. arXiv preprint arXiv:2309.07338.
  https://arxiv.org/abs/2309.07338

  Stivala, A., Wang, P., & Lomi, A. (2023). ALAAMEE: Open-source
  software for fitting autologistic actor attribute
  models. Unpublished manuscript.

  Wang, P., Robins, G., & Pattison, P. (2009). PNet: A program for the
  simulation and estimation of exponential random graph
  models. University of Melbourne. http://www.melnet.org.au/s/PNetManual.pdf

  Wang, P., Robins, G., Pattison, P., & Koskinen, J. (2014). MPNet: A
  program for the simulation and estimation of exponential random
  graph models for multilevel networks. University of
  Melbourne. http://www.melnet.org.au/s/MPNetManual.pdf

  Wang, P., Stivala, A., Robins, G.,Pattison, P., Koskinen, J., &
  Lomi, A. (2022) PNet: Program for the simulation and estimation of
  exponential random graph models for multilevel networks.
  http://www.melnet.org.au/s/MPNetManual2022.pdf

"""

import math
import functools

from utils import NA_VALUE
from BipartiteGraph import BipartiteGraph
import changeStatisticsALAAM


def changeBipartiteDensity(mode, G, A, i):
    """
    change statistic for bipartite [outcome attribute] Density
    DensityX[mode]

    *
    """
    return 1 if G.bipartite_node_mode(i) == mode else 0


def changeBipartiteActivity(mode, G, A, i):
    """
    change statistic for bipartite Activity
    ActivityX[mode]

    *--o
    """
    return G.degree(i) if G.bipartite_node_mode(i) == mode else 0


def changeBipartiteEgoTwoStar(mode, G, A, i):
    """
    Change statistic for bipartite ego two-star
    EgoX-2Star[mode]

    o--*--o
    """
    return (changeStatisticsALAAM.changeTwoStar(G, A, i)
            if G.bipartite_node_mode(i) == mode else 0)


def changeBipartiteEgoThreeStar(mode, G, A, i):
    """
    Change statistic for bipartite ego three-star
    EgoX-3Star[mode]

      o
     /
    *--o
     \
      o
    """
    return (changeStatisticsALAAM.changeThreeStar(G, A, i)
            if G.bipartite_node_mode(i) == mode else 0)

def changeBipartiteAlterTwoStar1(mode, G, A, i):
    """
    Change statistic for bipartite alter two-star 1
    AlterX-2Star1[mode]

    x--o--*
    """
    return (changeStatisticsALAAM.changePartnerActivityTwoPath(G, A, i)
            if G.bipartite_node_mode(i) == mode else 0)


def changeBipartiteAlterTwoStar2(mode, G, A, i):
    """
    Change statistic for bipartite alter two-star 2
    AlterX-2Star2[mode]

    *--o--*
    """
    return (changeStatisticsALAAM.changeIndirectPartnerAttribute(G, A, i)
            if G.bipartite_node_mode(i) == mode else 0)



def changeBipartiteFourCycle1(mode, G, A, i):
    """
    Change statistic for bipartite four-cycle 1
    C4X-1[mode]

        o
       / \
      x   *
       \ /
        o
    """
    return (sum([(p := G.twoPathsMatrix.getValue(i, j)) * (p - 1) / 2
                 for j in G.twoPathsMatrix.rowNonZeroColumnsIterator(i)])
            if G.bipartite_node_mode(i) == mode else 0)


def changeBipartiteFourCycle2(mode, G, A, i):
    """
    Change statistic for bipartite four-cycle 2
    C4X-2[mode]

        o
       / \
      *   *
       \ /
        o
    """
    # uses assignment operator := introduced in Pyton 3.8

    return sum([(p := G.twoPathsMatrix.getValue(i, j)) * (p - 1) / 2
                for j in G.twoPathsMatrix.rowNonZeroColumnsIterator(i)
                if A[j] == 1]) if G.bipartite_node_mode(i) == mode else 0



def changeBipartiteGWActivity(mode, alpha, G, A, i):
    """
    change statistic for Geometrically Weighted Bipartite Activity

       o
      /
     *--o
      \ :
       o


    This is an ALAAM analogue of the geometrically weighted degree
    statistic defined by Equation (11) in:

    Snijders, T. A., Pattison, P. E., Robins, G. L., & Handcock,
    M. S. (2006). New specifications for exponential random graph
    models. Sociological methodology, 36(1), 99-153.

    See also Section 3 (pp. 219-222) in:

    Hunter, D. R. (2007). Curved exponential family models for social
    networks. Social networks, 29(2), 216-230.

    and the Remark on p. 222 of Hunter (2007) relating the GWD
    statistic defined there to that defined in Snijders et al. (2006),
    and both papers for the relationships between gwdegree and the
    alternating k-star statistic.

    alpha > 0 is the decay parameter controlling the geometric rate of
    decrease in the weights. For large alpha, the contribution of
    positive outcomes on higher degree nodes is decreased. As alpha goes
    to 0, increasing weight is placed on outcome vectors with positive
    outcome on high degree nodes.  See Sjniders et a. (2006) p. 112.

    Note lambda_s = exp(alpha)/(exp(alpha)-1) [p. 113 Snjders et al. 2006]
    and 1/lambda_s = exp(-theta_s) = 1 - exp(-alpha) [p. 222 Hunter 2007]
    theta_s = -log(1/lambda_s)
    alpha = -log(1 - 1/lambda_s)
    So for the "traditional" value of lambda = 2 we have
    alpha = -log(1 - 1/2) = -log(1/2) = log(2) =appox 0.69


    The purpose of this statistic is to try to avoid problems with
    near-degeneracy when using the Activity, Two-Star, Three-Star,
    etc. parameters, by instead using this parameter to model
    alternating k-stars or alternatively as in this parameterization,
    geometrically weighted degree distribution.

    Note that the change statistic for ERGM (described in those
    papers) is not the change statistic here for ALAAM. In ERGM,
    modeling the network (stars or degree distribution here) the
    change statistic is for adding an edge, and so involves counting
    the additional number of stars created by adding an extra edge.
    However for ALAAM, the network is fixed, and the change statistic
    is for switching the outcome of node i from 0 to 1, and hence the
    number of stars (or activity degree) at the node is 0 before the
    the switch, and hence the change statistic is just related to the
    number of stars at the node i. And hence this is just the
    contribution of the single term for i in Equation (11) of Snijders
    et al. (2007), which is a sum over all nodes.

    Reference:

     Stivala, A. (2023). Overcoming near-degeneracy in the autologistic 
     actor attribute model. arXiv preprint arXiv:2309.07338.
     https://arxiv.org/abs/2309.07338

    """
    return (math.exp(-alpha * G.degree(i)) if G.bipartite_node_mode(i) == mode
            else 0)


def changeBpAlterSameTwoStar1(mode, attrname, G, A, i):
    """
    Change statistic for bipartite alter two-star 1
    with matching categorical attribute attrname.

    {x}--o--{*}

    This is like changeBipartiteAlterTwoStar1 but with the additional
    requirement that the two nodes on the ends of the two-path have
    the same value of the categorical attribute.
    """
    return (changeStatisticsALAAM.changeSamePartnerActivityTwoPath(attrname, G, A, i)
            if G.bipartite_node_mode(i) == mode else 0)


def changeBpAlterDiffTwoStar1(mode, attrname, G, A, i):
    """
    Change statistic for bipartite alter two-star 1
    with mismatching categorical attribute attrname.

    {x}--o--<*>

    This is like changeBipartiteAlterTwoStar1 but with the additional
    requirement that the two nodes on the ends of the two-path have
    different values of the categorical attribute.
    """
    return (changeStatisticsALAAM.changeDiffPartnerActivityTwoPath(attrname, G, A, i)
            if G.bipartite_node_mode(i) == mode else 0)



def changeBpAlterSameTwoStar2(mode, attrname, G, A, i):
    """Change statistic for bipartite alter two-star 2
    with matching categorical attribute attrname.

    {*}--o--{*}

    This is like changeBiparxtiteAlterTwoStar2 but with the additional
    requirement that the two nodes on the ends of the two-path have the
    same value of the named categorical attribute.

    """
    return (changeStatisticsALAAM.changeSameIndirectPartnerAttribute(attrname, G, A, i)
            if G.bipartite_node_mode(i) == mode else 0)


def changeBpAlterDiffTwoStar2(mode, attrname, G, A, i):
    """Change statistic for bipartite alter two-star 2
    with mismatching categorical attribute attrname.

    {*}--o--<*>

    This is like changeBiparxtiteAlterTwoStar2 but with the additional
    requirement that the two nodes on the ends of the two-path have
    different values of the named categorical attribute.

    """
    return (changeStatisticsALAAM.changeDiffIndirectPartnerAttribute(attrname, G, A, i)
            if G.bipartite_node_mode(i) == mode else 0)



def changeBpAlterBinaryTwoStar1(mode, attrname, G, A, i):
    """Change statistic for bipartite alter two-star 1 with binary
    attribute on central node.

    x--[o]--*

    This is like changeBipartiteAlterTwoStar1 but with the additional
    requirement that the node (of the other mode) in the center of the
    two-path (star) has the supplied binary attribute attrname true.

    """
    return (changeStatisticsALAAM.changeAlterBinaryTwoStar1(attrname, G, A, i)
            if G.bipartite_node_mode(i) == mode else 0)


def changeBpAlterBinaryTwoStar2(mode, attrname, G, A, i):
    """Change statistic for bipartite alter two-star 2
    with binary attribute on central node.

    *--[o]--*

    This is like changeBiparxtiteAlterTwoStar2 but with the additional
    requirement that the node (of the other mode) in the center of  the
    two-path (star) has the supplied binary attribute attrname true.

    """
    return (changeStatisticsALAAM.changeAlterBinaryTwoStar2(attrname, G, A, i)
            if G.bipartite_node_mode(i) == mode else 0)



# ================== old versions for regression testing ======================

def changeBipartiteAlterTwoStar1_SLOW(mode, G, A, i):
    """
    Change statistic for bipartite alter two-star 1
    AlterX-2Star1[mode]

    x--o--*
    """
    # # different (less efficient) implementation using twoPath as done in MPNet
    # delta2 = 0
    # if G.bipartite_node_mode(i) == mode:
    #     for v in G.nodeModeIterator(mode):
    #         delta2 += G.twoPaths(i, v)

    # one-liner more elegant but still inefficient version:
    delta3 = sum([G.twoPaths(i, v)  for v in G.nodeModeIterator(mode)]) if G.bipartite_node_mode(i) == mode else 0
            
    # assert delta2 == delta3
    return delta3

def changeBipartiteAlterTwoStar2_SLOW(mode, G, A, i):
    """
    Change statistic for bipartite alter two-star 2
    AlterX-2Star2[mode]

    *--o--*
    """
    # different (less efficient) implementation using twoPath as done in MPNet
    delta2 = 0
    # if G.bipartite_node_mode(i) == mode:
    #     for v in G.nodeModeIterator(mode):
    #         if A[v] == 1:
    #             delta2 += G.twoPaths(i, v)

    # one-liner more elegant but still inefficient version:
    delta3 = sum([G.twoPaths(i, v) if A[v] == 1 else 0  for v in G.nodeModeIterator(mode)]) if G.bipartite_node_mode(i) == mode else 0
    
    #assert delta2 == delta3
    return delta3

def changeBipartiteFourCycle1_OLD(mode, G, A, i):
    """
    Change statistic for bipartite four-cycle 1
    C4X-1[mode]

        o
       / \
      x   *
       \ /
        o
    """
    # different mplementation using twoPath as done in MPNet
    if G.bipartite_node_mode(i) == mode:
        delta = 0
        for v in G.nodeModeIterator(mode):
            twoPathCount = G.twoPaths(i, v)
            delta += twoPathCount * (twoPathCount - 1) / 2
        return delta
    else:
        return 0

# @functools.cache # Memoize the following function (Python 3.9)
def changeBipartiteFourCycle1_OLD2(mode, G, i):
    """
    Does not have numpy array A as parameter (not hashable), so we
    can use functools.cache
    
    Change statistic for bipartite four-cycle 1
    C4X-1[mode]

        o
       / \
      x   *
       \ /
        o
    """
    # uses assignment operator := introduced in Pyton 3.8
    delta = sum(
        [(twoPathCount := G.twoPaths(i,v)) * (twoPathCount - 1) / 2 for
         v in G.nodeModeIterator(mode)]
    ) if G.bipartite_node_mode(i) == mode else 0
    # delta_OLD = changeBipartiteFourCycle1_OLD(mode, G, A, i)
    # assert delta == delta_OLD
    return delta
    

def changeBipartiteFourCycle2_OLD(mode, G, A, i):
    """
    Change statistic for bipartite four-cycle 2
    C4X-2[mode]

        o
       / \
      *   *
       \ /
        o
    """
    # different mplementation using twoPath as done in MPNet
    if G.bipartite_node_mode(i) == mode:
        delta = 0
        for v in G.nodeModeIterator(mode):
            if (A[v] == 1):
                twoPathCount = G.twoPaths(i, v)
                delta += twoPathCount * (twoPathCount - 1) / 2
        return delta
    else:
        return 0
    
