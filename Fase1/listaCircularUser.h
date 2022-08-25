#pragma once


#include "nodoUser.h"
#include "listaSimpleItem.h"
#include "listaSimplePlays.h"
#include "colaTutorial.h"
#include <iostream>

using namespace std;

class listaCircularUser {
public:

    nodoUser* primero;
    nodoUser* ultimo;

    listaCircularUser() {
        primero = NULL;
        ultimo = NULL;
    }

    void loadFile(string ruta);
    void addToEnd(nodoUser* user);
    void login(listaCircularUser listaUsers, listaSimpleItem listItems, colaTutorial queue, listaSimplePlays* stack);
    void showList();
    void doGraphics();
    void editInfo(string);
    bool deleteUser(string,string);

    bool searchExist(string);

    void bubbleSortUP(listaCircularUser listaUsers);
    void bubbleSortDW(listaCircularUser listaUsers);

private:

};