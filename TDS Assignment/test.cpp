#include <iostream>
#include <fstream>
#include <cmath>
#include <cstdlib>
#include <string>
#include <sstream>
#include <iomanip>

#define TABLE_SIZE 10

using namespace std;
const int MAX_PRODUCTS = 100;
const int MAX_ORDERS = 100;
const int MAX_LINE_LENGTH = 256;
int productCount = 0;

// --------------------- FUNCTION PROTOTYPE ---------------------
void mainMenu();
void teamAMenu();
void teamBMenu();
void productMenu();
void orderMenu();
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

struct Order {
    string orderID;
    int customerID;
    int productID;
    string dateTime; 
    double totalAmount;
};

// --------------------- HASHING + LINKED LIST QUEUE ---------------------
class HashCustomer {
	private:
		// Node structure for linked list
		struct Node {
			Customer data;
			Node* next;
		};
	
		Node* front;// Front pointer of the linked list
		Node* rear;// Rear pointer of the linked list
		string filename;// File name for data persistence
		Node* table[TABLE_SIZE];// Hash table array for customer data
		
		// ID validate
		bool isValidID(const string& id){
			if (id.length() == 0) return false;

		    for (int i = 0; i < id.length(); i++){
		        if (id[i] < '0' || id[i] > '9'){
		            return false; 
		        }
		    }
		    return true; 
		}
		
		// Id existing validate
		bool isIDExists(const string& id){
			return search(id) != NULL;
		}
		
		// Name validate
		bool isValidName(const string& name){
		    const int MAX_LENGTH = 30;
		    const int MIN_LENGTH = 3;
		    int length = 0;
		    bool hasLetter = false;
		
		    for (int i = 0; name[i] != '\0'; ++i){
		        char c = name[i];
		        length++;
		
		        if (!((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || c == ' ')){
		            return false;
		        }
		
		        if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z')){
		            hasLetter = true;
		        }
		
		        if (length > MAX_LENGTH){
		            return false;
		        }
		    }
		
		    if (length < MIN_LENGTH || !hasLetter){
		        return false;
		    }
		
		    return true;
		}
		
		// Name existing validate
		bool isNameExists(const string& name){
		    for (int i = 0; i < TABLE_SIZE; i++){
		        Node* current = table[i];
		        while (current != NULL) {
		            if (current->data.name == name){
		                return true;
		            }
		            current = current->next;
		        }
		    }
		    return false;
		}
		
		// Phone number validate
		bool isValidPhone(const string& phone){
			const char* p = phone.c_str();
			int i = 0;
			int digitCount = 0;
		
			while (p[i] != '\0') {
				if (i == 3 && p[i] != '-'){
					return false;
				}
		
				char c = p[i];
		
				if (!((c >= '0' && c <= '9') || c == '-' )){
					return false;
				}
		
				if (c >= '0' && c <= '9'){
					digitCount++;
				}
		
				i++;
			}
		
			if (digitCount < 10 || digitCount > 11){
				return false;
			}
		
			if (i < 4){
				return false;
			}
		
			return true;
		}
		
		// Email validate
		bool isValidEmail(const string& email){
			if(email[0] == '\0') return false;
			
			bool hasAt = false;
			int atPos = -1;
			int i = 0;
			while(email[i] != '0'){
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
		
		// Hash function to generate an index from customer ID
		int hashFunction(string key){
	        unsigned int hash = 0;
	        for (char ch : key) {
	            hash = (hash << 5) + ch;
	        }
	        return hash % TABLE_SIZE;
	    }
	
	public:
		// Constructor: initialize pointers and hash table
		HashCustomer() : filename("customer.txt"), front(NULL), rear(NULL) {
		    for(int i = 0; i < TABLE_SIZE; i++) {
		        table[i] = NULL;
		    }
		}
	
		// Destructor: clean up linked list memory
		~HashCustomer() {
			Node* current = front;
			while (current != NULL) {
				Node* next = current->next;
				delete current;
				current = next;
			}
		}
		
		// Insert a customer into both linked list and hash table
		void insert(const Customer& customer) {
			// Insert to linked list
		    Node* newNode = new Node;
		    newNode->data = customer;
		    newNode->next = NULL;
		
		    if (isEmpty()) {
		        front = rear = newNode;
		    } else {
		        rear->next = newNode;
		        rear = newNode;
		    }
		
			// Insert to hash table
		    int index = hashFunction(customer.id);
		    newNode = new Node;
		    newNode->data = customer;
		    newNode->next = table[index];
		    table[index] = newNode;
		}
		
		// Search customer by ID in hash table
	    Customer* search(const string& customerId) {
	        int index = hashFunction(customerId);
	        Node* current = table[index];
	        
	        while(current != NULL) {
	            if(current->data.id == customerId) {
	                return &(current->data);
	            }
	            current = current->next;
	        }
	        return NULL;
	    }
		
		// Convert a line of text into a Customer object
		Customer parseCustomer(const string& line) {
			Customer c;
			stringstream ss(line);
			ss >> c.id >> c.name >> c.email >> c.phone;
			return c;
		}
	
		// Check if linked list is empty
		bool isEmpty() const {
			return front == NULL;
		}
	
		// Save all customers from linked list to file
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
	
		// Load customer data from file and insert into system
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
					insert(c);
				}
			}
	
			file.close();
		}
	
		// Display all customers from the linked list
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
	
		// Hashing Customer main menu
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
					{
						display();
						cout << "\nPress [Enter] back to menu...";
						cin.get(); 
						system("cls");
						break;
					}
						
					case 2: 
					{
						// Add customer information and validate customer details
						do{
							cout << "Enter customer ID : ";
							getline(cin, cus.id);
							if (!isValidID(cus.id)){
						        cout << "ID must contain digits only! Please try again.\n";
						    }else if (isIDExists(cus.id)){
						        cout << "This ID already exists! Please enter a different ID.\n";
						    }
						}while (!isValidID(cus.id) || isIDExists(cus.id));
						
						do{
							cout << "Enter customer name : ";
							getline(cin, cus.name);
							if (!isValidName(cus.name)){
						        cout << "Invalid name! Only letters and spaces are allowed, name must be 3 to 30 characters.\n";
						    }else if (isNameExists(cus.name)){
						        cout << "This name already exists! Please enter a different name.\n";
						    }
						}while (!isValidName(cus.name) || isNameExists(cus.name));
						
						
						do{
							cout << "Enter customer phone number (e.g. 010-1234567) : ";
							getline(cin, cus.phone);
							if (!isValidPhone(cus.phone)){
								cout << "Invalid phone number! Make sure it follows the format 010-1234567 and contains only digits with 10 or 11 numbers.\n";
							}
						}while(!isValidPhone(cus.phone));
						
						do{
							cout << "Enter customer email (e.g. john@example.com) : ";
							getline(cin, cus.email);
							if (!isValidEmail(cus.email)){
								cout << "Invalid email address! Make sure it contains '@' and a '.' and they are not at the beginning or end.\n";
							}
						}while(!isValidEmail(cus.email));
						
						insert(cus);
						cout << "\nPress [Enter] back to menu...";
						cin.get(); 
						system("cls");
						break;
					}
						
					case 3: 
					{
						// Search customer information by ID
						string searchID;
	                    cout << "Search Customer Information" << endl;
	                    cout << "Enter customer ID: ";
	                    getline(cin, searchID);
	                    
	                    Customer* foundCustomer = search(searchID);
	                    if (foundCustomer != NULL) {
	                        cout << "\nCustomer Found:" << endl;
	                        cout << "ID: " << foundCustomer->id << endl;
	                        cout << "Name: " << foundCustomer->name << endl;
	                        cout << "Email: " << foundCustomer->email << endl;
	                        cout << "Phone: " << foundCustomer->phone << endl;
	                    } else {
	                        cout << "\nCustomer not found!" << endl;
	                    }
	                    
	                    cout << "\nPress [Enter] back to menu...";
	                    cin.get(); 
	                    system("cls");
	                    break;
					}
	                    
					case 4: 
					{
						// Save customer data to file
						saveToFile();
						cout << "Saved the customer information to " << filename << endl;
						cout << "\nPress [Enter] back to menu...";
						cin.get(); 
						system("cls");
						break;
					}
						
					case 5: 
					{
						system("cls");
						teamAMenu();
						break;
					}
						
					default:
						cout << "Invalid choice." << endl;
						break;
				}
				
			} while (true);
		}
};

// --------------------- SHELL SORT ---------------------
void shellSort(Product arr[], int n)
{
    // Start with a big gap, then reduce the gap
    for (int gap = n/2; gap > 0; gap /= 2)
    {
        // Do a gapped insertion sort for this gap size.
        // The first gap elements a[0..gap-1] are already in gapped order
        // keep adding one more element until the entire array is gap sorted 
        for (int i = gap; i < n; i += 1)
        {
            // add a[i] to the elements that have been gap sorted
            // save a[i] in temp and make a hole at position i
            Product temp = arr[i];

            // shift earlier gap-sorted elements up until the correct 
            // location for a[i] is found
            int j;            
            for (j = i; j >= gap && arr[j - gap].id > temp.id; j -= gap)
                arr[j] = arr[j - gap];
            
            //  put temp (the original a[i]) in its correct location
            arr[j] = temp;
        }
    }
}

void shellSortOrdersByDateTime(Order arr[], int n) {
    // Convert datetime strings to comparable format and sort
    for (int gap = n/2; gap > 0; gap /= 2) {
        for (int i = gap; i < n; i += 1) {
            Order temp = arr[i];
            int j;
            
            // Compare datetime strings (newest first)
            for (j = i; j >= gap && arr[j - gap].dateTime < temp.dateTime; j -= gap) {
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

// ------------------------------------------- READ FROM FILE (load function)-------------------------------------------
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

int loadOrders(Order orders[]) {
    ifstream file("order.txt");
    if (!file) {
        cout << "Error opening order file!\n";
        return 0;
    }

    int count = 0;
    while (file >> orders[count].orderID) {
        file >> orders[count].customerID;
        file >> orders[count].productID;
        file.ignore(); // Ignore space before datetime
        getline(file, orders[count].dateTime, '"'); // Read until opening quote
        getline(file, orders[count].dateTime, '"'); // Read actual datetime
        file >> orders[count].totalAmount;
        count++;
    }

    file.close();
    return count;
}
//-------------------------------------------------------- MAIN MENU ------------------------------------------------------
void mainMenu(){
	system("cls");
	string choice;
	
	cout<<"=================================================="<<endl;
    cout<<"                  TDS Assignment                  "<<endl;
    cout<<"=================================================="<<endl;
    cout<<"1. Team A"<<endl;
    cout<<"2. Team B"<<endl;
    cout<<"3. Exit System"<<endl;
    cout<<"--------------------------------------------------"<<endl;
    cout<<"Enter your choice: ";
    getline(cin, choice);

    if(choice=="1"){
    	system("cls");
    	teamAMenu();
	}
	else if(choice=="2"){
		system("cls");
		teamBMenu();
	}
    else if(choice=="3"){
    	cout<<"\nThank you for using the system. Goodbye!"<<endl;
		exit(1);
	}
	else{
		cout<<"Invalid choice. Press Enter to try again";
		cin.get();		
		mainMenu();
	}
}


//--------------------------------------------------- TEAM A MENU -----------------------------------------------------
void teamAMenu(){
	HashCustomer HC;
	int choice;
	
	cout<<"=================================================="<<endl;
    cout<<"                    Team A Menu                   "<<endl;
    cout<<"=================================================="<<endl;
    cout<<"1. Hashing Customer"<<endl;
    cout<<"2. Return to Main Menu"<<endl;
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

//-------------------------------------------------- TEAM B MENU ----------------------------------------------
void teamBMenu(){
	string choice;

	cout<<"=================================================="<<endl;
    cout<<"                    Team B Menu                   "<<endl;
    cout<<"=================================================="<<endl;
    cout<<"1. Display Unsorted Products"<<endl;
    cout<<"2. Display Unsorted Order History"<<endl;
    cout<<"3. Return to Main Menu"<<endl;
    cout<<"--------------------------------------------------"<<endl;
    cout<<"Enter your choice: ";
    getline(cin,choice);

    if (choice == "1") {
	    system("cls");
	    productMenu();
	}
	else if (choice == "2") {
	    system("cls");
	    orderMenu();
	}
	else if (choice == "3") {
	    system("cls");
	    mainMenu();
	}
	else {
	    cout << "Invalid choice. Press Enter to try again";
	    cin.get();
	    system("cls");
	    teamBMenu();
	}
}

//----------------------------------------------------save products to raw product.txt----------------------------------------
void saveRawProducts(Product products[], int productCount) {
    ofstream outFile("raw_product.txt");
    if (!outFile) {
        cout << "Error opening file for writing!" << endl;
        return;
    }
    
    for (int i = 0; i < productCount; i++) {
        outFile << setw(3) << setfill('0') << products[i].id << " \"" 
                << products[i].name << "\" " 
                << fixed << setprecision(2) << products[i].price << " \"" 
                << products[i].description << "\"\n";
    }
    
    outFile.close();
}

//---------------------------------------------------- SAVE SORTED PRODUCTS --------------------------------------------------
void saveSortedProducts(Product products[], int productCount) {
    ofstream outFile("sorted_product.txt");
    if (!outFile) {
        cout << "Error opening file for writing!" << endl;
        return;
    }
    
    shellSort(products, productCount);
    for (int i = 0; i < productCount; i++) {
        outFile << setw(3) << setfill('0') << products[i].id << " \"" 
                << products[i].name << "\" " 
                << fixed << setprecision(2) << products[i].price << " \"" 
                << products[i].description << "\"\n";
    }
    
    outFile.close();
    cout << "Sorted products saved to sorted_product.txt" << endl;
    cout << "Press [ENTER] to return to Product Menu.";
	cin.get();    
}

//----------------------------------------------------------- SAVE SORTED ORDERS -----------------------------------------------
void saveSortedOrders(Order orders[], int orderCount) {
    ofstream outFile("sorted_order.txt");
    if (!outFile) {
        cout << "Error opening file for writing!" << endl;
        return;
    }
    
    for (int i = 0; i < orderCount; i++) {
        outFile << orders[i].orderID << " "
                << orders[i].customerID << " "
                << orders[i].productID << " "
                << "\"" << orders[i].dateTime << "\" " 
                << orders[i].totalAmount << "\n";
    }
    
    outFile.close();
    cout << "Sorted orders saved to sorted_order.txt\n";
}

//----------------------------------------------------------- ADD PRODUCT-------------------------------------------------------
bool isEmpty(const string& str) {
    for (size_t i = 0; i < str.length(); i++) {
        if (str[i] != ' ' && str[i] != '\t') {
            return false;
        }
    }
    return true;
}

// Manual string to int conversion; returns -1 if invalid
int StringToInt(const string& str) {
    int result = 0;
    if (str.length() == 0) return -1;

    for (size_t i = 0; i < str.length(); i++) {
        char c = str[i];
        if (c < '0' || c > '9') return -1;
        result = result * 10 + (c - '0');
    }
    return result;
}

// Manual string to float conversion; returns -1.0f if invalid
float StringToFloat(const string& str) {
    float result = 0.0f;
    bool decimalFound = false;
    float decimalDivisor = 10.0f;
    int digitCount = 0;
    if (str.length() == 0) return -1.0f;

    for (size_t i = 0; i < str.length(); i++) {
        char c = str[i];
        if (c == '.') {
            if (decimalFound) return -1.0f; // multiple dots
            decimalFound = true;
        }
        else if (c >= '0' && c <= '9') {
            int digit = c - '0';
            if (!decimalFound) {
                result = result * 10 + digit;
            } else {
                result = result + digit / decimalDivisor;
                decimalDivisor *= 10;
            }
            digitCount++;
        }
        else {
            return -1.0f; // invalid character
        }
    }
    if (digitCount == 0) return -1.0f; // no digits found
    return result;
}

void addProducts(Product products[]) {
    productCount = loadProducts(products);
    Product newProduct;
    bool idExist = false;
    string choice;
    int addCount = 0;
    const int MAX_ADD = 5;

    system("cls");

    do {
        // Sort and display current products (Assuming shellSort exists)
        // shellSort(products, productCount);

        cout << "\nCurrent Products:\n";
        for (int i = 0; i < productCount; i++) {
            // Print ID with leading zeros manually (3 digits)
            int id = products[i].id;
            if (id < 10) cout << "00" << id;
            else if (id < 100) cout << "0" << id;
            else cout << id;
            cout << " - " << products[i].name << endl;
        }

        // Enter ID
        string idStr;
        int idToAdd = -1;
        do {
            cout << "Enter ID in 3 digits [Press 0 to return to Product Menu] : ";
            getline(cin, idStr);

            // Check all digits
            idToAdd = StringToInt(idStr);
            if (idToAdd == -1) {
                cout << "Invalid input! ID must be digits only.\n";
                continue;
            }
            if (idToAdd == 0) {
                return;
            }
            if (idStr.length() != 3) {
                cout << "ID must be exactly 3 digits!\n";
                idToAdd = -1; // force re-entry
                continue;
            }

            // Check ID already exists
            idExist = false;
            for (int i = 0; i < productCount; i++) {
                if (products[i].id == idToAdd) {
                    cout << "This Product ID already exists! Please re-enter.\n";
                    idExist = true;
                    break;
                }
            }
        } while (idToAdd == -1 || idExist);

        newProduct.id = idToAdd;

        // Enter Product Name
        do {
            cout << "Enter Product Name      : ";
            getline(cin, newProduct.name);
            if (isEmpty(newProduct.name)) {
                cout << "Name cannot be empty or only spaces!\n";
            }
        } while (isEmpty(newProduct.name));

        // Enter Price
        string priceStr;
        float price = -1.0f;
        do {
            cout << "Enter Price             : ";
            getline(cin, priceStr);
            price = StringToFloat(priceStr);
            if (price < 0) {
                cout << "Invalid price input. Only digits and at most one dot allowed.\n";
            }
        } while (price < 0);
        newProduct.price = price;

        // Enter Description
        do {
            cout << "Enter Description       : ";
            getline(cin, newProduct.description);
            if (isEmpty(newProduct.description)) {
                cout << "Description cannot be empty or only spaces!\n";
            }
        } while (isEmpty(newProduct.description));

        // Add new product
        products[productCount] = newProduct;
        productCount++;
        addCount++;

        // Save to raw file immediately
        ofstream outFile("raw_product.txt", ios::app);
        if (!outFile) {
            cout << "Error opening file for writing!" << endl;
            return;
        }

        // Manually write ID with leading zeros
        if (newProduct.id < 10) outFile << "00" << newProduct.id;
        else if (newProduct.id < 100) outFile << "0" << newProduct.id;
        else outFile << newProduct.id;

        outFile << " \"" << newProduct.name << "\" ";
        outFile.setf(ios::fixed);
        outFile.precision(2);
        outFile << newProduct.price << " \"" << newProduct.description << "\"\n";
        outFile.close();

        cout << "\nProduct added successfully!" << endl;

        if (addCount < MAX_ADD) {
            cout << "Do you want to continue adding other products? [" << (MAX_ADD - addCount) << " times left]" << endl;
            cout << "___________________________________________" << endl;
            cout << "| Press 1 for YES / any other keys for NO |" << endl;
            cout << "|_________________________________________|" << endl;
            cout << "\nEnter your choice : ";
            getline(cin, choice);
        }
        else {
            cout << "Maximum of 5 products added.\n";
            choice = "2";
        }

    } while (choice == "1" && addCount < MAX_ADD);

    cout << "Press [ENTER] to return to Product Menu.";
    cin.get();
    system("cls");
}

//----------------------------------------------------------------------------Delete PRODUCTS----------------------------------------------------------------------------
void printIdWithLeadingZeros(int id) {
    if (id < 10) cout << "00" << id;
    else if (id < 100) cout << "0" << id;
    else cout << id;
}

void deleteProducts(Product products[]) {
    productCount = loadProducts(products);
    string inputStr;
    int idToDelete = -1;
    bool productFound = false;

    // Temporary sorted copy
    Product sortedProducts[MAX_PRODUCTS];
    for (int i = 0; i < productCount; i++) {
        sortedProducts[i] = products[i];
    }
    shellSort(sortedProducts, productCount);

    cout << "\nCurrent Products:\n";
    for (int i = 0; i < productCount; i++) {
        printIdWithLeadingZeros(sortedProducts[i].id);
        cout << " - " << sortedProducts[i].name << endl;
    }

    while (!productFound) {
        cout << "\nEnter ID in 3 digits [Press 0 to return to Product Menu] : ";
        getline(cin, inputStr);

        // Convert string to int manually
        idToDelete = StringToInt(inputStr);

        if (idToDelete == -1) {
            cout << "Invalid input! Please enter digits only.\n";
            continue; // ask again
        }

        if (idToDelete == 0) {
            return; // exit to menu
        }

        if (inputStr.length() != 3) {
            cout << "ID must be exactly 3 digits!\n";
            continue; // ask again
        }

        // Search in sortedProducts with jumpSearch
        int prodIndex = jumpSearch(sortedProducts, productCount, idToDelete);

        if (prodIndex != -1) {
            // Find actual index in unsorted products
            int actualID = -1;
            for (int i = 0; i < productCount; i++) {
                if (products[i].id == sortedProducts[prodIndex].id) {
                    actualID = i;
                    break;
                }
            }

            cout << "\nProduct Selected: ";
            printIdWithLeadingZeros(products[actualID].id);
            cout << " - " << products[actualID].name << endl;

            cout << "\nAre you sure you want to delete this product? "<< endl;
            cout << "___________________________________________" << endl;
            cout << "| Press 1 for YES / any other keys for NO |" << endl;
            cout << "|_________________________________________|" << endl;
            cout << "Enter you choice: ";
            string confirmString;
            getline(cin, confirmString);

            int confirm = StringToInt(confirmString);
            if (confirm == 1) {
                // Shift left to delete
                for (int i = actualID; i < productCount - 1; i++) {
                    products[i] = products[i + 1];
                }
                productCount--;

                // Save to file
                ofstream outFile("raw_product.txt");
                if (!outFile) {
                    cout << "Error opening file for writing!" << endl;
                    return;
                }

                for (int i = 0; i < productCount; i++) {
                    // Print ID with leading zeros manually
                    if (products[i].id < 10) outFile << "00" << products[i].id;
                    else if (products[i].id < 100) outFile << "0" << products[i].id;
                    else outFile << products[i].id;

                    outFile << " \"" << products[i].name << "\" "
                            << fixed << setprecision(2) << products[i].price << " \""
                            << products[i].description << "\"\n";
                }
                outFile.close();

                cout << "\nProduct deleted successfully!\n";
                productFound = true;
            } else {
                cout << "\nDeletion cancelled.\n";
                productFound = true;
            }
        } else {
            cout << "Product not found. Please re-enter!\n";
        }
    }

    cout << "Press [ENTER] to return to Product Menu.";
    cin.get();
}

//-------------------------------------------------------- SEARCH PRODUCT ----------------------------------------------------
void searchProducts(Product products[]){
	productCount = loadProducts(products);
	string IDToSearchString;
			
	cout << "\nEnter Product ID to search / 0 to return to Product Menu: ";
	getline(cin,IDToSearchString);
	
	if(IDToSearchString=="0"){
		productMenu();
	}
			
	int IDToSearch = StringToInt(IDToSearchString);
			    
	shellSort(products, productCount);
	int prodIndex = jumpSearch(products, productCount, IDToSearch);
			
	if (prodIndex != -1)
	{
		cout << "\nProduct Found:" << endl;
		cout << "==================================================================" << endl;
		cout << "ID: " << products[prodIndex].id << endl;
		cout << "Name: " << products[prodIndex].name << endl;
		cout << "Price: " << products[prodIndex].price << endl;
		cout << "Description:" << endl;
	    printWrappedText(products[prodIndex].description);
	    cout << "==================================================================" << endl;
	}
	else
	{
		cout << "Product not found.\n";
	}
	cout << "Press [ENTER] to Retry.";
	cin.get();  
	system("cls");
	searchProducts(products);  
}

//-------------------------------------------------------- PRODUCT MENU ----------------------------------------------------
void productMenu(){
	Product products[MAX_PRODUCTS];
	string choice;

	do {
		//display unsorted products first
		int productCount = loadProducts(products);
		
	    cout << "\nUnsorted Products:\n";
	    for (int i = 0; i < productCount; i++) {
	                    cout << "\nID   : " << setw(3) << setfill('0') << products[i].id << endl;
	                    cout << "Name : " << products[i].name << endl;
	                    cout << "Price: " << products[i].price << endl;
	                    cout << "\n";
	                    printWrappedText(products[i].description);
	                    cout << "_________________________________________________________________________________________" << endl;
	    }
	    
        cout << "|================================================|" << endl;
        cout << "|                 Available Actions              |" << endl;
        cout << "|================================================|" << endl;
        cout << "|1. Add New Product (min. 5 entries)             |" << endl;
        cout << "|2. Delete Product                               |" << endl;
        cout << "|3. Search Data by ID                            |" << endl;
        cout << "|4. Display Sorted Data                          |" << endl;
        cout << "|5. Save Sorted Data                             |" << endl;
        cout << "|6. Return to Team B Menu                        |" << endl;
        cout << "|________________________________________________|" << endl;
        cout << "Enter your choice: ";
        getline(cin,choice);
        
        if(choice=="1"){
        	system("cls");
            addProducts(products);
		}
        else if(choice=="2"){
        	system("cls");
            deleteProducts(products);
		}
        else if(choice=="3"){
        	system("cls");
        	searchProducts(products);
		}
		else if(choice=="4"){
			system("cls");
            shellSort(products, productCount);
            cout << "Products sorted by ID:\n";
            for (int i = 0; i < productCount; i++) {
                cout << "\nID   : " << setw(3) << setfill('0') << products[i].id << endl;
                cout << "Name : " << products[i].name << endl;
                cout << "Price: " << products[i].price << endl;
                cout << "\n";
                printWrappedText(products[i].description);
                cout << "_________________________________________________________________________________________" << endl;
            }
            cout << "\nPress [Enter] to return to Product Menu ";
		    cin.get();
		}
    	else if(choice=="5"){
    		system("cls");
	        saveSortedProducts(products, productCount);
		}
		else if(choice=="6"){
			system("cls");
            teamBMenu();
            return;
		}
	    else{
	    	cout << "Invalid input. Please enter a number between 1 and 5.\n";
		    cout << "Press [Enter] to continue...";
		    cin.get();
		    system("cls");
		    productMenu();
		}
            
        system("cls");
	}while (true);
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

//---------------------------------------------------- ADD ORDER ----------------------------------------------------
void addOrders(Order orders[]) {
    int orderCount = loadOrders(orders);
    Order newOrder;
    bool idExist = false;
    int choice;
    int addCount = 0;
    const int MAX_ADD = 5;
    
    system("cls");
    
    do {
        cout << "\nCurrent Orders:\n";
        for(int i = 0; i < orderCount; i++) {
            cout << orders[i].orderID << " - " 
                 << orders[i].dateTime << " - " 
                 << "Customer: " << orders[i].customerID << endl;
        }
        
        cout << endl;
        do {
            idExist = false;
            cout << "Enter Order ID [Press 0 to return to Order Menu] : ";
            cin >> newOrder.orderID;
            
            if(newOrder.orderID == "0"){
                return;
            }
        
            for(int i = 0; i < orderCount; i++) {
                if(orders[i].orderID == newOrder.orderID) {
                    cout << "This Order ID already exists! Please re-enter.\n";
                    idExist = true;
                    break;
                }
            }
        } while (idExist);

        cout << "Enter Customer ID: ";
        cin >> newOrder.customerID;
        
        cout << "Enter Product ID: ";
        cin >> newOrder.productID;
        
        cout << "Enter Date/Time (format: YYYY-MM-DD HH:MM:SS): ";
        cin.ignore();
        getline(cin, newOrder.dateTime);
        
        cout << "Enter Total Amount: ";
        cin >> newOrder.totalAmount;

        orders[orderCount] = newOrder;
        orderCount++;
        addCount++;

        // Save to order file
        ofstream outFile("order.txt", ios::app);
        if (!outFile) {
            cout << "Error opening file for writing!" << endl;
            return;
        }
        
        outFile << newOrder.orderID << " "
                << newOrder.customerID << " "
                << newOrder.productID << " "
                << "\"" << newOrder.dateTime << "\" " 
                << newOrder.totalAmount << "\n";
        outFile.close();

        cout << "\nOrder added successfully!" << endl;
        
        if(addCount < MAX_ADD) {
            cout << "Do you want to continue adding other orders? [" << (MAX_ADD-addCount) << " times left]" << endl;
            cout << "__________" << endl;
            cout << "| 1. YES |" << endl;
            cout << "| 2. NO  |" << endl;
            cout << "|________|" << endl;
            cout << "\nEnter your choice : ";
            cin >> choice;
        } else {
            cout << "Maximum of 5 orders added.\n";
            choice = 2;
        }
    } while(choice == 1 && addCount < MAX_ADD);

    cout << "Press [ENTER] to return to Order Menu.";
    cin.ignore(); 
    cin.get();     
    system("cls");
}

// --------------------- ORDER MENU ---------------------
void orderMenu(){
	Order orders[MAX_ORDERS];
	int choice;

	do {
		int  orderCount = loadOrders(orders);
		
	    cout << "\nUnsorted Orders:\n";
		for (int i = 0; i < orderCount; i++) {
		    cout << "\nOrder ID : " << orders[i].orderID << endl;
		    cout << "Customer ID: " << orders[i].customerID << endl;
		    cout << "Product ID: " << orders[i].productID << endl;
		    cout << "Date/Time: " << orders[i].dateTime << endl;
		    cout << "Total Amount: " << orders[i].totalAmount << endl;
		    cout << "\n";
		        
		    cout << "_________________________________________________________________________________________" << endl;
		}
	    
        cout << "|================================================|" << endl;
        cout << "|                 Available Actions              |" << endl;
        cout << "|================================================|" << endl;
        cout << "|1. Add New Order (min. 5 entries)               |" << endl;
        cout << "|2. Search Data by ID                            |" << endl;
        cout << "|3. Display Sorted Data                          |" << endl;
        cout << "|4. Save Sorted Data                             |" << endl;
        cout << "|5. Return to Team B Menu                        |" << endl;
        cout << "|________________________________________________|" << endl;
        cout << "Enter your choice: ";
        cin >> choice;
        
        switch(choice) {
        	case 1:
                system("cls");
                addOrders(orders);
                break;
            case 2:
			{
			    system("cls");
			    orderCount = loadOrders(orders);
			    string searchOrderID;  
			    
			    cout << "\nEnter Order ID to search: ";
			    cin >> searchOrderID;
			    
			    bool found = false;
			    for (int i = 0; i < orderCount; i++) {
			        if (orders[i].orderID == searchOrderID) {
			            cout << "\nOrder Found:" << endl;
			            cout << "==================================================================" << endl;
			            cout << "Order ID    : " << orders[i].orderID << endl;
			            cout << "Customer ID : " << orders[i].customerID << endl;
			            cout << "Product ID  : " << orders[i].productID << endl;
			            cout << "Date/Time   : " << orders[i].dateTime << endl;
			            cout << "Total Amount: " << orders[i].totalAmount << endl;
			            cout << "==================================================================" << endl;
			            found = true;
			            break;
			        }
			    }
			    
			    if (!found) {
			        cout << "Order not found.\n";
			    }
			    cout << "Press [ENTER] to Refresh.";
			    cin.ignore();
			    cin.get();     
			    break;
			}   
            case 3:
                system("cls");
                shellSortOrdersByDateTime(orders, orderCount);
                cout << "Orders sorted by Date/Time:\n";
                for (int i = 0; i < orderCount; i++) {
                    cout << "\nOrder ID: " << orders[i].orderID << endl;
                    cout << "Date/Time: " << orders[i].dateTime << endl;
                    cout << "Customer: " << orders[i].customerID << endl;
                    cout << "Product: " << orders[i].productID << endl;
                    cout << "Amount: RM" << orders[i].totalAmount << endl;
                    cout << "_________________________________________________________________________________________" << endl;
                }
                cout << "\nPress [Enter] to continue...";
		        cin.ignore();
		        cin.get();
                break;
			case 4:
	            system("cls");
	            saveSortedOrders(orders, orderCount);
	            break;
	        case 5:
                system("cls");
                teamBMenu();
                return;
            default:
                cout << "Invalid choice. Please try again.\n";
                break;   
		}
        system("cls");
	}while (true);
}

// --------------------- MAIN PROGRAM ---------------------
int main() {
    mainMenu();

    return 0;
}
