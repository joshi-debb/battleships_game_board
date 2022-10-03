

#pragma once

#include "nodoTutorial.h"
#include <iostream>

#include "crow.h"

using namespace std;

class colaTutorial
{

public:

    nodoTutorial* primero;
    nodoTutorial* ultimo;

    colaTutorial() {
        primero = NULL;
        ultimo = NULL;
    }

    void loadFile(string ruta);
    void addToEnd(nodoTutorial* user);
    vector<crow::json::wvalue>  showQueue();
    void doGraphics();

    bool is_empty();

private:
};
