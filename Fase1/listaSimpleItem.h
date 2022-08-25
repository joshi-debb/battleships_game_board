#pragma once



#include "nodoItem.h"
#include <iostream>

using namespace std;

class listaSimpleItem
{
public:

    nodoItem* primero;
    nodoItem* ultimo;

    listaSimpleItem() {
        primero = NULL;
        ultimo = NULL;

    }


    void loadFile(string ruta);
    void addToEnd(nodoItem* item);
    void showList();
    void bubbleSortUP(listaSimpleItem listaItems);
    void bubbleSortDW(listaSimpleItem listaItems);

private:
};

