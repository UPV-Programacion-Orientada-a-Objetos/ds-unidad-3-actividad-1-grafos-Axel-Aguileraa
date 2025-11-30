import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time
import os
import neuronet

st.set_page_config(page_title="NeuroNet", layout="wide")

st.title("NeuroNet: Análisis de Redes Masivas")
st.markdown("Sistema híbrido C++/Python para analizar la robustez de redes de comunicación masivas.")

st.sidebar.header("Configuración")

uploaded_file = st.sidebar.file_uploader("Cargar Dataset SNAP (Lista de Aristas)", type=["txt", "edges"])

if 'graph' not in st.session_state:
    st.session_state.graph = None
if 'graph_loaded' not in st.session_state:
    st.session_state.graph_loaded = False

def load_graph(file_path):
    g = neuronet.NeuroNet()
    start_time = time.time()
    g.load_data(file_path)
    end_time = time.time()
    return g, end_time - start_time

if uploaded_file is not None:
    temp_path = os.path.join("temp_graph.txt")
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.sidebar.button("Cargar Grafo"):
        with st.spinner("Cargando grafo en estructura C++ CSR..."):
            try:
                st.session_state.graph, load_time = load_graph(temp_path)
                st.session_state.graph_loaded = True
                st.success(f"¡Grafo cargado en {load_time:.4f} segundos!")
            except Exception as e:
                st.error(f"Error cargando el grafo: {e}")

if st.session_state.graph_loaded:
    g = st.session_state.graph
    stats = g.get_stats()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Nodos", stats["nodes"])
    col2.metric("Aristas", stats["edges"])
    
    st.divider()
    
    st.header("Análisis Topológico")
    
    tab1, tab2 = st.tabs(["Recorrido BFS", "Análisis de Nodos"])
    
    with tab1:
        st.subheader("Búsqueda en Anchura (BFS)")
        col_bfs1, col_bfs2 = st.columns(2)
        start_node = col_bfs1.number_input("Nodo Inicial", min_value=0, max_value=stats["nodes"]-1, value=0)
        max_depth = col_bfs2.number_input("Profundidad Máxima", min_value=1, max_value=10, value=2)
        
        if st.button("Ejecutar BFS"):
            start_time = time.time()
            visited_nodes = g.bfs(start_node, max_depth)
            duration = time.time() - start_time
            
            st.write(f"BFS encontró {len(visited_nodes)} nodos en {duration:.6f} segundos.")
            
            if len(visited_nodes) > 0 and len(visited_nodes) < 1000:
                st.subheader("Visualización del Subgrafo")
                nx_graph = nx.Graph()
                
                nodes_to_draw = visited_nodes[:100] 
                if len(visited_nodes) > 100:
                    st.warning("Visualizando solo los primeros 100 nodos.")
                
                for u in nodes_to_draw:
                    nx_graph.add_node(u)
                    neighbors = g.get_neighbors(u)
                    for v in neighbors:
                        if v in nodes_to_draw:
                            nx_graph.add_edge(u, v)
                
                fig, ax = plt.subplots(figsize=(10, 6))
                pos = nx.spring_layout(nx_graph)
                nx.draw(nx_graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10, ax=ax)
                nx.draw_networkx_nodes(nx_graph, pos, nodelist=[start_node], node_color='red', node_size=600, ax=ax)
                st.pyplot(fig)
            elif len(visited_nodes) >= 1000:
                st.info("Subgrafo demasiado grande para visualizar.")

    with tab2:
        st.subheader("Grado del Nodo")
        node_id = st.number_input("ID del Nodo", min_value=0, max_value=stats["nodes"]-1, value=0, key="node_degree")
        if st.button("Obtener Grado"):
            degree = g.get_degree(node_id)
            st.metric(f"Grado del Nodo {node_id}", degree)

else:
    st.info("Por favor, sube y carga un dataset de grafo para comenzar el análisis.")
