#pragma once



#include "nodoItem.h"
#include <iostream>

using namespace std;

class listaSimpleItem
{
public:

    nodoItem* primero;

    listaSimpleItem() {
        primero = NULL;

    }


    void loadFile(string ruta);
    void addToEnd(nodoItem* item);
    void showList();

private:
};

