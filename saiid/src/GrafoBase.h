#ifndef GRAFOBASE_H
#define GRAFOBASE_H

#include <vector>
#include <string>

class GrafoBase {
public:
    virtual ~GrafoBase() {}
    virtual void cargarDatos(const std::string& archivo) = 0;
    virtual std::vector<int> BFS(int nodoInicio, int maxDepth) = 0;
    virtual int obtenerGrado(int nodo) = 0;
    virtual std::vector<int> getVecinos(int nodo) = 0;
};

#endif
