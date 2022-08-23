

#pragma once

#include "nodoHeaderItem.h"


using namespace std;

class listaSimpleHeaders
{
public:
    nodoHeaderItem* primero;

    listaSimpleHeaders() {
        primero = NULL;
    }

    void loadFile(string ruta);
    void Imprimir();
    void GenerarGrafo();
    void Insertar(nodoItem* item, string categoria);
    nodoHeaderItem* BuscarPrincipal(nodoHeaderItem* inicioL, string categoria);

private:
};



