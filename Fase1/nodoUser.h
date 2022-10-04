#pragma once

#include <string>

using namespace std;

class nodoUser {
private:
    string nick, password;
    int coins = 0;
    int age = 0;
    int id = 0;

public:

    nodoUser* siguiente;
    nodoUser* atras;


    nodoUser() {
        siguiente = NULL;
        atras = NULL;
    }

    void setId(int id) {
        this->id = id;
    }

    void setNick(string n) {
        this->nick = n;
    }

    void setPassword(string p) {
        this->password = p;
    }

    void setAge(int a) {
        this->age = a;
    }

    void setCoins(int c) {
        this->coins = c;
    }

    string getNick() {
        return nick;
    }

    string getPassword() {
        return password;
    }

    int getAge() {
        return age;
    }

    int getCoins() {
        return coins;
    }

    int getId() {
        return id;
    }

};
