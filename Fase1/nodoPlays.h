
#pragma once


#include <string>

using namespace std;

class nodoPlays {
private:

    int x = 0;
    int y = 0;

public:

    nodoPlays* siguiente;

    nodoPlays() {
        siguiente = NULL;
    }

    void setX(int x) {
        this->x = x;
    }

    void setY(int y) {
        this->y = y;
    }

    int getX() {
        return x;
    }

    int getY() {
        return y;
    }
};