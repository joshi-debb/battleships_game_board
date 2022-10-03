

#pragma once

#include "nodoHeaderPlays.h"
#include "nodoUser.h"

using namespace std;

class listaSimplePlays
{
public:

    nodoHeaderPlays* primero;

    listaSimplePlays() {
        primero = NULL;
    }

    void Insertar(nodoPlays* plays, string categoria);
    nodoHeaderPlays* BuscarPrincipal(nodoHeaderPlays* inicioL, string categoria);
    void doGamePlays(nodoUser* user, int posx, int posy);
    void doGraphics();
    void showStruct();

    bool is_empty();

private:
};