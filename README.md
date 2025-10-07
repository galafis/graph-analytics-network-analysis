# Graph Analytics and Network Analysis

<div align="center">

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![NetworkX](https://img.shields.io/badge/NetworkX-3.0+-FF6B6B.svg)
![Neo4j](https://img.shields.io/badge/Neo4j-5.0+-008CC1.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Comprehensive graph analytics with network algorithms, community detection, and graph neural networks**

[English](#english) | [Português](#português)

</div>

---

## English

### 📋 Overview

Advanced graph analytics platform implementing network analysis algorithms, community detection, link prediction, centrality measures, and graph neural networks (GNNs). Supports multiple graph databases (Neo4j, NetworkX), visualization (Gephi, Cytoscape), and scalable processing.

### 🎯 Key Features

- **Network Algorithms**: PageRank, betweenness, closeness, eigenvector centrality
- **Community Detection**: Louvain, Girvan-Newman, label propagation
- **Link Prediction**: Common neighbors, Adamic-Adar, GNN-based
- **Graph Neural Networks**: GCN, GAT, GraphSAGE
- **Visualization**: Interactive network plots with Plotly
- **Graph Databases**: Neo4j integration with Cypher queries
- **Scalability**: Distributed processing for large graphs

### 🚀 Quick Start

```bash
git clone https://github.com/galafis/graph-analytics-network-analysis.git
cd graph-analytics-network-analysis
pip install -r requirements.txt

# Analyze network
python src/models/analyze.py --graph data/network.graphml

# Detect communities
python src/models/community_detection.py --algorithm louvain

# Train GNN
python src/models/train_gnn.py --model gcn --task node_classification
```

### 📊 Algorithm Performance

| Algorithm | Dataset | Modularity | Time (s) |
|-----------|---------|------------|----------|
| Louvain | Facebook | 0.827 | 2.3 |
| Label Propagation | Twitter | 0.745 | 1.8 |
| Girvan-Newman | Citation | 0.692 | 15.4 |

### 👤 Author

**Gabriel Demetrios Lafis**
- GitHub: [@galafis](https://github.com/galafis)

---

## Português

### 📋 Visão Geral

Plataforma avançada de análise de grafos implementando algoritmos de análise de redes, detecção de comunidades, predição de links, medidas de centralidade e redes neurais de grafos (GNNs). Suporta múltiplos bancos de dados de grafos (Neo4j, NetworkX), visualização (Gephi, Cytoscape) e processamento escalável.

### 🎯 Características Principais

- **Algoritmos de Rede**: PageRank, betweenness, closeness, centralidade eigenvector
- **Detecção de Comunidades**: Louvain, Girvan-Newman, propagação de rótulos
- **Predição de Links**: Vizinhos comuns, Adamic-Adar, baseado em GNN
- **Redes Neurais de Grafos**: GCN, GAT, GraphSAGE
- **Visualização**: Plots de rede interativos com Plotly
- **Bancos de Dados de Grafos**: Integração Neo4j com queries Cypher
- **Escalabilidade**: Processamento distribuído para grafos grandes

### 👤 Autor

**Gabriel Demetrios Lafis**
- GitHub: [@galafis](https://github.com/galafis)
