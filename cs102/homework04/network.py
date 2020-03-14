from api import get_friends
import matplotlib.pyplot as plt
import networkx as nx
import time

def users_ids(user_id):
    for i in range(6):
        try:
            x = get_friends(user_id)
            link = x.json()['response']['items']
            return link
        except:
            x = 0.1
            time.sleep(x)
            x = x * 3
            continue

def get_network(users_id, as_edgelist=True):
    vertices = users_ids(users_id)
    edges = []
    for i in vertices:
        friends = users_ids(i)
        if friends:
            for k in vertices:
                if i == k:
                    continue
                try:
                    friends.remove(k)
                    if edges.count((k,i)) == 0:
                        edges.append((i,k))
                except:
                    continue
    print(len(vertices),len(edges))
    # создание графа
    g = nx.Graph()
    g.add_edges_from(edges)
    pos = nx.spring_layout(g, k = 30, iterations = 5000)
    nx.draw_networkx_nodes(g, pos, node_size=2, node_color='blue')
    nx.draw_networkx_edges(g, pos, width=0.2, edge_color='grey')
    nx.draw_networkx_labels(g, pos, font_size=2)
    plt.axis('off')
    plt.savefig('output.png', dpi=800)
    return 'готово'
print(get_network(120831486))
