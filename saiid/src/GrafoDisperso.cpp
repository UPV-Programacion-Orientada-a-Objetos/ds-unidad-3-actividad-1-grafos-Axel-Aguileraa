#include "GrafoDisperso.h"
#include <fstream>
#include <sstream>
#include <algorithm>
#include <queue>
#include <set>
#include <map>

GrafoDisperso::GrafoDisperso() : numNodos(0), numAristas(0) {}

GrafoDisperso::~GrafoDisperso() {}

void GrafoDisperso::cargarDatos(const std::string& archivo) {
    std::cout << "Cargando datos desde: " << archivo << std::endl;
    std::ifstream file(archivo);
    if (!file.is_open()) {
        std::cerr << "Error abriendo archivo: " << archivo << std::endl;
        return;
    }

    std::vector<std::pair<int, int>> edges;
    int maxNodeId = -1;
    int u, v;
    std::string line;

    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;
        std::stringstream ss(line);
        if (ss >> u >> v) {
            edges.push_back({u, v});
            edges.push_back({v, u}); 
            
            if (u > maxNodeId) maxNodeId = u;
            if (v > maxNodeId) maxNodeId = v;
        }
    }
    file.close();

    numNodos = maxNodeId + 1;
    numAristas = edges.size();

    std::sort(edges.begin(), edges.end());

    edges.erase(std::unique(edges.begin(), edges.end()), edges.end());
    numAristas = edges.size();

    row_ptr.assign(numNodos + 1, 0);
    col_indices.resize(numAristas);
    values.assign(numAristas, 1);

    int currentEdge = 0;
    for (int i = 0; i < numNodos; ++i) {
        row_ptr[i] = currentEdge;
        while (currentEdge < numAristas && edges[currentEdge].first == i) {
            col_indices[currentEdge] = edges[currentEdge].second;
            currentEdge++;
        }
    }
    row_ptr[numNodos] = numAristas;

    std::cout << "Grafo cargado. Nodos: " << numNodos << ", Aristas: " << numAristas << std::endl;
}

std::vector<int> GrafoDisperso::BFS(int nodoInicio, int maxDepth) {
    std::vector<int> result;
    if (nodoInicio < 0 || nodoInicio >= numNodos) return result;

    std::vector<bool> visited(numNodos, false);
    std::queue<std::pair<int, int>> q;

    q.push({nodoInicio, 0});
    visited[nodoInicio] = true;
    result.push_back(nodoInicio);

    while (!q.empty()) {
        int u = q.front().first;
        int d = q.front().second;
        q.pop();

        if (d >= maxDepth) continue;

        for (int i = row_ptr[u]; i < row_ptr[u+1]; ++i) {
            int v = col_indices[i];
            if (!visited[v]) {
                visited[v] = true;
                q.push({v, d + 1});
                result.push_back(v);
            }
        }
    }
    return result;
}

int GrafoDisperso::obtenerGrado(int nodo) {
    if (nodo < 0 || nodo >= numNodos) return 0;
    return row_ptr[nodo+1] - row_ptr[nodo];
}

std::vector<int> GrafoDisperso::getVecinos(int nodo) {
    std::vector<int> vecinos;
    if (nodo < 0 || nodo >= numNodos) return vecinos;
    
    for (int i = row_ptr[nodo]; i < row_ptr[nodo+1]; ++i) {
        vecinos.push_back(col_indices[i]);
    }
    return vecinos;
}
