

#pragma once

#include "nodoTutorial.h"
#include <iostream>

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
    void showQueue();
    void doGraphics();

private:
};
