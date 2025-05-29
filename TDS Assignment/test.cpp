//Declare the used library
#include <iostream>
#include <fstream>
#include <cmath>
#include <cstdlib>
#include <string>
#include <sstream>
#include <iomanip>

//Chosen as a small prime number to reduce clustering and ensure better distribution in hash table
#define TABLE_SIZE 11

using namespace std;

//Declare constant & global variables 
const int MAX_PRODUCTS = 100;
const int MAX_ORDERS = 100;
const int MAX_LINE_LENGTH = 256;
int productCount = 0;

//----------------------------------------------- FUNCTION PROTOTYPES ----------------------------------------------
void mainMenu();
void teamAMenu();
void teamBMenu();
void productMenu();
void orderMenu();
void printWrappedText(const string& text);

//------------------------------------------------- HELPER FUNCTIONS -----------------------------------------------
//Function to determine minimum value
int getMin(int a, int b) {
    if (a < b) {
        return a;
    } else {
        return b;
    }
}

//Function to determine whether a string is "empty" ignoring whitespace like spaces ' ' & '\t'.
bool isEmpty(const string& str) {
    for (size_t i = 0; i < str.length(); i++) {
        if (str[i] != ' ' && str[i] != '\t') {
            return false;
        }
    }
    return true;
}

//Function to print '0' or '00' to ensure displayed product id is exactly 3 digits
void printIdWithLeadingZeros(int id) {
    if (id < 10) cout << "00" << id;
    else if (id < 100) cout << "0" << id;
    else cout << id;
}

//Function to wrapped the product description
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

//Function to get the string length
int getStringLength(string s) {
    int count = 0;
    while (s[count] != '\0') {
        count++;
    }
    return count;
}

//Function to check if the date-time is valid
bool isValidDateTime(string dt) {
    // Check length first
    if (getStringLength(dt) != 16) {
        return false;
    }

    // Check if the fixed characters are correct
    if (dt[4] != '-' || dt[7] != '-' || dt[10] != ' ' || dt[13] != ':') {
        return false;
    }

    // Check if the other characters are digits (without using isdigit)
    for (int i = 0; i < getStringLength(dt); i++) {
        if (i == 4 || i == 7 || i == 10 || i == 13) continue; // skip -, space, :
        if (dt[i] < '0' || dt[i] > '9') return false; // not a digit
    }

    // Check hour (HH)
    int hour = (dt[11] - '0') * 10 + (dt[12] - '0');
    if (hour < 0 || hour > 23) {
        cout << "Hour must be between 00 and 23.\n";
        return false;
    }

    // Check minute (MM)
    int minute = (dt[14] - '0') * 10 + (dt[15] - '0');
    if (minute < 0 || minute > 59) {
        cout << "Minute must be between 00 and 59.\n";
        return false;
    }

    return true;
}

//Function to convert string into int; while returning -1 if invalid character or format
/*
    Function Logic:
    1. Check each character to ensure it is a digit ('0' to '9').
    2. Convert the string to an integer by:
       - Multiplying the current result by 10 and adding the digit value.
    3. Return -1 if:
       - The string is empty.
       - Any character is not a digit.
    4. Otherwise, return the converted integer.
*/
int StringToInt(const string& str) {
    int result = 0;
    if (str.length() == 0) 
		return -1;

    for (size_t i = 0; i < str.length(); i++) {
        char c = str[i];
        if (c < '0' || c > '9') return -1;
        result = result * 10 + (c - '0');
    }
    return result;
}

//Function to convert string into float; while returning -1 if invalid character or format
/*
    Function Logic:
    1. Check for valid characters (digits and at maximum one decimal).
    2. Convert the string into a float:
       - Multiply and accumulate digits before the decimal point.
       - Divide and accumulate digits after the decimal point.
    3. Return -1.0f if:
       - The string is empty / multiple decimal points / no digits / non-digit & dot characters.
    4. Otherwise, return the converted float.
*/
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

//Function to convert uppercase to lowercase (Added to avoid using built-in function tolower())
/*
	Logic of this function
	1. declare an empty result first
	2. use for loop to check the received char
		- if there's uppercase: 
			i ) convert it to lowercase by adding 32 (according to ASCII) 
			ii) assign it to variable 'result'
		- if there's no uppercase: 
			i ) directly assign it to variable 'result'
*/
string toLowerCase(const string& str) {
	string result = "";
	
    for (char c : str) {
        if (c >= 'A' && c <= 'Z') {
            result += (c + 32);
        } else {
            result += c;
        }
    }
    return result;
}

//---------------------------------------------------- STRUCTURES --------------------------------------------------
//Structure to store product attributes
struct Product {
    int id;
    string name;
    double price;
    string description;
};
//Structure to store customer attributes
struct Customer {
    string cus_id;
    string cus_name;
    string cus_email;
    string cus_phone;
};
//Structure to store admin attributes
struct Admin {
    string admin_id;
    string admin_name;
    string admin_email;
    string admin_phone;
    string admin_position;
};
//Structure to store order attributes
struct Order {
    string orderID;
    int customerID;
    int productID;
    string dateTime; 
    double totalAmount;
};

// ---------------------------------------------- SHELL SORT ALGORITHM ---------------------------------------------
//Shell sort for product data
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

//Shell sort for order data
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

//--------------------------------------------------JUMP SEARCH ALGORITHM-------------------------------------------
/*
	Logic of JumpSearch
	1. declare a fixed step size (usually is the square-root of array size)
	2. jump through the array with fixed step size
	3. once reached the jump position, check if the value of the element is the target
		- 	if jump position=target, target found
		-	if jump position<target, proceed with another jump
		-	if jump position>target, return to the previous jump position and perform linear search to look for the target
	4. if it jump until the end of array without any result, then the target does not exist in this array
*/
int jumpSearch(Product arr[], int size, int targetID) {
    
    //declare and calculate the fixed step size
	int step = sqrt(size);
	
	//track the previous jump position
    int prev = 0;
	
	//while loop to jump throught the array until element >= target is found
    while (arr[getMin(step, size) - 1].id < targetID) {
        prev = step;
        step += sqrt(size);
        if (prev >= size) 
			return -1; //target is not in the array
    }
	
	//for loop to perform linear search
    for (int i = prev; i < getMin(step, size); i++) {
        if (arr[i].id == targetID) 
			return i; //target found
    }
	
	//return -1 if target not found
    return -1;
}

//------------------------------------------------------ QUEUE -----------------------------------------------------
template <typename T>
class ADTqueue {
private: 
    T queue[100]; 
    int head, tail;
    
public: 
    ADTqueue() { 
        tail = -1; 
        head = 0; 
    } 
    
    int empty() { 
        return head > tail;
    } 
    
    int full() { 
        return tail == 99; // 99 is last index of the array
    } 
    
    void append(T num) { 
        if (!full()) { 
            queue[++tail] = num; 
        } 
        else { 
            cout << "Queue is Full" << endl; 
        } 
    } 
    
    T serve() { 
        if(!empty()) { 
            return queue[head++]; 
        }
        else { 
            cout << "Queue is Empty" << endl; 
            return T(); // Return default value for type
        }
    }
    void display() {
        if(empty()) {
            cout << "Order queue is empty\n";
            return;
        }

        cout << "\nUnsorted Orders:\n";
        for(int i = head; i <= tail; i++) {
            cout << "\nOrder ID     : " << queue[i].orderID << endl;
        	cout << "Customer ID  : " << queue[i].customerID << endl;
            cout << "Product ID   : " << queue[i].productID << endl;
            cout << "Date/Time    : " << queue[i].dateTime << endl;
            cout << "Total Amount : RM " << fixed << setprecision(2) << queue[i].totalAmount << endl;
            cout << "\n";
			cout << "_________________________________________________________________________________________" << endl;
        }
        cout << "\nTotal orders in queue: " << (tail-head+1) << "/100\n\n";
    }
    
    void displayProduct() {
	    if (empty()) {
	        cout << "Product queue is empty\n";
	        return;
	    }
	
	    // Display unsorted product from queue
		cout << "\nUnsorted Products:\n";
	    for (int i = head; i <= tail; i++) {
	        Product& product = queue[i];  // Access product from queue
	
	        cout << "\nID    : " << setw(3) << setfill('0') << product.id << endl;
	        cout << "Name  : " << product.name << endl;
	        cout << "Price : RM " << fixed << setprecision(2) << product.price << endl;
	        cout << "\n";
	        printWrappedText(product.description);
	
	        cout << "_________________________________________________________________________________________" << endl;
	    }
	
	    cout << "\nTotal products in queue: " << (tail - head + 1) << "/100\n\n";
	}
};

class OrderQueue : public ADTqueue<Order> {
public:
	OrderQueue() {
        loadFromFile(); // Load data in constructor
    }
    
    void loadFromFile() {
        ifstream inFile("order.txt");
        if (!inFile) return;

        Order order;
        while (inFile >> order.orderID) {
            inFile >> order.customerID;
            inFile >> order.productID;
            inFile.ignore(); // Ignore space before datetime
            getline(inFile, order.dateTime, '"'); // Read until opening quote
            getline(inFile, order.dateTime, '"'); // Read actual datetime
            inFile >> order.totalAmount;
            
            if (!full()) {
                append(order);
            }
        }
        inFile.close();
    }
    
    void processNextOrder() {
	    if(!empty()) {
	        // Get the order to be processed
	        Order nextOrder = serve();
	        
	        // Display processing information
	        cout << "\nProcessing order: " << nextOrder.orderID << endl;
	        cout << "Customer ID     : " << nextOrder.customerID << endl;
			cout << "Product ID      : " << nextOrder.productID << endl;
	        cout << "Date/Time       : " << nextOrder.dateTime << endl;
			cout << "Total Amount    : RM " << fixed << setprecision(2) << nextOrder.totalAmount << endl;
	        
	        // Read all orders from file into an array
	        const int MAX_ORDERS = 1000; // Adjust as needed
	        Order orders[MAX_ORDERS];
	        int orderCount = 0;
	        
	        ifstream inFile("order.txt");
	        if (!inFile) {
	            cout << "Error opening order file for reading!\n";
	            return;
	        }
	
	        while (orderCount < MAX_ORDERS && 
	               inFile >> orders[orderCount].orderID) {
	            inFile >> orders[orderCount].customerID;
	            inFile >> orders[orderCount].productID;
	            inFile.ignore(); // Ignore space before datetime
	            getline(inFile, orders[orderCount].dateTime, '"'); // Read until opening quote
	            getline(inFile, orders[orderCount].dateTime, '"'); // Read actual datetime
	            inFile >> orders[orderCount].totalAmount;
	            orderCount++;
	        }
	        inFile.close();
	        
	        // Find and remove the processed order
	        bool found = false;
	        for (int i = 0; i < orderCount; i++) {
	            if (orders[i].orderID == nextOrder.orderID) {
	                // Shift remaining elements left
	                for (int j = i; j < orderCount - 1; j++) {
	                    orders[j] = orders[j + 1];
	                }
	                orderCount--;
	                found = true;
	                break;
	            }
	        }
	        
	        if (!found) {
	            cout << "Warning: Processed order not found in file!\n";
	        }
	        
	        // Rewrite the file without the processed order
	        ofstream outFile("order.txt");
	        if (!outFile) {
	            cout << "Error opening order file for writing!\n";
	            return;
	        }
	
	        for (int i = 0; i < orderCount; i++) {
	            outFile << orders[i].orderID << " "
	                    << orders[i].customerID << " "
	                    << orders[i].productID << " "
	                    << "\"" << orders[i].dateTime << "\" " 
	                    << fixed << setprecision(2) << orders[i].totalAmount;
	            
	            // Add newline unless it's the last order
	            if (i < orderCount - 1) {
	                outFile << "\n";
	            }
	        }
	        outFile.close();
	        
	        cout << "\nOrder processed successfully and removed from file.\n";
	    } else {
	        cout << "No orders to process.\n";
	    }
	}
};

class ProductQueue : public ADTqueue<Product> {
public:
	ProductQueue() {
        loadFromFile(); // Load data in constructor
    }
    
    void loadFromFile() {
        ifstream inFile("raw_product.txt");
        if (!inFile) return;

        Product product;
        while (inFile >> product.id) {
        	getline(inFile, product.name, '"');
	    	getline(inFile, product.name, '"'); // Read the product name inside quotes
            inFile >> product.price;
            inFile.ignore(); // Ignore space after product price
            getline(inFile, product.description, '"');
	    	getline(inFile, product.description, '"'); // Read product description inside quotes
            
            if (!full()) {
                append(product);
            }
        }
        inFile.close();
    }
    
    void deleteProduct() {
	    if(!empty()) {
	        // Get the product to be deleted
	        Product nextProduct = serve();
	        
	        // Display processing information
	        cout << "\nDeleting product: " << nextProduct.id << "-" << nextProduct.name << endl;
	        
	        // Read all products from file into an array
	        Product product[MAX_PRODUCTS];
	        int productCount = 0;
	        
	        ifstream inFile("raw_product.txt");
	        if (!inFile) {
	            cout << "Error opening product file for reading!\n";
	            return;
	        }
	
	        while (productCount < MAX_PRODUCTS && 
	            inFile >> product[productCount].id) {
	            getline(inFile, product[productCount].name, '"');
		    	getline(inFile, product[productCount].name, '"'); // Read the product name inside quotes
	            inFile >> product[productCount].price;
	            inFile.ignore(); // Ignore space after product price
	            getline(inFile, product[productCount].description, '"');
		    	getline(inFile, product[productCount].description, '"'); // Read product description inside quotes
	            productCount++;
	        }
	        inFile.close();
	        
	        // Find and remove the processed product
	        bool found = false;
	        for (int i = 0; i < productCount; i++) {
	            if (product[i].id == nextProduct.id) {
	                // Shift remaining elements left
	                for (int j = i; j < productCount - 1; j++) {
	                    product[j] = product[j + 1];
	                }
	                productCount--;
	                found = true;
	                break;
	            }
	        }
	        
	        if (!found) {
	            cout << "Warning: Targeted product not found in file!\n";
	        }
	        
	        // Rewrite the file without the processed order
	        ofstream outFile("raw_product.txt");
	        if (!outFile) {
	            cout << "Error opening product file for writing!\n";
	            return;
	        }
	
	        for (int i = 0; i < productCount; i++) {	            
	            outFile << setw(3) << setfill('0') << product[i].id << " \"" 
		                << product[i].name << "\" " 
		                << fixed << setprecision(2) << product[i].price << " \"" 
		                << product[i].description << "\"\n";
	        }
	        outFile.close();
	        
	        cout << "\nProduct deleted successfully and removed from raw_product.txt\n";
	    } else {
	        cout << "No products to delete.\n";
	    }
	}
};

//---------------------------------------------HASHING + LINKED LIST QUEUE------------------------------------------
/*
 	Class: HashCustomer
	Implements a hash table with separate chaining for storing Customer records
	- Uses a simple string hashing algorithm (bit-shifting + division method)
	- Collisions are resolved via linked list queue and separate chaining
	- Supports insertion, searching, and file persistence
*/
class HashCustomer {
	private:
		// Node structure for linked list queue and separate chaining in the hash table
		struct Node {
			Customer data; // Stores customer data
			Node* next; // Pointer to the next node in the chain
		};
	
		Node* front;// Front pointer of the linked list queue
		Node* rear;// Rear pointer of the linked list queue
		string filename;// File name for saving/loading customer data

		/*
			Using linked list queue and separate chaining for collision handling:
			- Simple to implement
			- Handles unlimited collisions (but degrades to O(n) in worst case)
		*/ 
		Node* table[TABLE_SIZE];// Hash table array for separate chaining
		
		// Checks if the given ID string is exactly 4 numeric digits and all characters are digits
		bool isValidID(const string& id) {
		    int length = 0;
		
		    while (id[length] != '\0') {
		        length++;
		    }
		
		    if (length != 4) {
		        return false;
		    }
		
		    for (int i = 0; i < length; i++) {
		        if (id[i] < '0' || id[i] > '9') {
		            return false;
		        }
		    }
		
		    return true;
		}
		
		// Checks if the given ID already exists in the hash table
		bool isIDExists(const string& id){
			return search(id) != NULL;
		}
		
		// Validates customer name
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
		
		// Checks if a name already exists in the hash table
		bool isNameExists(const string& name){
		    for (int i = 0; i < TABLE_SIZE; i++){
		        Node* current = table[i];
		        while (current != NULL) {
		            if (current->data.cus_name == name){
		                return true;
		            }
		            current = current->next;
		        }
		    }
		    return false;
		}
		
		// Validates phone number
		bool isValidPhone(const string& phone){
			const char* p = phone.c_str();
			int i = 0;
			int digitCount = 0;
			
			if (!(p[0] == '0' && p[1] == '1')) {
		        return false;
		    }
		
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
		
		// Checks if the phone number already exists in the hash table
		bool isPhoneExists(const string& phone){
			for (int i = 0; i < TABLE_SIZE; i++){
				Node* current = table[i];
				while (current != NULL) {
					if (current->data.cus_phone == phone){
						return true;
					}
					current = current->next;
				}
			}
			return false;
		}

		// Validates email
		bool isValidEmail(const string& email){
			if(email[0] == '\0') return false;
			
			bool hasAt = false;
			int atPos = -1;
			int i = 0;
			while(email[i] != '\0'){
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
		
		// Checks if the email already exists in the hash table
		bool isEmailExists(const string& email){
			for (int i = 0; i < TABLE_SIZE; i++){
				Node* current = table[i];
				while (current != NULL) {
					if (current->data.cus_email == email){
						return true;
					}
					current = current->next;
				}
			}
			return false;
		}
		
		// Check Hash function to generate an index from customer ID
		/*
			Computes the hash index for a given key
			- Uses bit-shifting (hash << 5) to spread bits
			- Applies the division method (mod TABLE_SIZE) for uniform distribution
			- Returns: Hash index (0 to TABLE_SIZE-1)
		*/
		int hashFunction(string key){
	        int hash = 0;
	        for (int i = 0; i < key.length(); i++) {
	            hash = (hash << 5) + key[i];
	        }
			// Return using the division method
	        return hash % TABLE_SIZE;
	    }
	
	public:
		// Constructor: initializes the hash table and linked list queue and separate chaining pointers
		HashCustomer() : filename("customer.txt"), front(NULL), rear(NULL) {
		    for(int i = 0; i < TABLE_SIZE; i++) {
		        table[i] = NULL;
		    }
		}
	
		// Destructor: cleans up dynamically allocated nodes in the linked list queue, separate chaining and hash table
		~HashCustomer() {
		    // Clean up queue
		    Node* current = front;
		    while (current != NULL) {
		        Node* next = current->next;
		        delete current;
		        current = next;
		    }
		    
		    // Clean up hash table
		    for(int i = 0; i < TABLE_SIZE; i++) {
		        current = table[i];
		        while(current != NULL) {
		            Node* next = current->next;
		            delete current;
		            current = next;
		        }
		    }
		}
		
		/*
			Inserts a customer into both the linked list queue and hash table
			- Linked list queue maintains insertion order for display
			- Hash table enables O(1) average-case search
			- Duplicate IDs are rejected via isIDExists()
		*/
		void insert(const Customer& customer) {
			// Insert to linked list queue
		    Node* listNode = new Node;
		    listNode->data = customer;
		    listNode->next = NULL;
		
		    if (isEmpty()) {
		        front = rear = listNode;
		    } else {
		        rear->next = listNode;
		        rear = listNode;
		    }
		
			// Insert to hash table (separate node)
		    Node* hashNode = new Node;
		    hashNode->data = customer;
		    int index = hashFunction(customer.cus_id);
		    hashNode->next = table[index];
		    table[index] = hashNode;
		}
		
		/*
			Searches for a customer by ID in hash table
			- Returns: Pointer to Customer if found, NULL otherwise
			- Time: O(1) average case, O(n) worst case (all collisions)
		*/
	    Customer* search(const string& customerId) {
	        int index = hashFunction(customerId);
	        Node* current = table[index];
	        
	        while(current != NULL) {
	            if(current->data.cus_id == customerId) {
	                return &(current->data);
	            }
	            current = current->next;
	        }
	        return NULL;
	    }
		
		// Convert a line of text into a Customer object
		/*
			Parses a line from customer.txt into a Customer object
			Expected format: "ID Name Email Phone"
			Example: "1001 Bob bob@gmail.com 011-25478951"
		*/
		Customer parseCustomer(const string& line) {
			Customer c;
			stringstream ss(line);
			string nameWithQuotes;

			ss >> c.cus_id;
			ss >> ws; 
			getline(ss, nameWithQuotes, '"'); 
			getline(ss, c.cus_name, '"');  
			ss >> c.cus_email >> c.cus_phone;
			
			return c;
		}
	
		// Check if linked list queue is empty
		bool isEmpty() const {
			return front == NULL;
		}
	
		/*
			Saves all customer records from the linked list queue to "customer.txt"
			- Format: "ID Name Email Phone"
			- Overwrites files if it exists
			- Returns: void (prints error if file fails to open)
		*/
		void saveToFile() {
			ofstream file("customer.txt");
			if (!file) {
				cout << "File fail to connect" << endl;
				return;
			}
	
			Node* current = front;
			while (current != NULL) {
				file << current->data.cus_id << " "
					 << "\"" << current->data.cus_name << "\" "
					 << current->data.cus_email << " "
					 << current->data.cus_phone << endl;
				current = current->next;
			}
	
			file.close();
		}
	
		// Loads customer records from customer.txt file into the hash table and linked list queue
		/*
			Example customer.txt content:
			1001 "Alice" alice@mail.com 012-3456789
			1002 "Bob" bob@mail.com 011-9876543
		*/ 
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
	
		/*
			Displays all customer records in FIFO order (from front to rear)
			- Prints ID, Name, Email, and Phone for each customer
			- Separates entries with a line for clarity
		*/
		void display() {
			cout << "Customer List\n" << endl;
			Node* current = front;
			int i = 1;
			while (current != NULL) {
				cout << "Cust ID  : " << current->data.cus_id << endl;
				cout << "Name     : " << current->data.cus_name << endl;
				cout << "Email    : " << current->data.cus_email << endl;
				cout << "Phone    : " << current->data.cus_phone << endl;
				cout << "_________________________________________________________________________________________" << endl;
				current = current->next;
				i++;
			}
		}
	
		// Hashing Customer main menu
		/*
			Menu Options:
			1. Display Customer Information (FIFO order)
			2. Add Customer Information (Validates input)
			3. Search Customer Information (O(1) avg time)
			4. Save Customer Information (Overwrites customer.txt)
			5. Return to Team A Menu (Exit)
		*/
		void hashingCustomer() {
			loadFromFile();
			
			string choice;
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
				cout<<"Enter your choice: ";
    			getline(cin,choice);
				cout << endl;
				
				if(choice == "1"){
					display();
					cout << "\nPress [Enter] back to menu...";
					cin.get();
					cin.get(); 
					system("cls");
				}else if(choice == "2"){
					system("cls");
					cout << "Current Customer List\n" << endl;
					Node* current = front;
					int i = 1;
					while (current != NULL) {
						cout << current->data.cus_id << " - " << current->data.cus_name << endl;
						current = current->next;
						i++;
					}
					// Add admin information and validate customer details
					string inputId;
					do {
					    cout << "\nEnter customer ID in 4 digits [Press 0 to return] : ";
					    getline(cin, inputId);
					        
					    // Check for exit condition first
					    if(inputId == "0") {
						    system("cls");
						    break;  // This will exit the do-while loop
					    }
					        
					    if (!isValidID(inputId)) {
					        cout << "Customer ID must contain digits only and exactly 4 digits! Please try again.\n";
					    } else if (isIDExists(inputId)) {
					        cout << "This customer ID already exists! Please enter a different ID.\n";
					    } else {
					        cus.cus_id = inputId;
					        break; // Exit the loop if valid
					    }
					} while (true);
					    
					// If user entered 0, skip the rest and return to menu
					if(inputId == "0")
					    continue;
						
					do{
						cout << "Enter customer name : ";
						getline(cin, cus.cus_name);
						if (!isValidName(cus.cus_name)){
						    cout << "Invalid name! Only letters and spaces are allowed, name must be 3 to 30 characters.\n";
						}else if (isNameExists(cus.cus_name)){
						    cout << "This name already exists! Please enter a different name.\n";
						}
					}while (!isValidName(cus.cus_name) || isNameExists(cus.cus_name));
						
						
					do{
						cout << "Enter customer phone number (e.g. 010-1234567) : ";
						getline(cin, cus.cus_phone);
						if (!isValidPhone(cus.cus_phone)){
							cout << "Invalid phone number! Make sure it follows the format 010-1234567, contains only digits with 10 or 11 numbers and strat with '01'.\n";
						}else if (isPhoneExists(cus.cus_phone)) {
							cout << "Phone number already exists!" << endl;
						}
					}while(!isValidPhone(cus.cus_phone) || isPhoneExists(cus.cus_phone));
						
					do {
						cout << "Enter customer email : ";
						getline(cin, cus.cus_email);
						if (!isValidEmail(cus.cus_email)) {
						    cout << "Invalid email format! Please enter a valid email.\n";
						} else if (isEmailExists(cus.cus_email)) {
						    cout << "This email already exists! Please enter a different email.\n";
						}
					} while (!isValidEmail(cus.cus_email) || isEmailExists(cus.cus_email));
						
					insert(cus);
					cout << "\nCustomer added successfully!\n\n";
					cout << "\nPress [Enter] back to menu...";
					cin.get(); 
					system("cls");
				}else if(choice =="3"){
					// Search customer information by ID
					string searchID;
	                cout << "Search Customer Information \n" << endl;
	                cout << "Enter customer ID (4 digits): ";
	                getline(cin, searchID);
	            
	                Customer* foundCustomer = search(searchID);
	                if (foundCustomer != NULL) {
	                    cout << "\nCustomer Found:\n" << endl;
	                    cout << "Cust ID  : " << foundCustomer->cus_id << endl;
	                    cout << "Name     : " << foundCustomer->cus_name << endl;
	                    cout << "Email    : " << foundCustomer->cus_email << endl;
	                    cout << "Phone    : " << foundCustomer->cus_phone << endl;
	                } else {
	                    cout << "\nCustomer not found!" << endl;
	                }
	                    
	                cout << "\nPress [Enter] back to menu...";
	                cin.get(); 
	                system("cls");
	                
				} else if (choice == "4"){
					// Save customer data to file
					saveToFile();
					cout << "Saved the customer information to " << filename << endl;
					cout << "\nPress [Enter] back to menu...";
					cin.get(); 
					system("cls");
				} else if (choice == "5"){
					system("cls");
					teamAMenu();
				} else {
					cout << "Invalid choice. Please Enter to try again" << endl;
					cin.get();
					system("cls");
				}
				
			} while (true);
		}
};

/*
	Class: HashAdmin
	Implements a hash table with separate chaining for storing Admin records
	- Uses a simple string hashing algorithm (bit-shifting + division method)
	- Collisions are resolved via linked list queue and separate chaining
	- Supports insertion, searching, and file persistence
 */
class HashAdmin {
	private:
		// Node structure for linked list queue and separate chaining in the hash table
		struct Node {
			Admin data; // Stores admin data
			Node* next; // Pointer to the next node in the chain
		};
	
		Node* front;// Front pointer of the linked list queue and separate chaining
		Node* rear;// Rear pointer of the linked list queue and separate chaining
		string filename;// File name for data persistence

		/*
			Using linked list queue and separate chaining for collision handling:
			- Simple to implement
			- Handles unlimited collisions (but degrades to O(n) in worst case)
		*/ 
		Node* table[TABLE_SIZE];// Hash table array for separate chaining
		
		// Checks if the given ID string is exactly 3 numeric digits and all characters are digits
		bool isValidID(const string& id) {
		    int length = 0;
		    
		    while (id[length] != '\0') {
		        length++;
		    }
		
		    if (length != 3) {
		        return false;
		    }
		
		    for (int i = 0; i < length; i++) {
		        if (id[i] < '0' || id[i] > '9') {
		            return false;
		        }
		    }
		
		    return true;
		}
		
		// Checks if the given ID already exists in the hash table
		bool isIDExists(const string& id){
			return search(id) != NULL;
		}
		
		// Validates customer name
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
		
		// Checks if a name already exists in the hash table
		bool isNameExists(const string& admin_name){
		    for (int i = 0; i < TABLE_SIZE; i++){
		        Node* current = table[i];
		        while (current != NULL) {
		            if (current->data.admin_name == admin_name){
		                return true;
		            }
		            current = current->next;
		        }
		    }
		    return false;
		}
		
		// Validates phone number
		bool isValidPhone(const string& admin_phone){
			const char* p = admin_phone.c_str();
			int i = 0;
			int digitCount = 0;
			
			if (!(p[0] == '0' && p[1] == '1')) {
		        return false;
		    }
		
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
		
		// Checks if the phone number already exists in the hash table
		bool isPhoneExists(const string& phone){
			for (int i = 0; i < TABLE_SIZE; i++){
				Node* current = table[i];
				while (current != NULL) {
					if (current->data.admin_phone == phone){
						return true;
					}
					current = current->next;
				}
			}
			return false;
		}
		
		// Validates email
		bool isValidEmail(const string& email){
			if(email[0] == '\0') return false;
			
			bool hasAt = false;
			int atPos = -1;
			int i = 0;
			while(email[i] != '\0'){
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
		
		// Checks if the email already exists in the hash table
		bool isEmailExists(const string& email){
			for (int i = 0; i < TABLE_SIZE; i++){
				Node* current = table[i];
				while (current != NULL) {
					if (current->data.admin_email == email){
						return true;
					}
					current = current->next;
				}
			}
			return false;
		}
		
		// Validates admin position
		bool isValidPosition(const string& position) {
			return position == "admin" || position == "superadmin";
		}
		
		// Check Hash function to generate an index from admin ID
		/*
			Computes the hash index for a given key
			- Uses bit-shifting (hash << 5) to spread bits
			- Applies the division method (mod TABLE_SIZE) for uniform distribution
			- Returns: Hash index (0 to TABLE_SIZE-1)
		*/
		int hashFunction(string key){
	        int hash = 0;
	        for (int i = 0; i < key.length(); i++) {
	            hash = (hash << 5) + key[i];
	        }
			// Return using the division method
	        return hash % TABLE_SIZE;
	    }
	
	public:
		// Constructor: initializes the hash table and linked list queue and separate chaining pointers
		HashAdmin() : filename("admin.txt"), front(NULL), rear(NULL) {
		    for(int i = 0; i < TABLE_SIZE; i++) {
		        table[i] = NULL;
		    }
		}
	
		// Destructor: cleans up dynamically allocated nodes in the linked list queue, separate chaining and hash table
		~HashAdmin() {
		    // Clean up queue
		    Node* current = front;
		    while (current != NULL) {
		        Node* next = current->next;
		        delete current;
		        current = next;
		    }
		    
		    // Clean up hash table
		    for(int i = 0; i < TABLE_SIZE; i++) {
		        current = table[i];
		        while(current != NULL) {
		            Node* next = current->next;
		            delete current;
		            current = next;
		        }
		    }
		}
		
		/*
			Inserts a admin into both the linked list queue and hash table
			- Linked list queue maintains insertion order for display
			- Hash table enables O(1) average-case search
			- Duplicate IDs are rejected via isIDExists()
		*/
		void insert(const Admin& admin) {
		    // Insert to linked list queue
		    Node* listNode = new Node;
		    listNode->data = admin;
		    listNode->next = NULL;
		
		    if (isEmpty()) {
		        front = rear = listNode;
		    } else {
		        rear->next = listNode;
		        rear = listNode;
		    }
		
		    // Insert to hash table (separate node)
		    Node* hashNode = new Node;
		    hashNode->data = admin;
		    int index = hashFunction(admin.admin_id);
		    hashNode->next = table[index];
		    table[index] = hashNode;
		}
		
		/*
			Searches for a admin by ID in hash table
			- Returns: Pointer to Admin if found, NULL otherwise
			- Time: O(1) average case, O(n) worst case (all collisions)
		*/
	    Admin* search(const string& admin_id) {
	        int index = hashFunction(admin_id);
	        Node* current = table[index];
	        
	        while(current != NULL) {
	            if(current->data.admin_id == admin_id) {
	                return &(current->data);
	            }
	            current = current->next;
	        }
	        return NULL;
	    }
		
		// Convert a line of text into a Admin object
		/*
			Parses a line from admin.txt into a Admin object
			Expected format: "ID Name Email Phone Position"
			Example: "103 limmei limmei88@gmail.com 012-34782910 admin"
		*/
		Admin parseAdmin(const string& line) {
			Admin a;
			stringstream ss(line);
			string nameWithQuotes;
			ss >> a.admin_id;
			ss >> ws;
			getline(ss, nameWithQuotes, '"'); 
			getline(ss, a.admin_name, '"');  
			ss >> a.admin_email >> a.admin_phone >> a.admin_position;
			return a;
		}
	
		// Check if linked list queue is empty
		bool isEmpty() const {
			return front == NULL;
		}
	
		/*
			Saves all admin records from the linked list queue to "admin.txt"
			- Format: "ID Name Email Phone"
			- Overwrites files if it exists
			- Returns: void (prints error if file fails to open)
		*/
		void saveToFile() {
			ofstream file("admin.txt");
			if (!file) {
				cout << "File fail to connect" << endl;
				return;
			}
	
			Node* current = front;
			while (current != NULL) {
				file << current->data.admin_id << " "
					 << "\"" << current->data.admin_name << "\" "
					 << current->data.admin_email << " "
					 << current->data.admin_phone << " "
					 << current->data.admin_position << endl;
				current = current->next;
			}
	
			file.close();
		}
	
		// Loads admin records from admin.txt file into the hash table and linked list queue
		/*
			Example admin.txt content:
			105 aishah aishahrahman@yahoo.com 013-90451277 admin
			106 darren darrenlim@gmail.com 012-78123309 admin
		*/ 
		void loadFromFile() {
			ifstream file("admin.txt");
			if (!file) {
				cout << "File fail to connect" << endl;
				return;
			}
	
			string line;
			while (getline(file, line)) {
				if(!line.empty()) {
					Admin a = parseAdmin(line);
					insert(a);
				}
			}
	
			file.close();
		}
	
		/*
			Displays all admin records in FIFO order (from front to rear)
			- Prints ID, Name, Email, Phone and Posiiton for each admin
			- Separates entries with a line for clarity
		*/
		void displayAdmin() {
			cout << "Admin List\n" << endl;
			Node* current = front;
			int i = 1;
			while (current != NULL) {
				cout << "Admin ID  : " << current->data.admin_id << endl;
				cout << "Name      : " << current->data.admin_name << endl;
				cout << "Email     : " << current->data.admin_email << endl;
				cout << "Phone     : " << current->data.admin_phone << endl;
				cout << "Position  : " << current->data.admin_position << endl;
				cout << "_________________________________________________________________________________________" << endl;
				current = current->next;
				i++;
			}
		}
	
		// Hashing Admin main menu
		/*
			Menu Options:
			1. Display Admin Information (FIFO order)
			2. Add Admin Information (Validates input)
			3. Search Admin Information (O(1) avg time)
			4. Save Admin Information (Overwrites admin.txt)
			5. Return to Team A Menu (Exit)
		*/
		void hashingAdmin() {
			loadFromFile();
			
			string choice;
			Admin ad;
			
			do {
				cout << "==================================================" << endl;
				cout << "                  Hashing Admin                " << endl;
				cout << "==================================================" << endl;
				cout << "1. Display Admin Information";
				cout << "\n2. Add Admin Information";
				cout << "\n3. Search Admin Information";
				cout << "\n4. Save Admin Information";
				cout << "\n5. Return to Team A Menu";
				cout << "\n--------------------------------------------------" << endl;
				cout << "Enter your choice: ";
		        getline(cin, choice);
		        cout << endl;
		
		        if (choice == "1") {
		            displayAdmin();
		            cout << "\nPress [Enter] back to menu...";
		            cin.get();
		            cin.get();
		            system("cls");
		
		        } else if (choice == "2") {
					system("cls");
					cout << "Current Admin List\n" << endl;
					Node* current = front;
					int i = 1;
					while (current != NULL) {
						cout << current->data.admin_id << " - " << current->data.admin_name << endl;
						current = current->next;
						i++;
					}
					// Add admin information and validate admin details
					string inputId;
					do {
					    cout << "\nEnter admin ID in 3 digits [Press 0 to return] : ";
					    getline(cin, inputId);
					        
					    // Check for exit condition first
					    if(inputId == "0") {
					        system("cls");
					        break;  // This will exit the do-while loop
					    }
					        
					    if (!isValidID(inputId)) {
					        cout << "Admin ID must contain digits only and exactly 3 digits! Please try again.\n";
					    } else if (isIDExists(inputId)) {
					        cout << "This admin ID already exists! Please enter a different ID.\n";
					    } else {
					        ad.admin_id = inputId;
					        break; // Exit the loop if valid
					    }
					} while (true);
					    
					// If user entered 0, skip the rest and return to menu
					if(inputId == "0")
					    continue;
						
					do{
						cout << "Enter admin name : ";
						getline(cin, ad.admin_name);
						if (!isValidName(ad.admin_name)){
						    cout << "Invalid name! Only letters and spaces are allowed, name must be 3 to 30 characters.\n";
						}else if (isNameExists(ad.admin_name)){
						    cout << "This name already exists! Please enter a different name.\n";
						}
					}while (!isValidName(ad.admin_name) || isNameExists(ad.admin_name));
						
						
					do{
						cout << "Enter admin phone number (e.g. 010-1234567) : ";
						getline(cin, ad.admin_phone);
						if (!isValidPhone(ad.admin_phone)){
							cout << "Invalid phone number! Make sure it follows the format 010-1234567, contains only digits with 10 or 11 numbers and strat with '01'.\n";
						}else if (isPhoneExists(ad.admin_phone)) {
							cout << "Phone number already exists!" << endl;
						}
					}while(!isValidPhone(ad.admin_phone) || isPhoneExists(ad.admin_phone));
						
					do{
						cout << "Enter admin email (e.g. john@example.com) : ";
						getline(cin, ad.admin_email);
						if (!isValidEmail(ad.admin_email)){
							cout << "Invalid email address! Make sure it contains '@' and a '.' and they are not at the beginning or end.\n";
						}else if (isEmailExists(ad.admin_email)) {
						    cout << "This email already exists! Please enter a different email.\n";
						}
					}while(!isValidEmail(ad.admin_email) || isEmailExists(ad.admin_email));
						
					do{
						cout << "Enter admin position (superadmin/admin) : ";
						getline(cin, ad.admin_position);
						if (!isValidPosition(ad.admin_position)){
							cout << "Invalid position entered. Please select either 'admin' or 'superadmin'.\n";
						}
					}while(!isValidPosition(ad.admin_position));
						
					insert(ad);
					cout << "\nPress [Enter] back to menu...";
					cin.get(); 
					system("cls");
				}else if (choice == "3") {
					// Search admin information by ID
		            string searchID;
		            cout << "Search Admin Information\n" << endl;
		            cout << "Enter admin ID (3 digits): ";
		            getline(cin, searchID);
		
		            Admin* foundAdmin = search(searchID);
		            if (foundAdmin != NULL) {
		                cout << "\nAdmin Found:\n" << endl;
		                cout << "Admin ID  : " << foundAdmin->admin_id << endl;
		                cout << "Name      : " << foundAdmin->admin_name << endl;
		                cout << "Email     : " << foundAdmin->admin_email << endl;
		                cout << "Phone     : " << foundAdmin->admin_phone << endl;
		                cout << "Position  : " << foundAdmin->admin_position << endl;
		            } else {
		                cout << "\nAdmin not found!" << endl;
		            }
		            cout << "\nPress [Enter] back to menu...";
		            cin.get();
		            system("cls");
				}else if (choice == "4") {
					// Save admin data to file
		            saveToFile();
		            cout << "Saved the admin information to " << filename << endl;
		            cout << "\nPress [Enter] back to menu...";
		            cin.get();
		            system("cls");
		
		        } else if (choice == "5") {
	             	system("cls");
		            teamAMenu();
		
		        } else {
		            cout << "Invalid choice. Please Enter to try again" << endl;
		            cin.get();
		            system("cls");
		        }
				
			} while (true);
		}
};

//---------------------------------------------READ FROM FILE (load function)----------------------------------------
//Load products
int loadProducts(Product products[]) {
	//Open the raw_product.txt in read mode
    ifstream file("raw_product.txt"); 
    
    //Error handling if file not found
    if (!file) {
        cout << "Error opening product file!\n";
        return 0;
    }
    
    //Initialize a count variable for reading the products with a loop
    int count = 0;
    
    //While loop to read unsorted product data line-by-line
    while (file >> products[count].id) {
	    file.ignore(); // Ignore the whitespace after ID
	    getline(file, products[count].name, '"');
	    getline(file, products[count].name, '"'); // Read the product name inside quotes
	    file >> products[count].price; // Read the product price
	    file.ignore(); // Ignore space after product price
	    getline(file, products[count].description, '"');
	    getline(file, products[count].description, '"'); // Read product description inside quotes
	    count++; //increase count variable to loop again
	}
    file.close(); //Close the raw_product.txt
    return count; //Return count value to get total of product data
}

//Load orders
int loadOrders(Order orders[]) {
    //Open the order.txt in read mode
	ifstream file("order.txt");
    
    //Error handling if file not found
	if (!file) {
        cout << "Error opening order file!\n";
        return 0;
    }
	
	//Initialize a count variable for reading the orders with a loop
    int count = 0;
    
    //While loop to read unsorted order data line-by-line
    while (file >> orders[count].orderID) {
        file >> orders[count].customerID; // Read the pcustomer id
        file >> orders[count].productID; // Read the product id
        file.ignore(); // Ignore space before datetime
        getline(file, orders[count].dateTime, '"'); 
        getline(file, orders[count].dateTime, '"'); // Read the order date inside quotes
        file >> orders[count].totalAmount; // Read the total amount
        count++;
    }

    file.close(); //Close the order.txt
    return count; //Return count value to get total of order data
}

//-------------------------------------------------------- Main Menu ------------------------------------------------------
void mainMenu(){
	system("cls");
	string choice;
	
	//Display the main menu
	cout<<"=================================================="<<endl;
    cout<<"                  TDS Assignment                  "<<endl;
    cout<<"=================================================="<<endl;
    cout<<"1. Team A"<<endl;
    cout<<"2. Team B"<<endl;
    cout<<"3. Exit System"<<endl;
    cout<<"--------------------------------------------------"<<endl;
    
    //Prompt user to enter the choice
	cout<<"Enter your choice: ";
    getline(cin, choice);
	
	//If-else case to determine the choice and its corresponding actions
    if(choice=="1"){
    	system("cls");
    	teamAMenu(); //Display Team A Menu
	}
	else if(choice=="2"){
		system("cls");
		teamBMenu(); //Display Team B Menu
	}
    else if(choice=="3"){
    	cout<<"\nThank you for using the system. Goodbye!"<<endl;
		exit(1); //Exit the program
	}
	else{
		cout<<"Invalid choice. Press Enter to try again";
		cin.get();		
		mainMenu(); // Error handling if choice invalid
	}
}

//--------------------------------------------------- Team A MENU -----------------------------------------------------
void teamAMenu(){
	HashCustomer HC;
	HashAdmin HA;
	string choice;
	
	cout<<"=================================================="<<endl;
    cout<<"                    Team A Menu                   "<<endl;
    cout<<"=================================================="<<endl;
    cout<<"1. Hashing Customer"<<endl;
    cout<<"2. Hashing Admin"<<endl;
    cout<<"3. Return to Main Menu"<<endl;
    cout<<"--------------------------------------------------"<<endl;
    cout<<"Enter your choice: ";
    getline(cin,choice);
	//If-else case to determine the choice and its corresponding actions
    if (choice == "1") {
	    system("cls");
	    HC.hashingCustomer(); //Display hashing customer menu
	}
	else if (choice == "2") {
	    system("cls");
	    HA.hashingAdmin(); //Display hashing admin menu
	}
	else if (choice == "3") {
	    system("cls");
	    mainMenu(); //Display main menu
	}
	else {
	    cout << "Invalid choice. Press Enter to try again";
	    cin.get();
	    system("cls");
	    teamAMenu(); //Error handling for invalid choice input
	}
}

//-------------------------------------------------- Team B MENU ----------------------------------------------
void teamBMenu(){
	string choice;
	
	//Display the team b menu
	cout<<"=================================================="<<endl;
    cout<<"                    Team B Menu                   "<<endl;
    cout<<"=================================================="<<endl;
    cout<<"1. Display Unsorted Products"<<endl;
    cout<<"2. Display Unsorted Order History"<<endl;
    cout<<"3. Return to Main Menu"<<endl;
    cout<<"--------------------------------------------------"<<endl;
    
	//Get user choice
	cout<<"Enter your choice: ";
    getline(cin,choice);
	
	//If-else case to determine the choice and its corresponding actions
    if (choice == "1") {
	    system("cls");
	    productMenu(); //Display product menu
	}
	else if (choice == "2") {
	    system("cls");
	    orderMenu(); //Display order menu
	}
	else if (choice == "3") {
	    system("cls");
	    mainMenu(); //Display main menu
	}
	else {
	    cout << "Invalid choice. Press Enter to try again";
	    cin.get();
	    system("cls");
	    teamBMenu(); //Error handling for invalid choice input
	}
}

//------------------------------------Save Unsorted Products data to "raw_product.txt"------------------------------
void saveRawProducts(Product products[], int productCount) {
    //Open "raw_product.txt" in write mode
	ofstream outFile("raw_product.txt");
	
	//Error handling if unable to open the file
    if (!outFile) {
        cout << "Error opening file for writing!" << endl;
        return;
    }
    
    //For loop to write the product data into file
    for (int i = 0; i < productCount; i++) {
        outFile << setw(3) << setfill('0') << products[i].id << " \"" 
                << products[i].name << "\" " 
                << fixed << setprecision(2) << products[i].price << " \"" 
                << products[i].description << "\"\n";
    }
    
    //Close the file
    outFile.close();
}

//------------------------------------Save Sorted Products data to "sorted_product.txt"-----------------------------
void saveSortedProducts(Product products[], int productCount) {
    //Open "sorted_product.txt" in write mode
	ofstream outFile("sorted_product.txt");
    
	//Error handling if unable to open the file
	if (!outFile) {
        cout << "Error opening file for writing!" << endl;
        return;
    }
    
    //Call shellsort function to sort products according to product id
    shellSort(products, productCount);
    
    //For loop to write the product data into file
    for (int i = 0; i < productCount; i++) {
        outFile << setw(3) << setfill('0') << products[i].id << " \"" 
                << products[i].name << "\" " 
                << fixed << setprecision(2) << products[i].price << " \"" 
                << products[i].description << "\"\n";
    }
    
    //Close the file
    outFile.close();
    
    //Message to notify user data have been saved successfully
    cout << "Sorted products saved to sorted_product.txt" << endl;
    cout << "Press [ENTER] to return to Product Menu.";
	cin.get();    
}

//----------------------------------Save Sorted Orders data to "sorted_order.txt"-----------------------------------
void saveSortedOrders(Order orders[], int orderCount) {
    
    //Call shellsort function to sort orders according to date-time
    shellSortOrdersByDateTime(orders,orderCount);
	
	//Open "sorted_order.txt" in write mode
	ofstream outFile("sorted_order.txt");
    
	//Error handling if unable to open the file
	if (!outFile) {
        cout << "Error opening file for writing!" << endl;
        return;
    }
    
    //For loop to write the order data into file
    for (int i = 0; i < orderCount; i++) {
        outFile << orders[i].orderID << " "
                << orders[i].customerID << " "
                << orders[i].productID << " "
                << "\"" << orders[i].dateTime << "\" " 
                << orders[i].totalAmount << "\n";
    }
    
    //Close the file
    outFile.close();
    
    //Message to notify user data have been saved successfully
    cout << "Sorted orders saved to sorted_order.txt\n";
    cout << "Press [ENTER] to return to Order Menu.";
	cin.get();   
}

//-------------------------------------------------Add New Products-------------------------------------------------
void addProducts(Product products[], ProductQueue &pq) {
    // Call loadProducts() to get the total of products
    int productCount = loadProducts(products);

    // Error handling if queue is full
    if (pq.full()) {
        cout << "Queue is full, cannot add more products.\n";
        return;
    }

    // Temporary sorted copy of product data
    Product sortedProducts[MAX_PRODUCTS];
    for (int i = 0; i < productCount; i++) {
        sortedProducts[i] = products[i];
    }
    shellSort(sortedProducts, productCount);

    // Declare variables
	Product newProduct;
    bool idExist = false;
    string choice;
    int addCount = 0;
    const int MAX_ADD = 5;

    system("cls");

    do {
	        // Display current product data
			system("cls");
	        cout << "\nCurrent Products:\n";
	        for (int i = 0; i < productCount; i++) {
	            printIdWithLeadingZeros(sortedProducts[i].id);
	            cout << " - " << sortedProducts[i].name << endl;
	        }
	
	        // Ask user to enter the ID for new product
			string idStr;
			int idToAdd = -1;
			bool isValid = false;
			do {
			    cout << "\nEnter ID in 3 digits [Press 0 to return to Product Menu] : ";
			    getline(cin, idStr);
			
			    if (idStr == "0") return;
			    isValid = true;
			
			    if (idStr.length() != 3) {
			        isValid = false;
			    } else {
			        for (char c : idStr) {
			            if (!isdigit(c)) {
			                isValid = false;
			                break;
			            }
			        }
			    }
			
			    if (!isValid) {
			        cout << "_________________________________________" << endl;
			        cout << "|Invalid Product ID!                    |" << endl;
			        cout << "|1. ID must be digits only.             |" << endl;
			        cout << "|2. ID must be exactly 3 digits.        |" << endl;
			        cout << "|_______________________________________|" << endl << endl;
			        continue;
			    }
			
			    idToAdd = StringToInt(idStr);
			
			    idExist = false;
			    int index = jumpSearch(sortedProducts, productCount, idToAdd);
			    if (index != -1 && sortedProducts[index].id == idToAdd) {
			        cout << "_________________________________________" << endl;
			        cout << "|This Product ID already exists!        |" << endl;
			        cout << "|_______________________________________|" << endl << endl;
			        idExist = true;
			    }else{
			    	newProduct.id = idToAdd;
				}
			} while (!isValid || idExist);

        // Ask user to enter the name for new product
		do {
            cout << "Enter Product Name      : ";
            getline(cin, newProduct.name);
            
			// Check if product name id empty
			if (isEmpty(newProduct.name)) {
                cout << "_______________________________________________" << endl;
		        cout << "|Product Name cannot be empty or spaces only! |" << endl;
		        cout << "|_____________________________________________|" << endl << endl;
                continue;
            }

            // Check if there's number and special character
			bool symbolAndNumber = false;
            for (char c : newProduct.name) {
                int ascii = (int)c;
                if (!(ascii == 32 || (ascii >= 65 && ascii <= 90) || (ascii >= 97 && ascii <= 122))) {
                    symbolAndNumber = true;
                    break;
                }
            }
            if (symbolAndNumber) {
                cout << "________________________________________________________" << endl;
		        cout << "|Number(s) & special character(s) are not allowed!     |" << endl;
		        cout << "|______________________________________________________|" << endl << endl;
                continue;
            }

            // Check if the product name already exists
			string newProductNameLower = toLowerCase(newProduct.name);
            bool exists = false;
            for (int i = 0; i < productCount; i++) {
                if (toLowerCase(products[i].name) == newProductNameLower) {
                    exists = true;
                    break;
                }
            }
            if (exists) {
                cout << "_________________________________________" << endl;
		        cout << "|This Product Name already exists!      |" << endl;
		        cout << "|_______________________________________|" << endl << endl;
                continue;
            }
            break;
        } while (true);

        string priceStr;
        float price = -1.0f;
        // Ask user to enter price for new product
		do {
            cout << "Enter Price             : ";
            getline(cin, priceStr);
            price = StringToFloat(priceStr);
            // Check if the price is lower than 0
			if (price <= 0) {
                cout << "____________________________________________________________" << endl;
                cout << "|Invalid price!                                             |" << endl;
                cout << "|1. Only digits with maximum one floating point are allowed |" << endl;
                cout << "|2. Price value must be greater than 0.                     |" << endl;
                cout << "|___________________________________________________________|" << endl << endl;
            }
        } while (price <= 0);
        newProduct.price = price;

        // Ask user to enter description for new product
		do {
            cout << "Enter Description       : ";
            getline(cin, newProduct.description);
            
			// Check if the description is empty
			if (isEmpty(newProduct.description)) {
                cout << "________________________________________________________" << endl;
	        	cout << "|Description cannot be empty or spaces only!           |" << endl;
	        	cout << "|______________________________________________________|" << endl << endl;
            }
        } while (isEmpty(newProduct.description));

        // Add new product to array
        products[productCount] = newProduct;
        productCount++;
        addCount++;

        // Add to queue
        if (!pq.full()) {
            pq.append(newProduct);
        } else {
            cout << "| Product Queue is full. Product not added to queue! |\n";
        }

		// Save to file
		ofstream outFile("raw_product.txt", ios::app);
		if (!outFile) {
		    cout << "Error opening file for writing!" << endl;
		    return;
		}
		
		outFile << setw(3) << setfill('0') << newProduct.id << " "; // format ID like 004
		outFile << "\"" << newProduct.name << "\" ";
		outFile << fixed << setprecision(2) << newProduct.price << " ";
		outFile << "\"" << newProduct.description << "\"" << endl;
		
		outFile.close();

        cout << "\nProduct added successfully!" << endl;
        
        // Reload the product data with latest record
		productCount = loadProducts(products);
        for (int i = 0; i < productCount; i++) {
		    sortedProducts[i] = products[i];
		}
		shellSort(sortedProducts, productCount);

        // Ask the user if wanted to add another product
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

//------------------------------------------------- Search Product -------------------------------------------------
void searchProducts(Product products[]){
	// Call loadProducts() to get the total of products
	productCount = loadProducts(products);
	
	// Ask user to enter targeted product id
	string IDToSearchString;		
	cout << "\nEnter Product ID to search / 0 to return to Product Menu: ";
	getline(cin,IDToSearchString);
	
	// Return to Product Menu if entered '0'
	 if(IDToSearchString=="0"){
		productMenu();
	}
			
	// Convert targeted product id into int
	int IDToSearch = StringToInt(IDToSearchString);
			    
	// Shellsort the products data and search the target product with jumpsearch
	shellSort(products, productCount);
	int prodIndex = jumpSearch(products, productCount, IDToSearch);
			
	// Display seraching result
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

//-------------------------------------------------- Product Menu --------------------------------------------------
void productMenu(){
	Product products[MAX_PRODUCTS];
	ProductQueue pq;
	string choice;

	do {
		// Call loadProducts() to get the total of products
		int productCount = loadProducts(products);
		
	    // Display unsorted products
	    pq.displayProduct();

	    // Display available operations
        cout << "|================================================|" << endl;
        cout << "|                 Available Actions              |" << endl;
        cout << "|================================================|" << endl;
        cout << "|1. Add New Product (min. 5 entries)             |" << endl;
        cout << "|2. Delete First Product in Queue                |" << endl;
        cout << "|3. Search Data by ID                            |" << endl;
        cout << "|4. Display Sorted Data                          |" << endl;
        cout << "|5. Save Sorted Data                             |" << endl;
        cout << "|6. Return to Team B Menu                        |" << endl;
        cout << "|________________________________________________|" << endl;
        
		// Get choice from user
		cout << "Enter your choice: ";
        getline(cin,choice);
        // If-else case to determine the choice with corresponding actions
        if(choice=="1"){
        	system("cls");
            addProducts(products, pq); // call add product function
		}
        else if(choice=="2"){
		    system("cls");
		    pq.deleteProduct(); // delete from file and queue
		    cout << "\nPress [Enter] to return to Product Menu...";
		    cin.get();
		    pq = ProductQueue(); // re-load updated product list from file
		    system("cls");
		}
        else if(choice=="3"){
        	system("cls");
        	searchProducts(products); // call search product function
		}
		else if(choice=="4"){
			// Display sorted products
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
	        saveSortedProducts(products, productCount); // call save sorted product function
		}
		else if(choice=="6"){
			system("cls");
            teamBMenu(); // Return to Team B Menu
            return;
		}
	    else{
	    	cout << "Invalid input. Please enter a number between 1 and 5.\n";
		    cout << "Press [Enter] to continue...";
		    cin.get();
		    system("cls");
		    productMenu(); // Error handling for invalid input
		}
        system("cls");
	}while (true);
}

//------------------------------------------------- Add New Order --------------------------------------------------
void addOrders(Order orders[],OrderQueue &oq) {

	// Error handling if queue is full
	if(oq.full()) {
        cout << "Queue is full, cannot add more orders.\n";
        return;
    }

    // Call loadOrders() to get the total of orders
	int orderCount = loadOrders(orders);

	// Temporary sorted copy of order data according to date-time
    Order sortedOrders[MAX_PRODUCTS];
    for (int i = 0; i < orderCount; i++) {
        sortedOrders[i] = orders[i];
    }
    shellSortOrdersByDateTime(sortedOrders,orderCount);
    
    // Declare variables
	Order newOrder;
    bool idExist = false;
    string choice;
    int addCount = 0;
    const int MAX_ADD = 5;
    
    // Load customer and product data for validation
    HashCustomer HC;
    HC.loadFromFile();
    Product products[MAX_PRODUCTS];
    int productCount = loadProducts(products);

	// Sort products by ID for jump search
    shellSort(products, productCount);
    
    system("cls");
    
    do {
        cout << "\nCurrent Orders:\n";
        for(int i = 0; i < orderCount; i++) {
            cout << sortedOrders[i].orderID << " - " 
                 << sortedOrders[i].dateTime << " - " 
                 << "Customer: " << sortedOrders[i].customerID << endl;
        }
        
        cout << endl;
        
        // Validate Order ID
        bool validOrderID = false;
        do {
            cout << "Enter Order ID (format: ORD followed by 3 digits, e.g. ORD001) [Press 0 to return to Order Menu]: ";
            getline(cin, newOrder.orderID);
            
            if(newOrder.orderID == "0") {
                return;
            }
            
            // Check if starts with ORD and has exactly 3 digits after
            if(newOrder.orderID.length() != 6 || 
               newOrder.orderID[0] != 'O' || 
               newOrder.orderID[1] != 'R' || 
               newOrder.orderID[2] != 'D') {
                cout << "Invalid Order ID format! Must be ORD followed by 3 digits (e.g. ORD001).\n\n";
                continue;
            }
            
            // Check the last 3 characters are digits (0-9)
            bool allDigits = true;
            for(int i = 3; i < 6; i++) {
                if(newOrder.orderID[i] < '0' || newOrder.orderID[i] > '9') {
                    allDigits = false;
                    break;
                }
            }
            
            if(!allDigits) {
                cout << "Invalid Order ID format! Last 3 characters must be digits.\n\n";
                continue;
            }
            
            // Check if ID exists
            idExist = false;
            for(int i = 0; i < orderCount; i++) {
                if(orders[i].orderID == newOrder.orderID) {
                    cout << "This Order ID already exists! Please re-enter.\n\n";
                    idExist = true;
                    break;
                }
            }
            
            if(!idExist) {
                validOrderID = true;
            }
        } while(!validOrderID);
        
        // Validate Customer ID
        bool validCustomer = false;
        string customerIDStr;
        do {
            cout << "\nEnter Customer ID (must exist in system): ";
            getline(cin, customerIDStr);
            
            if(isEmpty(customerIDStr)) {
                cout << "Customer ID cannot be empty!\n";
                continue;
            }
            
            // Check if customer ID contains only digits (0-9)
            bool allDigits = true;
            for(int i = 0; i < customerIDStr.length(); i++) {
                if(customerIDStr[i] < '0' || customerIDStr[i] > '9') {
                    allDigits = false;
                    break;
                }
            }
            
            if(!allDigits) {
                cout << "Customer ID must contain only digits!\n";
                continue;
            }
            
            // Manual string to int conversion
            int customerID = StringToInt(customerIDStr);

            Customer* foundCustomer = HC.search(customerIDStr);
            if(foundCustomer == NULL) {
                cout << "Customer ID not found in system! Please enter a valid customer ID.\n";
            } else {
                validCustomer = true;
                newOrder.customerID = customerID;
            }
        } while(!validCustomer);
        
        // Validate Product ID
        bool validProduct = false;
        string productIDStr;
        do {
            cout << "\nEnter Product ID (must exist in system): ";
            getline(cin, productIDStr);
            
            if(isEmpty(productIDStr)) {
                cout << "Product ID cannot be empty!\n";
                continue;
            }
            
            // Check if product ID contains only digits (0-9)
            bool allDigits = true;
            for(int i = 0; i < productIDStr.length(); i++) {
                if(productIDStr[i] < '0' || productIDStr[i] > '9') {
                    allDigits = false;
                    break;
                }
            }
            
            if(!allDigits) {
                cout << "Product ID must contain only digits!\n";
                continue;
            }
            // Manual string to int conversion
            int productID = StringToInt(productIDStr);
			
            // Use jum search to check if the product exist
            int foundIndex = jumpSearch(products, productCount, productID);
            
            if (foundIndex == -1) {
                cout << "Product ID not found in system! Please re-enter.\n";
            } else {
                validProduct = true;
                newOrder.productID = productID; // Assign valid product ID
            }
        } while(!validProduct);
        
        // Validate Date/Time
        bool validDateTime = false;
        do {
            cout << "\nEnter Date/Time (format: YYYY-MM-DD HH:MM): ";
            getline(cin, newOrder.dateTime);
            
            if(isEmpty(newOrder.dateTime)) {
                cout << "Date/Time cannot be empty!\n";
                continue;
            }
            
            // Basic format validation
            if(!isValidDateTime(newOrder.dateTime)) {
                cout << "Invalid date/time format! Please use YYYY-MM-DD HH:MM\n";
                continue;
            }
            
            // Check all other characters are digits (0-9) except the separators
            bool validFormat = true;
            for(int i = 0; i < 15; i++) {
                if(i == 4 || i == 7 || i == 10 || i == 13 ) continue;
                if(newOrder.dateTime[i] < '0' || newOrder.dateTime[i] > '9') {
                    validFormat = false;
                    break;
                }
            }
            
            if(!validFormat) {
                cout << "Invalid characters in date/time! Please use format YYYY-MM-DD HH:MM:SS\n";
                continue;
            }
            
            validDateTime = true;
        } while(!validDateTime);
        
        // Validate Total Amount
        bool validAmount = false;
        string amountStr;
        do {
            cout << "\nEnter Total Amount (must be positive number): ";
            getline(cin, amountStr);
            
            if(isEmpty(amountStr)) {
                cout << "Amount cannot be empty!\n";
                continue;
            }
            
            // Check for valid number format
            bool hasDecimal = false;
            bool validNumber = true;
            int decimalPlaces = 0;
            for(int i = 0; i < amountStr.length(); i++) {
                if(amountStr[i] == '.') {
                    if(hasDecimal) {
                        validNumber = false;
                        break;
                    }
                    hasDecimal = true;
                }
                else if(amountStr[i] < '0' || amountStr[i] > '9') {
                    validNumber = false;
                    break;
                }
                else if(hasDecimal) {
                    decimalPlaces++;
                }
            }
            
            if(!validNumber) {
                cout << "Invalid amount! Please enter a valid positive number.\n";
                continue;
            }
            
            // Manual string to double conversion
            double amount = 0.0;
            double decimalMultiplier = 0.1;
            bool decimalReached = false;
            for(int i = 0; i < amountStr.length(); i++) {
                if(amountStr[i] == '.') {
                    decimalReached = true;
                }
                else if(!decimalReached) {
                    amount = amount * 10 + (amountStr[i] - '0');
                }
                else {
                    amount += (amountStr[i] - '0') * decimalMultiplier;
                    decimalMultiplier *= 0.1;
                }
            }
            
            if(amount <= 0) {
                cout << "Amount must be a positive number!\n";
            } else {
                validAmount = true;
                newOrder.totalAmount = amount;
            }
        } while(!validAmount);

		oq.append(newOrder);

        orders[orderCount] = newOrder;
        orderCount++;
        addCount++;

        // Save to order file
        ofstream outFile("order.txt", ios::app);
        if (!outFile) {
            cout << "Error opening file for writing!" << endl;
            return;
        }
        
        outFile << "\n" << newOrder.orderID << " "
                << newOrder.customerID << " "
                << newOrder.productID << " "
                << "\"" << newOrder.dateTime << "\" " 
                << fixed << setprecision(2) << newOrder.totalAmount << "\n";
        outFile.close();

        cout << "\nOrder added successfully!" << endl;
        
        if(addCount < MAX_ADD) {
            cout << "Do you want to continue adding other orders? [" << (MAX_ADD-addCount) << " times left]" << endl;
            cout << "__________" << endl;
            cout << "| 1. YES |" << endl;
            cout << "| 2. NO  |" << endl;
            cout << "|________|" << endl;
            cout << "\nEnter your choice : ";
            getline(cin, choice);
        } else {
            cout << "Maximum of 5 orders added.\n";
            choice = "2";
        }
    } while(choice == "1" && addCount < MAX_ADD);

    cout << "Press [ENTER] to return to Order Menu.";
    cin.get();     
    system("cls");
}

//----------------------------------------------------Order Menu----------------------------------------------------
void orderMenu(){
	Order orders[MAX_ORDERS];
	string choice;
	OrderQueue oq;
	do {
		int  orderCount = loadOrders(orders);
		// Display order data
		oq.display();
	    // Display available operations
        cout << "|================================================|" << endl;
        cout << "|                 Available Actions              |" << endl;
        cout << "|================================================|" << endl;
        cout << "|1. Add New Order                                |" << endl;
        cout << "|2. Search Data by ID                            |" << endl;
        cout << "|3. Display Sorted Data (Latest first)           |" << endl;
        cout << "|4. Save Sorted Data                             |" << endl;
        cout << "|5. Process Next Order                           |" << endl;
		cout << "|6. Return to Team B Menu                        |" << endl;
        cout << "|________________________________________________|" << endl;    
		// Get choice from user
		cout << "Enter your choice: ";
        getline(cin,choice);
        
        // If-else case to determine the choice with the corresponding actions
        if(choice=="1"){
            system("cls");
            addOrders(orders,oq); // Call add order function
    	}
      	else if(choice=="2"){
			system("cls");
			orderCount = loadOrders(orders);
			string searchOrderID;  
			// Ask user to enter the targeted order id to search   
			cout << "\nEnter Order ID to search / 0 to return to Order Menu: ";
			getline(cin,searchOrderID);
			
			// Return to Order Menu if entered '0'
			if(searchOrderID=="0"){
				orderMenu();
			}
			    
			// Apply linear search using order ID (we don't implement jumpsearch here because Order ID is a string)
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
			cout << "Press [ENTER] to Return.";
			cin.ignore();
			cin.get();  
		}   
		else if(choice=="3"){
            // Display sorted order data
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
		}
 		else if(choice=="4"){
	        system("cls");
	        saveSortedOrders(orders, orderCount); // Call save order function
		}
		else if(choice=="5"){
            system("cls");
		    oq.processNextOrder(); // Call process order function
		    cout << "\nPress [Enter] to return to Order Menu.";
		    cin.get();
		}
		else if(choice=="6"){
            system("cls");
            teamBMenu(); // return to Team B Menu
            return;
		}
		else{
	    	cout << "Invalid input. Please enter a number between 1 and 5.\n";
		    cout << "Press [Enter] to continue...";
		    cin.get();
		    system("cls");
		    orderMenu(); // Error handling for invalid input
		}
        system("cls");
	}while (true);
}

//---------------------------------------------------Main Program---------------------------------------------------
int main() {
	//call the mainMenu function (it works as the landing page of the program)
    mainMenu();

    return 0;
}