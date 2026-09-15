"""
================================================================================
SCRIPT 07: ML-AUGMENTED DYNAMIC ROUTE OPTIMIZATION SIMULATION (DIJKSTRA & A*)
Project: BMTC Intelligent Public Transport Delay Prediction & Dynamic Routing
Output Directory: MODEL BUILDING/OUTPUTS/Route_Optimization/
================================================================================
"""

import os
import sys
import json
import time
import math
import heapq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "OUTPUTS", "Route_Optimization")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# 1. Road Network Topography Definition (Bengaluru Transit Corridors)
# ----------------------------------------------------------------------
STOPS_COORDINATES = {
    'BS_HEB': {'name': 'Hebbal Bus Stop', 'lat': 13.0358, 'lon': 77.5970},
    'BS_NAG': {'name': 'Nagavara Junction', 'lat': 13.0440, 'lon': 77.6205},
    'BS_HEN': {'name': 'Hennur Cross', 'lat': 13.0350, 'lon': 77.6400},
    'BS_KRP': {'name': 'KR Puram Station', 'lat': 13.0012, 'lon': 77.6960},
    'BS_MAR': {'name': 'Marathahalli Bridge', 'lat': 12.9560, 'lon': 77.7011},
    'BS_BEL': {'name': 'Bellandur EcoSpace', 'lat': 12.9280, 'lon': 77.6830},
    'BS_AGR': {'name': 'Agara Junction', 'lat': 12.9210, 'lon': 77.6520},
    'BS_SIL': {'name': 'Silk Board Junction', 'lat': 12.9177, 'lon': 77.6238},
    'BS_BTM': {'name': 'BTM Layout Water Tank', 'lat': 12.9160, 'lon': 77.6100},
    'BS_JAY': {'name': 'Jayanagar 4th Block', 'lat': 12.9290, 'lon': 77.5830},
    'BS_MAJ': {'name': 'Majestic KBS Terminal', 'lat': 12.9770, 'lon': 77.5710},
    'BS_MG_': {'name': 'MG Road Metro', 'lat': 12.9750, 'lon': 77.6080},
    'BS_IND': {'name': 'Indiranagar 100ft Rd', 'lat': 12.9780, 'lon': 77.6400},
    'BS_WFD': {'name': 'Whitefield TTMC', 'lat': 12.9690, 'lon': 77.7500},
    'BS_EC_': {'name': 'Electronic City Phase 1', 'lat': 12.8450, 'lon': 77.6600}
}

# Corridors with base distance in km and free-flow speed (45 km/h)
CORRIDOR_EDGES = [
    ('BS_HEB', 'BS_NAG', 3.5),
    ('BS_NAG', 'BS_HEN', 2.8),
    ('BS_HEN', 'BS_KRP', 7.2),
    ('BS_KRP', 'BS_MAR', 6.5),
    ('BS_MAR', 'BS_BEL', 4.2),
    ('BS_BEL', 'BS_AGR', 3.8),
    ('BS_AGR', 'BS_SIL', 3.1),
    ('BS_SIL', 'BS_BTM', 2.0),
    ('BS_BTM', 'BS_JAY', 3.5),
    ('BS_JAY', 'BS_MAJ', 6.0),
    ('BS_HEB', 'BS_MAJ', 8.5),
    ('BS_MAJ', 'BS_MG_', 4.5),
    ('BS_MG_', 'BS_IND', 4.0),
    ('BS_IND', 'BS_MAR', 7.5),
    ('BS_KRP', 'BS_WFD', 8.0),
    ('BS_MAR', 'BS_WFD', 7.0),
    ('BS_SIL', 'BS_EC_', 12.0),
    ('BS_AGR', 'BS_IND', 8.0)
]

def haversine_distance(node1, node2):
    """Haversine distance in km for A* heuristic."""
    lat1, lon1 = STOPS_COORDINATES[node1]['lat'], STOPS_COORDINATES[node1]['lon']
    lat2, lon2 = STOPS_COORDINATES[node2]['lat'], STOPS_COORDINATES[node2]['lon']
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def run_dijkstra(graph, start, goal, weight_key='weight'):
    """Standard Dijkstra Shortest Path."""
    start_time = time.perf_counter()
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    previous_nodes = {node: None for node in graph.nodes}
    pq = [(0, start)]
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        if current_node == goal:
            break
        if current_dist > distances[current_node]:
            continue
            
        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor][weight_key]
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
                
    path = []
    curr = goal
    while curr is not None:
        path.append(curr)
        curr = previous_nodes[curr]
    path.reverse()
    latency_ms = (time.perf_counter() - start_time) * 1000.0
    return path, distances[goal], latency_ms

def run_astar(graph, start, goal, weight_key='weight'):
    """A* Search with Haversine distance heuristic."""
    start_time = time.perf_counter()
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = (haversine_distance(start, goal) / 45.0) * 60.0
    
    previous_nodes = {node: None for node in graph.nodes}
    open_set = [(f_score[start], start)]
    
    while open_set:
        _, current_node = heapq.heappop(open_set)
        if current_node == goal:
            break
            
        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor][weight_key]
            tentative_g = g_score[current_node] + weight
            
            if tentative_g < g_score[neighbor]:
                previous_nodes[neighbor] = current_node
                g_score[neighbor] = tentative_g
                h = (haversine_distance(neighbor, goal) / 45.0) * 60.0
                f_score[neighbor] = tentative_g + h
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                
    path = []
    curr = goal
    while curr is not None:
        path.append(curr)
        curr = previous_nodes[curr]
    path.reverse()
    latency_ms = (time.perf_counter() - start_time) * 1000.0
    return path, g_score[goal], latency_ms

def simulate_dynamic_routing():
    print("=" * 80)
    print(" BMTC ML PIPELINE: STAGE 07 - ML-AUGMENTED DYNAMIC ROUTE OPTIMIZATION")
    print("=" * 80)
    
    # Construct Graph
    G = nx.Graph()
    for u, v, dist in CORRIDOR_EDGES:
        free_flow_time = (dist / 45.0) * 60.0 # 45 km/h baseline free flow in minutes
        G.add_edge(u, v, distance=dist, free_flow_time=free_flow_time, dynamic_cost=free_flow_time)
        
    print(f"[1/4] Built OSM Road Network Graph: {G.number_of_nodes()} Stops, {G.number_of_edges()} Corridors")
    
    # Scheduled Route for Bus 500D (Hebbal to Silk Board via ORR)
    scheduled_orr_path = ['BS_HEB', 'BS_NAG', 'BS_HEN', 'BS_KRP', 'BS_MAR', 'BS_BEL', 'BS_AGR', 'BS_SIL']
    
    # Simulate a Heavy Peak-Hour Disruption & Monsoon Flood Incident on ORR Central Segment
    print("\n[2/4] Injecting Real-Time ML Predicted Delays & Incident Penalties on ORR...")
    G['BS_KRP']['BS_MAR']['dynamic_cost'] = G['BS_KRP']['BS_MAR']['free_flow_time'] + 22.5 + 15.0 # +37.5 min ML delay & crash
    G['BS_MAR']['BS_BEL']['dynamic_cost'] = G['BS_MAR']['BS_BEL']['free_flow_time'] + 18.0        # +18.0 min ML delay
    G['BS_BEL']['BS_AGR']['dynamic_cost'] = G['BS_BEL']['BS_AGR']['free_flow_time'] + 12.0        # +12.0 min ML delay
    
    origin = 'BS_HEB' # Hebbal
    destination = 'BS_SIL' # Silk Board
    
    # Calculate travel time along scheduled ORR route during active congestion
    orr_congested_time = sum(G[scheduled_orr_path[i]][scheduled_orr_path[i+1]]['dynamic_cost'] for i in range(len(scheduled_orr_path)-1))
    
    # Calculate Dynamic ML Detour Route via A* search
    dynamic_path_astar, dynamic_time_astar, dynamic_lat_astar = run_astar(G, origin, destination, weight_key='dynamic_cost')
    dynamic_path_dijkstra, dynamic_time_dijkstra, dynamic_lat_dijkstra = run_dijkstra(G, origin, destination, weight_key='dynamic_cost')
    
    minutes_saved = orr_congested_time - dynamic_time_astar
    pct_saved = (minutes_saved / orr_congested_time) * 100.0
    
    print("\n[3/4] Routing Benchmark Results:")
    print("=" * 70)
    print("  [SCHEDULED ROUTE 500D] Default Outer Ring Road (Congested):")
    print(f"     Path: {' -> '.join(scheduled_orr_path)}")
    print(f"     Total Travel Time under Traffic: {orr_congested_time:.2f} minutes")
    print("  [DYNAMIC DETOUR] ML-Augmented A* Search:")
    print(f"     Path: {' -> '.join(dynamic_path_astar)}")
    print(f"     Optimized Travel Time:           {dynamic_time_astar:.2f} minutes")
    print(f"  [BENEFIT] {minutes_saved:.2f} Minutes Saved ({pct_saved:.1f}% Travel Time Reduction)")
    print(f"  [SPEED] Dijkstra Latency = {dynamic_lat_dijkstra:.4f} ms | A* Latency = {dynamic_lat_astar:.4f} ms")
    print("=" * 70)
    
    # Save Benchmark JSON
    benchmark_data = {
        "origin_stop": origin,
        "origin_name": STOPS_COORDINATES[origin]['name'],
        "destination_stop": destination,
        "destination_name": STOPS_COORDINATES[destination]['name'],
        "scheduled_congested_route": {
            "path": scheduled_orr_path,
            "path_names": [STOPS_COORDINATES[s]['name'] for s in scheduled_orr_path],
            "travel_time_congested_minutes": float(orr_congested_time)
        },
        "ml_dynamic_detour_route": {
            "path": dynamic_path_astar,
            "path_names": [STOPS_COORDINATES[s]['name'] for s in dynamic_path_astar],
            "optimized_travel_time_minutes": float(dynamic_time_astar)
        },
        "performance_improvement": {
            "minutes_saved": float(minutes_saved),
            "percentage_travel_time_reduction": float(pct_saved)
        },
        "algorithm_latency_benchmark": {
            "dijkstra_latency_ms": float(dynamic_lat_dijkstra),
            "astar_latency_ms": float(dynamic_lat_astar)
        }
    }
    
    metrics_path = os.path.join(OUTPUT_DIR, "dynamic_routing_benchmark_results.json")
    with open(metrics_path, "w", encoding='utf-8') as f:
        json.dump(benchmark_data, f, indent=4)
    print(f"  -> Saved Benchmark Metrics: {metrics_path}")
    
    # 4. Generate Visual Detour Map
    print("\n[4/4] Generating Route Visualization Maps...")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    pos = {node: (coords['lon'], coords['lat']) for node, coords in STOPS_COORDINATES.items()}
    
    # Base network
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#bdc3c7', width=2, alpha=0.7)
    
    # Highlight Scheduled Congested Route (Red dashed)
    scheduled_edges = [(scheduled_orr_path[i], scheduled_orr_path[i+1]) for i in range(len(scheduled_orr_path)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=scheduled_edges, ax=ax, edge_color='#e74c3c', width=4, style='dashed', label=f'Scheduled ORR Route ({orr_congested_time:.1f} min - Traffic & Incident)')
    
    # Highlight Dynamic ML Detour Route (Green solid)
    dynamic_edges = [(dynamic_path_astar[i], dynamic_path_astar[i+1]) for i in range(len(dynamic_path_astar)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=dynamic_edges, ax=ax, edge_color='#2ecc71', width=5, label=f'ML Detour Route ({dynamic_time_astar:.1f} min - Saved {minutes_saved:.1f} min)')
    
    # Nodes
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='#34495e', node_size=350)
    nx.draw_networkx_nodes(G, pos, nodelist=[origin], ax=ax, node_color='#3498db', node_size=600)
    nx.draw_networkx_nodes(G, pos, nodelist=[destination], ax=ax, node_color='#f39c12', node_size=600)
    
    # Labels
    labels = {node: node.replace('BS_', '') for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color='white', font_weight='bold', ax=ax)
    
    ax.set_title(f'ML-Augmented Dynamic Route Optimization: Detour Around ORR Bottleneck\n(Hebbal to Silk Board: {minutes_saved:.1f} Minutes Saved / {pct_saved:.1f}% Faster)', fontsize=12, fontweight='bold', pad=15)
    ax.set_xlabel('Longitude (°E)', fontsize=10)
    ax.set_ylabel('Latitude (°N)', fontsize=10)
    ax.legend(loc='lower left', frameon=True, fontsize=9)
    plt.tight_layout()
    map_path = os.path.join(OUTPUT_DIR, "dynamic_rerouting_trajectory_map.png")
    plt.savefig(map_path, dpi=300)
    plt.close()
    print(f"  -> Saved Detour Route Map: {map_path}")
    
    print("\n" + "=" * 80)
    print(" Stage 07 Complete. All Route Optimization outputs saved to Route_Optimization/")
    print("=" * 80)

if __name__ == "__main__":
    simulate_dynamic_routing()
