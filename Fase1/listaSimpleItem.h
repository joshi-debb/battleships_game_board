#pragma once



#include "nodoItem.h"
#include <iostream>
#include "crow.h"


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

    vector<crow::json::wvalue> bubbleSortUP();
    vector<crow::json::wvalue> bubbleSortDW();

    bool searchExist(string name);
    bool is_empty();

};

