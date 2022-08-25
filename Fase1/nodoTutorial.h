

#pragma once

#include <string>

using namespace std;

class nodoTutorial {
private:

    int alto = 0;
    int ancho = 0;
    int x = 0;
    int y = 0;

public:

    nodoTutorial* siguiente;

    nodoTutorial() {
        siguiente = NULL;
    }

    void setAlto(int al) {
        this->alto = al;
    }

    void setAncho(int an) {
        this->ancho = an;
    }

    void setX(int x) {
        this->x = x;
    }

    void setY(int y) {
        this->y = y;
    }

    int getAlto() {
        return alto;
    }

    int getAncho() {
        return ancho;
    }

    int getX() {
        return x;
    }

    int getY() {
        return y;
    }
};
