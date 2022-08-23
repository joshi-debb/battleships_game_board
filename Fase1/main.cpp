

#include <iostream>
#include <cstdlib>

#include "listaCircularUser.h"
#include "listaSimpleHeaders.h"
#include "listaSimpleItem.h"
#include "menu.h"

using namespace std;

int main() {

    listaSimpleItem listItem;
    listaSimpleHeaders structList;
    listaCircularUser listaUsers;

    menu nuevoMenu;
    nuevoMenu.main_menu(listaUsers, structList, listItem);

    return 0;
}
