#include "menu.h"

#include <iostream>
#include <cstdlib>

#include "listaCircularUser.h"
#include "listaSimpleHeaders.h"
#include "listaSimplePlays.h"
#include "listaSimpleItem.h"
#include "colaTutorial.h"
#include "nodoUser.h"
#include "nodoPlays.h"


// menus
void menu::main_menu(listaCircularUser listaUsers, listaSimpleHeaders structList, listaSimpleItem listItem, colaTutorial queue, listaSimplePlays* stack) {

    nodoUser* nuevo;

    char opcion;
    bool repetir = true;

    string ruta;

    string n;
    string p;
    int a = 0;

    do {
        system("cls");

        cout << "\n\nMenu" << endl;
        cout << "1. Carga Masiva" << endl;
        cout << "2. Registrar Usuario" << endl;
        cout << "3. Login" << endl;
        cout << "4. Reportes" << endl;
        cout << "5. Salir del Juego" << endl;

        cout << "\nIngrese una opcion: " << endl;
        cin >> opcion;

        switch (opcion) {
            case '1':

                cout << "Bienvenido a la carga masiva!" << endl;
                cout << "Ingrese el nombre de su archivo con extension: " << endl;
                cin >> ruta;

                listaUsers.loadFile(ruta);
                structList.loadFile(ruta);
                listItem.loadFile(ruta);
                queue.loadFile(ruta);
                system("pause");
                break;

            case '2':

                nuevo = new nodoUser();
                cout << "\n-> Bienvenido al registro de Usuarios! <- \n\n";
                cout << " > Ingrese su nombre de usuario: ";
                cin >> n;
                if (listaUsers.searchExist(n) != true) {
                    nuevo->setNick(n);
                    cout << " > Ingrese su Edad: ";
                    cin >> a;
                    nuevo->setAge(a);
                    cout << " > Ingrese su Password: ";
                    cin >> p;
                    nuevo->setPassword(p);

                    listaUsers.addToEnd(nuevo);
                }
                else {
                    cout << "Nombre de usuario existente!" << endl;
                    cout << "Intente con uno nuevo!" << endl;
                }
                
                system("pause");
                break;

            case '3':
                listaUsers.login(listaUsers,listItem,queue,stack);
                system("pause");
                break;

            case '4':

                third_menu(listaUsers,structList,listItem,queue,stack);
                system("pause");
                break;

            case '5':
                repetir = false;
                break;

            default:
                cout << "Elija una opcion valida" << endl;
                system("pause");
                break;
            }
    } while (repetir);
}

void menu::sec_menu(listaCircularUser listaUsers,nodoUser* user,listaSimpleItem listaItems,colaTutorial queue,listaSimplePlays* stack) {

    listaSimplePlays* newStack = new listaSimplePlays();
    newStack = stack;

    nodoUser* nuevoUser = new nodoUser();
    nuevoUser = user;

    nodoPlays* nuevo = new nodoPlays();

    char opcion;
    bool repetir = true;
    int coins = 0;
    int posX = 0;
    int posY = 0;

    do {
        system("cls");

        cout << "\n\n>Usuario Activo: " << nuevoUser->getNick() << "\n\n";

        cout << "a. Editar Informacion" << endl;
        cout << "b. Eliminar Cuenta" << endl;
        cout << "c. Ver el tutorial" << endl;
        cout << "d. Ver articulos de la tienda" << endl;
        cout << "e. Realizar movimientos" << endl;
        cout << "f. Volver al menu principal" << endl;

        cout << "\nIngrese una opcion: " << endl;
        cin >> opcion;

        switch (opcion) {
        case 'a':
            listaUsers.editInfo(nuevoUser->getNick());
            system("pause");
            break;

        case 'b':
            if (listaUsers.deleteUser(nuevoUser->getNick(),nuevoUser->getPassword()) == true) {
                repetir = false;
            }
            system("pause");
            break;

        case 'c':

            queue.showQueue();
            system("pause");
            break;

        case 'd':

            listaItems.showList();
            system("pause");
            break;

        case 'e':

            newStack->doGamePlays(nuevoUser);
            
            system("pause");
            break;

        case 'f':
            repetir = false;
            break;

        default:
            cout << "Elija una opcion valida" << endl;
            system("pause");
            break;
        }
    } while (repetir);
}

void menu::third_menu(listaCircularUser listaUsers,listaSimpleHeaders structList,listaSimpleItem listItem,colaTutorial queue,listaSimplePlays* stack) {

    listaSimplePlays* newStack = new listaSimplePlays();
    listaSimpleItem listaOrd;

    newStack = stack;


    char opcion;
    bool repetir = true;

    do {
        system("cls");

        cout << "\n\n> -> Reportes <- " << "!\n\n";

        cout << "a. Lista Ciruclar" << endl;
        cout << "b. Lista de Listas" << endl;
        cout << "c. Cola de Movimientos" << endl;
        cout << "d. Lista de Pilas" << endl;
        cout << "e. Listado de Usuarios" << endl;
        cout << "f. Listado de Articulos" << endl;
        cout << "g. salir de reportes" << endl;

        cout << "\nIngrese una opcion: " << endl;
        cin >> opcion;

        switch (opcion) {
        case 'a':
            cout << "Grafico de Estructura" << endl;
            listaUsers.doGraphics();
            system("pause");
            break;

        case 'b':

            cout << "Grafico de Estructura" << endl;
            structList.showStruct();
            structList.doGraphics();
            system("pause");
            break;

        case 'c':

            cout << "Grafico de Estructura" << endl;
            queue.doGraphics();
            system("pause");
            break;

        case 'd':

            cout << "Grafico de Estructura" << endl;
            newStack->showStruct();
            newStack->doGraphics();
            system("pause");
            break;

        case 'e':

            cout << "\n\nDespliegue Ascendente: " << endl;
            listaUsers.bubbleSortUP(listaUsers);
            listaUsers.showList();

            cout << "\n\nDespliegue Descendente: " << endl;
            listaUsers.bubbleSortDW(listaUsers);
            listaUsers.showList();
            system("pause");
            break;

        case 'f':
            
            cout << "\n\nDespliegue Ascendente: " << endl;
            listItem.bubbleSortUP(listItem);
            listItem.showList();

            cout << "\n\nDespliegue Descendente: " << endl;
            listItem.bubbleSortDW(listItem);
            listItem.showList();

            system("pause");
            break;

        case 'g':
            repetir = false;
            break;

        default:
            cout << "Elija una opcion valida" << endl;
            system("pause");
            break;
        }
    } while (repetir);
}