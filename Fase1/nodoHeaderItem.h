



#pragma once


#include "listaSimpleItem.h"


class nodoHeaderItem
{
public:

    listaSimpleItem listainterna;
    string categoria;


    nodoHeaderItem* sig;
    nodoHeaderItem() {
        sig = NULL;
    }

    void setCat(string c) {
        this->categoria = c;
    }

    string getCat() {
        return categoria;
    }

private:


};

