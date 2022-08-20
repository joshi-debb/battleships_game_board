#include <iostream>

#include <cstdlib>

using namespace std;

// menus
void main_menu();
void sec_menu(string, string, string);

// Login
void login();

// Clase Usuario
class usuario
{
private:
	string nick, password, age;

public:
	usuario() {}

	void setNick(string n)
	{
		nick = n;
	}

	void setPassword(string p)
	{
		password = p;
	}

	void setAge(string a)
	{
		age = a;
	}

	string getNick()
	{
		return nick;
	}

	string getPassword()
	{
		return password;
	}

	string getAge()
	{
		return age;
	}

	usuario *siguiente;
	usuario *atras;
} * primero, *ultimo;

void addToEnd();
void showList();

// Aniadir al final
void addToEnd()
{

	string n;
	string p;
	string a;

	usuario *nuevo = new usuario();
	cout << "\n-> Bienvenido al registro de Usuarios! <- \n\n";
	cout << " > Ingrese su nombre de usuario: ";
	cin >> n;
	nuevo->setNick(n);
	cout << " > Ingrese su Edad: ";
	cin >> a;
	nuevo->setAge(a);
	cout << " > Ingrese su Password: ";
	cin >> p;
	nuevo->setPassword(p);

	if (primero == NULL)
	{
		primero = nuevo;
		ultimo = nuevo;
		primero->siguiente = primero;
		primero->atras = ultimo;
	}
	else
	{
		ultimo->siguiente = nuevo;
		nuevo->atras = ultimo;
		nuevo->siguiente = primero;
		ultimo = nuevo;
		primero->atras = ultimo;
	}
	cout << "\n>Usuario Registrado!\n\n";
}

// Mostrar elementos
void showList()
{
	usuario *actual = new usuario();
	actual = primero;
	if (primero != NULL)
	{
		do
		{
			cout << "\tNombre: " << actual->getNick() << "\tage: " << actual->getAge() << "\tPassword: " << actual->getPassword() << "\n";
			actual = actual->siguiente;
		} while (actual != primero);
	}
	else
	{
		cout << "\n>La lista se Encuentra Vacia\n\n";
	}
}

// Buscar por nombre
void login()
{
	usuario *actual = new usuario();
	actual = primero;
	bool encontrado = false;
	string aux;
	if (primero == NULL)
	{
		cout << "No hay usuarios registrados!\n\n";
	}else{
		cout << " > Ingrese el nombre del usuario: ";
		cin >> aux;
		do
		{
			if (actual->getNick() == aux)
			{
				cout << ">Usuario Encontrado!\n\n";
				encontrado = true;

				string pass;
				cout << " > Ingrese su Password: ";
				cin >> pass;

				if (pass == actual->getPassword() && aux == actual->getNick())
				{
					sec_menu(actual->getNick(), actual->getPassword(), actual->getAge());
				}
				else
				{
					cout << ">password incorrecto!\n";
					system("pause");
				}
			}
			actual = actual->siguiente;
		} while (actual != primero && encontrado != true);

		if (!encontrado)
		{
			cout << "\n usuario no Encontrado\n\n";
		}
	}
}

// menus
void main_menu()
{
	char opcion;
	bool repetir = true;

	do
	{
		system("cls");

		cout << "\n\nMenu" << endl;
		cout << "1. Carga Masiva" << endl;
		cout << "2. Registrar Usuario" << endl;
		cout << "3. Login" << endl;
		cout << "4. Reportes" << endl;
		cout << "5. Salir del Juego" << endl;

		cout << "\nIngrese una opcion: " << endl;
		cin >> opcion;

		switch (opcion)
		{
		case '1':

			cout << "Bienvenido a la carga masiva!";
			system("pause");
			break;

		case '2':
			addToEnd();
			system("pause");
			break;

		case '3':
			login();
			system("pause");
			break;

		case '4':
			showList();
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

void sec_menu(string _nick, string _pass, string _age)
{

	char opcion;
	bool repetir = true;

	do
	{
		system("cls");

		cout << "\n\n>Bienvenido -> " << _nick << "!\n\n";

		cout << "a. Editar Informacion" << endl;
		cout << "b. Eliminar Cuenta" << endl;
		cout << "c. Ver el tutorial" << endl;
		cout << "d. Ver articulos de la tienda" << endl;
		cout << "e. Realizar movimientos" << endl;
		cout << "f. Volver al menu principal" << endl;

		cout << "\nIngrese una opcion: " << endl;
		cin >> opcion;

		switch (opcion)
		{
		case 'a':
			cout << "hola hola" << endl;
			system("pause");
			break;

		case 'b':

			system("pause");
			break;

		case 'c':

			system("pause");
			break;

		case 'd':

			system("pause");
			break;

		case 'e':

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

int main()
{

	main_menu();
	return 0;
}
