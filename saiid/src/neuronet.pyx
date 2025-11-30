# distutils: language = c++

from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "GrafoBase.h":
    cdef cppclass GrafoBase:
        pass

cdef extern from "GrafoDisperso.h":
    cdef cppclass GrafoDisperso(GrafoBase):
        GrafoDisperso() except +
        void cargarDatos(string archivo)
        vector[int] BFS(int nodoInicio, int maxDepth)
        int obtenerGrado(int nodo)
        vector[int] getVecinos(int nodo)
        int getNumNodos()
        int getNumAristas()

cdef class NeuroNet:
    cdef GrafoDisperso* c_grafo

    def __cinit__(self):
        self.c_grafo = new GrafoDisperso()

    def __dealloc__(self):
        del self.c_grafo

    def load_data(self, filename: str):
        self.c_grafo.cargarDatos(filename.encode('utf-8'))

    def bfs(self, start_node: int, max_depth: int):
        return self.c_grafo.BFS(start_node, max_depth)

    def get_degree(self, node: int):
        return self.c_grafo.obtenerGrado(node)

    def get_neighbors(self, node: int):
        return self.c_grafo.getVecinos(node)
        
    def get_stats(self):
        return {
            "nodes": self.c_grafo.getNumNodos(),
            "edges": self.c_grafo.getNumAristas()
        }
