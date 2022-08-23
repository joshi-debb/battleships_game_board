#pragma once

#include <string>
using namespace std;

class nodoItem {
private:
    string id, category, name, src;
    int price = 0;

public:

    nodoItem* siguiente;

    nodoItem() {
        siguiente = NULL;
    }


    void setId(string i) {
        this->id = i;
    }

    void setCategory(string c) {
        this->category = c;
    }

    void setName(string n) {
        this->name = n;
    }

    void setSrc(string s) {
        this->src = s;
    }

    void setPrice(int p) {
        this->price = p;
    }

    string getId() {
        return id;
    }

    string getCategory() {
        return category;
    }

    string getName() {
        return name;
    }

    string getSrc() {
        return src;
    }

    int getPrice() {
        return price;
    }
};