

#include <iostream>
#include <cstdlib>

#include "listaCircularUser.h"
#include "listaSimpleHeaders.h"
#include "listaSimplePlays.h"
#include "listaSimpleItem.h"
#include "colaTutorial.h"

#include "menu.h"

using namespace std;

int main() {

    listaSimpleItem listItem;
    listaSimpleHeaders structList;
    listaCircularUser listaUsers;
    colaTutorial queue;

    listaSimplePlays* newStack = new listaSimplePlays();

    menu nuevoMenu;
    nuevoMenu.main_menu(listaUsers,structList,listItem,queue,newStack);

    return 0;
}
