

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
    void doGraphics();
    void Insertar(nodoItem* item, string categoria);
    nodoHeaderItem* BuscarPrincipal(nodoHeaderItem* inicioL, string categoria);

private:
};



