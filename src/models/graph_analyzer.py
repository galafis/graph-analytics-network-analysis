"""
Graph Analytics and Network Analysis

Network analysis algorithms including centrality, community detection, and link prediction.

Author: Gabriel Demetrios Lafis
"""

import networkx as nx
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from loguru import logger


class GraphAnalyzer:
    """
    Graph analytics and network analysis toolkit.
    """
    
    def __init__(self, graph: nx.Graph = None):
        """
        Initialize graph analyzer.
        
        Args:
            graph: NetworkX graph object
        """
        self.graph = graph if graph is not None else nx.Graph()
        logger.info(f"Initialized GraphAnalyzer with {len(self.graph.nodes())} nodes")
    
    def load_from_edgelist(self, filepath: str, delimiter: str = ','):
        """
        Load graph from edge list file.
        
        Args:
            filepath: Path to edge list file
            delimiter: Delimiter character
        """
        self.graph = nx.read_edgelist(filepath, delimiter=delimiter)
        logger.info(f"Loaded graph with {len(self.graph.nodes())} nodes and {len(self.graph.edges())} edges")
    
    def add_edges_from_dataframe(self, df: pd.DataFrame, source_col: str, target_col: str, weight_col: str = None):
        """
        Add edges from DataFrame.
        
        Args:
            df: DataFrame with edge data
            source_col: Source node column
            target_col: Target node column
            weight_col: Weight column (optional)
        """
        if weight_col:
            edges = [(row[source_col], row[target_col], row[weight_col]) 
                    for _, row in df.iterrows()]
            self.graph.add_weighted_edges_from(edges)
        else:
            edges = [(row[source_col], row[target_col]) 
                    for _, row in df.iterrows()]
            self.graph.add_edges_from(edges)
        
        logger.info(f"Added {len(edges)} edges to graph")
    
    def calculate_centrality(self, measure: str = 'degree') -> Dict:
        """
        Calculate node centrality.
        
        Args:
            measure: Centrality measure ('degree', 'betweenness', 'closeness', 'eigenvector', 'pagerank')
            
        Returns:
            Dictionary of node centralities
        """
        logger.info(f"Calculating {measure} centrality...")
        
        if measure == 'degree':
            centrality = nx.degree_centrality(self.graph)
        elif measure == 'betweenness':
            centrality = nx.betweenness_centrality(self.graph)
        elif measure == 'closeness':
            centrality = nx.closeness_centrality(self.graph)
        elif measure == 'eigenvector':
            centrality = nx.eigenvector_centrality(self.graph, max_iter=1000)
        elif measure == 'pagerank':
            centrality = nx.pagerank(self.graph)
        else:
            raise ValueError(f"Unknown centrality measure: {measure}")
        
        return centrality
    
    def detect_communities(self, algorithm: str = 'louvain') -> Dict[int, int]:
        """
        Detect communities in the graph.
        
        Args:
            algorithm: Community detection algorithm ('louvain', 'label_propagation', 'greedy_modularity')
            
        Returns:
            Dictionary mapping nodes to community IDs
        """
        logger.info(f"Detecting communities using {algorithm}...")
        
        if algorithm == 'louvain':
            import community as community_louvain
            communities = community_louvain.best_partition(self.graph)
        elif algorithm == 'label_propagation':
            communities_gen = nx.community.label_propagation_communities(self.graph)
            communities = {}
            for idx, community in enumerate(communities_gen):
                for node in community:
                    communities[node] = idx
        elif algorithm == 'greedy_modularity':
            communities_gen = nx.community.greedy_modularity_communities(self.graph)
            communities = {}
            for idx, community in enumerate(communities_gen):
                for node in community:
                    communities[node] = idx
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        n_communities = len(set(communities.values()))
        logger.success(f"Found {n_communities} communities")
        
        return communities
    
    def calculate_modularity(self, communities: Dict[int, int]) -> float:
        """
        Calculate modularity of community partition.
        
        Args:
            communities: Dictionary mapping nodes to community IDs
            
        Returns:
            Modularity score
        """
        # Convert to list of sets
        community_sets = {}
        for node, comm_id in communities.items():
            if comm_id not in community_sets:
                community_sets[comm_id] = set()
            community_sets[comm_id].add(node)
        
        communities_list = list(community_sets.values())
        modularity = nx.community.modularity(self.graph, communities_list)
        
        logger.info(f"Modularity: {modularity:.4f}")
        return modularity
    
    def predict_links(self, method: str = 'common_neighbors', k: int = 10) -> List[Tuple]:
        """
        Predict missing links.
        
        Args:
            method: Link prediction method ('common_neighbors', 'jaccard', 'adamic_adar', 'preferential_attachment')
            k: Number of top predictions to return
            
        Returns:
            List of (node1, node2, score) tuples
        """
        logger.info(f"Predicting links using {method}...")
        
        if method == 'common_neighbors':
            preds = nx.common_neighbor_centrality(self.graph)
        elif method == 'jaccard':
            preds = nx.jaccard_coefficient(self.graph)
        elif method == 'adamic_adar':
            preds = nx.adamic_adar_index(self.graph)
        elif method == 'preferential_attachment':
            preds = nx.preferential_attachment(self.graph)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Sort by score and get top-k
        predictions = sorted(preds, key=lambda x: x[2], reverse=True)[:k]
        
        return predictions
    
    def get_graph_statistics(self) -> Dict:
        """
        Calculate basic graph statistics.
        
        Returns:
            Dictionary with graph statistics
        """
        stats = {
            'n_nodes': self.graph.number_of_nodes(),
            'n_edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'is_connected': nx.is_connected(self.graph),
        }
        
        if nx.is_connected(self.graph):
            stats['diameter'] = nx.diameter(self.graph)
            stats['avg_shortest_path'] = nx.average_shortest_path_length(self.graph)
        else:
            stats['n_components'] = nx.number_connected_components(self.graph)
            largest_cc = max(nx.connected_components(self.graph), key=len)
            subgraph = self.graph.subgraph(largest_cc)
            stats['largest_component_size'] = len(largest_cc)
            stats['largest_component_diameter'] = nx.diameter(subgraph)
        
        stats['avg_clustering'] = nx.average_clustering(self.graph)
        stats['transitivity'] = nx.transitivity(self.graph)
        
        logger.info(f"Graph statistics: {stats}")
        return stats
    
    def get_top_nodes(self, centrality_measure: str = 'degree', k: int = 10) -> List[Tuple]:
        """
        Get top-k nodes by centrality.
        
        Args:
            centrality_measure: Centrality measure
            k: Number of top nodes
            
        Returns:
            List of (node, centrality) tuples
        """
        centrality = self.calculate_centrality(centrality_measure)
        top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:k]
        return top_nodes
    
    def visualize(self, layout: str = 'spring', node_color: str = 'lightblue', 
                  node_size: int = 300, with_labels: bool = True):
        """
        Visualize the graph.
        
        Args:
            layout: Layout algorithm ('spring', 'circular', 'kamada_kawai')
            node_color: Node color
            node_size: Node size
            with_labels: Whether to show node labels
        """
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(12, 8))
        
        if layout == 'spring':
            pos = nx.spring_layout(self.graph)
        elif layout == 'circular':
            pos = nx.circular_layout(self.graph)
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(self.graph)
        else:
            pos = nx.spring_layout(self.graph)
        
        nx.draw(
            self.graph,
            pos,
            node_color=node_color,
            node_size=node_size,
            with_labels=with_labels,
            font_size=8,
            font_weight='bold',
            edge_color='gray',
            alpha=0.7
        )
        
        plt.title("Network Graph Visualization")
        plt.axis('off')
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # Example usage
    
    # Create sample graph
    G = nx.karate_club_graph()
    
    analyzer = GraphAnalyzer(G)
    
    # Calculate statistics
    stats = analyzer.get_graph_statistics()
    print("\nGraph Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Calculate centrality
    pagerank = analyzer.calculate_centrality('pagerank')
    top_nodes = analyzer.get_top_nodes('pagerank', k=5)
    
    print("\nTop 5 nodes by PageRank:")
    for node, score in top_nodes:
        print(f"  Node {node}: {score:.4f}")
    
    # Detect communities
    communities = analyzer.detect_communities('louvain')
    modularity = analyzer.calculate_modularity(communities)
    
    print(f"\nCommunity Detection:")
    print(f"  Number of communities: {len(set(communities.values()))}")
    print(f"  Modularity: {modularity:.4f}")
