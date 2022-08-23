



#pragma once


#include "listaSimpleItem.h"


class nodoHeaderItem
{
public:

    listaSimpleItem inList;
    string categoria;


    nodoHeaderItem* siguiente;
    nodoHeaderItem() {
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

