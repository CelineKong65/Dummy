import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define file paths
PRODUCT_FILE = os.path.join(SCRIPT_DIR, "product.txt")
MEMBERS_FILE = os.path.join(SCRIPT_DIR, "member.txt")
MEMBERS_ID_FILE = os.path.join(SCRIPT_DIR, "member_id.txt")
ADMINS_FILE = os.path.join(SCRIPT_DIR, "admin.txt")
PURCHASE_HISTORY_FILE = os.path.join(SCRIPT_DIR, "purchase_history.txt")  
ORDER_ID_FILE = os.path.join(SCRIPT_DIR, "order_id_counter.txt")
RATING_FILE = os.path.join(SCRIPT_DIR, "rating.txt") 

# Structures
class Member:
    def __init__(self, full_name="", member_id="", email="", password="", age="", gender="" , contact="", status="Active"):
        self.member_id = member_id
        self.full_name = full_name
        self.email = email
        self.password = password
        self.age = age
        self.gender = gender
        self.contact = contact
        self.status = status
    
    def __str__(self):
        return f"{self.member_id}\n{self.full_name}\n{self.email}\n{self.password}\n{self.age}\n{self.gender}\n{self.contact}\n{self.status}"
    
class Admin:
    def __init__(self, name="", password="", contact="", position="admin", status="Active"):
        allowed_positions = ["admin", "superadmin"]
        if position not in allowed_positions:
            raise ValueError(f"Invalid position: {position}. Must be 'admin' or 'superadmin'.")
        
        self.name = name
        self.password = password
        self.contact = contact
        self.position = position
        self.status = status

    def __str__(self):
        return f"{self.name}\n{self.password}\n{self.contact}\n{self.position}\n{self.status}"

class Product:
    def __init__(self, product_id="", name="", category="", price=0.0, stock=0, status=""):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.status = status

class CartItem:
    def __init__(self, product=None, product_id="", name="", price=0.0, quantity=0, total=0.0, status=""):
        self.product = product if product else Product()
        self.product_id = product_id if product_id else (product.product_id if product else "")
        self.name = name if name else (product.name if product else "")
        self.price = price if price else (product.price if product else 0.0)
        self.quantity = quantity
        self.total = total if total else (self.price * quantity)
        self.status = status if status else (product.status if product else "")

# Global variables
products = []
members = []
admins = []
logged_in_member = ""
logged_in_admin = ""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_members():
    global members
    try:
        with open(MEMBERS_FILE, "r", encoding='utf-8') as file:
            members = []
            data_lines = []
            for line in file:
                line = line.strip()
                if line != "":
                    data_lines.append(line)

                if len(data_lines) == 8:
                    member = Member(
                        member_id=data_lines[0],
                        full_name=data_lines[1],
                        email=data_lines[2],
                        password=data_lines[3],
                        age=data_lines[4],
                        gender=data_lines[5],
                        contact=data_lines[6],
                        status=data_lines[7]
                    )
                    members.append(member)
                    data_lines = []
    except FileNotFoundError:
        open(MEMBERS_FILE, "w", encoding='utf-8').close()

def load_admins():
    global admins
    admins = []
    try:
        with open(ADMINS_FILE, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
            
            i = 0
            while i < len(lines):
                if i + 4 < len(lines):
                    admin = Admin(
                        name=lines[i],
                        password=lines[i+1],
                        contact=lines[i+2],
                        position=lines[i+3],
                        status=lines[i+4]
                    )
                    admins.append(admin)
                    i += 5
                else:
                    i += 1
    except FileNotFoundError:
        open(ADMINS_FILE, "w", encoding="utf-8").close()

def get_next_member_id():
    try:
        with open(MEMBERS_ID_FILE, "r", encoding='utf-8') as file:
            read_current_id = file.read().splitlines()
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
    with open(MEMBERS_FILE, "a+", encoding='utf-8') as file:
        file.seek(0)
        
        content = file.read()
        if content and not content.endswith('\n'):
            file.write("\n") 
        
        file.write("\n")
        file.write(member.member_id + "\n")
        file.write(member.full_name + "\n")
        file.write(member.email + "\n")
        file.write(member.password + "\n")
        file.write(member.age + "\n")
        file.write(member.gender + "\n")
        file.write(member.contact + "\n")
        file.write(member.status + "\n") 


def signup():
    global logged_in_member 

    member_id = get_next_member_id()
    status = "Active"
    
    while True:
        full_name = input("Enter your full name, [R] to return to the main menu :").strip()

        if full_name == 'R' or full_name == 'r':
            clear_screen()
            return main_menu()

        valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
        is_valid = True

        for char in full_name:
            if char not in valid_chars:
                is_valid = False
                break

        name_only = ""
        for char in full_name:
            if char != ' ':
                name_only += char

        if not is_valid or len(name_only) < 2:
            print("Invalid name. Name must have at least 2 letters and contain only letters and spaces.")
            continue

        same = False
        for member in members:
            stored_name = member.full_name

            if len(stored_name) == len(full_name):
                match = True
                for i in range(len(full_name)):
                    if full_name[i] != stored_name[i]:
                        match = False
                        break
                if match:
                    same = True
                    break

        if same:
            print("This name is already registered. Please use a different name!")
            continue

        break 

    while True:
        email = input("Enter your email (example: xuanting@example.com): ")

        clean_email = ""
        
        at = False
        dot = False
        for char in email:
            if char != ' ' and char != '\n':
                clean_email += char
            if char == '@':
                at = True
            if char == '.':
                dot = True

        if not at or not dot:
            print("Invalid email format. Please include @ and . in your email!")
            continue

        same = False
        for member in members:
            stored_email = member.email

            if len(stored_email) == len(email):
                match = True
                for i in range(len(email)):
                    if email[i] != stored_email[i]:
                        match = False
                        break
                if match:
                    same = True
                    break

        if same:
            print("This email is already registered. Please use a different email!")
            continue
        
        break

    while True:
        password = ""
        password = input("Enter your new password (example: Xuanting123): ")

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

    while True:
        contact = input("Enter your contact number (example: 012-34567890): ")

        if len(contact) < 4 or contact[3] != '-':
            print("Format must be like 012-34567890 with a dash at the 4th position!")
            continue

        part1 = ""
        part2 = ""
        for i in range(len(contact)):
            if i < 3:
                part1 += contact[i]
            elif i > 3:
                part2 += contact[i]


        if not (part1[0] == '0' and part1[1] == '1'):
            print("Phone number must start with '01'!")
            continue

        combined = part1 + part2
        only_digits = True
        for c in combined:
            if not ('0' <= c <= '9'):
                only_digits = False
                break
        if not only_digits:
            print("Phone number cannot contain symbols or space!")
            continue

        if len(combined) != 10 and len(combined) != 11:
            print("Phone number must be 10 or 11 digits!")
            continue
    
        break
   
    if not all([full_name, password, confirm_password, email, age, gender, contact]):
        print("Error : All fields are required!")
    elif password != confirm_password:
        print("Error : Passwords do not match!")
    else:
        new_member = Member(full_name=full_name, member_id=member_id, email=email, password=password, age=age, gender=gender, contact=contact,status=status)
        members.append(new_member)

        with open(MEMBERS_ID_FILE, "a+", encoding='utf-8') as file:
            file.seek(0)

            content = ""
            while True:
                c = file.read(1)
                if not c:
                    break
                content += c

            if len(content) == 0 or content[-1] != '\n':
                file.write("\n")

            for ch in member_id:
                file.write(ch)
            file.write("\n")
            
        save_member(new_member)
        print(f"Registration successful! Your Member ID: {member_id}")
        input("\nPress [ENTER] to return to login menu.")
        clear_screen()

def to_lower_case(s):
    result = ""
    for char in s:
        if 'A' <= char <= 'Z':
            result += chr(ord(char) + 32)
        else:
            result += char
    return result

def login():
    global logged_in_member 
    
    email = input("\nEnter your email, [R] to return to the main menu: ").strip()

    if email == 'R' or email == 'r':
        clear_screen()
        main_menu()
        return
    
    password = input("Enter your password :").strip()

    try:
        with open(MEMBERS_FILE, "r", encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() != ''] 

        for i in range(0, len(lines), 8):  
            stored_email = lines[i + 2]
            stored_password = lines[i + 3]
            status = lines[i + 7]

            if email == stored_email:
                if to_lower_case(status) != "active":
                    print("Your account is inactive. Please contact admin.")
                    input("\nPress [ENTER] to return to login menu.")
                    clear_screen()
                    return False
                
                attempts = 0
                while attempts < 3:
                    if password == stored_password:
                        print("Logged in Successfully!")
                        logged_in_member = Member(
                            full_name=lines[i + 1],
                            member_id=lines[i],
                            email=lines[i + 2],
                            password=lines[i + 3],
                            age=lines[i + 4],
                            gender=lines[i + 5],
                            contact=lines[i + 6],
                            status=lines[i + 7]
                        )
                        input("\nPress [ENTER] to continue.")
                        return main_menu()
                    else:
                        attempts += 1
                        print(f"Incorrect password! Attempts left: {3 - attempts}")
                        password = input("Please enter your password again: ").strip()

                print("Too many failed attempts. Login terminating.")
                input("\nPress [ENTER] to return to login menu.")
                clear_screen()
                return False
                    
        print("Email not found.\n")
        input("\nPress [ENTER] to continue.")
        clear_screen()
        return False

    except FileNotFoundError:
        print("Error: Members file not found!")
        return False

def update_member(updated_member):
    try:
        with open(MEMBERS_FILE, "r", encoding='utf-8') as file:
            content = file.read().strip()

        members = content.split("\n\n")

        updated_members = []

        for member_data in members:
            fields = member_data.splitlines()

            if fields and fields[0] == updated_member.member_id:
                new_member_data = [
                    updated_member.member_id,
                    updated_member.full_name,
                    updated_member.email,
                    updated_member.password,
                    str(updated_member.age),
                    updated_member.gender,
                    updated_member.contact,
                    updated_member.status,
                ]
                updated_members.append("\n".join(new_member_data))
            else:
                updated_members.append(member_data)

        new_content = "\n\n".join(updated_members)

        with open(MEMBERS_FILE, "w", encoding='utf-8') as file:
            file.write(new_content)

    except FileNotFoundError:
        print("Member file not found.")
    except Exception as e:
        print(f"An error occurred while updating member: {e}")
    
def member_profile():
    global logged_in_member 

    clear_screen()

    while True:
        print("------------------------------------------------------------------")
        print("|                         YOUR PROFILE                           |")
        print("------------------------------------------------------------------")
        print(f"| 1. Member ID         : {logged_in_member.member_id:<40}|")
        print(f"| 2. Full Name         : {logged_in_member.full_name:<40}|")
        print(f"| 3. Email             : {logged_in_member.email:<40}|")
        print(f"| 4. Password          : {logged_in_member.password:<40}|")
        print(f"| 5. Age               : {logged_in_member.age:<40}|")
        print(f"| 6. Gender            : {logged_in_member.gender:<40}|")
        print(f"| 7. Contact Number    : {logged_in_member.contact:<40}|")
        print("------------------------------------------------------------------")

        choice = input("\nDo you want to edit your profile? (Y/N) : ")

        if choice == "Y" or choice == "y" or choice == "yes":
            edit_member_profile()
        elif choice == "N" or choice == "n" or choice == "no":
            input("Press [Enter] to return to the main menu.")
            clear_screen()
            return main_menu()
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")
            clear_screen()

def edit_member_profile():
    global logged_in_member 
    load_members()

    while True:
        clear_screen()
        print("------------------------------------------------------------------")
        print("|                       EDIT YOUR PROFILE                        |")
        print("------------------------------------------------------------------")
        print("| 1. Member ID (Not Editable)                                    |")
        print("| 2. Full Name                                                   |")
        print("| 3. Email                                                       |")
        print("| 4. Password                                                    |")
        print("| 5. Age                                                         |")
        print("| 6. Gender                                                      |")
        print("| 7. Contact Number                                              |")
        print("| 8. Return to Profile Menu                                      |")
        print("------------------------------------------------------------------")

        choice = input("\nSelect the number you want to edit (1-8): ")

        if choice == "1":
            input("\nMember ID cannot be edited. Press [ENTER] to continue.")

        elif choice == "2":
            while True:
                new_name = input("Enter new Full Name: ")

                letter_count = 0
                is_valid = True
                for char in new_name:
                    if not (
                        ('A' <= char <= 'Z') or
                        ('a' <= char <= 'z') or
                        char == ' '
                    ):
                        is_valid = False
                        break
                    if char != ' ':
                        letter_count += 1

                if not is_valid or letter_count < 2:
                    print("Invalid name. Must contain only letters and spaces, with at least 2 letters.")
                    continue

                cleaned_new_name = ""
                for char in new_name:
                    if char != ' ':
                        if 'A' <= char <= 'Z':
                            cleaned_new_name += chr(ord(char) + 32)
                        else:
                            cleaned_new_name += char

                name_exists = False
                for member in members:
                    if member.member_id == logged_in_member.member_id:
                        continue

                    cleaned_existing = ""
                    for char in member.full_name:
                        if char != ' ':
                            if 'A' <= char <= 'Z':
                                cleaned_existing += chr(ord(char) + 32)
                            else:
                                cleaned_existing += char

                    if cleaned_existing == cleaned_new_name:
                        name_exists = True
                        break

                if name_exists:
                    print("This name is already registered. Please use a different name!")
                    continue

                logged_in_member.full_name = new_name
                update_member(logged_in_member)
                print("Full Name updated successfully!")
                input("Press [ENTER] to continue.")
                break

        elif choice == "3":
            while True:
                new_email = input("Enter new email: ")

                has_at = False
                has_dot = False
                for char in new_email:
                    if char == '@':
                        has_at = True
                    if char == '.':
                        has_dot = True

                if not has_at or not has_dot:
                    print("Invalid email format. Must contain @ and .")
                    continue

                cleaned_new_email = ""
                for char in new_email:
                    if char != ' ':
                        if 'A' <= char <= 'Z':
                            cleaned_new_email += chr(ord(char) + 32)
                        else:
                            cleaned_new_email += char

                email_exists = False
                for member in members:
                    if member.member_id == logged_in_member.member_id:
                        continue

                    cleaned_existing = ""
                    for char in member.email:
                        if char != ' ':
                            if 'A' <= char <= 'Z':
                                cleaned_existing += chr(ord(char) + 32)
                            else:
                                cleaned_existing += char

                    if cleaned_existing == cleaned_new_email:
                        email_exists = True
                        break

                if email_exists:
                    print("This email is already registered. Please use a different email!")
                    continue

                logged_in_member.email = new_email
                update_member(logged_in_member)
                print("Email updated successfully!")
                input("Press [ENTER] to continue.")
                break

        elif choice == "4":
            while True:
                logged_in_member.password = ""
                logged_in_member.password = input("Enter your new password (example: Xuanting123): ")

                if len(logged_in_member.password) < 8:
                    print("Password must be at least 8 characters!")
                    continue

                upper = False
                lower = False
                digit = False

                for char in logged_in_member.password:
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
                if confirm_password != logged_in_member.password:
                    print("Passwords do not match!")
                    continue
            
                update_member(logged_in_member)
                print("Password updated successfully!")
                input("Press [ENTER] to continue.")
                break

        elif choice == "5":
            try:
                while True:
                    logged_in_member.age = input("Enter new age: ")

                    if len(logged_in_member.age) != 2:
                        print("Age must be exactly 2 digits!")
                        continue

                    is_digit = True
                    for char in logged_in_member.age:
                        if char < '0' or char > '9':
                            is_digit = False

                    if not is_digit:
                        print("Age must contain only digits!")
                        continue

                    if logged_in_member.age[0] == '0':
                        print("Age cannot start with 0!")
                        continue

                    update_member(logged_in_member)
                    print("Age updated successfully!")
                    break
            except ValueError:
                print("Invalid input! Age must be a number.")
            input("Press [ENTER] to continue.")

        elif choice == "6":
            while True:
                logged_in_member.gender = input("Enter new gender (male or female): ")

                is_valid= False

                if len(logged_in_member.gender) == 4:
                    if ((logged_in_member.gender[0] == 'M' or logged_in_member.gender[0] == 'm') and
                        (logged_in_member.gender[1] == 'a' or logged_in_member.gender[1] == 'A') and
                        (logged_in_member.gender[2] == 'l' or logged_in_member.gender[2] == 'L') and
                        (logged_in_member.gender[3] == 'e' or logged_in_member.gender[3] == 'E')):
                        is_valid = True

                elif len(logged_in_member.gender) == 6:
                    if ((logged_in_member.gender[0] == 'F' or logged_in_member.gender[0] == 'f') and
                        (logged_in_member.gender[1] == 'e' or logged_in_member.gender[1] == 'E') and
                        (logged_in_member.gender[2] == 'm' or logged_in_member.gender[2] == 'M') and
                        (logged_in_member.gender[3] == 'a' or logged_in_member.gender[3] == 'A') and
                        (logged_in_member.gender[4] == 'l' or logged_in_member.gender[4] == 'L') and
                        (logged_in_member.gender[5] == 'e' or logged_in_member.gender[5] == 'E')):
                        is_valid = True

                if not is_valid:
                    print("Please enter 'Male', 'Female', 'male' or 'female'!")
                    continue

                update_member(logged_in_member)
                print("Gender updated successfully!")
                input("Press [ENTER] to continue.")
                break

        elif choice == "7":
            while True:
                logged_in_member.contact  = input("Enter your contact number (example: 012-34567890): ")

                if len(logged_in_member.contact) < 4 or logged_in_member.contact[3] != '-':
                    print("Format must be like 012-34567890 with a dash at the 4th position!")
                    continue

                part1 = ""
                part2 = ""
                for i in range(len(logged_in_member.contact)):
                    if i < 3:
                        part1 += logged_in_member.contact[i]
                    elif i > 3:
                        part2 += logged_in_member.contact[i]


                if not (part1[0] == '0' and part1[1] == '1'):
                    print("Phone number must start with '01'!")
                    continue

                combined = part1 + part2
                only_digits = True
                for c in combined:
                    if not ('0' <= c <= '9'):
                        only_digits = False
                        break
                if not only_digits:
                    print("Phone number cannot contain symbols or space!")
                    continue

                if len(combined) != 10 and len(combined) != 11:
                    print("Phone number must be 10 or 11 digits!")
                    continue
    
                update_member(logged_in_member)
                print("Contact Number updated successfully!")
                input("Press [ENTER] to continue.")
                break
        
        elif choice == "8":
            input("\nPress [ENTER] to return to your profile.")
            clear_screen()
            return member_profile()
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")
            clear_screen()

def admin_login():
    global logged_in_admin

    name = input("\nEnter your name, [R] to return to the main menu:").strip()

    if name == 'R' or name == 'r':
        clear_screen()
        main_menu()
        return
    
    password = input("Enter your password :").strip()

    try:
        with open(ADMINS_FILE, "r", encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() != ''] 

        for i in range(0, len(lines), 5):  
            stored_name = lines[i]
            stored_password = lines[i + 1]
            stored_position = lines[i + 3]
            status = lines[i + 4]

            if name == stored_name:
                if to_lower_case(status) != "active":
                    print("Your account is inactive. Please contact superadmin.")
                    input("\nPress [ENTER] to return to login menu.")
                    clear_screen()
                    return False
                
                attempts = 0
                while attempts < 3:
                    if password == stored_password:
                        print("Logged in Successfully!")
                        print(f"Welcome {stored_position}!\n")
                        logged_in_admin = Admin(
                            name=lines[i],
                            password=lines[i + 1],
                            contact=lines[i + 2],
                            position=lines[i + 3],
                            status=lines[i + 4]
                        )
                        input("\nPress [ENTER] to continue.")
                        clear_screen()
                        return admin_menu()
                        
                    else:
                        attempts += 1
                        print(f"Incorrect password! Attempts left: {3 - attempts}")
                        password = input("Please enter your password again: ").strip()

                print("Too many failed attempts. Login terminating.")
                input("\nPress [ENTER] to return to login menu.")
                clear_screen()
                return False

        print("Name not found.\n")
        input("\nPress [ENTER] to continue.")
        clear_screen()
        return False

    except FileNotFoundError:
        print("Error: Admins file not found!")
        return False
    
def update_admin(updated_admin, original_name):
    try:
        with open(ADMINS_FILE, "r", encoding="utf-8") as file:
            lines = []
            for line in file:
                is_empty = True
                for ch in line:
                    if ch != '\n' and ch != '\r':
                        is_empty = False
                        break
                if not is_empty:
                    clean_line = ""
                    for ch in line:
                        if ch != '\n' and ch != '\r':
                            clean_line += ch
                    lines.append(clean_line)

        updated_admins = []

        i = 0
        while i < len(lines):
            name = lines[i]
            password = lines[i + 1]
            contact = lines[i + 2]
            position = lines[i + 3]
            status = lines[i + 4]

            same = True
            if len(name) == len(original_name):
                j = 0
                while j < len(name):
                    a = name[j]
                    b = original_name[j]
                    if 'A' <= a <= 'Z':
                        a = chr(ord(a) + 32)
                    if 'A' <= b <= 'Z':
                        b = chr(ord(b) + 32)
                    if a != b:
                        same = False
                        break
                    j += 1
            else:
                same = False

            if same:
                updated_admins.append([
                    updated_admin.name,
                    updated_admin.password,
                    updated_admin.contact,
                    updated_admin.position,
                    updated_admin.status
                ])
            else:
                updated_admins.append([name, password, contact, position, status])

            i += 5

        with open(ADMINS_FILE, "w", encoding="utf-8") as file:
            idx = 0
            while idx < len(updated_admins):
                admin = updated_admins[idx]
                j = 0
                while j < 5:
                    file.write(admin[j])
                    file.write("\n")
                    j += 1
                if idx != len(updated_admins) - 1:
                    file.write("\n")
                idx += 1

    except Exception as e:
        print("Error:", e)



def admin_profile():
    global logged_in_admin

    clear_screen()

    while True:
        print("------------------------------------------------------------------")
        print("|                         YOUR PROFILE                           |")
        print("------------------------------------------------------------------")
        print(f"| 1. Name              : {logged_in_admin.name:<40}|")
        print(f"| 2. Password          : {logged_in_admin.password:<40}|")
        print(f"| 3. Contact Number    : {logged_in_admin.contact:<40}|")
        print(f"| 4. Position          : {logged_in_admin.position:<40}|")
        print("------------------------------------------------------------------")

        choice = input("\nDo you want to edit your profile? (Y/N) : ")

        if choice == "Y" or choice == "y" or choice == "yes":
            edit_admin_profile()
        elif choice == "N" or choice == "n" or choice == "no":
            input("Press [Enter] to return to the admin menu.")
            clear_screen()
            return admin_menu()
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")
            clear_screen()

def edit_admin_profile():
    global logged_in_admin

    while True:
        clear_screen()
        print("------------------------------------------------------------------")
        print("|                       EDIT YOUR PROFILE                        |")
        print("------------------------------------------------------------------")
        print("| 1. Name                                                        |")
        print("| 2. Password                                                    |")
        print("| 3. Contact Number                                              |")
        print("| 4. Position (Not Editable)                                     |")
        print("| 5. Return to Profile Menu                                      |")
        print("------------------------------------------------------------------")

        choice = input("\nSelect the number you want to edit (1-5): ")

        if choice == "1":
            while True:
                new_name = input("Enter new Full Name: ")

                letter_count = 0
                is_valid = True
                for char in new_name:
                    if not (
                        ('A' <= char <= 'Z') or
                        ('a' <= char <= 'z') or
                        char == ' '
                    ):
                        is_valid = False
                        break
                    if char != ' ':
                        letter_count += 1

                if not is_valid or letter_count < 2:
                    print("Invalid name. Must contain only letters and spaces, with at least 2 letters.")
                    continue

                load_admins()

                cleaned_new = ""
                for char in new_name:
                    if char != ' ':
                        if 'A' <= char <= 'Z':
                            cleaned_new += chr(ord(char) + 32)
                        else:
                            cleaned_new += char

                cleaned_current_admin = ""
                for char in logged_in_admin.name:
                    if char != ' ':
                        if 'A' <= char <= 'Z':
                            cleaned_current_admin += chr(ord(char) + 32)
                        else:
                            cleaned_current_admin += char

                name_exists = False
                for admin in admins:
                    cleaned_admin_name = ""
                    for char in admin.name:
                        if char != ' ':
                            if 'A' <= char <= 'Z':
                                cleaned_admin_name += chr(ord(char) + 32)
                            else:
                                cleaned_admin_name += char

                    if cleaned_admin_name == cleaned_new and cleaned_admin_name != cleaned_current_admin:
                        name_exists = True
                        break

                if name_exists:
                    print("This name is already registered. Please use a different name!")
                    continue

                original_name = logged_in_admin.name
                logged_in_admin.name = new_name
                update_admin(logged_in_admin, original_name)
                print("Name updated successfully!")
                input("Press [ENTER] to continue.")
                break

        elif choice == "2":
            while True:
                logged_in_admin.password = ""
                logged_in_admin.password = input("Enter your new password (example: Xuanting123): ")

                if len(logged_in_admin.password) < 8:
                    print("Password must be at least 8 characters!")
                    continue

                upper = False
                lower = False
                digit = False

                for char in logged_in_admin.password:
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
                
                confirm_password = input("Confirm your password: ")
                if confirm_password != logged_in_admin.password:
                    print("Passwords do not match!")
                    continue
            
                update_admin(logged_in_admin)
                print("Password updated successfully!")
                input("Press [ENTER] to continue.")
                break

        elif choice == "3":
            while True:
                logged_in_admin.contact  = input("Enter your contact number (example: 012-34567890): ")

                if len(logged_in_admin.contact) < 4 or logged_in_admin.contact[3] != '-':
                    print("Format must be like 012-34567890 with a dash at the 4th position!")
                    continue

                part1 = ""
                part2 = ""
                for i in range(len(logged_in_admin.contact)):
                    if i < 3:
                        part1 += logged_in_admin.contact[i]
                    elif i > 3:
                        part2 += logged_in_admin.contact[i]


                if not (part1[0] == '0' and part1[1] == '1'):
                    print("Phone number must start with '01'!")
                    continue

                combined = part1 + part2
                only_digits = True
                for c in combined:
                    if not ('0' <= c <= '9'):
                        only_digits = False
                        break
                if not only_digits:
                    print("Phone number cannot contain symbols or space!")
                    continue

                if len(combined) != 10 and len(combined) != 11:
                    print("Phone number must be 10 or 11 digits!")
                    continue
    
                update_admin(logged_in_admin)
                print("Contact Number updated successfully!")
                input("Press [ENTER] to continue.")
                break
        elif choice == "4":
            input("\nYour position cannot be edited. Press [ENTER] to continue.")
        
        elif choice == "5":
            input("\nPress [ENTER] to return to your profile.")
            clear_screen()
            return admin_profile()
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")
            clear_screen()

def login_menu():
    global logged_in_member 

    while True:
        print("\n===============================================================")
        print("                   WELOCOME TO YESMOLAR BAKERY                 ")
        print("===============================================================")
        print("1.    Sign Up  ")
        print("2.    Login  ")
        print("3.    Admin Login  ")
        print("4.    Exit  ")
        print("===============================================================")

        choice = input("Enter your choice: ")

        if choice == '1':
            load_members()
            clear_screen()
            print("\n===============================================================")
            print("                    Signing Up As Member...                    ")
            print("===============================================================")
            signup()
        elif choice == '2':
            clear_screen()
            print("\n===============================================================")
            print("                    Logging In As Member...                    ")
            print("===============================================================")
            login()
        elif choice == '3':
            clear_screen()
            print("\n===============================================================")
            print("                    Logging In As Admin...                    ")
            print("===============================================================")
            admin_login()
        elif choice == '4':
            print("\nThank you for visiting Yesmolar Bakery!\n")
            exit()
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")
            clear_screen()
            
def admin_menu():
    global logged_in_member 

    while True:
        print("===============================================================")
        print("                          ADMIN MENU                           ")
        print("===============================================================")
        print(" [1] Manage Pastry Inventory")
        print(" [2] Manage Member List")
        print(" [3] Manage Admin List")
        print(" [4] Manage Feedback and Rating")
        print(" [5] View Dashboard")
        print(" [6] My profile")
        print(" [7] Log Out")
        print("===============================================================")

        choice = input("Enter your choice: ")

        if choice == '1':
            return
        elif choice == '2':
            return
        elif choice == '3':
            return
        elif choice == '4':
            return
        elif choice == '5':
            return
        elif choice == '6':
            admin_profile()
        elif choice == '7':
            input("\nPress [ENTER] to logout.")
            clear_screen()
            return login_menu()
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")
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
    if product.status == "Active":
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
                product.status, ss = get_quoted_field(ss)

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
                status = f'"{product.status}"' if ',' in product.status else product.status

                file.write(f"{pid},{name},{category},{price},{stock},{status}\n")
        return True
    except IOError as e:
        print(f"Error: Could not update the product file: {e}")
        return False

def get_cart_filename(member_id):
    """Returns the full path to the cart file for a given member ID"""
    return os.path.join(SCRIPT_DIR, f"{member_id}_cart.txt")

def load_cart(cart):
    if not logged_in_member:
        print("Error: Cannot load cart. No user logged in.")
        return False

    cart_file = get_cart_filename(logged_in_member.member_id)
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

    cart_file = get_cart_filename(logged_in_member.member_id)
    try:
        with open(cart_file, 'w', encoding='utf-8') as file:
            for item in cart:
                pid = item.product_id if item.product_id else (item.product.product_id if item.product else "")
                name = item.name if item.name else (item.product.name if item.product else "")
                price = item.price if item.price is not None else (item.product.price if item.product else 0.0)
                quantity = item.quantity
                total = item.total if item.total is not None else (price * quantity)
                status = item.status if item.status else (item.product.status if item.product else "")

                file.write(f"{logged_in_member.member_id},{pid},{name},{price:.2f},{quantity},{total:.2f}\n")
        return True
    except IOError as e:
        print(f"Error: Could not update cart file: {e}")
        return False
    
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
        status = item.product.status if item.product and item.product.status else "N/A"

        print(f"Item {i}:")
        print(f"Product ID : {pid}")
        print(f"Name       : {name}")

        if status=="Inactive":
            total=0.0
            print("SORRY! This product is currently unavailable :(")
        else:
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
            delete_cart(cart)
            break
        elif choice == '2':
            edit_cart(cart)
            break
        elif choice == '3':
            proceed_to_payment(products,cart)
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
    
    if selected_product.status == "Inactive":
        print("Error: This product is currently unavailable.")
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
            quantity=quantity,
            status=selected_product.status
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
            # Only show active products in this category
            filtered = [p for p in products if p.category.lower() == selected_category.lower() and p.status == "Active"]

            if not filtered:
                print(f"\nNo available products found in '{selected_category}' category.")
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
            # Check all products (not just filtered) to see if ID exists
            for p in products:
                if p.product_id == product_id:
                    product = p
                    break

            if not product:
                print(f"\nProduct with ID '{product_id}' not found.")
                input("Press [ENTER] to continue.")
                continue

            # Check if product is inactive
            if product.status == "Inactive":
                print("\nThis product is currently unavailable.")
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
        print(" [4] Purchase History")
        print(" [5] Rate Our System")
        print(" [6] Log Out")
        print("===============================================================")

        choice = input("Enter your choice: ")

        if choice == '1':
            filter_products()
        elif choice == '2':
            cart = []
            display_cart(cart)
        elif choice == '3':
            member_profile()
        elif choice == '4':
            view_purchase_history()
            return
        elif choice == '5':
            return
        elif choice == '6':
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