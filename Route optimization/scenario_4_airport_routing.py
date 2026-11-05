import os
import sys
import json
import time
import math
import heapq
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import contextily as ctx
import ssl
import urllib3

# Fix SSL Certificate issues on Windows globally
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
requests.packages.urllib3.disable_warnings()

# Monkeypatch requests to bypass SSL for contextily
import requests.sessions
old_request = requests.sessions.Session.request
def new_request(*args, **kwargs):
    kwargs['verify'] = False
    return old_request(*args, **kwargs)
requests.sessions.Session.request = new_request

ox.settings.requests_kwargs = {'verify': False}

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = BASE_DIR
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print(" FINAL YEAR PROJECT: SCENARIO 4 - AIRPORT HIGHWAY DETOUR ")
print("=" * 80)

print("\n[1/4] Downloading North Bangalore Graph (KIAL Airport to City)...")
# North Bangalore Bounding Box
north, south, east, west = 13.23, 13.01, 77.72, 77.57
bbox = (west, south, east, north)

try:
    bus_corridor_filter = (
        '["highway"~"motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link"]'
        '["area"!="yes"]["access"!~"private"]'
    )
    G = ox.graph_from_bbox(bbox=bbox, custom_filter=bus_corridor_filter)
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)
    print(f"  -> Graph downloaded successfully! Nodes: {len(G.nodes):,}, Edges: {len(G.edges):,}")
except Exception as e:
    print(f"Error downloading graph: {e}")
    sys.exit(1)

def get_nearest_node(lat, lon):
    return ox.distance.nearest_nodes(G, X=lon, Y=lat)

STOPS = {
    'KIAL_Airport': {'lat': 13.1989, 'lon': 77.7068},
    'Hebbal': {'lat': 13.0358, 'lon': 77.5970},
}

print("  -> Resolving GPS coordinates to OSM Nodes...")
nodes = {}
for name, coords in STOPS.items():
    nodes[name] = get_nearest_node(coords['lat'], coords['lon'])

# ---------------------------------------------------------
# 2. ALGORITHMS
# ---------------------------------------------------------
def haversine(node1, node2, graph):
    lat1, lon1 = graph.nodes[node1]['y'], graph.nodes[node1]['x']
    lat2, lon2 = graph.nodes[node2]['y'], graph.nodes[node2]['x']
    R = 6371.0 
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return (R * c) / 45.0 * 3600 

def run_dijkstra(graph, start, goal, weight='travel_time'):
    start_time = time.perf_counter()
    distances = {n: float('inf') for n in graph.nodes}
    distances[start] = 0
    previous = {n: None for n in graph.nodes}
    pq = [(0, start)]
    explored = set()
    
    while pq:
        curr_dist, curr = heapq.heappop(pq)
        explored.add(curr)
        if curr == goal: break
        if curr_dist > distances[curr]: continue
            
        for neighbor in graph.neighbors(curr):
            edge_data = graph.get_edge_data(curr, neighbor)
            min_weight = min([d.get(weight, 1.0) for d in edge_data.values()])
            dist = curr_dist + min_weight
            if dist < distances[neighbor]:
                distances[neighbor] = dist
                previous[neighbor] = curr
                heapq.heappush(pq, (dist, neighbor))
                
    path = []
    curr = goal
    while curr is not None:
        path.append(curr)
        curr = previous[curr]
    path.reverse()
    latency_ms = (time.perf_counter() - start_time) * 1000
    return path, distances[goal], latency_ms, explored

def run_astar(graph, start, goal, weight='travel_time'):
    start_time = time.perf_counter()
    g_score = {n: float('inf') for n in graph.nodes}
    g_score[start] = 0
    f_score = {n: float('inf') for n in graph.nodes}
    f_score[start] = haversine(start, goal, graph)
    
    previous = {n: None for n in graph.nodes}
    open_set = [(f_score[start], start)]
    explored = set()
    
    while open_set:
        _, curr = heapq.heappop(open_set)
        explored.add(curr)
        if curr == goal: break
            
        for neighbor in graph.neighbors(curr):
            edge_data = graph.get_edge_data(curr, neighbor)
            min_weight = min([d.get(weight, 1.0) for d in edge_data.values()])
            tentative_g = g_score[curr] + min_weight
            if tentative_g < g_score[neighbor]:
                previous[neighbor] = curr
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + haversine(neighbor, goal, graph)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                
    path = []
    curr = goal
    while curr is not None:
        path.append(curr)
        curr = previous[curr]
    path.reverse()
    latency_ms = (time.perf_counter() - start_time) * 1000
    return path, g_score[goal], latency_ms, explored

def plot_route_with_metrics(graph, actual_route, optimized_route, explored_nodes, blocked_nodes, filename, title, metrics, is_astar, origin_name, dest_name):
    fig, ax = ox.plot_graph(graph, show=False, close=False, node_size=0, edge_color='#666666', edge_linewidth=0.5, edge_alpha=0.3, bgcolor='none')
    
    if explored_nodes:
        search_color = '#3498db' if is_astar else '#e74c3c'
        nc = ['none' if n not in explored_nodes else search_color for n in graph.nodes]
        ns = [0 if n not in explored_nodes else 8 for n in graph.nodes]
        ox.plot_graph(graph, ax=ax, show=False, close=False, node_color=nc, node_size=ns, edge_linewidth=0, bgcolor='none', node_alpha=0.15)
    
    # Highlight the blocked highway in RED
    if blocked_nodes:
        blocked_lats = [graph.nodes[n]['y'] for n in blocked_nodes]
        blocked_lons = [graph.nodes[n]['x'] for n in blocked_nodes]
        ax.plot(blocked_lons, blocked_lats, color='red', linewidth=8, alpha=0.8, zorder=5)
        # Add 'Accident Zone' text
        mid_idx = len(blocked_nodes) // 2
        ax.text(blocked_lons[mid_idx], blocked_lats[mid_idx], ' MASSIVE ACCIDENT ', color='white', 
                backgroundcolor='red', fontsize=10, fontweight='bold', zorder=12, ha='center')

    # Plot Optimized Detour Route (Green)
    if optimized_route:
        ox.plot_graph_route(graph, optimized_route, ax=ax, route_color='#2ecc71', route_linewidth=6, route_alpha=1, show=False, close=False)
        
    start_lat, start_lon = graph.nodes[optimized_route[0]]['y'], graph.nodes[optimized_route[0]]['x']
    end_lat, end_lon = graph.nodes[optimized_route[-1]]['y'], graph.nodes[optimized_route[-1]]['x']
    
    ax.scatter([start_lon, end_lon], [start_lat, end_lat], c=['blue', 'orange'], s=200, zorder=10, edgecolors='white', linewidths=2)
    
    bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=2, alpha=0.9)
    ax.annotate(origin_name, (start_lon, start_lat), xytext=(-20, 25), textcoords='offset points', 
                fontsize=11, fontweight='bold', bbox=bbox_props, zorder=11, ha='center')
    ax.annotate(dest_name, (end_lon, end_lat), xytext=(20, -30), textcoords='offset points', 
                fontsize=11, fontweight='bold', bbox=bbox_props, zorder=11, ha='center')
    
    try:
        ctx.add_basemap(ax, crs="EPSG:4326", source=ctx.providers.Esri.WorldStreetMap, alpha=0.6)
    except Exception as e:
        print(f"Warning: Could not add basemap: {e}")
    
    textstr = f"{title}\n"
    textstr += "-"*30 + "\n"
    textstr += f"Algorithm: {'A* Search' if is_astar else 'Dijkstra'}\n"
    textstr += f"Scheduled Time: {metrics['actual_time']:.1f} mins\n"
    textstr += f"Optimized Time: {metrics['opt_time']:.1f} mins\n"
    textstr += f"Time Saved: {metrics['saved_time']:.1f} mins\n"
    textstr += f"Latency: {metrics['latency']:.2f} ms\n"
    textstr += f"Nodes Searched: {metrics['nodes_searched']:,}"
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.95, edgecolor='black', linewidth=2)
    ax.text(0.02, 0.02, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='bottom', color='black', bbox=props, fontweight='bold', zorder=12)
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)

# ---------------------------------------------------------
# 3. RUNNING SCENARIO 4
# ---------------------------------------------------------
print("\n[2/4] Simulating NH44 Highway Accident (Vayu Vajra Bus)...")
G_S4 = G.copy()

# Step 1: Find the normal, clear-highway route
normal_path, _, _, _ = run_astar(G, nodes['KIAL_Airport'], nodes['Hebbal'])

# Step 2: Simulate a massive accident on the middle of the highway
# We take the middle 40% of the highway route and multiply travel time by 200x
path_len = len(normal_path)
start_block = int(path_len * 0.3)
end_block = int(path_len * 0.7)
blocked_nodes = normal_path[start_block:end_block]

for u, v in zip(blocked_nodes[:-1], blocked_nodes[1:]):
    if G_S4.has_edge(u, v):
        G_S4[u][v][0]['travel_time'] *= 200

# Calculate what the time would be if the bus stayed on the scheduled highway
congested_time_sec = sum(G_S4[u][v][0]['travel_time'] for u, v in zip(normal_path[:-1], normal_path[1:]) if G_S4.has_edge(u, v))

print("\n[3/4] Running A* and Dijkstra for Detour...")
a_path, a_time_sec, a_lat, a_exp = run_astar(G_S4, nodes['KIAL_Airport'], nodes['Hebbal'])
d_path, d_time_sec, d_lat, d_exp = run_dijkstra(G_S4, nodes['KIAL_Airport'], nodes['Hebbal'])

metrics_a = {'actual_time': congested_time_sec/60, 'opt_time': a_time_sec/60, 'saved_time': (congested_time_sec - a_time_sec)/60, 'latency': a_lat, 'nodes_searched': len(a_exp)}
metrics_d = {'actual_time': congested_time_sec/60, 'opt_time': d_time_sec/60, 'saved_time': (congested_time_sec - d_time_sec)/60, 'latency': d_lat, 'nodes_searched': len(d_exp)}

print("\n[4/4] Generating Maps (This takes ~30 seconds)...")
plot_route_with_metrics(G_S4, None, a_path, a_exp, blocked_nodes, "scenario_4_vayu_vajra_astar.png", "Scenario 4: Airport Highway Detour", metrics_a, True, "Origin: KIAL Airport", "Dest: Hebbal")
plot_route_with_metrics(G_S4, None, d_path, d_exp, blocked_nodes, "scenario_4_vayu_vajra_dijkstra.png", "Scenario 4: Airport Highway Detour", metrics_d, False, "Origin: KIAL Airport", "Dest: Hebbal")

print("\nScenario 4 generated successfully! Check output folder.")
