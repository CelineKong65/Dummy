import os

# Constants
MEMBERS_FILE = "member.txt"
PRODUCT_FILE = "product.txt"

# Structures
class Member:
    def __init__(self, member_id="", username="", password="", contact=""):
        self.member_id = member_id
        self.username = username
        self.password = password
        self.contact = contact

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
        print("===============================================================")
        print(f"             Main Menu (Logged in as: {logged_in_member})     ")
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
            return
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")

def main():
    global logged_in_member
    logged_in_member = "guest"  # Default the member for testing
    
    if not os.path.exists(PRODUCT_FILE):
        print(f"Error: Product file '{PRODUCT_FILE}' not found.")
        input("Press [ENTER] to exit.")
        return

    main_menu()
main()