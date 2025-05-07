#include <iostream>
#include <fstream>
#include <cmath>
#include <cstdlib>
using namespace std;
const int MAX_PRODUCTS = 100;

// --------------------- FUNCTION PROTOTYPE ---------------------
void mainMenu();
void teamAMenu();
void teamBMenu();
void sortSearchProduct();

// --------------------- STRUCTURES ---------------------
struct Product {
    int id;
    string name;
    double price;
    string description;
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
int loadProducts(Product products[]) {
    ifstream file("raw_product.txt");
    int count = 0;
    while (file >> products[count].id) {
	    file.ignore(); // Ignore the whitespace after ID
	    getline(file, products[count].name, '"');
	    getline(file, products[count].name, '"'); // Read name inside quotes
	    file >> products[count].price;
	    file.ignore(); // Ignore space after price
	    getline(file, products[count].description, '"');
	    getline(file, products[count].description, '"'); // Read description inside quotes
	    count++;
	}
    file.close();
    return count;
}
//---------------------- MAIN MENU ------------------------
void mainMenu(){
	int choice;
	
	cout<<"=================================================="<<endl;
    cout<<"                  TDS Assignment                  "<<endl;
    cout<<"=================================================="<<endl;
    cout<<"1. Team A"<<endl;
    cout<<"2. Team B"<<endl;
    cout<<"3. Exit System"<<endl;
    cout<<"--------------------------------------------------"<<endl;
    cout<<"Enter your choice: ";
    cin>>choice;
    
    switch(choice){
    	case 1:
    		{
    			system("cls");
    			teamAMenu();
    			break;
			}
		case 2:
			{
				system("cls");
				teamBMenu();
				break;
			}
		case 3:
			{
				cout<<"\nThank you for using the system. Goodbye!"<<endl;
				exit(1);
				break;
			}
		default:
			{
				cout<<"Invalid choice. Press Enter to try again"<<endl;
				cin.ignore();
				cin.get();
				mainMenu();
				break;
			}
	}
}

//---------------------- TEAM A MENU ------------------------
void teamAMenu(){
	int choice;
	
	cout<<"=================================================="<<endl;
    cout<<"                    Team A Menu                   "<<endl;
    cout<<"=================================================="<<endl;
    cout<<"1. Hashing Customer"<<endl;
    cout<<"2. Hashing Rating"<<endl;
    cout<<"3. Return to Main Menu"<<endl;
    cout<<"--------------------------------------------------"<<endl;
    cout<<"Enter your choice: ";
    cin>>choice;
    switch(choice){
    	case 1:
    		{
    			system("cls");
    			cout<<"Successfully enter page hashing customer";
    			break;
			}
		case 2:
			{
				system("cls");
    			cout<<"Successfully enter page hashing rating";
				break;
			}
		case 3:
			{
				system("cls");
				mainMenu();
				break;
			}
		default:
			{
				cout<<"Invalid choice. Press Enter to try again"<<endl;
				cin.ignore();
				cin.get();
				system("cls");
				teamAMenu();
				break;
			}
	}
}

//---------------------- TEAM B MENU ------------------------
void teamBMenu(){
	int choice;
	
	cout<<"=================================================="<<endl;
    cout<<"                    Team B Menu                   "<<endl;
    cout<<"=================================================="<<endl;
    cout<<"1. Product"<<endl;
    cout<<"2. Order History"<<endl;
    cout<<"3. Return to Main Menu"<<endl;
    cout<<"--------------------------------------------------"<<endl;
    cout<<"Enter your choice: ";
    cin>>choice;
    switch(choice){
    	case 1:
    		{
    			system("cls");
    			sortSearchProduct();
    			break;
			}
		case 2:
			{
				system("cls");
    			cout<<"Successfully enter page hashing rating";
				break;
			}
		case 3:
			{
				system("cls");
				mainMenu();
				break;
			}
		default:
			{
				cout<<"Invalid choice. Press Enter to try again"<<endl;
				cin.ignore();
				cin.get();
				system("cls");
				teamBMenu();
				break;
			}
	}
}

//---------------------- SORT & SEARCH PRODUCT-------------------
void sortSearchProduct(){
	Product products[MAX_PRODUCTS];
	
	int productCount = loadProducts(products);

    shellSort(products, productCount);

    cout << "\nSorted Products by ID:\n";
    for (int i = 0; i < productCount; i++) {
        cout << "ID   : " << products[i].id << endl;
        cout << "Name : " << products[i].name << endl;
        cout << "Price: " << products[i].price << endl;
		cout << products[i].description << endl;
        cout <<"______________________________________________________________________________________________________________________________"<< endl;
    }

    int searchProdID;

    cout << "\nEnter Product ID to search: ";
    cin >> searchProdID;
    int prodIndex = jumpSearch(products, productCount, searchProdID);

    if (prodIndex != -1)
    {
    	cout << "Product Found:\n";
		cout << "ID: " << products[prodIndex].id << "\n";
		cout << "Name: " << products[prodIndex].name << "\n";
		cout << "Price: " << products[prodIndex].price << "\n";
		cout << "Description: " << products[prodIndex].description << "\n";
    }
    else
        cout << "Product not found.\n";
}

// --------------------- MAIN PROGRAM ---------------------
int main() {
    mainMenu();

    return 0;
}
