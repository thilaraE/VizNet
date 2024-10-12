import sys
sys.path.insert(1,"ALAAMEE/python") ### Add the path to ALAAMEE/python directory here
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtCore import QSize
from Digraph import Digraph
from Graph import Graph
from utils import int_or_na,NA_VALUE
from NetworkXGraph import NetworkXGraph
import networkx as nx
import estimateALAAMSA_mod
from functools import partial
from changeStatisticsALAAMdirected import *
from changeStatisticsALAAM import changeDensity, changeoOc, param_func_to_label
from gof_stats import gof_funcs
import datetime





class AnalysisReport():
    def __init__(self):
        return

        
        
    def setHtmlContent(self, alaam_inputs):
        model_session = str(datetime.datetime.now()).split(".")[0].replace(" ", "-").replace(":","")
        directed = alaam_inputs["directed"]
        html_content = ""
        html_content += self.getHTMLHeader()

        outcome_bin_filename = alaam_inputs["outcome_bin_filename"]
        edgelist_filename = alaam_inputs["edgelist_filename"]

        if directed:
            G = Digraph(edgelist_filename) 
        else:
            G= Graph(edgelist_filename)

        outcome_binvar = list(map(int_or_na, open(outcome_bin_filename).read().split()[1:]))
        assert(len(outcome_binvar) == G.numNodes())
        A = outcome_binvar
        html_content += self.getDescriptiveAnalysis(G, directed, A, model_session)

        alaam_analysis , alaam_output = self.getALAAMSAAnalysis(model_session, alaam_inputs)
        html_content += alaam_analysis
        html_content += self.getInterpretations(alaam_output)
        html_content += self.getHTMLFooter()

        saving_file = "Reports/modelAnalysis-"+model_session+".html"       
        
        with open(saving_file, 'w') as f:
            f.write(html_content)
        return html_content

    def getHTMLFooter (self):
        html_footer = "</body></html>"        
        return html_footer
    
    def getHTMLHeader (self):
        html_header = "<html><head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"> <style> .scrollable-table { height: 300px; overflow-y: scroll; display: block; } .container {display: flex; justify-content: space-between; gap:20px;} table { width: 100%; border-collapse: collapse; } thead th { position: sticky; top: 0; background-color: #f1f1f1; padding: 8px; text-align: left; border: 1px solid #ddd;} td { border: 1px solid black; padding: 8px; text-align: left; } tbody tr:nth-child(even) {background-color: #ececec;} .bordered {border: 1px solid black; padding: 20px; margin: 10px;} .division1 { background-color: white; } .division2 { background-color: white; } .division3 { background-color: white; } .table-title {font-weight: bold; text-align: center; margin-bottom: 10px;} .bold-row {font-weight: bold;} .red-text { color: red; } .green-text { color: green; } .config-img {height: 40px; width: 50px;}</style></head><body><h1>SNA Report</h1>"
        return html_header

    def getDescriptiveAnalysis(self, G, directed, A, model_session):
        networkXGraph = NetworkXGraph()
        g, color_map =networkXGraph.createGraph(G, A)
        stats =networkXGraph.graphStats(g)
        node_betweenness = networkXGraph.nodeBetweenness(g)
        node_degree_centrality = networkXGraph.nodeDegreeCentrality(g)
        node_closeness = networkXGraph.nodeCloseness(g)
        node_eigenvector = networkXGraph.nodeEigenVectorCentrality(g)
        networkXGraph.pyvisGraph(g, A, model_session)
        descriptive_analysis = '<div class="bordered division1"><h2>Descriptive Analysis of the Network</h2><h3>Network Visualisation</h3>'
        graph_plot = self.createNetworkGraph(networkXGraph, g, color_map, model_session)
        graph_analysis = "<h3>Graph Analysis</h3><table border=\"1\"><tr><th>Number of Nodes</th><th>Number of Edges</th><th>Average Clustering Coefficient</th><th>Density</th></tr><tr><td>"+str(stats["nodes"])+"</td><td>"+str(stats["edges"])+"</td><td>"+str(stats["average_clustering"])+"</td><td>"+str(stats["density"])+"</td></tr></table>"
        
        if directed :
            node_analysis = "<h3>Individual Node Analysis</h3><div class=\"scrollable-table\"><table><thead><tr><th>Node ID</th><th>In-degree</th><th>Out-degree</th><th>Degree Centrality</th><th>Betweenness Centrality</th><th>Closeness Cenrality</th><th>Eigenvector Cenrality</th></tr></thead><tbody>"
        else:
            node_analysis = "<h3>Individual Node Analysis</h3><div class=\"scrollable-table\"><table><thead><tr><th>Node ID</th><th>Degree</th><th>Degree Centrality</th><th>Betweenness Centrality</th><th>Closeness Cenrality</th><th>Eigenvector Cenrality</th></tr></thead><tbody>"

        for i in G.nodeIterator():
            betweenness = str(round(node_betweenness[i],3))
            degree_centrality = str(round(node_degree_centrality[i],3))
            closeness = str(round(node_closeness[i],3))
            eigenvector_centrality = str(round(node_eigenvector[i],3))

            if directed:
                node_analysis += "<tr><td>"+str(i)+"</td><td>"+str(G.indegree(i))+"</td><td>"+str(G.outdegree(i))+"</td><td>"+degree_centrality+"</td><td>"+betweenness+"</td><td>"+closeness+"</td><td>"+eigenvector_centrality+"</td></tr>"
            else:
                node_analysis += "<tr><td>"+str(i)+"</td><td>"+str(G.degree(i))+"</td><td>"+degree_centrality+"</td><td>"+betweenness+"</td><td>"+closeness+"</td><td>"+eigenvector_centrality+"</td></tr>"
        node_analysis += "</tbody></table></div></div>"

        return descriptive_analysis+graph_plot+graph_analysis+node_analysis
    

    
    def getALAAMSAAnalysis(self, model_session, alaam_inputs):
        print(alaam_inputs)

        model_param_funcs = [changeDensity, changeSender, changeReceiver, changeContagion, changeReciprocity, changeContagionReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar, changeTransitiveTriangleT1, partial(changeoOc, "sport"), partial(changeoOc, "drugs"), partial(changeoOc, "alcohol")]


        output = estimateALAAMSA_mod.run_on_network_attr(
            alaam_inputs["edgelist_filename"],
            model_param_funcs,      #Adding temporary because parameters arent set from main form
           [param_func_to_label(f) for f in model_param_funcs], #Adding temporary because parameters arent set from main form
            alaam_inputs["outcome_bin_filename"],
            alaam_inputs["binattr_filename"],
            alaam_inputs["contattr_filename"],
            alaam_inputs["catattr_filename"],
            alaam_inputs["sampler_func"],
            alaam_inputs["zone_filename"],
            alaam_inputs["directed"],
            alaam_inputs["bipartite"],
            alaam_inputs["GoFiterationInStep"],
            alaam_inputs["GoFburnIn"],
            alaam_inputs["bipartiteGoFfixedMode"],
            alaam_inputs["add_gof_param_func_list"],
            alaam_inputs["outputGoFstatsFilename"],
            alaam_inputs["outputObsStatsFilename"]
        )

        directed = alaam_inputs["directed"]
        if directed :
            img_file_dir = "images/directed/"
        else :
            img_file_dir = "images/undirected/"

        alaam_analysis = '<div class="bordered division2"><h2>ALAAM Analysis of the Network</h2>'
        model_analysis = "<div class=\"container\"><div class=\"table-title\">Model Analysis</div><table border=\"1\" width='45%'><tr><th>Parameter</th><th>Configuration</th><th>Estimate</th><th>Std Error</th><th>t-ratio</th></tr>"
        
        for i in range(len(output["theta"])):
            
            if("oOc" in output["labels"][i]):
                image_path = img_file_dir + "oOc.png"
            elif ("oOb" in output["labels"][i]):
                image_path = img_file_dir + "oOb.png"
            else:
                image_path = img_file_dir + output["labels"][i] + ".png"

            if output["significant"][i]:
                model_analysis += "<tr class=\"bold-row\"><td>"+output["labels"][i]+"</td><td><img class=\"config-img\" src=\""+image_path+"\"</td><td>"+str(round(output["theta"][i],3))+"</td><td>"+str(round(output["std_error"][i],3))+"</td><td>"+str(round(output["t_ratio"][i],3))+'*'+"</td></tr>"
            else:
                model_analysis += "<tr><td>"+output["labels"][i]+"</td><td><img class=\"config-img\" src=\""+image_path+"\"</td><td>"+str(round(output["theta"][i],3))+"</td><td>"+str(round(output["std_error"][i],3))+"</td><td>"+str(round(output["t_ratio"][i],3))+"</td></tr>"

        model_analysis += "</table>"

        gof_analysis = "<div class=\"table-title\">Goodness of Fit</div><table border=\"1\" width='45%'><tr><th>Parameter</th><th>t-ratio</th></tr>"
        for j in range(output["gof_n"]):
            gof_analysis += "<tr><td>"+output["goflabels"][j]+"</td><td>"+str(round(output["gofresults"][j],3))+"</td></tr>"
        self.saveScatterPlots(model_session)
        saving_file = "Plots/scatterplot-"+model_session+".html" 

        gof_analysis += "</table></div><a href=\""+saving_file+"\" class=\"button\">Show GoF Stats</a></div>"

        return alaam_analysis+model_analysis+gof_analysis, output


    def getInterpretations(self, alaam_output):
        interpretations = '<div class="bordered division2"><h2>ALAAM Interpretations</h2>'
        significant_interpretations = "<div><table border=\"1\"><tr><th>Effect</th><th>Coef</th><th>Std Error</th><th>t-ratio</th><th>Interpretation</th></tr>"

        for i in range(len(alaam_output["theta"])):
            if alaam_output["significant"][i]:
                if (alaam_output["theta"][i] > 0):
                    significant_interpretations += "<tr class= \"green-text\"><td>"+alaam_output["labels"][i]+"</td><td>"+str(round(alaam_output["theta"][i],3))+"</td><td>"+str(round(alaam_output["std_error"][i],3))+"</td><td>"+str(round(alaam_output["t_ratio"][i],3))+"</td><td >POSITIVE EFFECT</td></tr>"
                else:
                    significant_interpretations += "<tr class= \"red-text\"><td>"+alaam_output["labels"][i]+"</td><td>"+str(round(alaam_output["theta"][i],3))+"</td><td>"+str(round(alaam_output["std_error"][i],3))+"</td><td>"+str(round(alaam_output["t_ratio"][i],3))+"</td><td >NEGATIVE EFFECT</td></tr>"

        significant_interpretations += "</table></div></div>"

        return interpretations+significant_interpretations

    def saveScatterPlots(self, model_session):
        import pandas as pd
        import matplotlib.pyplot as plt
        import base64
        from io import BytesIO
        import numpy as np


        # Read data from a file (assuming it's in CSV format)
        file_path = 'outputGoFstatsFile.txt'  # Replace with your file path
        df = pd.read_csv(file_path, delim_whitespace=True)
        observed = pd.read_csv("outputObsStatsFile.txt", delim_whitespace=True)
        observed_columns = observed.columns[:24]



        columns = df.columns[:23]  # Take the first 24 columns, or specify them as needed

        # Create 24 scatterplots
        plt.figure(figsize=(20, 20))  # Adjust figure size for better readability

        for i in range(22):
            plt.subplot(6, 4, i + 1)  # 6 rows, 4 columns to fit 24 plots
            plt.scatter(df[columns[0]], df[columns[(i + 1)]])
            plt.title(f'Scatter plot of {columns[0]} vs {columns[(i + 1) % len(columns)]}')
            plt.xlabel(columns[0])
            plt.ylabel(columns[(i + 1)])

            y_value = observed[columns[(i + 1)]].iloc[0]  # You can choose a different index or condition to select the point
    
            # Draw a horizontal line at the chosen y-value
            plt.axhline(y=y_value, color='red', linestyle='--', label=f'Line at y = {y_value:.2f}')
            plt.legend() 

        plt.tight_layout()  # Adjusts spacing to prevent overlap
        tmpfile = BytesIO()
        plt.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue())

        html_header = "<html><head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"></head><body><h1>GoF Statisctic Plots for each Iteration</h1>"
        scatterplot_html ='<img src="data:image/png;base64, {}"></a></div>'.format(encoded.decode('utf-8'))
        html_footer = "</body></html>"  

        saving_file = "Reports/Plots/scatterplot-"+model_session+".html"       
        
        with open(saving_file, 'w') as f:
            f.write(html_header+scatterplot_html+html_footer)
        return





    def createNetworkGraph(self, networkXGraph, g, color_map, model_session):
        import base64
        from io import BytesIO

        plt = networkXGraph.createGraphPlot(g, color_map)
        tmpfile = BytesIO()
        plt.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue())

        imgHtml ='<div style="text-align: center;"><a href="Plots/pyvisNetwork-'+model_session+'.html" target="_blank"><img src="data:image/png;base64, {}"></a></div>'.format(encoded.decode('utf-8'))
        return imgHtml


    def displayHtmlContent(self, html_content):
        # create a QWebEngineView widget
        self.web_view = QWebEngineView(self)
        self.web_view.setHtml(html_content)
        self.setFixedSize(QSize(974, 667))
        # set the widget as the main window's central widget
        self.setCentralWidget(self.web_view)


