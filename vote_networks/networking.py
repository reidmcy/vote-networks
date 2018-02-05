import networkx as nx

def makeLikeNetwork(targetRepo):
    G = nx.DiGraph()
    for issue in targetRepo.issues:
        for response in issue.reactions:
            if (response.actor, issue.actor) not in G.edges:
                G.add_edge(response.actor, issue.actor, weight = 1)
            else:
                G.edges[response.actor, issue.actor]['weight'] += 1
    return G

def mergeGraphs(*graphs):
    G = nx.DiGraph()
    for g in graphs:
        G.add_nodes_from(g)
        for n1, n2, dat in g.edges(data = True):
            if (n1, n2) in G:
                G.edges[n1, n2]['weight'] += dat['weight']
            else:
                G.add_edge(n1, n2, **dat)
    return G

