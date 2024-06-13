import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def creationGraphe(M, wifeList, husbandList):
    G = nx.DiGraph()

    # Add all nodes to the graph before defining the edges
    all_nodes = set(wifeList + husbandList)
    G.add_nodes_from(all_nodes)

    # Définition des arêtes
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j] != float('inf'):
                wife_name = wifeList[i]
                husband_name = husbandList[j]
                G.add_edge(wife_name, husband_name, weight=M[i][j])

    # Créer un layout personnalisé pour placer les wives à gauche et les husbands à droite
    pos = {}
    num_wives = len(wifeList)
    num_husbands = len(husbandList)
    wife_spacing = 2.0 / (num_wives + 1)
    husband_spacing = 2.0 / (num_husbands + 1)

    # Positionner les wives à gauche
    for i, wife in enumerate(wifeList):
        pos[wife] = (-1, wife_spacing * (i + 1) - 1)

    # Positionner les husbands à droite
    for j, husband in enumerate(husbandList):
        pos[husband] = (1, husband_spacing * (j + 1) - 1)

    # Dessiner les nœuds avec des couleurs différentes pour wives et husbands
    nx.draw_networkx_nodes(G, pos, nodelist=wifeList, node_color='lightblue', node_size=700, label='Wives')
    nx.draw_networkx_nodes(G, pos, nodelist=husbandList, node_color='lightgreen', node_size=700, label='Husbands')

    # Définir les arêtes droites et courbes
    edges = G.edges()
    straight_edges = [(u, v) for (u, v) in edges if u != v]
    curved_edges = [(u, v) for (u, v) in edges if u == v]

    # Dessiner les arêtes droites
    nx.draw_networkx_edges(G, pos, edgelist=straight_edges, width=2, arrowsize=20)

    # Dessiner les arêtes courbes avec un angle de courbure spécifié
    arc_rad = 0.2  # Ajuster l'angle de courbure si nécessaire
    for edge in curved_edges:
        nx.draw_networkx_edges(G, pos, edgelist=[edge], width=2, arrowsize=20, connectionstyle=f'arc3, rad={arc_rad}')

    # Dessiner les étiquettes des nœuds
    nx.draw_networkx_labels(G, pos, labels={node: node for node in all_nodes}, font_size=15, font_family="sans-serif")

    # Ajouter une légende sans chevauchement
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=2, fontsize=12)

    # Ajustements des marges et suppression des axes
    plt.margins(0.2)
    plt.axis("off")
    plt.tight_layout(pad=2)
    plt.show()
