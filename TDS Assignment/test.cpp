#include <iostream>
#include <fstream>
#include <cmath>
using namespace std;

const int MAX_CUSTOMERS = 100;
const int MAX_PRODUCTS = 100;

// --------------------- STRUCTURES ---------------------
struct Customer {
    int id;
    char name[50];
};

struct Product {
    int id;
    char name[50];
};

// --------------------- SHELL SORT ---------------------
template<typename T>
void shellSort(T arr[], int size) {
    for (int gap = size / 2; gap > 0; gap /= 2) {
        for (int i = gap; i < size; i++) {
            T temp = arr[i];
            int j;
            for (j = i; j >= gap && arr[j - gap].id > temp.id; j -= gap) {
                arr[j] = arr[j - gap];
            }
            arr[j] = temp;
        }
    }
}

// --------------------- JUMP SEARCH ---------------------
template<typename T>
int jumpSearch(T arr[], int size, int targetID) {
    int step = sqrt(size);
    int prev = 0;

    while (arr[min(step, size) - 1].id < targetID) {
        prev = step;
        step += sqrt(size);
        if (prev >= size) return -1;
    }

    for (int i = prev; i < min(step, size); i++) {
        if (arr[i].id == targetID) return i;
    }

    return -1;
}

// --------------------- READ FROM FILE ---------------------
int loadCustomers(Customer customers[]) {
    ifstream file("customer.txt");
    int count = 0;
    while (file >> customers[count].id >> customers[count].name) {
        count++;
    }
    file.close();
    return count;
}

int loadProducts(Product products[]) {
    ifstream file("product.txt");
    int count = 0;
    while (file >> products[count].id >> products[count].name) {
        count++;
    }
    file.close();
    return count;
}

// --------------------- MAIN PROGRAM ---------------------
int main() {
    Customer customers[MAX_CUSTOMERS];
    Product products[MAX_PRODUCTS];

    int customerCount = loadCustomers(customers);
    int productCount = loadProducts(products);

    shellSort(customers, customerCount);
    shellSort(products, productCount);

    cout << "Sorted Customers by ID:\n";
    for (int i = 0; i < customerCount; i++) {
        cout << customers[i].id << " " << customers[i].name << endl;
    }

    cout << "\nSorted Products by ID:\n";
    for (int i = 0; i < productCount; i++) {
        cout << products[i].id << " " << products[i].name << endl;
    }

    int searchCustID, searchProdID;
    cout << "\nEnter Customer ID to search: ";
    cin >> searchCustID;
    int custIndex = jumpSearch(customers, customerCount, searchCustID);

    if (custIndex != -1)
        cout << "Customer Found: " << customers[custIndex].name << endl;
    else
        cout << "Customer not found.\n";

    cout << "\nEnter Product ID to search: ";
    cin >> searchProdID;
    int prodIndex = jumpSearch(products, productCount, searchProdID);

    if (prodIndex != -1)
        cout << "Product Found: " << products[prodIndex].name << endl;
    else
        cout << "Product not found.\n";

    return 0;
}
