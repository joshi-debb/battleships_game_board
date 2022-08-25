

#pragma once

#include "nodoPlays.h"
#include <iostream>

using namespace std;

class pilaPlays
{

public:

    nodoPlays* primero;

    pilaPlays() {
        primero = NULL;
    }

    void addToEnd(nodoPlays* plays);
    void showStack();
    void doGraphics();

private:
};

