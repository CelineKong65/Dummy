#include <iostream>
#include <fstream>
#include <string>
#include <ctime>
#include <cctype>
#include <cstring>
#include <cmath>

using namespace std;

// File paths
const string PRODUCT_FILE = "product.txt";
const string MEMBERS_FILE = "member.txt";
const string MEMBERS_ID_FILE = "member_id.txt";
const string ADMINS_FILE = "admin.txt";
const string ADMINS_ID_FILE = "admin_id.txt";

// Structures
#include <string>
using namespace std;

struct Member {
    string member_id;
    string full_name;
    string email;
    string password;
    string contact;
    string status;

    Member(string id="", string name="", string mail="", string pass="", string cont="", string stat="Active") {
        member_id = id;
        full_name = name;
        email = mail;
        password = pass;
        contact = cont;
        status=stat;
    }
};

struct Admin {
    string admin_id;
    string full_name;
    string email;
    string password;
    string contact;
    string position;
    string status;

    Admin(string id="", string name="", string mail="", string pass="", string cont="", string level="Admin", string stat="Active") {
        admin_id = id;
        full_name = name;
        email = mail;
        password = pass;
        contact = cont;
        position = level;
        status = stat;
    }
};

struct Product {
    string product_id;
    string product_name;
    string category;
    double price;
    int stock;
    string description;
    string status;

    Product(string id = "", string name = "", string cat = "", double cost = 0.0,
            int quantity = 0, string desc = "", string stat = "") {
        product_id = id;
        product_name = name;
        category = cat;
        price = cost;
        stock = quantity;
        description = desc;
        status = stat;
    }
};

struct CartItem {
    Product product;
    string product_id;
    string product_name;
    double price;
    int quantity;
    double total;
    string status;

    CartItem(Product p = Product(), string pid = "", string name = "", double pr = 0.0,
             int q = 0, double t = 0.0, string stat = "") {
        product = p;
        product_id = pid;
        product_name = name;
        price = pr;
        quantity = q;
        total = t;
        status = stat;
    }
};

// Global variables
Product* products = nullptr;
int productCount = 0;
Member* members = nullptr;
int memberCount = 0;
Admin* admins = nullptr;
int adminCount = 0;
Member loggedInMember;
Admin loggedInAdmin;

// Function Prototype
void mainMenu();
void memberMenu(Member loggedInMember);
void adminMenu(Admin loggedInAdmin);

// Helper functions
void clearScreen() {
    system("cls");
}

int getLength(const string* arr, int maxSize) {
    int count = 0;
    while (count < maxSize && !arr[count].empty()) {
        count++;
    }
    return count;
}

int getLength(const Product* arr, int maxSize) {
    int count = 0;
    while (count < maxSize && !arr[count].product_id.empty()) {
        count++;
    }
    return count;
}

int getLength(const Member* arr, int maxSize) {
    int count = 0;
    while (count < maxSize && !arr[count].member_id.empty()) {
        count++;
    }
    return count;
}

int getLength(const Admin* arr, int maxSize) {
    int count = 0;
    while (count < maxSize && !arr[count].full_name.empty()) {
        count++;
    }
    return count;
}

int getLength(const CartItem* arr, int maxSize) {
    int count = 0;
    while (count < maxSize && !arr[count].product_id.empty()) {
        count++;
    }
    return count;
}

// Bubble sort implementation
template <typename T>
void bubbleSort(T* arr, int n, string key = "") {
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            bool shouldSwap = false;
            
            if (key == "product_id") 
				{shouldSwap = arr[j].product_id > arr[j+1].product_id;} 
			else if (key == "member_id") 
				{shouldSwap = arr[j].member_id > arr[j+1].member_id;} 
			else if (key == "admin_id") 
				{shouldSwap = arr[j].member_id > arr[j+1].member_id;} 
			else
			{
				// Default comparison
                shouldSwap = arr[j] > arr[j+1];
			}
                
            if (shouldSwap) {
                T temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

// Binary search implementation
template <typename T>
T* binarySearch(T* arr, int low, int high, string target, string key = "") {
    while (low <= high) {
        int mid = low + (high - low) / 2;

        string current;
        if (key == "product_id") {
            current = arr[mid].product_id;
        } else if (key == "member_id") {
            current = arr[mid].member_id;
        } else if (key == "admin_id") {
            current = arr[mid].admin_id;
        } else {
            current = arr[mid].name; // Default
        }

        if (current == target) {
            return &arr[mid];
        } else if (current < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return nullptr;
}

// Function to load members from file
void loadMembers() {
    ifstream file(MEMBERS_FILE);
    if (!file.is_open()) {
        ofstream createFile(MEMBERS_FILE);
        createFile.close();
        return;
    }

    // Count members first
    int count = 0;
    string line;
    while (getline(file, line)) {
        if (!line.empty()) count++;
    }
    memberCount = count / 8;
    file.close();

    // Allocate memory
    if (members) delete[] members;
    members = new Member[memberCount];

    // Read data
    file.open(MEMBERS_FILE);
    int index = 0;
    for (int i = 0; i < memberCount; i++) {
        getline(file, members[i].member_id);
        getline(file, members[i].full_name);
        getline(file, members[i].email);
        getline(file, members[i].password);
        getline(file, members[i].contact);
        getline(file, members[i].status);
    }
    file.close();
}

// Function to load admins from file
void loadAdmins() {
    ifstream file(ADMINS_FILE);
    if (!file.is_open()) {
        ofstream createFile(ADMINS_FILE);
        createFile.close();
        return;
    }

    // Count admins first
    int count = 0;
    string line;
    while (getline(file, line)) {
        if (!line.empty()) count++;
    }
    adminCount = count / 5;
    file.close();

    // Allocate memory
    if (admins) delete[] admins;
    admins = new Admin[adminCount];

    // Read data
    file.open(ADMINS_FILE);
    for (int i = 0; i < adminCount; i++) {
        getline(file, admins[i].admin_id);
        getline(file, admins[i].full_name);
        getline(file, admins[i].email);
        getline(file, admins[i].password);
        getline(file, admins[i].contact);
        getline(file, admins[i].position);
        getline(file, admins[i].status);
    }
    file.close();
}

// Function to get next member ID
string getNextMemberId() {
    ifstream file(MEMBERS_ID_FILE);
    string lastId;
    
    if (file.is_open()) {
        string line;
        while (getline(file, line)) {
            if (!line.empty()) lastId = line;
        }
        file.close();
    } else {
        ofstream createFile(MEMBERS_ID_FILE);
        createFile << "U0001\n";
        createFile.close();
        return "U0001";
    }

    if (!lastId.empty()) {
        int num = stoi(lastId.substr(1)) + 1;
        char buffer[10];
        snprintf(buffer, sizeof(buffer), "U%04d", num);
        return string(buffer);
    }
    return "U0001";
}

// Function to get next admin ID
string getNextAdminId() {
    ifstream file(ADMINS_ID_FILE);
    string lastId;
    
    if (file.is_open()) {
        string line;
        while (getline(file, line)) {
            if (!line.empty()) lastId = line;
        }
        file.close();
    } else {
        ofstream createFile(ADMINS_ID_FILE);
        createFile << "A0001\n";
        createFile.close();
        return "A0001";
    }

    if (!lastId.empty()) {
        int num = stoi(lastId.substr(1)) + 1;
        char buffer[10];
        snprintf(buffer, sizeof(buffer), "A%04d", num);
        return string(buffer);
    }
    return "A0001";
}

// Function to save member
void saveMember(const Member& member) {
    ofstream file(MEMBERS_FILE, ios::app);
    if (file.is_open()) {
        file.seekp(0, ios::end);
        if (file.tellp() > 0) {
            file << "\n";
        }
        file << member.member_id << "\n";
        file << member.full_name << "\n";
        file << member.email << "\n";
        file << member.password << "\n";
        file << member.contact << "\n";
        file << member.status << "\n";
        file.close();
    }
}

// Function to update member
void updateMember(const Member& updatedMember) {
    ifstream inFile(MEMBERS_FILE);
    if (!inFile.is_open()) {
        cout << "Member file not found." << endl;
        return;
    }

    string content;
    string line;
    bool found = false;

    while (getline(inFile, line)) {
        if (line == updatedMember.member_id) {
            found = true;
            content += updatedMember.member_id + "\n";
            content += updatedMember.full_name + "\n";
            content += updatedMember.email + "\n";
            content += updatedMember.password + "\n";
            content += updatedMember.contact + "\n";
            content += updatedMember.status + "\n";
            // Skip the next 5 lines (original data)
            for (int i = 0; i < 5; i++) getline(inFile, line);
        } else {
            content += line + "\n";
        }
    }
    inFile.close();

    if (found) {
        ofstream outFile(MEMBERS_FILE);
        outFile << content;
        outFile.close();
    } else {
        cout << "Member not found for update." << endl;
    }
}

// Main menu functions
void signup() {
    string member_id = getNextMemberId();
    string status = "Active";
    string full_name, email, password, confirm_password, contact;
	
	cin.ignore();
    // Full name validation
    while (true) {
        cout << "Enter your full name, [R] to return to the main menu: ";
        getline(cin, full_name);
        
        if (full_name == "R" || full_name == "r") {
            clearScreen();
            mainMenu();
            return;
        }

        bool valid = true;
        int letterCount = 0;
        for (char c : full_name) {
            if (!isalpha(c) && c != ' ') {
                valid = false;
                break;
            }
            if (isalpha(c)) letterCount++;
        }

        if (!valid || letterCount < 2) {
            cout << "Invalid name. Name must have at least 2 letters and contain only letters and spaces." << endl;
            continue;
        }

        break;
    }

    // Email validation
    while (true) {
        cout << "Enter your email (example: user@example.com): ";
        getline(cin, email);

        bool hasAt = false, hasDot = false;
        for (char c : email) {
            if (c == '@') hasAt = true;
            if (c == '.') hasDot = true;
        }

        if (!hasAt || !hasDot) {
            cout << "Invalid email format. Please include @ and . in your email!" << endl;
            continue;
        }

        // Check if email already exists
        bool exists = false;
        for (int i = 0; i < memberCount; i++) {
            if (members[i].email == email) {
                exists = true;
                break;
            }
        }

        if (exists) {
            cout << "This email is already registered. Please use a different email!" << endl;
            continue;
        }

        break;
    }

    // Password validation
    while (true) {
        cout << "Enter your new password (example: Xuanting123): ";
        getline(cin, password);

        if (password.length() < 8) {
            cout << "Password must be at least 8 characters!" << endl;
            continue;
        }

        bool hasUpper = false, hasLower = false, hasDigit = false;
        for (char c : password) {
            if (isupper(c)) hasUpper = true;
            if (islower(c)) hasLower = true;
            if (isdigit(c)) hasDigit = true;
        }

        if (!hasUpper) {
            cout << "Password must contain at least one uppercase letter!" << endl;
            continue;
        }
        if (!hasLower) {
            cout << "Password must contain at least one lowercase letter!" << endl;
            continue;
        }
        if (!hasDigit) {
            cout << "Password must contain at least one digit!" << endl;
            continue;
        }

        cout << "Confirm your password: ";
        getline(cin, confirm_password);
        if (confirm_password != password) {
            cout << "Passwords do not match!" << endl;
            continue;
        }

        break;
    }

    // Contact validation
    while (true) {
        cout << "Enter your contact number (example: 012-34567890): ";
        getline(cin, contact);

        if (contact.length() < 4 || contact[3] != '-') {
            cout << "Format must be like 012-34567890 with a dash at the 4th position!" << endl;
            continue;
        }

        string part1 = contact.substr(0, 3);
        string part2 = contact.substr(4);

        if (!(part1[0] == '0' && part1[1] == '1')) {
            cout << "Phone number must start with '01'!" << endl;
            continue;
        }

        string combined = part1 + part2;
        bool onlyDigits = true;
        for (char c : combined) {
            if (!isdigit(c)) {
                onlyDigits = false;
                break;
            }
        }

        if (!onlyDigits) {
            cout << "Phone number cannot contain symbols or space!" << endl;
            continue;
        }

        if (combined.length() != 10 && combined.length() != 11) {
            cout << "Phone number must be 10 or 11 digits!" << endl;
            continue;
        }

        break;
    }

    // Create and save new member
    Member newMember(full_name, member_id, email, password, contact, status);
    
    // Add to members array
    Member* temp = new Member[memberCount + 1];
    for (int i = 0; i < memberCount; i++) {
        temp[i] = members[i];
    }
    temp[memberCount] = newMember;
    delete[] members;
    members = temp;
    memberCount++;

    saveMember(newMember);

    // Update member ID file
    ofstream idFile(MEMBERS_ID_FILE, ios::app);
    if (idFile.is_open()) {
        idFile << member_id << "\n";
        idFile.close();
    }

    cout << "Registration successful! Your Member ID: " << member_id << endl;
    cout << "\nPress [ENTER] to return to login menu.";
    cin.ignore();
    clearScreen();
}

void login() {
    string email, password;
    
    cin.ignore();
    cout << "\nEnter your email, [R] to return to the main menu: ";
    getline(cin, email);

    if (email == "R" || email == "r") {
        clearScreen();
        mainMenu();
        return;
    }

    cout << "Enter your password: ";
    getline(cin, password);

    ifstream file(MEMBERS_FILE);
    if (!file.is_open()) {
        cout << "Error: Members file not found!" << endl;
        return;
    }

    string lines[6];
    int lineCount = 0;
    bool found = false;

    while (getline(file, lines[lineCount % 6])) {
        if (!lines[lineCount % 6].empty()) {
            lineCount++;
            if (lineCount % 6 == 0) {
                if (lines[2] == email) {
                    found = true;
                    if (lines[5] != "Active") {
                        cout << "Your account is inactive. Please contact admin." << endl;
                        cout << "\nPress [ENTER] to return to login menu.";
                        cin.ignore();
                        clearScreen();
                        file.close();
                        return;
                    }

                    int attempts = 0;
                    string currentPassword = password;
                    while (attempts < 3) {
                        if (currentPassword == lines[3]) {
                            cout << "Logged in Successfully!" << endl;
                            loggedInMember = Member(lines[0], lines[1], lines[2], lines[3], 
                                                   lines[4], lines[5]);
                            cout << "\nPress [ENTER] to continue.";
                            cin.ignore();
                            memberMenu(loggedInMember);
                            file.close();
                            return;
                        } else {
                            attempts++;
                            cout << "Incorrect password! Attempts left: " << 3 - attempts << endl;
                            cout << "Please enter your password again: ";
                            getline(cin, currentPassword);
                        }
                    }

                    cout << "Too many failed attempts. Login terminating." << endl;
                    cout << "\nPress [ENTER] to return to login menu.";
                    cin.ignore();
                    clearScreen();
                    file.close();
                    return;
                }
            }
        }
    }

    if (!found) {
        cout << "Email not found.\n" << endl;
    }

    cout << "\nPress [ENTER] to continue.";
    cin.ignore();
    clearScreen();
    file.close();
}

void adminLogin() {
    string email, password;
    
    cin.ignore();
    cout << "\nEnter your email, [R] to return to the main menu: ";
    getline(cin, email);

    if (email == "R" || email == "r") {
        clearScreen();
        mainMenu();
        return;
    }

    cout << "Enter your password: ";
    getline(cin, password);

    ifstream file(ADMINS_FILE);
    if (!file.is_open()) {
        cout << "Error: Admins file not found!" << endl;
        return;
    }

    string lines[7];
    int lineCount = 0;
    bool found = false;

    while (getline(file, lines[lineCount % 7])) {
        if (!lines[lineCount % 7].empty()) {
            lineCount++;
            if (lineCount % 7 == 0) {
                if (lines[2] == email) {
                    found = true;
                    if (lines[6] != "Active") {
                        cout << "Your account is inactive. Please contact Superadmin." << endl;
                        cout << "\nPress [ENTER] to return to login menu.";
                        cin.ignore();
                        clearScreen();
                        file.close();
                        return;
                    }

                    int attempts = 0;
                    string currentPassword = password;
                    while (attempts < 3) {
                        if (currentPassword == lines[3]) {
                            cout << "Logged in Successfully!" << endl;
                            loggedInAdmin = Admin(lines[0], lines[1], lines[2], lines[3], 
                                                   lines[4], lines[5], lines[6]);
                            cout << "\nPress [ENTER] to continue.";
                            cin.ignore();
                            adminMenu(loggedInAdmin);
                            file.close();
                            return;
                        } else {
                            attempts++;
                            cout << "Incorrect password! Attempts left: " << 3 - attempts << endl;
                            cout << "Please enter your password again: ";
                            getline(cin, currentPassword);
                        }
                    }

                    cout << "Too many failed attempts. Login terminating." << endl;
                    cout << "\nPress [ENTER] to return to login menu.";
                    cin.ignore();
                    clearScreen();
                    file.close();
                    return;
                }
            }
        }
    }

    if (!found) {
        cout << "Email not found.\n" << endl;
    }

    cout << "\nPress [ENTER] to continue.";
    cin.ignore();
    clearScreen();
    file.close();
}

void mainMenu() {
    while (true) {
        clearScreen();
        cout << "\n===============================================================" << endl;
        cout << "               WELOCOME TO YESMOLAR PIZZA STORE                " << endl;
        cout << "===============================================================" << endl;
        cout << "1.    Sign Up  " << endl;
        cout << "2.    Login  " << endl;
        cout << "3.    Admin Login  " << endl;
        cout << "4.    Exit  " << endl;
        cout << "===============================================================" << endl;

        int choice;
        cout << "Enter your choice: ";
        cin >> choice;

        switch(choice){
        	case 1:{
        		loadMembers();
	            clearScreen();
	            cout << "\n===============================================================" << endl;
	            cout << "                    Signing Up As Member...                    " << endl;
	            cout << "===============================================================" << endl;
	            signup();
				break;
			}
			case 2:{
        		clearScreen();
	            cout << "\n===============================================================" << endl;
	            cout << "                    Logging In As Member...                    " << endl;
	            cout << "===============================================================" << endl;
	            login();
			}
			case 3:{
        		clearScreen();
	            cout << "\n===============================================================" << endl;
	            cout << "                    Logging In As Admin...                    " << endl;
	            cout << "===============================================================" << endl;
	            adminLogin();
			}
			case 4:{
        		cout << "\nThank you for visiting Yesmolar Pizza Store!\n" << endl;
            	exit(0);
			}
			default :{
	            cout << "\nInvalid choice. Press [ENTER] to try again." << endl;
	            cin.ignore();
	            cin.get();
	            clearScreen();
			}
    	}
	}
}

void memberMenu(Member loggedInMember){
	clearScreen();
        cout << "\n===============================================================" << endl;
        cout << "               WELOCOME " << loggedInMember.full_name << endl;
        cout << "===============================================================" << endl;
        cout << "1.    Browse Product  " << endl;
        cout << "2.    View My Cart  " << endl;
        cout << "3.    View Order History  " << endl;
        cout << "4.    View My Profile  " << endl;
        cout << "5.    Rate Our System  " << endl;
        cout << "6.    Log Out  " << endl;
        cout << "===============================================================" << endl;
        
        int choice;
        
        cout << "Enter your choice: ";
        cin >> choice;
        
        switch(choice){
        	case 6:
        		mainMenu();
		}
}

void adminMenu(Admin loggedInAdmin){
	clearScreen();
        cout << "\n===============================================================" << endl;
        cout << "               WELOCOME " << loggedInAdmin.full_name << endl;
        cout << "===============================================================" << endl;
        cout << "1.    View Product Inventory  " << endl;
        cout << "2.    View Admin List  " << endl;
        cout << "3.    View Member List  " << endl;
        cout << "4.    View Order Record  " << endl;
        cout << "5.    View Rating Record  " << endl;
        cout << "6.    View Sales Report  " << endl;
        cout << "7.    View My Admin Profile  " << endl;
        cout << "8.    Log Out  " << endl;
        cout << "===============================================================" << endl;
        
        int choice;
        
        cout << "Enter your choice: ";
        cin >> choice;
        
        switch(choice){
        	case 8:
        		mainMenu();
		}
}

// Main function
int main() {
    // Initialize global arrays
    products = new Product[100]; // Adjust size as needed
    members = new Member[100];
    admins = new Admin[50];

    // Check if product file exists
    ifstream productFile(PRODUCT_FILE);
    if (!productFile.is_open()) {
        cout << "Error: Product file '" << PRODUCT_FILE << "' not found." << endl;
        cout << "Press [ENTER] to exit." << endl;
        cin.ignore();
        return 1;
    }
    productFile.close();

    // Start with login menu
    mainMenu();

    // Clean up memory
    delete[] products;
    delete[] members;
    delete[] admins;

    return 0;
}
