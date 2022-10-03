

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

    vector<crow::json::wvalue> showStruct();

    void showList();
    void doGraphics();
    void Insertar(nodoItem* item, string categoria);
    nodoHeaderItem* BuscarPrincipal(nodoHeaderItem* inicioL, string categoria);

    bool searchExist(string name);
    bool is_empty();

private:
};



