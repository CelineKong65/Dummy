#include <iostream>
#include <iomanip>
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
const int MAX_FIELDS = 7; 

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
void filterProducts();
void displayCart(Member loggedInMember);
void printWrappedText(const string& text);

// Helper functions
void clearScreen() {
    system("cls");
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
void bubbleSortProduct(Product* arr, int n, const string& key) {
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            bool shouldSwap = false;

            if (key == "product_id") {
                shouldSwap = arr[j].product_id > arr[j+1].product_id;
            }

            if (shouldSwap) {
                Product temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

void bubbleSortMember(Member* arr, int n, const string& key) {
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            bool shouldSwap = false;

            if (key == "member_id") {
                shouldSwap = arr[j].member_id > arr[j+1].member_id;
            }

            if (shouldSwap) {
                Member temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

void bubbleSortAdmin(Admin* arr, int n, const string& key) {
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            bool shouldSwap = false;

            if (key == "admin_id") {
                shouldSwap = arr[j].admin_id > arr[j+1].admin_id;
            }

            if (shouldSwap) {
                Admin temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

void bubbleSortCartItem(CartItem* arr, int n, const string& key) {
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            bool shouldSwap = false;

            if (key == "product_id") {
                shouldSwap = arr[j].product_id > arr[j+1].product_id;
            }

            if (shouldSwap) {
                CartItem temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

Product* binarySearchProduct(Product* arr, int low, int high, const string& target, const string& key) {
    while (low <= high) {
        int mid = low + (high - low) / 2;
        string current;

        if (key == "product_id") {
            current = arr[mid].product_id;
        }

        if (current == target) return &arr[mid];
        else if (current < target) low = mid + 1;
        else high = mid - 1;
    }
    return nullptr;
}

CartItem* binarySearchCartItem(CartItem* arr, int low, int high, const string& target, const string& key) {
    while (low <= high) {
        int mid = low + (high - low) / 2;
        string current;

        if (key == "product_id") {
            current = arr[mid].product_id;
        }

        if (current == target) return &arr[mid];
        else if (current < target) low = mid + 1;
        else high = mid - 1;
    }
    return nullptr;
}

Member* binarySearchMember(Member* arr, int low, int high, const string& target, const string& key) {
    while (low <= high) {
        int mid = low + (high - low) / 2;
        string current;

        if (key == "member_id") {
            current = arr[mid].member_id;
        }

        if (current == target) return &arr[mid];
        else if (current < target) low = mid + 1;
        else high = mid - 1;
    }
    return nullptr;
}

Admin* binarySearchAdmin(Admin* arr, int low, int high, const string& target, const string& key) {
    while (low <= high) {
        int mid = low + (high - low) / 2;
        string current;

        if (key == "admin_id") {
            current = arr[mid].admin_id;
        }

        if (current == target) return &arr[mid];
        else if (current < target) low = mid + 1;
        else high = mid - 1;
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

//===============================================================================Member Menu===================================================================================
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
        	case 1:{
        		clearScreen();
        		filterProducts();
				break;
			}
			case 2:{
				clearScreen();
				displayCart(loggedInMember);
				break;
			}
        	case 6:{
        		clearScreen();
        		mainMenu();
				break;
			}
			default:{
				cout << "Invalid choice! Press [ENTER] to retry." ;
				cin.ignore();
				cin.get();
				memberMenu(loggedInMember);
				break;
			}
		}
}

// Function to display a product
void displayProduct(const Product& product) {
    if (product.status == "Active") {
        cout << "----------------------------------------------------------------------" << endl;
        cout << "| Product ID: " << left << setw(55) << product.product_id << "|" << endl;
        cout << "----------------------------------------------------------------------" << endl;
        cout << "| Name      : " << left << setw(55) << product.product_name << "|" << endl;
        cout << "| Category  : " << left << setw(55) << product.category << "|" << endl;
        cout << "| Price     : RM " << left << setw(52) << fixed << setprecision(2) << product.price << "|" << endl;

        if (product.stock <= 0) {
            cout << "| WARNING   : SORRY! THIS PRODUCT IS CURRENTLY OUT OF STOCK!         |" << endl;
        } else {
            cout << "| Stock     : " << left << setw(55) << product.stock << "|" << endl;
            cout << "|                                                                    |" << endl;
            cout << "|";
            printWrappedText(product.description);
        }
        cout << "----------------------------------------------------------------------" << endl;
    }
}

int splitCSVLine(const string& line, string* parts, int maxParts) {
    int count = 0;
    bool inQuotes = false;
    string current;

    for (size_t i = 0; i < line.size(); i++) {
        char c = line[i];

        if (c == '"') {
            inQuotes = !inQuotes;  // Toggle inQuotes flag
        } 
        else if (c == ',' && !inQuotes) {
            if (count < maxParts) {
                parts[count++] = current;
                current.clear();
            }
            else {
                // More fields than expected, ignore extras or break
                break;
            }
        } 
        else {
            current += c;
        }
    }

    if (count < maxParts) {
        parts[count++] = current;
    }

    return count;
}

// Trim surrounding quotes from a string if present
string trimQuotes(const string& s) {
    if (s.length() >= 2 && s.front() == '"' && s.back() == '"') {
        return s.substr(1, s.length() - 2);
    }
    return s;
}

bool loadProducts() {
	
    ifstream file(PRODUCT_FILE);
    if (!file.is_open()) {
        cout << "Error: Product file not found!" << endl;
        return false;
    }

    // First count the number of non-empty lines (products)
    productCount = 0;
    string line;
    while (getline(file, line)) {
        if (!line.empty()) productCount++;
    }
    file.close();

    // Allocate memory for products
    if (products) delete[] products;
    products = new Product[productCount];

    // Open file again to read data
    file.open(PRODUCT_FILE);
    if (!file.is_open()) {
        cout << "Error: Product file not found on second open!" << endl;
        return false;
    }

    int index = 0;
    while (getline(file, line) && index < productCount) {
        if (line.empty()) continue;

        string parts[MAX_FIELDS];
        int fieldsFound = splitCSVLine(line, parts, MAX_FIELDS);
        if (fieldsFound < MAX_FIELDS) {
            cout << "Warning: Line skipped due to insufficient fields: " << line << endl;
            continue;
        }

        // Trim quotes
        for (int i = 0; i < MAX_FIELDS; i++) {
            parts[i] = trimQuotes(parts[i]);
        }

        // Assign to product struct, with simple error handling for conversions
        products[index].product_id = parts[0];
        products[index].product_name = parts[1];
        products[index].category = parts[2];
        try {
            products[index].price = stod(parts[3]);
        } catch (...) {
            cout << "Warning: Invalid price format in line: " << line << endl;
            products[index].price = 0;
        }
        try {
            products[index].stock = stoi(parts[4]);
        } catch (...) {
            cout << "Warning: Invalid stock format in line: " << line << endl;
            products[index].stock = 0;
        }
        products[index].description = parts[5];
        products[index].status = parts[6];

        index++;
    }
    file.close();

    // Adjust productCount if some lines were skipped
    productCount = index;

    // Sort products by product_id - assuming bubbleSortProduct is implemented
    bubbleSortProduct(products, productCount, "product_id");

    return true;
}

// Function to update product file
bool updateProductFile() {
    ofstream file(PRODUCT_FILE);
    if (!file.is_open()) {
        cout << "Error: Could not update product file!" << endl;
        return false;
    }

    for (int i = 0; i < productCount; i++) {
        file << products[i].product_id << ","
             << products[i].product_name << ","
             << products[i].category << ","
             << fixed << setprecision(2) << products[i].price << ","
             << products[i].stock << ","
             << products[i].description << ","
             << products[i].status << endl;
    }
    file.close();
    return true;
}

// Function to get cart filename
string getCartFilename(const string& member_id) {
    return member_id + "_cart.txt";
}

bool loadCart(CartItem*& cart, int& cartSize, const string& member_id) {
    if (member_id.empty()) {
        cout << "Error: Cannot load cart. No user logged in." << endl;
        return false;
    }

    string cartFile = getCartFilename(member_id);
    ifstream file(cartFile);
    if (!file.is_open()) {
        // Create an empty cart file if not found
        ofstream newFile(cartFile);
        if (!newFile.is_open()) {
            cout << "Error: Cannot create cart file for member " << member_id << endl;
            return false;
        }
        newFile.close();

        cartSize = 0;
        cart = nullptr;
        return true;
    }

    // Count non-empty lines first
    cartSize = 0;
    string line;
    while (getline(file, line)) {
        if (!line.empty()) cartSize++;
    }
    file.close();

    if (cartSize == 0) {
        cart = nullptr; // no items
        return true;
    }

    // Allocate memory
    if (cart) delete[] cart;
    cart = new CartItem[cartSize];

    // Reopen to read data
    file.open(cartFile);
    if (!file.is_open()) {
        cout << "Error: Cart file not found on second open!" << endl;
        return false;
    }

    int index = 0;
    while (getline(file, line) && index < cartSize) {
        if (line.empty()) continue;

        string parts[6];
        int fieldsFound = splitCSVLine(line, parts, 6);
        if (fieldsFound < 6) {
            cout << "Warning: Skipping invalid cart line: " << line << endl;
            continue;
        }

        for (int i = 0; i < 6; i++) {
            parts[i] = trimQuotes(parts[i]);
        }

        // Assign cart item fields
        // parts[0] = user id (member id), parts[1] = product_id, etc.
        cart[index].product_id = parts[1];
        cart[index].product_name = parts[2];
        try {
            cart[index].price = stod(parts[3]);
            cart[index].quantity = stoi(parts[4]);
            cart[index].total = stod(parts[5]);
        } catch (...) {
            cout << "Warning: Invalid number format in cart line: " << line << endl;
            cart[index].price = 0;
            cart[index].quantity = 0;
            cart[index].total = 0;
        }

        // Find the product info from products array
        Product* product = binarySearchProduct(products, 0, productCount - 1, cart[index].product_id, "product_id");
        if (product) {
            cart[index].product = *product;
        } else {
            // If product not found, clear or default product data if needed
        }

        index++;
    }
    file.close();

    // Adjust cartSize if some lines skipped
    cartSize = index;

    return true;
}

// Function to save cart to file
bool saveCart(CartItem* cart, int cartSize, const string& member_id) {
    if (member_id.empty()) {
        cout << "Error: Cannot save cart. No user logged in." << endl;
        return false;
    }

    string cartFile = getCartFilename(member_id);
    ofstream file(cartFile);
    if (!file.is_open()) {
        cout << "Error: Could not update cart file!" << endl;
        return false;
    }

    for (int i = 0; i < cartSize; i++) {
        file << member_id << ","
             << cart[i].product_id << ","
             << cart[i].product_name << ","
             << fixed << setprecision(2) << cart[i].price << ","
             << cart[i].quantity << ","
             << fixed << setprecision(2) << (cart[i].price * cart[i].quantity) << endl;
    }
    file.close();
    return true;
}

// Function to check if string is a number
bool isInteger(const string& s) {
    if (s.empty()) return false;
    for (char c : s) {
        if (!isdigit(c)) return false;
    }
    return true; 
}

// Function to display cart
void displayCart(Member loggedInMember) {
	cin.ignore();
	loadProducts();
    if (loggedInMember.member_id.empty()) {
        cout << "Error: No user logged in." << endl;
        cout << "Press [ENTER] to continue.";
        cin.ignore();
        cin.get();
        return;
    }

    clearScreen();

    CartItem* cart = nullptr;
    int cartSize = 0;
    if (!loadCart(cart, cartSize, loggedInMember.member_id)) {
        cout << "Could not load cart data." << endl;
        cout << "Press [ENTER] to return.";
        cin.ignore();
        return;
    }

    if (cartSize == 0) {
        cout << "==================================================================" << endl;
        cout << "|                            MY CART                             |" << endl;
        cout << "==================================================================" << endl;
        cout << "|                                                                |" << endl;
        cout << "|                        Your cart is empty.                     |" << endl;
        cout << "|                                                                |" << endl;
        cout << "==================================================================" << endl;
        cout << "\n1. Return to product list" << endl;
        cout << "2. Return to main menu" << endl;

        while (true) {
            string choice;
            cout << "\nEnter your choice: ";
            getline(cin, choice);

            if (choice == "1") {
                clearScreen();
                filterProducts();
                return;
            } else if (choice == "2") {
                clearScreen();
                mainMenu();
                return;
            } else {
                cout << "Invalid choice. Please enter 1 or 2." << endl;
            }
        }
    }

    cout << "==================================================================" << endl;
    cout << "|                            MY CART                             |" << endl;
    cout << "==================================================================" << endl;
    double grand_total = 0.0;

    for (int i = 0; i < cartSize; i++) {
        string pid = cart[i].product_id;
        string name = cart[i].product_name;
        string category = cart[i].product.category;
        double price = cart[i].price;
        int quantity = cart[i].quantity;
        double total = cart[i].total;
        string status = cart[i].product.status;

        cout << " ----------------------------------------------------------------" << endl;
        cout << "| Item " << left << setw(58) << to_string(i+1) + ":" << "|" << endl;
        cout << "| Product ID : " << left << setw(50) << pid << "|" << endl;
        cout << "| Name       : " << left << setw(50) << name << "|" << endl;

        if (status == "Inactive") {
            total = 0.0;
            cout << "| SORRY! This product is currently unavailable :(                |" << endl;
            cout << " ----------------------------------------------------------------" << endl;
        } else {
            cout << "| Price      : RM " << left << setw(47) << fixed << setprecision(2) << price << "|" << endl;
            cout << "| Quantity   : " << left << setw(50) << quantity << "|" << endl;
            cout << "| Total      : RM " << left << setw(47) << fixed << setprecision(2) << total << "|" << endl;
            cout << " ----------------------------------------------------------------" << endl;
        }
        grand_total += total;
    }

    cout << "==================================================================" << endl;
    cout << "| Total Price: RM " << left << setw(47) << fixed << setprecision(2) << grand_total << "|" << endl;
    cout << "==================================================================\n" << endl;
    cout << "------------------------------------------------------------------" << endl;

    cout << " ____________________________________" << endl;
    cout << "|                                    |" << endl;
    cout << "|    Options:                        |" << endl;
    cout << "|  1. Delete an item from cart       |" << endl;
    cout << "|  2. Edit quantity of an item       |" << endl;
    cout << "|  3. Proceed to payment             |" << endl;
    cout << "|  4. Back to product list           |" << endl;
    cout << "|  5. Back to member menu            |" << endl;
    cout << "|____________________________________|" << endl;

    while (true) {
        string choice;
        cout << "\nEnter your choice: ";
        getline(cin, choice);

        if (choice == "1") {
            //delete cart function(cart, cartSize);
            break;
        } else if (choice == "2") {
            //edit cart function (cart, cartSize);
            break;
        } else if (choice == "3") {
            // proceed to payment function(cart, cartSize);
            break;
        } else if (choice == "4") {
            clearScreen();
            filterProducts();
            return;
        } else if (choice == "5") {
            clearScreen();
            memberMenu(loggedInMember);
            return;
        } else {
            cout << "Invalid choice. Press [ENTER] to retry." << endl;
            cin.ignore();
            cin.get();
            displayCart(loggedInMember);
        }
    }

    displayCart(loggedInMember);
}

void addToCart(const string& product_id, int quantity) {
    if (loggedInMember.member_id.empty()) {
        cout << "Error: Cannot add to cart. No user logged in." << endl;
        return;
    }

    if (!products || productCount == 0) {
        if (!loadProducts()) {
            cout << "Error: Could not load products." << endl;
            return;
        }
    }

    Product* selected_product = binarySearchProduct(products, 0, productCount - 1, product_id, "product_id");

    if (!selected_product) {
        cout << "Error: Product with ID " << product_id << " not found." << endl;
        return;
    }

    if (selected_product->status == "Inactive") {
        cout << "Error: This product is currently unavailable.\n" << endl;
        return;
    }

    if (quantity <= 0) {
        cout << "Error: Quantity must be positive." << endl;
        return;
    }

    if (selected_product->stock < quantity) {
        cout << "Error: Not enough stock for " << selected_product->product_name 
             << ". Available: " << selected_product->stock << endl;
        return;
    }

    CartItem* cart = nullptr;
    int cartSize = 0;
    if (!loadCart(cart, cartSize, loggedInMember.member_id)) {
        cout << "Error: Could not load current cart." << endl;
        return;
    }

    // Check if item is already in the cart
    bubbleSortCartItem(cart, cartSize, "product_id");
    CartItem* item = binarySearchCartItem(cart, 0, cartSize - 1, product_id, "product_id");

    if (item) {
        if (selected_product->stock < item->quantity + quantity) {
            cout << "Error: Adding " << quantity << " would exceed stock." << endl;
            delete[] cart;
            return;
        }
        item->quantity += quantity;
        item->total = item->quantity * item->price;
    } else {
        // Create new cart array with increased size
        CartItem* newCart = new CartItem[cartSize + 1];
        for (int i = 0; i < cartSize; i++) {
            newCart[i] = cart[i];
        }
        
        newCart[cartSize] = CartItem(
            *selected_product,
            selected_product->product_id,
            selected_product->product_name,
            selected_product->price,
            quantity,
            selected_product->price * quantity,
            selected_product->status
        );
        
        delete[] cart;
        cart = newCart;
        cartSize++;
    }

    selected_product->stock -= quantity;

    if (saveCart(cart, cartSize, loggedInMember.member_id) && updateProductFile()) {
        cout << "\nSuccessfully added " << quantity << " x " << selected_product->product_name << " to cart!" << endl;
        cin.ignore();
        cin.get();
        clearScreen();
        filterProducts();
    } else {
        // Revert stock if saving failed
        selected_product->stock += quantity;
        cout << "\nError: Could not save changes." << endl;
    }

    delete[] cart;
}

void filterProducts() {
    if (!loadProducts()) {
        cout << "Failed to load products." << endl;
        cout << "Press [ENTER] to return to main menu.";
        cin.ignore();
        cin.get();
        clearScreen();
        mainMenu();
        return;
    }

    while (true) {
        clearScreen();
        cout << "===============================================================" << endl;
        cout << "|                  WELCOME TO OUR PIZZA STORE!                |" << endl;
        cout << "===============================================================" << endl;
        cout << "| Select a category:                                          |" << endl;
        cout << "| 1. Pizza                                                    |" << endl;
        cout << "| 2. Side                                                     |" << endl;
        cout << "| 3. Beverage                                                 |" << endl;
        cout << "| 4. Back to Main Menu                                        |" << endl;
        cout << "===============================================================" << endl;

        int choice;
        cout << "Enter your choice : ";
        cin >> choice;
        
        if (choice == 4) {
            clearScreen();
            memberMenu(loggedInMember);
            return;
        }

        string categories[] = {"Pizza", "Side", "Beverage"};

        if (choice < 1 || choice > 4) {
            cout << "Invalid choice. Press [ENTER] to retry." << endl;
            cin.ignore();
            cin.get();
            filterProducts();
        }

        string selected_category = categories[choice - 1];

        while (true) {
            clearScreen();
            cout << "Products in Category: " << selected_category << endl;
            loadProducts();
            
            // Display products in this category
            bool found = false;
            for (int i = 0; i < productCount; i++) {
                if (products[i].category == selected_category && products[i].status == "Active") {
                    displayProduct(products[i]);
                    found = true;
                }
            }

            if (!found) {
                cout << "\nNo available products found in '" << selected_category << "' category." << endl;
            }

            cout << "\n-----------------------------------------------------------------" << endl;
            cout << " _________________________________" << endl;
            cout << "|                                 |" << endl;
            cout << "|    Options:                     |" << endl;
            cout << "| Enter Product ID to add to cart |" << endl;
            cout << "| [C] View Cart                   |" << endl;
            cout << "| [B] Back to Category Selection  |" << endl;
            cout << "| [M] Back to Main Menu           |" << endl;
            cout << "|_________________________________|" << endl;

            string selection;
            cout << "\nEnter your choice: ";
            cin >> selection;

            if (selection == "C" || selection == "c") {
                displayCart(loggedInMember);
                continue;
            } else if (selection == "B" || selection == "b") {
                break;
            } else if (selection == "M" || selection == "m") {
                clearScreen();
                memberMenu(loggedInMember);
                return;
            }

            string product_id = selection;
            Product* product = binarySearchProduct(products, 0, productCount - 1, product_id, "product_id");

            if (!product) {
                cout << "Product with ID '" << product_id << "' not found." << endl;
                cout << "Press [ENTER] to continue.";
                cin.ignore();
                cin.get();
                continue;
            }

            // Check if product is inactive
            if (product->status == "Inactive") {
                cout << "\nThis product is currently unavailable." << endl;
                cout << "Press [ENTER] to continue.";
                cin.ignore();
                cin.get();
                continue;
            }

            if (product->stock <= 0) {
                cout << "\nSorry, this product is out of stock!" << endl;
                cout << "Press [ENTER] to continue.";
                cin.ignore();
                cin.get();
                continue;
            }

            while (true) {
                cout << "\nEnter quantity (available: " << product->stock << "): ";
                string qtyStr;
                cin >> qtyStr;

                if (!isInteger(qtyStr)) {
                    cout << "Invalid input. Please enter a number." << endl;
                    continue;
                }

                int qty = stoi(qtyStr);
                if (qty <= 0) {
                    cout << "Quantity must be positive." << endl;
                } else if (qty > product->stock) {
                    cout << "Not enough stock available." << endl;
                } else {
                    addToCart(product_id, qty);
                    cout << "Press [ENTER] to continue.";
                    cin.ignore();
                    cin.get();
                    break;
                }
            }
        }
    }
}

void adminMenu(Admin loggedInAdmin){
	clearScreen();
        cout << "\n===============================================================" << endl;
        cout << "               WELCOME " << loggedInAdmin.full_name << endl;
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