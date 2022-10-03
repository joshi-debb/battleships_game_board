

#include <iostream>
#include <cstdlib>

#include "listaCircularUser.h"
#include "listaSimpleHeaders.h"
#include "listaSimplePlays.h"
#include "listaSimpleItem.h"
#include "colaTutorial.h"

#include "menu.h"

#include "crow.h"



using namespace std;
using std::stoi;

int main() {

	listaCircularUser listaUsers;
	listaSimpleItem listItem;
	listaSimpleHeaders structList;
	colaTutorial queue;

	listaSimplePlays* newStack = new listaSimplePlays();

   //menu nuevoMenu;
   //nuevoMenu.main_menu(listaUsers, structList, listItem, queue, newStack);


    crow::SimpleApp app;
    CROW_ROUTE(app, "/")
        ([] {
		return crow::response("API -> UP!");
			});


	CROW_ROUTE(app, "/login")
		([&listaUsers](const crow::request& req)
			{
				auto x = crow::json::load(req.body);
				if (!x)
					return crow::response(400);
				string nick = x["nick"].s();
				string pass = x["password"].s();

				nodoUser* usuario = listaUsers.searchUsers(nick);

				if (usuario == nullptr) {
					return crow::response("Usuario no encontrado");
				}

				if (usuario->getPassword() == pass) {
					return crow::response(usuario->getNick());
				}

				return crow::response("incorrecta");
			
			});


	CROW_ROUTE(app, "/sign_up")
		.methods("POST"_method)([&listaUsers](const crow::request& req)
			{
				auto x = crow::json::load(req.body);
				if (!x)
					return crow::response(400);

				nodoUser* nuevo;
				
				string nick = x["nick"].s();
				string pass = x["password"].s();
				string age = x["edad"].s();

				if (listaUsers.searchExist(nick) != true) {
					nuevo = new nodoUser();

					nuevo->setNick(nick);
					nuevo->setPassword(pass);
					nuevo->setAge(stoi(age));

					listaUsers.addToEnd(nuevo);
					return crow::response("registrado");
				}

				return crow::response("repetido");
				
			});
	
	CROW_ROUTE(app, "/edit")
		.methods("PUT"_method)([&listaUsers](const crow::request& req)
			{
				auto x = crow::json::load(req.body);
				if (!x)
					return crow::response(400);
				string name = x["name"].s();
				string nick = x["nick"].s();
				string pass = x["password"].s();
				string age = x["edad"].s();

				nodoUser* usuario = listaUsers.searchUsers(name);

				if (nick != "") {
					usuario->setNick(nick);
				}
				if(age != "") {
					usuario->setAge(stoi(age));
				}
				if (pass != "") {
					usuario->setPassword(pass);
				}

				return crow::response("datos actualizados");

			});



	CROW_ROUTE(app, "/delete")
		.methods("DELETE"_method)([&listaUsers](const crow::request& req)
			{
				auto x = crow::json::load(req.body);
				if (!x)
					return crow::response(400);
				string nick = x["nick"].s();
				string pass = x["password"].s();

				nodoUser* usuario = listaUsers.searchUsers(nick);

				if (listaUsers.deleteUser(usuario->getNick(), usuario->getPassword()) == true) {
					return crow::response("Usuario Eliminado!");
				}

				return crow::response("Eliminacion imcompleta!");
			
			});


	CROW_ROUTE(app, "/up_plays")
		.methods("POST"_method)([&listaUsers,&newStack](const crow::request& req)
			{
				auto x = crow::json::load(req.body);
				if (!x)
					return crow::response(400);

				string nick = x["nick"].s();
				string posx = x["x"].s();
				string posy = x["y"].s();

				nodoUser* usuario = listaUsers.searchUsers(nick);

				if (usuario != NULL) {

					newStack->doGamePlays(usuario, stoi(posx), stoi(posy));
					return crow::response("Juagada aniadida");

				}

				return crow::response("Usuario no encontrado");

			});
	
	CROW_ROUTE(app, "/up_coins")
		.methods("PUT"_method)([&listaUsers](const crow::request& req)
			{
				auto x = crow::json::load(req.body);
				if (!x)
					return crow::response(400);
				string nick = x["nick"].s();
				string coins = x["monedas"].s();

				nodoUser* usuario = listaUsers.searchUsers(nick);

				if (coins != "") {
					usuario->setCoins(stoi(coins));
				}

				return crow::response("Monedas actualizadas");

			});



	CROW_ROUTE(app, "/masiva")
		.methods("POST"_method)([&listaUsers, &structList, &listItem, &queue](const crow::request& req)
			{
				auto x = crow::json::load(req.body);
				if (!x)
					return crow::response(400);

				string ruta = x["ruta"].s();

				listaUsers.loadFile(ruta);
				structList.loadFile(ruta);
				listItem.loadFile(ruta);
				queue.loadFile(ruta);
				
				return crow::response("Informacion Cargada!");
			});

	

	CROW_ROUTE(app, "/usersUp")
		([&listaUsers]()
			{
				std::vector<crow::json::wvalue> temp = listaUsers.bubbleSortUP();
				crow::json::wvalue final = std::move(temp);
				return crow::response(std::move(final));
			});


	CROW_ROUTE(app, "/usersDw")
		([&listaUsers]()
			{
				std::vector<crow::json::wvalue> temp = listaUsers.bubbleSortDW();
				crow::json::wvalue final = std::move(temp);
				return crow::response(std::move(final));
			});


	CROW_ROUTE(app, "/itemsUp")
		([&listItem]()
			{
				std::vector<crow::json::wvalue> temp = listItem.bubbleSortUP();
				crow::json::wvalue final = std::move(temp);
				return crow::response(std::move(final));
			});


	CROW_ROUTE(app, "/itemsDw")
		([&listItem]()
			{
				std::vector<crow::json::wvalue> temp = listItem.bubbleSortDW();
				crow::json::wvalue final = std::move(temp);
				return crow::response(std::move(final));
			});
	
	CROW_ROUTE(app, "/items")
		([&structList]()
			{
				std::vector<crow::json::wvalue> temp = structList.showStruct();
				crow::json::wvalue final = std::move(temp);
				return crow::response(std::move(final));
			});

	CROW_ROUTE(app, "/tuto")
		([&queue]()
			{
				std::vector<crow::json::wvalue> temp = queue.showQueue();
				crow::json::wvalue final = std::move(temp);
				return crow::response(std::move(final));
			});


	CROW_ROUTE(app, "/circular_graph")
		([&listaUsers]() {
			
				if (listaUsers.is_empty()) {
					return crow::response("nografica");
				}else {
					listaUsers.doGraphics();
					return crow::response("grafica");
				}
			});


	CROW_ROUTE(app, "/listas_graph")
		([&structList]
			{
				
				if (structList.is_empty()) {
					return crow::response("nografica");
				}
				else {
					structList.doGraphics();
					return crow::response("grafica");
				}

			});


	CROW_ROUTE(app, "/cola_graph")
		([&queue]
			{
				if (queue.is_empty()) {
					return crow::response("nografica");
				}
				else {
					queue.doGraphics();
					return crow::response("grafica");
				}

			});

	CROW_ROUTE(app, "/pila_graph")
		([&newStack]
			{
				if (newStack->is_empty()) {
					return crow::response("nografica");
				}
				else {
					newStack->doGraphics();
					return crow::response("grafica");
				}

			});


	

	CROW_ROUTE(app, "/coins")
		([&listaUsers](const crow::request& req)
			{
				auto x = crow::json::load(req.body);
				if (!x)
					return crow::response(400);
				string nick = x["nick"].s();

				nodoUser* usuario = listaUsers.searchUsers(nick);

				if (usuario == nullptr) {
					return crow::response("Usuario no encontrado");
				}

				int aux = usuario->getCoins();
				stringstream ss;
				ss << aux;
				string str = ss.str();

				return crow::response(str);
			});

	app.port(5000).multithreaded().run();




    return 0;
}
