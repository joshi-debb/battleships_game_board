#pragma once


#include "nodoUser.h"
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
    void login(listaCircularUser listaUsers);
    void showList();
    void editInfo(string);
    bool deleteUser();

private:

};