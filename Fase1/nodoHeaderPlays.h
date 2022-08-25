#pragma once

#include "pilaPlays.h"


class nodoHeaderPlays
{
public:

    pilaPlays inStack;
    string categoria;


    nodoHeaderPlays* siguiente;
    nodoHeaderPlays() {
        siguiente = NULL;
    }

    void setCat(string c) {
        this->categoria = c;
    }

    string getCat() {
        return categoria;
    }

private:


};