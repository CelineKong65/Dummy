import os

# Constants
MEMBERS_FILE = "member.txt"
PRODUCT_FILE = "product.txt"
MEMBERS_ID_FILE = "member_id.txt"

# Structures
class Member:
    def __init__(self, full_name="", member_id="", email="", password="", age="", gender="" , contact=""):
        self.member_id = member_id
        self.full_name = full_name
        self.email = email
        self.password = password
        self.age = age
        self.gender = gender
        self.contact = contact
    
    def __str__(self):
        return f"{self.member_id}\n{self.full_name}\n{self.email}\n{self.password}\n{self.age}\n{self.gender}\n{self.contact}"

class Product:
    def __init__(self, product_id="", name="", category="", price=0.0, stock=0):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

class CartItem:
    def __init__(self, product=None, product_id="", name="", price=0.0, quantity=0, total=0.0):
        self.product = product if product else Product()
        self.product_id = product_id if product_id else (product.product_id if product else "")
        self.name = name if name else (product.name if product else "")
        self.price = price if price else (product.price if product else 0.0)
        self.quantity = quantity
        self.total = total if total else (self.price * quantity)

# Global variables
products = []
members = []
logged_in_member = ""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_members():
    global members
    try:
        with open(MEMBERS_FILE, "r", encoding='utf-8') as file:
            members = []
            data_lines = []
            for line in file:
                data_lines.append(line.strip())
                if len(data_lines) == 5:
                    member = Member.from_string(data_lines)
                    if member:
                        members.append(member)
                    data_lines = [] 
    except FileNotFoundError:
        open(MEMBERS_FILE, "w", encoding='utf-8').close()

def get_next_member_id():
    try:
        with open(MEMBERS_ID_FILE, "r", encoding='utf-8') as file:
            read_current_id = file.readlines()
            if read_current_id:
                last_id = read_current_id[-1].strip()
                last_id_number = int(last_id[1:])
                next_id_number = last_id_number + 1 
                next_id = f"U{next_id_number:04d}"
                return next_id
            else:
                return "U0001"
    except FileNotFoundError:
        with open(MEMBERS_ID_FILE, "w", encoding='utf-8') as file:
            file.write("U0001\n")
        return "U0001"

def save_member(member):
    with open(MEMBERS_FILE, "a", encoding='utf-8') as file:
        file.write(str(member) + "\n\n")

def signup():
    global logged_in_member 

    # Member id
    member_id = get_next_member_id()
    #Enter name
    full_name = input("Enter your full name: ")

    # Enter email
    while True:
        email = input("Enter your email (example: xuanting@example.com): ")
        if "@" not in email or "." not in email:
            print("Invalid email format. Please include @ and . in your email!")
            continue
        break

    # Enter password
    while True:
        password = ""
        password = input("Enter your new password (example: MyPass123): ")

        if len(password) < 8:
            print("Password must be at least 8 characters!")
            continue

        upper = False
        lower = False
        digit = False

        for char in password:
            if 'A' <= char <= 'Z':
                upper = True
            elif 'a' <= char <= 'z': 
                lower = True
            elif '0' <= char <= '9': 
                digit = True

        if not upper:
            print("Password must contain at least one uppercase letter!")
            continue
        if not lower:
            print("Password must contain at least one lowercase letter!")
            continue
        if not digit:
            print("Password must contain at least one digit!")
            continue
        
        confirm_password = input("Confrim your password: ")
        if confirm_password != password:
            print("Passwords do not match!")
            continue
    
        break

    # Enter age 
    while True:
        age = input("Enter your age: ")

        if len(age) != 2:
            print("Age must be exactly 2 digits!")
            continue

        is_digit = True
        for char in age:
            if char < '0' or char > '9':
                is_digit = False

        if not is_digit:
            print("Age must contain only digits!")
            continue

        if age[0] == '0':
            print("Age cannot start with 0!")
            continue

        break

    # Enter gender
    while True:
        gender = input("Enter your gender (male or female): ")

        is_valid= False

        if len(gender) == 4:
            if ((gender[0] == 'M' or gender[0] == 'm') and
                (gender[1] == 'a' or gender[1] == 'A') and
                (gender[2] == 'l' or gender[2] == 'L') and
                (gender[3] == 'e' or gender[3] == 'E')):
                is_valid = True

        elif len(gender) == 6:
            if ((gender[0] == 'F' or gender[0] == 'f') and
                (gender[1] == 'e' or gender[1] == 'E') and
                (gender[2] == 'm' or gender[2] == 'M') and
                (gender[3] == 'a' or gender[3] == 'A') and
                (gender[4] == 'l' or gender[4] == 'L') and
                (gender[5] == 'e' or gender[5] == 'E')):
                is_valid = True

        if not is_valid:
            print("Please enter 'Male', 'Female', 'male' or 'female'!")
            continue
        break

    # Enter contact number
    while True:
        contact = input("Enter your contact number (example: 012-34567890): ")
        clean_contact = ""
        for char in contact:
            if char != '-':
                clean_contact += char


        is_valid = True

        if contact[3] != '-':
            print("Format must with dash like 012-34567890!")
            continue

        if len(clean_contact) >= 2 and (clean_contact[0] != '0' or clean_contact[1] != '1'):
            print("Phone number must start with '01'!")
            is_valid = False
            continue

        if len(clean_contact) != 10 and len(clean_contact) != 11:
            print("Invalid phone number length. It must be exactly 11 digits!")
            is_valid = False
            continue

        for char in clean_contact:
            if char < '0' or char > '9':
                print("Phone number must contain only digits!")
                is_valid = False
    
        break
   
    if not all([full_name, password, confirm_password, email, age, gender, contact]):
        print("Error : All fields are required!")
    elif password != confirm_password:
        print("Error : Passwords do not match!")
    else:
        new_member = Member(full_name=full_name, member_id=member_id, email=email, password=password, age=age, gender=gender, contact=contact)
        members.append(new_member)

        with open(MEMBERS_ID_FILE, "a", encoding='utf-8') as file:
            file.write(member_id + "\n")
            
        save_member(new_member)
        print(f"Registration successful! Your Member ID: {member_id}")
        input("\nPress [ENTER] to login menu.")
        clear_screen()

def reset_pass(email): ##### reset pass save format got problem
    new_password = input("Enter your new password: ").strip()
    confirm_password = input("Confirm your new password: ").strip()
    
    if new_password != confirm_password:
        print("Error: Passwords do not match!")
        return False

    try:
        with open(MEMBERS_FILE, "r", encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() != ''] 

        for i in range(0, len(lines), 7):
            if lines[i + 2].strip() == email:
                lines[i + 3] = new_password + "\n"
                break
        else:
            print("Error: Email not found!")
            return False
        
        with open(MEMBERS_FILE, "w", encoding='utf-8') as f:
            f.writelines(lines)

        print("Password has been reset successfully.")
        input("\nPress [ENTER] back login menu.")
        clear_screen()
        return True
    
    except FileNotFoundError:
        print("Error: Members file not found!")
        return False

def login():
    global logged_in_member 
    
    email = input("\nEnter your email :").strip()
    password = input("Enter your password :").strip()

    try:
        with open(MEMBERS_FILE, "r", encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() != ''] 

        for i in range(0, len(lines), 7):  
            stored_email = lines[i + 2]
            stored_password = lines[i + 3]    

            if email == stored_email:
                for attempt in range(3):
                    if password == stored_password:
                        print("Logged in Successfully!")
                        logged_in_member = Member(
                            full_name=lines[i + 1],
                            member_id=lines[i],
                            email=lines[i + 2],
                            password=lines[i + 3],
                            age=lines[i + 4],
                            gender=lines[i + 5],
                            contact=lines[i + 6]
                        )
                        input("\nPress [ENTER] to continue.")
                        return main_menu()
                    else:
                        print(f"Incorrect password! Attempts left: {2 - attempt}")
                        password = input("Please enter your password again: ").strip()

                print("Too many incorrect password attempts.")
                if reset_pass(email):
                    logged_in_member = email
                    return True
                else:
                    print("Password reset failed. Returning to login.")
                    input("\nPress [ENTER] back login menu.")
                    clear_screen()
                    return False
                    
        print("Email not found.\n")
        input("\nPress [ENTER] to continue.")
        clear_screen()
        return False

    except FileNotFoundError:
        print("Error: Members file not found!")
        return False


def login_menu():
    global logged_in_member 

    while True:
        print("===============================================================")
        print("                   WELOCOME TO YESMOLAR BAKERY                 ")
        print("===============================================================")

        print("1.    Sign Up  ")
        print("2.    Login  ")
        print("3.    Admin Login  ")
        print("4.    Exit  ")

        print("===============================================================")

        choice = int(input("\nEnter your choice :"))

        if (choice == 1):
            signup()
        elif(choice == 2):
            if login():
                return
        elif(choice == 3):
            print("adminlogin")
            exit()
        elif(choice == 4):
            print("\nThank you for visiting Yesmolar Bakery!\n")
            exit()
        else:
            print("Invalid choice. Please try again.")
            input("\nPress [ENTER] to try again.")
            clear_screen()



def get_quoted_field(ss):
    field = ""
    ss = ss.strip()
    if not ss:
        return "", ""

    if ss.startswith('"'):
        ss = ss[1:]
        try:
            quote_end_index = ss.index('"')
            field = ss[:quote_end_index]
            ss = ss[quote_end_index + 1:]
            if ss.startswith(','):
                ss = ss[1:]
        except ValueError:
            field = ss
            ss = ""
    else:
        split = ss.split(',', 1)
        field = split[0]
        ss = split[1] if len(split) > 1 else ""

    return field.strip(), ss.strip()

def display_product(product):
    print("---------------------------------------------------------------")
    print(f"Product ID: {product.product_id}")
    print("---------------------------------------------------------------")
    print(f"| Name     : {product.name}")
    print(f"| Category : {product.category}")
    print(f"| Price    : RM {product.price:.2f}")

    if product.stock <= 0:
        print("| WARNING  : SORRY! THIS PRODUCT IS CURRENTLY OUT OF STOCK!")
    else:
        print(f"| Stock    : {product.stock}")
    print("---------------------------------------------------------------")

def load_products():
    global products
    products = []
    try:
        with open(PRODUCT_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                ss = line
                product = Product()

                product.product_id, ss = get_quoted_field(ss)
                product.name, ss = get_quoted_field(ss)
                product.category, ss = get_quoted_field(ss)
                price_str, ss = get_quoted_field(ss)
                stock_str, ss = get_quoted_field(ss)

                try:
                    product.price = float(price_str) if price_str else 0.0
                except ValueError:
                    print(f"Warning: Invalid price format '{price_str}'. Setting price to 0.0.")
                    product.price = 0.0

                try:
                    product.stock = int(stock_str) if stock_str else 0
                except ValueError:
                    print(f"Warning: Invalid stock format '{stock_str}'. Setting stock to 0.")
                    product.stock = 0

                products.append(product)
    except FileNotFoundError:
        print(f"Error: Product file '{PRODUCT_FILE}' not found!")
        return False
    except IOError as e:
        print(f"Error: Could not read the product file: {e}")
        return False
    return True

def update_product_file():
    global products
    try:
        with open(PRODUCT_FILE, 'w', encoding='utf-8') as file:
            for product in products:
                pid = f'"{product.product_id}"' if ',' in product.product_id else product.product_id
                name = f'"{product.name}"' if ',' in product.name else product.name
                category = f'"{product.category}"' if ',' in product.category else product.category
                price = str(product.price)
                stock = str(product.stock)

                file.write(f"{pid},{name},{category},{price},{stock}\n")
        return True
    except IOError as e:
        print(f"Error: Could not update the product file: {e}")
        return False

def load_cart(cart):
    if not logged_in_member:
        print("Error: Cannot load cart. No user logged in.")
        return False

    cart_file = f"{logged_in_member}_cart.txt"
    cart.clear()
    
    if not products and not load_products():
        print("Error: Failed to load products.")
        return False

    try:
        if not os.path.exists(cart_file) or os.path.getsize(cart_file) == 0:
            return True

        with open(cart_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(',')
                if len(parts) != 6:
                    continue

                item = CartItem()
                item.product_id = parts[1].strip()
                item.name = parts[2].strip()
                
                try:
                    item.price = float(parts[3].strip())
                    item.quantity = int(parts[4].strip())
                    item.total = float(parts[5].strip())
                except ValueError:
                    continue

                for p in products:
                    if p.product_id == item.product_id:
                        item.product = p
                        break

                cart.append(item)
    except IOError as e:
        print(f"Error reading cart file: {e}")
        return False
    return True

def save_cart(cart):
    if not logged_in_member:
        print("Error: Cannot save cart. No user logged in.")
        return False

    cart_file = f"{logged_in_member}_cart.txt"
    try:
        with open(cart_file, 'w', encoding='utf-8') as file:
            for item in cart:
                pid = item.product_id if item.product_id else (item.product.product_id if item.product else "")
                name = item.name if item.name else (item.product.name if item.product else "")
                price = item.price if item.price is not None else (item.product.price if item.product else 0.0)
                quantity = item.quantity
                total = item.total if item.total is not None else (price * quantity)

                file.write(f"{logged_in_member},{pid},{name},{price:.2f},{quantity},{total:.2f}\n")
        return True
    except IOError as e:
        print(f"Error: Could not update cart file: {e}")
        return False

def display_cart(cart):
    if not logged_in_member:
        print("Error: No user logged in.")
        input("Press [ENTER] to continue.")
        return

    clear_screen()

    if not load_cart(cart):
        print("Could not load cart data.")
        input("Press [ENTER] to return.")
        return

    if not cart:
        print("------------------------------------------------------------------")
        print("                              MY CART                             ")
        print("------------------------------------------------------------------")
        print("\n                          Your cart is empty.                   ")
        print("\n------------------------------------------------------------------")
        print("\n1. Return to product list")
        print("2. Return to main menu")

        while True:
            choice = input("\nEnter your choice: ")
            if choice == '1':
                clear_screen()
                filter_products()
                return
            elif choice == '2':
                clear_screen()
                main_menu()
                return
            else:
                print("Invalid choice. Please enter 1 or 2.")

    print("------------------------------------------------------------------")
    print("                              MY CART                             ")
    print("------------------------------------------------------------------")
    grand_total = 0.0

    for i, item in enumerate(cart, 1):
        pid = item.product_id if item.product_id else (item.product.product_id if item.product else "N/A")
        name = item.name if item.name else (item.product.name if item.product else "N/A")
        category = item.product.category if item.product and item.product.category else "N/A"
        price = item.price if item.price is not None else (item.product.price if item.product else 0.0)
        quantity = item.quantity
        total = item.total if item.total is not None else (price * quantity)

        print(f"Item {i}:")
        print(f"Product ID : {pid}")
        print(f"Name       : {name}")
        print(f"Category   : {category}")
        print(f"Price      : RM {price:.2f}")
        print(f"Quantity   : {quantity}")
        print(f"Total      : RM {total:.2f}")
        print("------------------------------------------------------------------")

        grand_total += total

    print(f"Total Price: RM {grand_total:.2f}")
    print("------------------------------------------------------------------")

    print("\n_____________________________________")
    print("|Options:                            |")
    print("|  1. Delete an item from cart       |")
    print("|  2. Edit quantity of an item       |")
    print("|  3. Proceed to payment             |")
    print("|  4. Back to product list           |")
    print("|  5. Back to main menu              |")
    print("|____________________________________|")

    while True:
        choice = input("\nEnter your choice: ")
        if choice == '1':
            break
        elif choice == '2':
            break
        elif choice == '3':
            break
        elif choice == '4':
            clear_screen()
            filter_products()
            return
        elif choice == '5':
            clear_screen()
            main_menu()
            return
        else:
            print("Invalid choice. Please try again.")

    display_cart(cart)

def add_to_cart(cart, product_id, quantity):
    if not logged_in_member:
        print("Error: Cannot add to cart. No user logged in.")
        return

    global products
    if not products and not load_products():
        print("Error: Could not load products.")
        return

    selected_product = None
    for p in products:
        if p.product_id == product_id:
            selected_product = p
            break

    if not selected_product:
        print(f"Error: Product with ID {product_id} not found.")
        return

    if quantity <= 0:
        print("Error: Quantity must be positive.")
        return

    if selected_product.stock < quantity:
        print(f"Error: Not enough stock for {selected_product.name}. Available: {selected_product.stock}")
        return

    if not load_cart(cart):
        print("Error: Could not load current cart.")
        return

    found = False
    for item in cart:
        if (item.product_id == product_id or 
            (item.product and item.product.product_id == product_id)):
            if selected_product.stock < item.quantity + quantity:
                print(f"Error: Adding {quantity} would exceed stock.")
                return
            item.quantity += quantity
            item.price = selected_product.price
            item.total = item.quantity * item.price
            found = True
            break

    if not found:
        cart.append(CartItem(
            product=selected_product,
            product_id=selected_product.product_id,
            name=selected_product.name,
            price=selected_product.price,
            quantity=quantity
        ))

    selected_product.stock -= quantity

    if save_cart(cart) and update_product_file():
        print(f"\nSuccessfully added {quantity} x {selected_product.name} to cart!")
    else:
        selected_product.stock += quantity
        print("\nError: Could not save changes.")

def filter_products():
    global products
    cart = []

    if not load_products():
        print("Failed to load products.")
        input("Press [ENTER] to return to main menu.")
        clear_screen()
        main_menu()
        return

    while True:
        clear_screen()
        print("===============================================================")
        print("                   WELCOME TO OUR PASTRY PAN!                  ")
        print("===============================================================")
        print("Select a category:")
        categories = {
            '1': 'Bread', '2': 'Pastries', '3': 'Cakes', '4': 'Donuts',
            '5': 'Cupcakes & Muffins', '6': 'Cookies', '7': 'Pies & Tarts',
            '8': 'Savories & Sandwiches'
        }
        for key, value in categories.items():
            print(f" [{key}] {value}")
        print(" [9] Back to Main Menu")
        print("===============================================================")

        choice = input("Enter your choice (1-9): ")
        if choice == '9':
            clear_screen()
            main_menu()
            return
        elif choice not in categories:
            print("Invalid choice. Please try again.")
            input("Press [ENTER] to continue.")
            continue

        selected_category = categories[choice]
        while True:
            clear_screen()
            print(f"===== Products in Category: {selected_category} =====")
            load_products()
            filtered = [p for p in products if p.category.lower() == selected_category.lower()]

            if not filtered:
                print(f"\nNo products found in '{selected_category}' category.")
            else:
                for product in filtered:
                    display_product(product)
            print("---------------------------------------------------------------")

            print("_____________________________________")
            print("|Options:                            |")
            print("| -> Enter Product ID to add to cart |")
            print("| -> [C] View Cart                   |")
            print("| -> [B] Back to Category Selection  |")
            print("| -> [M] Back to Main Menu           |")
            print("|____________________________________|")

            selection = input("\nEnter your choice: ").upper()

            if selection == 'C':
                display_cart(cart)
                continue
            elif selection == 'B':
                break
            elif selection == 'M':
                clear_screen()
                main_menu()
                return

            product_id = selection
            product = None
            for p in filtered:
                if p.product_id == product_id:
                    product = p
                    break

            if not product:
                print(f"\nProduct with ID '{product_id}' not found under this category.")
                input("Press [ENTER] to continue.")
                continue

            if product.stock <= 0:
                print("\nSorry, this product is out of stock!")
                input("Press [ENTER] to continue.")
                continue

            while True:
                try:
                    qty = int(input(f"\nEnter quantity (available: {product.stock}): "))
                    if qty <= 0:
                        print("Quantity must be positive.")
                    elif qty > product.stock:
                        print("Not enough stock available.")
                    else:
                        add_to_cart(cart, product_id, qty)
                        input("Press [ENTER] to continue.")
                        break
                except ValueError:
                    print("Invalid input. Please enter a number.")

def main_menu():
    global logged_in_member
    if not logged_in_member:
        print("Error: No user logged in.")
        return

    while True:
        clear_screen()
        print(f"Welcome {logged_in_member.full_name} ! ")
        print("===============================================================")
        print("                            Main Menu                          ")
        print("===============================================================")
        print(" [1] Browse Products")
        print(" [2] View My Cart")
        print(" [3] My Profile")
        print(" [4] Rate Our System")
        print(" [5] Log Out")
        print("===============================================================")

        choice = input("Enter your choice: ")

        if choice == '1':
            filter_products()
        elif choice == '2':
            cart = []
            display_cart(cart)
        elif choice == '3':
            return
        elif choice == '4':
            return
        elif choice == '5':
            input("\nPress [ENTER] to logout.")
            clear_screen()
            return login_menu()
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")

def main():
    global logged_in_member
    logged_in_member = None 

    if not os.path.exists(PRODUCT_FILE):
        print(f"Error: Product file '{PRODUCT_FILE}' not found.")
        input("Press [ENTER] to exit.")
        return
    
    login_menu()

    main_menu()
main()