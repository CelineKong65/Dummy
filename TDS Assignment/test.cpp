#include <iostream>
#include <fstream>
#include <cmath>
#include <cstdlib>
#include <string>
#include <sstream>

using namespace std;
const int MAX_PRODUCTS = 100;

// --------------------- FUNCTION PROTOTYPE ---------------------
void mainMenu();
void teamAMenu();
void teamBMenu();
void sortSearchProduct();
void printWrappedText(const string& text);

// --------------------- STRUCTURES ---------------------
struct Product {
    int id;
    string name;
    double price;
    string description;
};

struct Customer {
    string id;
    string name;
    string email;
    string phone;
};

// --------------------- HASHING + LINKED LIST QUEUE ---------------------
class HashCustomer {
	private:
		struct Node {
			Customer data;
			Node* next;
		};
	
		Node* front;
		Node* rear;
		string filename;
		
		
		bool isValidPhone(const string& phone) {
			const char* p = phone.c_str();
			int i = 0;
			int digitCount = 0;
		
			while (p[i] != '\0') {
				if (i == 3 && p[i] != '-') {
					return false;
				}
		
				char c = p[i];
		
				if (!((c >= '0' && c <= '9') || c == '-' )) {
					return false;
				}
		
				if (c >= '0' && c <= '9') {
					digitCount++;
				}
		
				i++;
			}
		
			if (digitCount < 10 || digitCount > 11) {
				return false;
			}
		
			if (i < 4) {
				return false;
			}
		
			return true;
		}
	
		
		bool isValidEmail(const string& email) {
			if(email[0] == '\0') return false;
			
			bool hasAt = false;
			int atPos = -1;
			int i = 0;
			while(email[i] != '0') {
				if(email[i] == '@'){
					hasAt = true;
					atPos = i;
					break;
				}
				i++;
			}
			
			if(!hasAt) return false;
			
			if (atPos == 0 || email[atPos + 1] == '\0') return false;
		
			bool hasDot = false;
			i = atPos + 1;
			while (email[i] != '\0') {
				if (email[i] == '.') {
					hasDot = true;
					if (email[i + 1] == '\0') return false;
					break;
				}
				i++;
			}
			return hasDot;
		}
	
	public:
		HashCustomer() : front(NULL), rear(NULL), filename("customer.txt") {}
	
		~HashCustomer() {
			Node* current = front;
			while (current != NULL) {
				Node* next = current->next;
				delete current;
				current = next;
			}
		}
	
		void enqueue(const Customer& customer) {
			Node* newNode = new Node;
			newNode->data = customer;
			newNode->next = NULL;
			
			if (isEmpty()) {
				front = rear = newNode;
			} else {
				rear->next = newNode;
				rear = newNode;
			}
		}
		
		Customer parseCustomer(const string& line) {
			Customer c;
			stringstream ss(line);
			ss >> c.id >> c.name >> c.email >> c.phone;
			return c;
		}
	
		bool isEmpty() const {
			return front == NULL;
		}
	
		void saveToFile() {
			ofstream file("customer.txt");
			if (!file) {
				cout << "File fail to connect" << endl;
				return;
			}
	
			Node* current = front;
			while (current != NULL) {
				file << current->data.id << " "
					 << current->data.name << " "
					 << current->data.email << " "
					 << current->data.phone << endl;
				current = current->next;
			}
	
			file.close();
		}
	
		void loadFromFile() {
			ifstream file("customer.txt");
			if (!file) {
				cout << "File fail to connect" << endl;
				return;
			}
	
			string line;
			while (getline(file, line)) {
				if(!line.empty()) {
					Customer c = parseCustomer(line);
					enqueue(c);
				}
			}
	
			file.close();
		}
	
		void display() {
			Node* current = front;
			int i = 1;
			while (current != NULL) {
				cout << i << "." << current->data.id << " " 
								 << current->data.name << " " 
								 << current->data.email << " "
								 << current->data.phone << endl;
				current = current->next;
				i++;
			}
		}
	
		void hashingCustomer() {
			loadFromFile();
			
			int choice;
			Customer cus;
			
			do {
				cout << "==================================================" << endl;
				cout << "                  Hashing Customer                " << endl;
				cout << "==================================================" << endl;
				cout << "1. Display Customer Information";
				cout << "\n2. Add Customer Information";
				cout << "\n3. Search Customer Information";
				cout << "\n4. Save Customer Information";
				cout << "\n5. Return to Team A Menu";
				cout << "\n--------------------------------------------------" << endl;
				cout << "\nEnter your choice: ";
				cin >> choice;
				cin.ignore();
				cout << endl;
				
				switch(choice) {
					case 1:
						display();
						cout << "\nPress [Enter] back to menu...";
						cin.get(); 
						system("cls");
						break;
						
					case 2: 
						cout << "Enter customer ID : ";
						getline(cin, cus.id);
						
						cout << "Enter customer name : ";
						getline(cin, cus.name);
						
						do {
							cout << "Enter customer phone number (e.g. 010-1234567) : ";
							getline(cin, cus.phone);
							if (!isValidPhone(cus.phone)) {
								cout << "Invalid phone number! Please try again.\n";
							}
						} while (!isValidPhone(cus.phone));
						
						do {
							cout << "Enter customer email (e.g. john@example.com) : ";
							getline(cin, cus.email);
							if (!isValidEmail(cus.email)) {
								cout << "Invalid email address! Please try again.\n";
							}
						} while (!isValidEmail(cus.email));
						
						enqueue(cus);
						cout << "\nPress [Enter] back to menu...";
						cin.get(); 
						system("cls");
						break;
						
					case 3: 
						saveToFile();
						cout << "Search Customer Information" << endl;
						cout << "\nPress [Enter] back to menu...";
						cin.get(); 
						system("cls");
						break;
						
					case 4: 
						saveToFile();
						cout << "Saved the customer information to " << filename << endl;
						cout << "\nPress [Enter] back to menu...";
						cin.get(); 
						system("cls");
						break;
						
					case 5: 
						system("cls");
						teamAMenu();
						break;
						
					default:
						cout << "Invalid choice." << endl;
						break;
				}
				
			} while (true);
		}
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
	HashCustomer HC;
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
    			HC.hashingCustomer();
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
        cout << "\nID   : " << products[i].id << endl;
        cout << "Name : " << products[i].name << endl;
        cout << "Price: " << products[i].price << endl;
		cout << "\n";
        printWrappedText(products[i].description);
        cout <<"_________________________________________________________________________________________"<< endl;
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
		cout << "Description:\n";
        printWrappedText(products[prodIndex].description);
    }
    else
        cout << "Product not found.\n";
}

//---------------------- function to wrapped the description----------
void printWrappedText(const string& text) {
	int lineLength = 60;
    int count = 0;
    for (size_t i = 0; i < text.length(); ++i) {
        cout << text[i];
        count++;

        // Wrap at space only
        if (count >= lineLength && text[i] == ' ') {
            cout << '\n';
            count = 0;
        }
    }
    cout << endl;
}

// --------------------- MAIN PROGRAM ---------------------
int main() {
    mainMenu();

    return 0;
}
