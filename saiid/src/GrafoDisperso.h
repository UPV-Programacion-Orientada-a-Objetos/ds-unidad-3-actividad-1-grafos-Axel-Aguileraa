#ifndef GRAFODISPERSO_H
#define GRAFODISPERSO_H

#include "GrafoBase.h"
#include <vector>
#include <string>
#include <iostream>

class GrafoDisperso : public GrafoBase {
private:
    std::vector<int> values;
    std::vector<int> col_indices;
    std::vector<int> row_ptr;
    int numNodos;
    int numAristas;

public:
    GrafoDisperso();
    ~GrafoDisperso();

    void cargarDatos(const std::string& archivo) override;
    std::vector<int> BFS(int nodoInicio, int maxDepth) override;
    int obtenerGrado(int nodo) override;
    std::vector<int> getVecinos(int nodo) override;
    
    int getNumNodos() const { return numNodos; }
    int getNumAristas() const { return numAristas; }
};

#endif
