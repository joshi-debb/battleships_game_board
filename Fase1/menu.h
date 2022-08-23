#pragma once

#include <string>

#include "listaCircularUser.h"
#include "listaSimpleHeaders.h"
#include "listaSimpleItem.h"

using namespace std;

class menu {
public:

    // menus
    void main_menu(listaCircularUser listaUsers, listaSimpleHeaders strutctList, listaSimpleItem listItem);
    void sec_menu(listaCircularUser listaUsers, string);
    void third_menu(listaCircularUser listaUsers, listaSimpleHeaders strutctList, listaSimpleItem listItem);

    menu() {

    }

private:

};