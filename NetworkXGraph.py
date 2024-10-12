import matplotlib.pyplot as plt
import networkx as nx


class NetworkXGraph:
    def __init__(self):
        return

    def createGraph(self, G, A):
        ##### Networkx ####
        g = nx.Graph()
        color_map = []
        for i in G.nodeIterator():
            g.add_node(i)
            if (A[i]): color_map.append("red") 
            else: color_map.append("blue")

            for j in G.outIterator(i):
                g.add_edge(i,j)
            for k in G.inIterator(i):
                g.add_edge(k,i)

        return g,color_map
    
    def pyvisGraph (self,g, A, model_session):
        from pyvis.network import Network
        nt = Network('600px', '100%')
        for i in g.nodes():
            if(A[i]):
                nt.add_node(i, label=str(i), color="red")
            else:
                nt.add_node(i, label=str(i), color="blue")
        for e in g.edges():
            nt.add_edge(e[0],e[1])  
        file_path = "Reports/Plots/pyvisNetwork-"+model_session+".html"      
        nt.write_html(file_path)
        return
    
    def graphStats(self, g):
        stats = {}
        stats["nodes"] = len(g.nodes())
        stats["edges"] = len(g.edges())
        stats["density"] = nx.density(g)
        stats["average_clustering"] = nx.average_clustering(g)
        return stats
    
    def createGraphPlot(self, g, color_map):              
        nx.draw(g, node_size=60,font_size=8, node_color=color_map)
        return plt
    
    def nodeBetweenness(self, g):
        return nx.betweenness_centrality(g)
    
    def nodeDegreeCentrality(self, g):
        return nx.degree_centrality(g)
    
    def nodeCloseness(self, g):
        return nx.closeness_centrality(g)
    
    def nodeEigenVectorCentrality(self, g):
        return nx.eigenvector_centrality(g)
