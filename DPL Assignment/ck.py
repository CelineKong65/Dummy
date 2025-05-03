ORDER_ID_FILE = os.path.join(SCRIPT_DIR, "order_id_counter.txt")




def is_integer(string):
    if string == "":
        return False
    for char in string:
        if char < '0' or char > '9':
            return False
    return True

def delete_cart(cart):
    while True:
        item_num_input = input("\nEnter item number to delete (or 0 to cancel): ").strip()

        if not is_integer(item_num_input):
            print("Invalid input. Please enter a number.")
            continue

        item_num = int(item_num_input)

        if item_num == 0:
            return False
        elif item_num < 1 or item_num > len(cart):
            print(f"Invalid item number. Please enter between 1 and {len(cart)}")
            continue
        else:
            break

    deleted_item = cart[item_num - 1]

    new_cart = cart[:item_num - 1] + cart[item_num:]

    for product in products:
        if product.product_id == deleted_item.product_id:
            product.stock += deleted_item.quantity
            break

    original_cart = cart[:]  

    cart[:] = new_cart  

    if save_cart(cart) and update_product_file():
        print(f"'{deleted_item.name}' removed from cart successfully!")
    else:
        cart[:] = original_cart  
        for product in products:
            if product.product_id == deleted_item.product_id:
                product.stock -= deleted_item.quantity
                break
        print("Failed to update cart. Changes reverted.")

    input("Press [ENTER] to continue.")
    return True

def edit_cart(cart):
    global logged_in_member
    if not logged_in_member:
        print("Error: No user logged in.")
        input("Press [ENTER] to continue.")
        return False

    if not load_cart(cart):
        print("Error: Could not load cart data.")
        input("Press [ENTER] to continue.")
        return False

    if not cart:
        print("Your cart is empty. Nothing to edit.")
        input("Press [ENTER] to continue.")
        return False

    while True:
        item_num_input = input("\nEnter item number to edit (or 0 to cancel): ").strip()

        if not is_integer(item_num_input):
            print("Invalid input. Please enter a number.")
            continue

        item_num = int(item_num_input)

        if item_num == 0:
            return False
        elif item_num < 1 or item_num > len(cart):
            print(f"Invalid item number. Please enter between 1 and {len(cart)}")
            continue
        else:
            break

    selected_item = cart[item_num - 1]
    product_id = selected_item.product_id if selected_item.product_id else (
        selected_item.product.product_id if selected_item.product else "")
    
    product = None
    for p in products:
        if p.product_id == product_id:
            product = p
            break

    if not product:
        print("Error: Product not found in inventory.")
        input("Press [ENTER] to continue.")
        return False

    while True:
        print(f"\nCurrent quantity: {selected_item.quantity}")
        print(f"Available stock: {product.stock + selected_item.quantity}")
        new_qty_input = input("Enter new quantity (or 0 to remove item): ").strip()

        if not is_integer(new_qty_input):
            print("Invalid input. Please enter a number.")
            continue

        new_qty = int(new_qty_input)

        if new_qty == 0:
            product.stock += selected_item.quantity
            cart[:] = cart[:item_num - 1] + cart[item_num:]
            
            if save_cart(cart) and update_product_file():
                print("Item removed from cart successfully!")
            else:
                product.stock -= selected_item.quantity
                cart.insert(item_num - 1, selected_item)
                print("Failed to update cart. Changes reverted.")
            break
        elif new_qty < 0:
            print("Quantity cannot be negative.")
            continue
        elif new_qty > (product.stock + selected_item.quantity):
            print(f"Not enough stock available. Maximum: {product.stock + selected_item.quantity}")
            continue
        else:
            diff = new_qty - selected_item.quantity
            
            product.stock -= diff
            selected_item.quantity = new_qty
            selected_item.total = selected_item.price * new_qty
            
            if save_cart(cart) and update_product_file():
                print("Cart updated successfully!")
            else:
                product.stock += diff
                selected_item.quantity -= diff
                selected_item.total = selected_item.price * (selected_item.quantity - diff)
                print("Failed to update cart. Changes reverted.")
            break

    input("Press [ENTER] to continue.")
    return True

def clear_cart(member_id):
    cart_file = get_cart_filename(member_id)
    try:
        with open(cart_file, "w", encoding='utf-8') as file:
            file.write("") 
        return True
    except IOError as e:
        print(f"Error clearing cart file: {e}")
        return False

def proceed_to_payment(products, cart):
    if not cart:
        print("Your cart is empty. Please add items to your cart before proceeding to payment.")
        return

    clear_screen()
    total_payment = 0.00
    
    print("------------------------------------------------------------------")
    print("                              RECEIPT                             ")
    
    for i in range(len(cart)):
        print("------------------------------------------------------------------")
        print(f"Title    : {cart[i].product.name}")
        print(f"Price    : RM {cart[i].price:.2f}")
        print(f"Quantity : {cart[i].quantity}")
        print(f"Total    : RM {cart[i].total:.2f}")
        
        total_payment += cart[i].total

    print("==================================================================")
    print(f"Payment Amount: RM {total_payment:.2f}")
    print("==================================================================")
    
    if logged_in_member:
        if total_payment >= 100 and total_payment < 120:
            add_on = 0.00
            proceed = ''
            add_on = 120 - total_payment
            print(f"\nAdd-on RM {add_on:.2f} to get 5% discount!")
            proceed = input("\nEnter [0] to back to product list, enter [1] to proceed the payment: ").strip()
            
            while proceed != '0' and proceed != '1':
                print("Invalid input.")
                proceed = input("Enter 0 to back to product list, 1 to continue proceed to payment: ").strip()
            
            if proceed == '0':
                filter_products(products, cart)
                return
        
        if total_payment >= 120:
            discount = 0.05
            discount_amount = total_payment * discount
            total_payment -= discount_amount
            print("\nCongratulations, you get 5% discount!")
            print("_________________________")
            print(f"|Discount: RM {discount_amount:.2f}\t|")
            print(f"|Total   : RM {total_payment:.2f}\t|")
            print("|_______________________|")
    
    payment_method = ''
    print("\nChoose your payment method")
    print("1. Cash")
    print("2. Debit card")
    
    payment_method = input("\nYour choice [0 to cancel payment]: ").strip()
    
    while payment_method != '0' and payment_method != '1' and payment_method != '2':
        payment_method = input("Invalid choice. Please enter again: ").strip()
    
    if payment_method == '0':
        print("Back to main menu...")
        input()
        clear_screen()
        main_menu()
    elif payment_method == '1':
        cash_payment(products, cart, total_payment)
    elif payment_method == '2':
        debit_card_payment(cart, total_payment)

def debit_card_payment(cart, total_payment):
    card_number = input("Credit card number (13-16 digits): ").strip()
    
    while not is_valid_card_number(card_number):
        card_number = input("\nInvalid number. Please re-enter credit card number (13-16 digits): ").strip()
    
    expiry_date = input("\nExpiry date (MM/YY): ").strip()
    
    while not is_valid_expiry_date(expiry_date):
        expiry_date = input("\nInvalid date. Please re-enter expiry date (MM/YY): ").strip()
    
    cvv = input("\nCVV: ").strip()
    
    while not is_valid_cvv(cvv):
        cvv = input("\nInvalid CVV. Please re-enter CVV (3 or 4 digits): ").strip()

    print("\n\nProcessing payment...")
    print("\nValidating card details")
    
    print("\n\nPayment successful! Thank you for your purchase.")
    
    purchase_history(cart, total_payment)

    cart.clear()
    clear_cart(logged_in_member.member_id)
    
    try:
        with open(f"{logged_in_member.member_id}_cart.txt", "w") as output_file:
            pass
    except:
        print("Error: Could not open the cart file for writing!")
        return
    
    print("\nYour cart has been cleared.")
    more_purchase = input("\nDo you want to make more purchase[Y/N]?: ").strip()
    
    if more_purchase == 'Y' or more_purchase == 'y':
        print("\nPress [ENTER] to continue...")
        input()
        clear_screen()
        main_menu()
    elif more_purchase == 'N'or more_purchase == 'n':
        print("\nPress [ENTER] to log out...")
        input()
        clear_screen()
        login_menu()

def cash_payment(products, cart, total_payment):
    cash = 0.0

    cash = float(input("\nCash  : RM "))
    
    while cash < total_payment:
        print("Your cash is not enough!")
        cash = float(input("\nCash  : RM "))
    
    if cash > total_payment:
        change = cash - total_payment
        print(f"Change: RM {change:.2f}")
    
    print("\n\nProcessing payment", end='')
    
    print("\nPayment successful! Thank you for your purchase.")
    
    purchase_history(cart, total_payment)

    cart.clear()
    clear_cart(logged_in_member.member_id)
    
    print("\nYour cart has been cleared.")
    more_purchase = input("\nDo you want to make more purchase[Y/N]?: ").strip()
    
    if more_purchase == 'Y' or more_purchase == 'y':
        print("\nPress [ENTER] to continue...")
        input()
        clear_screen()
        main_menu()
    elif more_purchase == 'N' or more_purchase == 'n':
        print("\nPress [ENTER] to log out...")
        input()
        clear_screen()
        login_menu()

def is_valid_card_number(card_number):
    length = len(card_number)
    if length < 13 or length > 16:
        return False
    
    for char in card_number:
        if char < '0' or char > '9':
            return False
    
    return True

def is_valid_expiry_date(expiry_date):
    if len(expiry_date) != 5 or expiry_date[2] != '/':
        return False
    
    month = 0
    for i in range(2):
        char = expiry_date[i]
        if char < '0' or char > '9':
            return False 
        month = month * 10 + (ord(char) - ord('0')) 
    
    if month < 1 or month > 12:
        return False
    
    import time
    now = time.localtime()
    current_year = now.tm_year
    current_month = now.tm_mon
    
    year = 0
    for i in range(3, 5):
        char = expiry_date[i]
        if char < '0' or char > '9':
            return False 
        year = year * 10 + (ord(char) - ord('0')) 
    
    expiry_year = 2000 + year
    
    if expiry_year < current_year or (expiry_year == current_year and month < current_month):
        return False
    
    return True

def is_valid_cvv(cvv):
    length = len(cvv)
    if length != 3 and length != 4:
        return False
    
    for char in cvv:
        if char < '0' or char > '9':
            return False
    
    return True

def purchase_history(cart, total_payment):
    global logged_in_member
    
    if not logged_in_member:
        print("Error: No member logged in to record purchase history.")
        return False
    
    if not cart:
        print("Error: Cart is empty. No purchase to record.")
        return False
    
    try:
        from datetime import datetime
        purchase_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order_id = get_order_id()

        with open(PURCHASE_HISTORY_FILE, "a", encoding="utf-8") as file:
            file.write(f"{logged_in_member.member_id},{logged_in_member.full_name},{order_id},{purchase_time}\n")

            for item in cart:
                product_id = item.product_id if item.product_id else (item.product.product_id if item.product else "")
                name = item.name if item.name else (item.product.name if item.product else "")
                category = item.product.category if item.product else ""
                price = item.price if item.price is not None else (item.product.price if item.product else 0.0)
                quantity = item.quantity
                total = item.total if item.total is not None else (price * quantity)
                
                file.write(f"{logged_in_member.member_id},{logged_in_member.full_name},{order_id},{product_id},{name},{category},{price:.2f},{quantity},{total:.2f}\n")
            
            file.write(f"{logged_in_member.member_id},{logged_in_member.full_name},{order_id},TOTAL,{total_payment:.2f}\n\n")
        
        return True
    
    except Exception as e:
        print(f"Error recording purchase history: {e}")
        return False

def get_order_id():
    try:
        with open(ORDER_ID_FILE, "r", encoding='utf-8') as file:
            current_id = file.read().strip()
            if current_id:
                next_id = int(current_id) + 1
            else:
                next_id = 1
    except FileNotFoundError:
        next_id = 1
    
    with open(ORDER_ID_FILE, "w", encoding='utf-8') as file:
        file.write(str(next_id))
    
    return f"ORD{next_id:04d}"

def view_purchase_history():
    global logged_in_member
    
    if not logged_in_member:
        print("Error: No member logged in to view purchase history.")
        input("Press [ENTER] to continue.")
        return
    
    try:
        clear_screen()
        print("------------------------------------------------------------------")
        print("                      YOUR PURCHASE HISTORY                      ")
        print("==================================================================")
        
        with open(PURCHASE_HISTORY_FILE, "r", encoding="utf-8") as file:
            content = file.read()
        
        records = content.strip().split("\n\n")
        found = False
        
        for record in records:
            if not record.strip():
                continue
                
            lines = record.strip().split("\n")
            if len(lines) < 2:
                continue
                
            header = lines[0].split(',')
            if len(header) < 4:
                continue
                
            member_id = header[0]
            if member_id != logged_in_member.member_id:
                continue
                
            found = True
            order_id = header[2]
            purchase_time = header[3]
            
            print(f"Purchase Time: {purchase_time}")
            print("------------------------------------------------------------------")
            
            total_payment = 0.0
            items = []
            
            for line in lines[1:-1]:
                parts = line.split(',')
                if len(parts) < 9:
                    continue
                    
                product_id = parts[3]
                name = parts[4]
                category = parts[5]
                price = float(parts[6])
                quantity = int(parts[7])
                total = float(parts[8])
                
                print(f"Product ID : {product_id}")
                print(f"Name       : {name}")
                print(f"Category   : {category}")
                print(f"Price      : RM {price:.2f}")
                print(f"Quantity   : {quantity}")
                print(f"Total      : RM {total:.2f}")
                print("------------------------------------------------------------------")
                
                items.append((name, price, quantity, total))
                total_payment += total
            
            # Get the actual total from the last line
            total_line = lines[-1].split(',')
            if len(total_line) >= 5 and total_line[3] == "TOTAL":
                total_payment = float(total_line[4])
            
            print(f"Total Purchase: RM {total_payment:.2f}")
            print("==================================================================\n")
        
        if not found:
            print("No purchase history found for your account.")
        
        input("\nPress [ENTER] to return to main menu.")
        clear_screen()
        main_menu()
    
    except FileNotFoundError:
        print("No purchase history found.")
        input("Press [ENTER] to continue.")
        clear_screen()
        main_menu()
    except Exception as e:
        print(f"Error viewing purchase history: {e}")
        input("Press [ENTER] to continue.")