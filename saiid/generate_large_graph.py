import random

def generate_large_graph(filename, num_nodes, num_edges):
    print(f"Generando grafo con {num_nodes} nodos y {num_edges} aristas...")
    with open(filename, 'w') as f:
        f.write(f"# Grafo sintético: {num_nodes} nodos, {num_edges} aristas\n")
        for _ in range(num_edges):
            u = random.randint(0, num_nodes - 1)
            v = random.randint(0, num_nodes - 1)
            if u != v:
                f.write(f"{u} {v}\n")
    print(f"Archivo {filename} generado exitosamente.")

if __name__ == "__main__":
    # 100,000 nodos, 1,000,000 aristas
    generate_large_graph("large_graph.txt", 100000, 1000000)
