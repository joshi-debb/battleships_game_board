#pragma once

#include <string>

#include "listaCircularUser.h"
#include "listaSimpleHeaders.h"
#include "listaSimpleItem.h"
#include "listaSimplePlays.h"
#include "colaTutorial.h"
#include "nodoUser.h"

using namespace std;

class menu {

public:

    // menus
    void main_menu(listaCircularUser listaUsers,listaSimpleHeaders strutctList,listaSimpleItem listItem,colaTutorial queue,listaSimplePlays* stack);
    void sec_menu(listaCircularUser listaUsers,nodoUser* user, listaSimpleItem listItem,colaTutorial queue,listaSimplePlays* stack);
    void third_menu(listaCircularUser listaUsers,listaSimpleHeaders strutctList,listaSimpleItem listItem,colaTutorial queue,listaSimplePlays* stack);

    menu() {
    
    }

private:

};