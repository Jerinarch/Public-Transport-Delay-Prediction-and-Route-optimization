import os
import sys
import json
import time
import math
import heapq
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import contextily as ctx

# Ensure correct encoding for Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import ssl
import urllib.request
import requests

ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()
ox.settings.requests_kwargs = {'verify': False}

# Configure Output Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = BASE_DIR
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print(" FINAL YEAR PROJECT: ADVANCED OSM ROUTE OPTIMIZATION ")
print("=" * 80)

# ---------------------------------------------------------
# 1. GRAPH ACQUISITION & PREPARATION
# ---------------------------------------------------------
print("\n[1/5] Downloading OpenStreetMap Graph (Hebbal to Silk Board Bounding Box)...")
north, south, east, west = 13.05, 12.90, 77.72, 77.55
bbox = (west, south, east, north)

try:
    # Limitation 1 Fix: Vehicle Physical Constraints
    # Only download wide, transit-capable main roads (blocking narrow residential alleyways)
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
    'Hebbal': {'lat': 13.0358, 'lon': 77.5970},
    'Nagavara': {'lat': 13.0440, 'lon': 77.6205},
    'Hennur': {'lat': 13.0350, 'lon': 77.6400},
    'KR_Puram': {'lat': 13.0012, 'lon': 77.6960},
    'Silk_Board': {'lat': 12.9177, 'lon': 77.6238},
    'Majestic': {'lat': 12.9770, 'lon': 77.5710}
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

# ---------------------------------------------------------
# PLOTTING WITH REALISTIC BASEMAPS AND STOP LABELS
# ---------------------------------------------------------
def plot_route_with_metrics(graph, actual_route, optimized_route, explored_nodes, filename, title, metrics, is_astar, origin_name, dest_name):
    # Create plot with transparent background so basemap shows
    fig, ax = ox.plot_graph(graph, show=False, close=False, node_size=0, edge_color='#666666', edge_linewidth=0.5, edge_alpha=0.3, bgcolor='none')
    
    # Plot Explored Nodes (Search Space) - Reduced size/alpha to look like a subtle cloud, not random colors
    if explored_nodes:
        search_color = '#3498db' if is_astar else '#e74c3c'
        nc = ['none' if n not in explored_nodes else search_color for n in graph.nodes]
        ns = [0 if n not in explored_nodes else 8 for n in graph.nodes]
        ox.plot_graph(graph, ax=ax, show=False, close=False, node_color=nc, node_size=ns, edge_linewidth=0, bgcolor='none', node_alpha=0.15)
    
    # Plot Actual Route (Red)
    if actual_route:
        ox.plot_graph_route(graph, actual_route, ax=ax, route_color='#e74c3c', route_linewidth=5, route_alpha=0.9, show=False, close=False)
    
    # Plot Optimized Route (Green)
    if optimized_route:
        ox.plot_graph_route(graph, optimized_route, ax=ax, route_color='#2ecc71', route_linewidth=6, route_alpha=1, show=False, close=False)
        
    # Plot and clearly label Waypoints
    start_lat, start_lon = graph.nodes[optimized_route[0]]['y'], graph.nodes[optimized_route[0]]['x']
    end_lat, end_lon = graph.nodes[optimized_route[-1]]['y'], graph.nodes[optimized_route[-1]]['x']
    
    ax.scatter([start_lon, end_lon], [start_lat, end_lat], c=['blue', 'orange'], s=200, zorder=10, edgecolors='white', linewidths=2)
    
    # Text Annotation for Bus Stops (Offset to avoid covering the stop)
    bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=2, alpha=0.9)
    ax.annotate(origin_name, (start_lon, start_lat), xytext=(-20, 25), textcoords='offset points', 
                fontsize=11, fontweight='bold', bbox=bbox_props, zorder=11, ha='center')
    ax.annotate(dest_name, (end_lon, end_lat), xytext=(20, -30), textcoords='offset points', 
                fontsize=11, fontweight='bold', bbox=bbox_props, zorder=11, ha='center')
    
    # Add Realistic Basemap from Contextily (Esri doesn't block access or require API keys)
    try:
        ctx.add_basemap(ax, crs="EPSG:4326", source=ctx.providers.Esri.WorldStreetMap, alpha=0.6)
    except Exception as e:
        print(f"Warning: Could not add basemap: {e}")
    
    # Add Text Box with Metrics (Moved to Bottom Left to avoid routes)
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
# 3. RUNNING SCENARIOS
# ---------------------------------------------------------
master_metrics = {}

# --- SCENARIO 1: MACRO DETOUR (Hebbal to Silk Board avoiding ORR) ---
print("\n[2/5] Running Scenario 1: Macro-Detour (Express Bus)...")
G_S1 = G.copy()
for u, v, k, data in G_S1.edges(keys=True, data=True):
    if G_S1.nodes[u]['x'] > 77.65:
        data['travel_time'] = data['travel_time'] * 50

s1_actual_path, _, _, _ = run_astar(G, nodes['Hebbal'], nodes['Silk_Board'])
s1_congested_time_sec = sum(G_S1[u][v][0]['travel_time'] for u, v in zip(s1_actual_path[:-1], s1_actual_path[1:]))

s1_a_path, s1_a_time_sec, s1_a_lat, s1_a_exp = run_astar(G_S1, nodes['Hebbal'], nodes['Silk_Board'])
s1_d_path, s1_d_time_sec, s1_d_lat, s1_d_exp = run_dijkstra(G_S1, nodes['Hebbal'], nodes['Silk_Board'])

m1_a = {'actual_time': s1_congested_time_sec/60, 'opt_time': s1_a_time_sec/60, 'saved_time': (s1_congested_time_sec - s1_a_time_sec)/60, 'latency': s1_a_lat, 'nodes_searched': len(s1_a_exp)}
m1_d = {'actual_time': s1_congested_time_sec/60, 'opt_time': s1_d_time_sec/60, 'saved_time': (s1_congested_time_sec - s1_d_time_sec)/60, 'latency': s1_d_lat, 'nodes_searched': len(s1_d_exp)}
master_metrics['Scenario_1_Macro_Detour'] = {'A_Star': m1_a, 'Dijkstra': m1_d}

plot_route_with_metrics(G_S1, s1_actual_path, s1_a_path, s1_a_exp, "scenario_1_macro_detour_astar.png", "Scenario 1: Express Detour", m1_a, True, "Origin: Hebbal", "Destination: Silk Board")
plot_route_with_metrics(G_S1, s1_actual_path, s1_d_path, s1_d_exp, "scenario_1_macro_detour_dijkstra.png", "Scenario 1: Express Detour", m1_d, False, "Origin: Hebbal", "Destination: Silk Board")


# --- SCENARIO 2: MICRO ROUTING (Nagavara to Hennur avoiding main road accident) ---
print("\n[3/5] Running Scenario 2: Micro-Routing (Standard Bus)...")
G_S2 = G.copy()
s2_actual_path, _, _, _ = run_astar(G, nodes['Nagavara'], nodes['Hennur'])
for u, v in zip(s2_actual_path[:-1], s2_actual_path[1:]):
    if G_S2.has_edge(u, v):
        G_S2[u][v][0]['travel_time'] *= 100

s2_congested_time_sec = sum(G_S2[u][v][0]['travel_time'] for u, v in zip(s2_actual_path[:-1], s2_actual_path[1:]) if G_S2.has_edge(u, v))

s2_a_path, s2_a_time_sec, s2_a_lat, s2_a_exp = run_astar(G_S2, nodes['Nagavara'], nodes['Hennur'])
s2_d_path, s2_d_time_sec, s2_d_lat, s2_d_exp = run_dijkstra(G_S2, nodes['Nagavara'], nodes['Hennur'])

m2_a = {'actual_time': s2_congested_time_sec/60, 'opt_time': s2_a_time_sec/60, 'saved_time': (s2_congested_time_sec - s2_a_time_sec)/60, 'latency': s2_a_lat, 'nodes_searched': len(s2_a_exp)}
m2_d = {'actual_time': s2_congested_time_sec/60, 'opt_time': s2_d_time_sec/60, 'saved_time': (s2_congested_time_sec - s2_d_time_sec)/60, 'latency': s2_d_lat, 'nodes_searched': len(s2_d_exp)}
master_metrics['Scenario_2_Micro_Routing'] = {'A_Star': m2_a, 'Dijkstra': m2_d}

plot_route_with_metrics(G_S2, s2_actual_path, s2_a_path, s2_a_exp, "scenario_2_micro_routing_astar.png", "Scenario 2: Waypoint Micro-Routing", m2_a, True, "Stop: Nagavara", "Stop: Hennur")
plot_route_with_metrics(G_S2, s2_actual_path, s2_d_path, s2_d_exp, "scenario_2_micro_routing_dijkstra.png", "Scenario 2: Waypoint Micro-Routing", m2_d, False, "Stop: Nagavara", "Stop: Hennur")


# --- SCENARIO 3: EXTREME WEATHER GRIDLOCK (Algorithmic Comparison) ---
print("\n[4/5] Running Scenario 3: Extreme Gridlock Benchmarking...")
G_S3 = G.copy()
import random
random.seed(42)
for u, v, k, data in G_S3.edges(keys=True, data=True):
    if random.random() > 0.5:
        data['travel_time'] *= 5

s3_actual_path, _, _, _ = run_astar(G, nodes['Hebbal'], nodes['Silk_Board'])
s3_congested_time_sec = sum(G_S3[u][v][0]['travel_time'] for u, v in zip(s3_actual_path[:-1], s3_actual_path[1:]) if G_S3.has_edge(u, v))

s3_a_path, s3_a_time_sec, s3_a_lat, s3_a_exp = run_astar(G_S3, nodes['Hebbal'], nodes['Silk_Board'])
s3_d_path, s3_d_time_sec, s3_d_lat, s3_d_exp = run_dijkstra(G_S3, nodes['Hebbal'], nodes['Silk_Board'])

m3_a = {'actual_time': s3_congested_time_sec/60, 'opt_time': s3_a_time_sec/60, 'saved_time': (s3_congested_time_sec - s3_a_time_sec)/60, 'latency': s3_a_lat, 'nodes_searched': len(s3_a_exp)}
m3_d = {'actual_time': s3_congested_time_sec/60, 'opt_time': s3_d_time_sec/60, 'saved_time': (s3_congested_time_sec - s3_d_time_sec)/60, 'latency': s3_d_lat, 'nodes_searched': len(s3_d_exp)}
master_metrics['Scenario_3_Extreme_Gridlock'] = {'A_Star': m3_a, 'Dijkstra': m3_d}

plot_route_with_metrics(G_S3, s3_actual_path, s3_a_path, s3_a_exp, "scenario_3_extreme_gridlock_astar.png", "Scenario 3: Algorithmic Benchmark", m3_a, True, "Start: Hebbal", "End: Silk Board")
plot_route_with_metrics(G_S3, s3_actual_path, s3_d_path, s3_d_exp, "scenario_3_extreme_gridlock_dijkstra.png", "Scenario 3: Algorithmic Benchmark", m3_d, False, "Start: Hebbal", "End: Silk Board")


print("\n[5/5] Saving Metrics JSON...")
with open(os.path.join(OUTPUT_DIR, 'comprehensive_routing_metrics.json'), 'w') as f:
    json.dump(master_metrics, f, indent=4)

print("\nAll scenarios generated successfully! Check output folder.")
