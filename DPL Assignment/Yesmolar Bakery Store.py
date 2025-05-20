import os
from datetime import datetime
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCT_FILE = os.path.join(SCRIPT_DIR, "product.txt")
MEMBERS_FILE = os.path.join(SCRIPT_DIR, "member.txt")
MEMBERS_ID_FILE = os.path.join(SCRIPT_DIR, "member_id.txt")
ADMINS_FILE = os.path.join(SCRIPT_DIR, "admin.txt")
PURCHASE_HISTORY_FILE = os.path.join(SCRIPT_DIR, "purchase_history.txt")  
ORDER_ID_FILE = os.path.join(SCRIPT_DIR, "order_id_counter.txt")
RATING_FILE = os.path.join(SCRIPT_DIR, "rating.txt") 

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

class PurchaseRecord:
    def __init__(self, record_dict):
        self.lines = record_dict["lines"]
        self.datetime = record_dict["datetime"]
        self.datetime_obj = record_dict["datetime_obj"]
        self.total = record_dict["total"]
        self.order_id = record_dict["order_id"]
        self.payment_method = record_dict["payment_method"]

class Feedback:
    def __init__(self, name, rating, comment, timestamp):
        self.name = name
        self.rating = int(rating)
        self.comment = comment
        self.timestamp = timestamp
        self.datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

products = []
members = []
admins = []
logged_in_member = ""
logged_in_admin = ""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

ascii_table = [
    '\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', 
    '\x08', '\t', '\n', '\x0b', '\x0c', '\r', '\x0e', '\x0f', 
    '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', 
    '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f', 
    ' ', '!', '"', '#', '$', '%', '&', "'", 
    '(', ')', '*', '+', ',', '-', '.', '/', 
    '0', '1', '2', '3', '4', '5', '6', '7', 
    '8', '9', ':', ';', '<', '=', '>', '?', 
    '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 
    'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 
    'X', 'Y', 'Z', '[', '\\', ']', '^', '_', 
    '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 
    'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 
    'x', 'y', 'z', '{', '|', '}', '~', '\x7f'
]

def custom_chr(code):
    if 0 <= code <= 127:
        return ascii_table[code]
    else:
        return ascii_table[code % 128]
    
def is_integer(string):
    if string == "":
        return False
    for char in string:
        if char < '0' or char > '9':
            return False
    return True
    
def has_attribute(obj, attr):
    try:
        obj.__dict__
    except AttributeError:
        return False

    return attr in obj.__dict__

def get_attribute(obj, attr):
    try:
        return obj.__dict__[attr]
    except (AttributeError, KeyError):
        return None

def my_split(s, delimiter=' '):
    result = []
    temp = ''
    i = 0
    while i < len(s):
        # Check if the substring matches the delimiter
        if s[i:i+len(delimiter)] == delimiter:
            result.append(temp)
            temp = ''
            i += len(delimiter)
        else:
            temp += s[i]
            i += 1
    result.append(temp)
    return result

def second_split(s, delimiter=','):
    result = []
    temp = ''
    found_delimiter = False
    
    for char in s:
        if char == delimiter and not found_delimiter:
            result.append(temp)
            temp = ''
            found_delimiter = True
        else:
            temp += char

    result.append(temp)
    
    return result

def my_enumerate(iterable, start=0):
    result = []
    index = start
    for item in iterable:
        result.append((index, item))
        index += 1
    return result

def join_strings(separator, sequence):
    if not sequence:
        return ""
    
    result = ""
    first_item = True
    
    for item in sequence:
        if not first_item:
            result += separator
        result += str(item)
        first_item = False
    
    return result

def split_lines(text):
    lines = []
    current_line = []
    
    for char in text:
        if char == '\n' or char == '\r':
            lines.append(join_strings("", current_line))
            current_line = []
        else:
            current_line.append(char)
    
    if current_line:
        lines.append(join_strings("", current_line))
    
    return lines

def raw_keys(dictionary):
    keys = []
    for key in dictionary:
        keys.append(key)
    return keys

def raw_items(dictionary):
    items = []
    for key in dictionary:
        items.append((key, dictionary[key]))
    return items

def raw_replace(s, old, new):
    result = ""
    i = 0
    while i < len(s):
        if s[i:i+len(old)] == old:
            result += new
            i += len(old)
        else:
            result += s[i]
            i += 1
    return result

def get_quoted_field(ss):
    field = ""
    ss = ss.strip()
    
    if not ss:
        return "", ""

    if len(ss) > 0 and ss[0] == '"':
        ss = ss[1:]
        try:
            quote_end_index = -1
            for i in range(len(ss)):
                if ss[i] == '"':
                    quote_end_index = i
                    break

            if quote_end_index == -1:
                # No closing quote found
                field = ss
                ss = ""
            else:
                field = ss[:quote_end_index]
                ss = ss[quote_end_index + 1:]

                if len(ss) > 0 and ss[0] == ',':
                    ss = ss[1:]

        except IndexError:
            field = ss
            ss = ""
    else:
        line = second_split(ss, ',')
        field = line[0]
        ss = line[1] if len(line) > 1 else ""

    return field.strip(), ss.strip()

def bubble_sort(arr, key=None, reverse=False):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            if key:
                a = get_attribute(arr[j], key) if has_attribute(arr[j], key) else arr[j]
                b = get_attribute(arr[j+1], key) if has_attribute(arr[j+1], key) else arr[j+1]
            else:
                a = arr[j]
                b = arr[j + 1]

            if (a > b) if not reverse else (a < b):
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break

def min_val(a, b):
    return a if a < b else b

def jump_search(arr, target, key=None):
    n = len(arr)
    if n == 0:
        return None

    step = 1
    while step * step < n:
        step += 1

    prev = 0
    while True:
        index = step - 1
        if index >= n:
            index = n - 1

        if key:
            current_val = get_attribute(arr[min_val(step, n)-1], key) if has_attribute(arr[min_val(step, n)-1], key) else None
        else:
            current_val = arr[min_val(step, n)-1]

        if current_val is None:
            return None

        if current_val < target:
            prev = step
            step += int(n ** 0.5)
            if prev >= n:
                return None
        else:
            break

    if key:
        while get_attribute(arr[prev], key) < target:
            prev += 1
            if prev == min_val(step, n):
                return None
            
    else:
        while arr[prev] < target:
            prev += 1
            if prev == min_val(step, n):
                return None
            
    if key:
        if get_attribute(arr[prev], key) == target:
            return arr[prev]
        
    else:
        if arr[prev] == target:
            return arr[prev]
    return None 

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
            file_content = file.read()
            all_lines = split_lines(file_content)
            non_empty_lines = [line.strip() for line in all_lines if line.strip()]
            
            if non_empty_lines:
                last_id = non_empty_lines[-1] 
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
        
        content = ""
        while True:
            char = file.read(1)
            if not char:
                break
            content += char
        
        last_char_is_newline = False
        if len(content) > 0:
            last_char = content[-1]
            if last_char == '\n':
                last_char_is_newline = True
        
        if len(content) > 0 and not last_char_is_newline:
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
        full_name = input("\nEnter your full name, [R] to return: ").strip()

        if full_name == 'R' or full_name == 'r':
            clear_screen()
            login_menu()

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
            print("Invalid name. Name must have at least 2 letters and contain only letters and spaces.\n")
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
        email = input("\nEnter your email (example: xuanting@example.com): ")

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
        password = input("\nEnter your new password (example: Xuanting123): ")

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
        
        confirm_password = input("\nConfirm your password: ")
        if confirm_password != password:
            print("Passwords do not match!")
            continue
    
        break

    while True:
        age = input("\nEnter your age: ")

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
        gender = input("\nEnter your gender (male or female): ")

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
        contact = input("\nEnter your contact number (example: 012-34567890): ")

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
   
    new_member = Member(
        full_name=full_name,
        member_id=member_id,
        email=email,
        password=password,
        age=age,
        gender=gender,
        contact=contact,
        status=status
    )
    members.append(new_member)

    with open(MEMBERS_ID_FILE, "a+", encoding='utf-8') as file:
        file.seek(0)
        content = file.read()

        needs_newline = True
        if len(content) > 0:
            last_char = content[-1]
            if last_char == '\n':
                needs_newline = False
        
        if needs_newline:
            file.write('\n')

        for char in member_id:
            file.write(char)
        file.write('\n')

    save_member(new_member)
    print(f"\nRegistration successful! Your Member ID: {member_id}")
    input("\nPress [ENTER] to return to login menu.")
    clear_screen()

def login():
    global logged_in_member 
    
    email = input("\nEnter your email, [R] to return: ").strip()

    if email == 'R' or email == 'r':
        clear_screen()
        login_menu()
        return
    
    password = input("\nEnter your password: ").strip()

    try:
        with open(MEMBERS_FILE, "r", encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() != ''] 

        for i in range(0, len(lines), 8):  
            stored_email = lines[i + 2]
            stored_password = lines[i + 3]
            status = lines[i + 7]

            if email == stored_email:
                if status.lower() != "active":
                    print("Your account is inactive. Please contact admin.")
                    input("\nPress [ENTER] to return to login menu.")
                    clear_screen()
                    return False
                
                attempts = 0
                while attempts < 3:
                    if password == stored_password:
                        print("\nLogged in Successfully!")
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
                        print(f"Incorrect password! Attempts left: {3 - attempts}\n")
                        password = input("Please enter your password again: ").strip()

                print("Too many failed attempts. Login terminating.")
                input("\nPress [ENTER] to return to login menu.")
                clear_screen()
                return False
                    
        print("\nEmail not found.")
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

        members = []
        current_member = []
        blank_line_count = 0
        
        for char in content:
            if char == '\n':
                blank_line_count += 1
                if blank_line_count == 2:
                    members.append(join_strings("", current_member))
                    current_member = []
                    blank_line_count = 0
            else:
                if blank_line_count == 1:
                    current_member.append('\n')
                    blank_line_count = 0
                current_member.append(char)
        
        if current_member:
            members.append(join_strings("", current_member))

        updated_members = []

        for member_data in members:
            fields = split_lines(member_data)

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
                updated_members.append(join_strings("\n", new_member_data))
            else:
                updated_members.append(member_data)

        new_content = join_strings("\n\n", updated_members)

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
        print("============================================================================")
        print("|                               YOUR PROFILE                               |")
        print("============================================================================")
        print(f"| 1. Member ID         : {logged_in_member.member_id:<50}|")
        print(f"| 2. Full Name         : {logged_in_member.full_name:<50}|")
        print(f"| 3. Email             : {logged_in_member.email:<50}|")
        print(f"| 4. Password          : {logged_in_member.password:<50}|")
        print(f"| 5. Age               : {logged_in_member.age:<50}|")
        print(f"| 6. Gender            : {logged_in_member.gender:<50}|")
        print(f"| 7. Contact Number    : {logged_in_member.contact:<50}|")
        print("============================================================================")

        choice = input("\nDo you want to edit your profile? (Y/N) : ")

        if choice == "Y" or choice == "y" or choice == "yes":
            edit_member_profile()
        elif choice == "N" or choice == "n" or choice == "no":
            input("\nPress [Enter] to return to the main menu.")
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
        print("============================================================================")
        print("|                             EDIT YOUR PROFILE                            |")
        print("============================================================================")
        print("| 1. Member ID (Not Editable)                                              |")
        print("| 2. Full Name                                                             |")
        print("| 3. Email                                                                 |")
        print("| 4. Password                                                              |")
        print("| 5. Age                                                                   |")
        print("| 6. Gender                                                                |")
        print("| 7. Contact Number                                                        |")
        print("| 8. Return to Profile Menu                                                |")
        print("============================================================================")

        choice = input("\nSelect the number you want to edit (1-8): ")

        if choice == "1":
            input("\nMember ID cannot be edited. Press [ENTER] to continue.")

        elif choice == "2":
            while True:
                new_name = input("\nEnter new Full Name: ")

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
                            cleaned_new_name += custom_chr(ord(char) + 32)
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
                                cleaned_existing += custom_chr(ord(char) + 32)
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
                print("\nFull Name updated successfully!")
                input("\nPress [ENTER] to continue.")
                break

        elif choice == "3":
            while True:
                new_email = input("\nEnter new email: ")

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
                            cleaned_new_email += custom_chr(ord(char) + 32)
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
                                cleaned_existing += custom_chr(ord(char) + 32)
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
                print("\nEmail updated successfully!")
                input("\nPress [ENTER] to continue.")
                break

        elif choice == "4":
            while True:
                logged_in_member.password = ""
                logged_in_member.password = input("\nEnter your new password (example: Xuanting123): ")

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
                
                confirm_password = input("\nConfirm your password: ")
                if confirm_password != logged_in_member.password:
                    print("Passwords do not match!")
                    continue
            
                update_member(logged_in_member)
                print("\nPassword updated successfully!")
                input("\nPress [ENTER] to continue.")
                break

        elif choice == "5":
            try:
                while True:
                    logged_in_member.age = input("\nEnter new age: ")

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
                    print("\nAge updated successfully!")
                    break
            except ValueError:
                print("Invalid input! Age must be a number.")
            input("\nPress [ENTER] to continue.")

        elif choice == "6":
            while True:
                logged_in_member.gender = input("\nEnter new gender (male or female): ")

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
                print("\nGender updated successfully!")
                input("\nPress [ENTER] to continue.")
                break

        elif choice == "7":
            while True:
                logged_in_member.contact  = input("\nEnter your contact number (example: 012-34567890): ")

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
                print("\nContact Number updated successfully!")
                input("\nPress [ENTER] to continue.")
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

    name = input("\nEnter your name, [R] to return: ").strip()

    if name == 'R' or name == 'r':
        clear_screen()
        login_menu()
        return
    
    password = input("\nEnter your password: ").strip()

    try:
        with open(ADMINS_FILE, "r", encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() != ''] 

        for i in range(0, len(lines), 5):  
            stored_name = lines[i]
            stored_password = lines[i + 1]
            stored_position = lines[i + 3]
            status = lines[i + 4]

            if name == stored_name:
                if status.lower() != "active":
                    print("Your account is inactive. Please contact superadmin.")
                    input("\nPress [ENTER] to return to login menu.")
                    clear_screen()
                    return False
                
                attempts = 0
                while attempts < 3:
                    if password == stored_password:
                        print("\nLogged in Successfully!")
                        print(f"Welcome {stored_position}!")
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
                        print(f"Incorrect password! Attempts left: {3 - attempts}\n")
                        password = input("Please enter your password again: ").strip()

                print("Too many failed attempts. Login terminating.")
                input("\nPress [ENTER] to return to login menu.")
                clear_screen()
                return False

        print("Name not found.")
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
                        a = custom_chr(ord(a) + 32)
                    if 'A' <= b <= 'Z':
                        b = custom_chr(ord(b) + 32)
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
        print("============================================================================")
        print("|                               YOUR PROFILE                               |")
        print("============================================================================")
        print(f"| 1. Name              : {logged_in_admin.name:<50}|")
        print(f"| 2. Password          : {logged_in_admin.password:<50}|")
        print(f"| 3. Contact Number    : {logged_in_admin.contact:<50}|")
        print(f"| 4. Position          : {logged_in_admin.position:<50}|")
        print("============================================================================")

        choice = input("\nDo you want to edit your profile? (Y/N) : ")

        if choice == "Y" or choice == "y" or choice == "yes":
            edit_admin_profile()
        elif choice == "N" or choice == "n" or choice == "no":
            input("\nPress [Enter] to return to the admin menu.")
            clear_screen()
            return admin_menu()
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")
            clear_screen()

def edit_admin_profile():
    global logged_in_admin

    while True:
        clear_screen()
        print("============================================================================")
        print("|                              EDIT YOUR PROFILE                           |")
        print("============================================================================")
        print("| 1. Name                                                                  |")
        print("| 2. Password                                                              |")
        print("| 3. Contact Number                                                        |")
        print("| 4. Position (Not Editable)                                               |")
        print("| 5. Return to Profile Menu                                                |")
        print("============================================================================")

        choice = input("\nSelect the number you want to edit (1-5): ")

        if choice == "1":
            while True:
                new_name = input("\nEnter new Full Name: ")

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
                            cleaned_new += custom_chr(ord(char) + 32)
                        else:
                            cleaned_new += char

                cleaned_current_admin = ""
                for char in logged_in_admin.name:
                    if char != ' ':
                        if 'A' <= char <= 'Z':
                            cleaned_current_admin += custom_chr(ord(char) + 32)
                        else:
                            cleaned_current_admin += char

                name_exists = False
                for admin in admins:
                    cleaned_admin_name = ""
                    for char in admin.name:
                        if char != ' ':
                            if 'A' <= char <= 'Z':
                                cleaned_admin_name += custom_chr(ord(char) + 32)
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
                print("\nName updated successfully!")
                input("\nPress [ENTER] to continue.")
                break

        elif choice == "2":
            while True:
                logged_in_admin.password = ""
                logged_in_admin.password = input("\nEnter your new password (example: Xuanting123): ")

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
                
                confirm_password = input("\nConfirm your password: ")
                if confirm_password != logged_in_admin.password:
                    print("\nPasswords do not match!")
                    continue
            
                update_admin(logged_in_admin, logged_in_admin.name)
                print("\nPassword updated successfully!")
                input("\nPress [ENTER] to continue.")
                break

        elif choice == "3":
            while True:
                logged_in_admin.contact  = input("\nEnter your contact number (example: 012-34567890): ")

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
    
                update_admin(logged_in_admin, logged_in_admin.name)
                print("\nContact Number updated successfully!")
                input("\nPress [ENTER] to continue.")
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

def filter_feedback_rating():
    try:
        rate_input = input("Enter the rating level to filter by (1 to 5): ")

        if rate_input == "":
            print("Invalid input. Rating cannot be empty.\n")
            return filter_feedback_rating()
        
        only_digits = True
        for ch in rate_input:
            if not ('0' <= ch <= '9'):
                only_digits = False
                break

        if not only_digits:
            print("Invalid input. Please enter a valid number between 1 and 5.\n")
            return filter_feedback_rating()
        
        rate_filter = int(rate_input)

        if not (1 <= rate_filter <= 5):
            print("Invalid rating. Please enter a number between 1 and 5.\n")
            return filter_feedback_rating()

        if 1 <= rate_filter <= 5:       
            print("===========================================================================")
            print(f"|                    Filtered Feedback (Rating = {rate_filter})                       |")

            found = False

            try:
                with open(RATING_FILE, 'r', encoding='utf-8') as file:
                    content = file.read()
                    for line in split_lines(content):
                        line = line.strip()
                        if line:
                            parts = my_split(line, ',')
                            if len(parts) == 4:
                                name, rating, comment, timestamp = parts
                                if str(rate_filter) == rating:
                                    found = True
                                    print("===========================================================================")
                                    print(f"| Date & Time  : {timestamp:<57}|")
                                    print("===========================================================================")
                                    print(f"| Name         : {name:<57}|")
                                    print(f"| Rating       : {rating:<57}|")
                                    print(f"| Comment      : {comment:<57}|")
                                    print("---------------------------------------------------------------------------")
                                 
                                
                if not found:
                    print("===========================================================================")
                    print("|                                                                         |")
                    print(f"|                   No records found for rating level {rate_filter}                   |")
                    print("|                                                                         |")
                    print("---------------------------------------------------------------------------")

            except FileNotFoundError:
                print("Feedback file not found.")
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")
    input("\nPress [ENTER] to return to feedback menu.")
    clear_screen()
    return view_feedback_rating()

def sort_feedback_rating():
    try:
        feedback_rating = []
        with open(RATING_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
            for line in split_lines(content):
                line = line.strip()
                if line:
                    parts = my_split(line, ',')
                    if len(parts) == 4:
                        name, rating, comment, timestamp = parts
                        feedback_rating.append(Feedback(name, rating, comment, timestamp))

        if not feedback_rating:
            print("============================================================================")
            print("|                                                                         |")
            print("|                    No feedback records found to sort.                   |")
            print("|                                                                         |")
            print("---------------------------------------------------------------------------")
            input("\nPress [ENTER] to return to feedback menu.")
            clear_screen()
            return view_feedback_rating()
        
        print("\nSort feedback by:")
        print("1. Rating (Highest First)")
        print("2. Rating (Lowest First)")
        print("3. Date (Newest First)")
        print("4. Date (Oldest First)")
        print("5. Cancel")

        choice = input("\nEnter your choice (1-5): ")

        if choice == '1':
            print("============================================================================")
            print("|            SORTED FEEDBACK & RATING (Rating - Highest First)             |")
            bubble_sort(feedback_rating, key='rating', reverse=True)
        elif choice == '2':
            print("============================================================================")
            print("|            SORTED FEEDBACK & RATING (Rating - Lowest First)              |")
            bubble_sort(feedback_rating, key='rating', reverse=False)
        elif choice == '3':
            print("============================================================================")
            print("|             SORTED FEEDBACK & RATING (Date – Newest First)               |")
            bubble_sort(feedback_rating, key='datetime', reverse=True)
        elif choice == '4':
            print("============================================================================")
            print("|             SORTED FEEDBACK & RATING (Date – Oldest First)               |")
            bubble_sort(feedback_rating, key='datetime', reverse=False)
        elif not choice:
            print("Invalid input. The choice cannot be empty.\n")
            return sort_feedback_rating()
        elif choice == '5':
            input("\nPress [ENTER] to return rating menu.")
            clear_screen()
            return view_feedback_rating()
        else:
            print("Invalid rating. Please enter a number between 1 and 5.")
            return sort_feedback_rating()

        for record in feedback_rating:
            print("============================================================================")
            print(f"| Date & Time  : {record.timestamp:<58}|")
            print("===========================================================================")
            print(f"| Name         : {record.name:<58}|")
            print(f"| Rating       : {record.rating:<58}|")
            print(f"| Comment      : {record.comment:<58}|")
            print("----------------------------------------------------------------------------")

        input("\nPress [ENTER] to return to feedback menu.")
        return view_feedback_rating()
    except FileNotFoundError:
        print("Feedback file not found.")
        input("Press [ENTER] to return to the admin menu.")
    except Exception as e:
        print(f"Error sorting feedback: {e}")
        input("Press [ENTER] to continue.")

def view_feedback_rating():
    global logged_in_admin

    clear_screen()

    print("===========================================================================")
    print("|                        Feedback and Rating Records                      |")

    try:
        with open(RATING_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = split_lines(content)

        if not lines:
            print("|                                                                         |")
            print("|                       No feedback records found.                        |")
            print("|                                                                         |")
            print("---------------------------------------------------------------------------")
            input("Press [Enter] to return to the admin menu.")
            return admin_menu()

        for line in lines:
            line = line.strip()
            if line:
                parts = my_split(line, ',')
                if len(parts) == 4:
                    name, rating, comment, timestamp = parts
                    print("===========================================================================")
                    print(f"| Date & Time  : {timestamp:<57}|")
                    print("===========================================================================")
                    print(f"| Name         : {name:<57}|")
                    print(f"| Rating       : {rating:<57}|")
                    print(f"| Comment      : {comment:<57}|")
                print("---------------------------------------------------------------------------")

    except FileNotFoundError:
        print("Feedback file not found.")
        input("Press [Enter] to return to the admin menu.")
        return admin_menu()

    while True:
        print("1. Filter feedback by rate level")
        print("2. Sort feedback and rating")
        choice = input("\nEnter your choice (R for return): ")

        if choice == '1':
            clear_screen()
            filter_feedback_rating()

        elif choice == '2':
            clear_screen()
            sort_feedback_rating()
        
        elif choice in['R','r']:
            input("Press [Enter] to return to the admin menu.")
            clear_screen()
            return admin_menu()
        
        elif not choice:
            print("Invalid input. The choice cannot be empty.\n")

        else:
            print("Invalid choice. Please enter 1, 2 or R.\n")

def login_menu():
    global logged_in_member 

    while True:
        
        print("\n============================================================================")
        print("|                                                                          |")
        print("|                             W E L C O M E   T O                          |")
        print("|                         Y E S M O L A R   B A K E R Y                    |")
        print("|                                                                          |")
        print("============================================================================")
        print("|                                                                          |")
        print("|                                                          .--.            |")
        print("|                                                  ✧     / _   /           |")
        print("|  1.    Sign Up                                        / __  /            |")
        print("|  2.    Login                                         / __  /  ✧          |")
        print("|  3.    Admin Login                                  '  _  /              |")
        print("|  4.    Exit                                     ✧   `..-'                |")
        print("|                                                                          |")
        print("============================================================================")

        choice = input("Enter your choice: ")

        if choice == '1':
            load_members()
            clear_screen()
            print("\n===========================================================================")
            print("|                            Signing Up As Member...                      |")
            print("===========================================================================")
            signup()
        elif choice == '2':
            clear_screen()
            print("\n===========================================================================")
            print("|                          Logging In As Member...                        |")
            print("===========================================================================")
            login()
        elif choice == '3':
            clear_screen()
            print("\n===========================================================================")
            print("|                           Logging In As Admin...                        |")
            print("===========================================================================")
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
        clear_screen()
        print("===========================================================================")
        print("|                                ADMIN MENU                               |")
        print("===========================================================================")
        print("| [1] Manage Pastry Inventory                                             |")
        print("| [2] Manage Member List                                                  |")
        print("| [3] Manage Admin List                                                   |")
        print("| [4] Manage Feedback and Rating                                          |")
        print("| [5] View Dashboard                                                      |")
        print("| [6] View Order History                                                  |")
        print("| [7] View Sales Report                                                   |")
        print("| [8] My profile                                                          |")
        print("| [9] Log Out                                                             |")
        print("===========================================================================")

        choice = input("Enter your choice: ")

        if choice == '1':
            filter_product_admin()
        elif choice == '2':
            manage_member()
        elif choice == '3':
            manage_admin()
        elif choice == '4':
            view_feedback_rating()
            return
        elif choice == '5':
            view_dashboard()
        elif choice == '6':
            view_order_history()
        elif choice == '7':
            view_sales_report()
        elif choice == '8':
            admin_profile()
        elif choice == '9':
            input("\nPress [ENTER] to logout.")
            clear_screen()
            return login_menu()
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")
            clear_screen()

def filter_product_admin():
    global products

    if not load_products():
        print("Failed to load products.")
        input("Press [ENTER] to return to main menu.")
        clear_screen()
        main_menu()
        return

    while True:
        clear_screen()
        print("===========================================================================")
        print("|                    YESMOLAR BAKERY STORE INVENTORY                      |")
        print("===========================================================================")
        print("| Select a category:                                                      |")
        categories = {
            '1': 'Bread', '2': 'Pastries', '3': 'Cakes', '4': 'Donuts',
            '5': 'Cupcakes & Muffins', '6': 'Cookies', '7': 'Pies & Tarts',
            '8': 'Savories & Sandwiches'
        }
        for key, value in raw_items(categories):
            print(f"| [{key}] {value:<68}|")
        print(f"| {'[9] Back to Main Menu':<72}|")
        print("===========================================================================")

        choice = input("Enter your choice (1-9): ")
        if choice == '9':
            clear_screen()
            admin_menu()
            return
        elif choice not in categories:
            print("Invalid choice. Please try again.")
            input("Press [ENTER] to continue.")
            continue

        selected_category = categories[choice]
        while True:
            clear_screen()
            print(f"Products in Category: {selected_category}                ")
            load_products()

            display_product_admin(products, selected_category)
            print("\n---------------------------------------------------------------------------")
            print(" ________________________________________")
            print("|                                        |")
            print("|    Options:                            |")
            print("| [1] Add New Product to This Category   |")
            print("| [2] Edit Existing Product              |")
            print("| [3] Restock Product                    |")
            print("| [4] Return to Category Selection       |")
            print("|________________________________________|")
        
            admin_choice = input("\nEnter your choice: ")
        
            if admin_choice == '1':
                add_product(products, selected_category)
            elif admin_choice == '2':
                edit_product(products, selected_category)
            elif admin_choice == '3':
                restock_product(products, selected_category)
            elif admin_choice == '4':
                clear_screen()
                filter_product_admin()
                continue
            else:
                print("Invalid option, returning to category selection.")
                clear_screen()

def add_product(products, category):
    new_product = Product()
    new_product.category = category
    
    while True:
        new_product.product_id = input("\nEnter ID in 3 digits: ").strip()
        if len(new_product.product_id) != 3 or not is_integer(new_product.product_id):
            print("ID must be exactly 3 digits and numeric only!")
            continue

        id_exists = jump_search(products, new_product.product_id, key='product_id')
        if id_exists:
            print("Product ID already exists! Please enter a different ID.")
        else:
            break

    
    while True:
        new_product.name = input("\nEnter product name: ").strip()
        if len(new_product.name) == 0:
            print("Name cannot be empty!")
            continue
        break
    
    while True:
        price_input = input("\nEnter price: ")
        try:
            new_product.price = float(price_input)
            if new_product.price <= 0:
                print("Price must be positive!")
                continue
            break
        except:
            print("Invalid price! Please enter a valid number.")
    
    while True:
        stock_input = input("\nEnter stock quantity: ")
        try:
            new_product.stock = int(stock_input)
            if new_product.stock < 0:
                print("Stock cannot be negative!")
                continue
            break
        except:
            print("Invalid quantity! Please enter a whole number.")

    while True:
        status_input = input("\nEnter status [Active/Inactive]: ").strip()
        if len(status_input) > 0:
            status_input = status_input[0].upper() + status_input[1:].lower()
        new_product.status = status_input

        if new_product.status not in ["Active", "Inactive"]:
            print("Status must be either 'Active' or 'Inactive'!")
            continue
        break
    
    products.append(new_product)
    if update_product_file():
        print("\nProduct added successfully!\n")
    else:
        print("\nError saving product to file!")
    
    input("Press [ENTER] to continue.")
    filter_product_admin()

def edit_product(products, category):
    if not products:
        print("No products available to edit.")
        input("Press [ENTER] to continue.")
        return
        
    product_id = input("\nEnter the Product ID to edit: ")
    
    product_to_edit = None
    product_to_edit = jump_search(products, product_id, key='product_id')
    
    if not product_to_edit:
        print("No product found with that ID in this category!")
        input("\nPress [ENTER] to continue.")
        return
    
    print(f"\nEditing product: {product_to_edit.name}")
    
    while True:
        new_name = input(f"\nEnter new name [{product_to_edit.name}]: ").strip()
        if len(new_name) == 0:
            new_name = product_to_edit.name
            break
        if len(new_name) < 2:
            print("Name must be at least 2 characters!")
            continue
        break
    
    while True:
        price_input = input(f"\nEnter new price [{product_to_edit.price}]: ").strip()
        if len(price_input) == 0:
            new_price = product_to_edit.price
            break
        try:
            new_price = float(price_input)
            if new_price <= 0:
                print("Price must be positive!")
                continue
            break
        except:
            print("Invalid price! Please enter a valid number.")
    
    while True:
        stock_input = input(f"\nEnter new stock [{product_to_edit.stock}]: ").strip()
        if len(stock_input) == 0:
            new_stock = product_to_edit.stock
            break
        try:
            new_stock = int(stock_input)
            if new_stock < 0:
                print("Stock cannot be negative!")
                continue
            break
        except:
            print("Invalid quantity! Please enter a whole number.")
    
    while True:
        status_input = input("\nEnter status [Active/Inactive]: ").strip()

        if len(status_input) > 0:
            status_input = status_input[0].upper() + status_input[1:].lower()

        if status_input not in ["Active", "Inactive"]:
            print("Status must be either 'Active' or 'Inactive'!")
            continue

        new_status = status_input
        break

    product_to_edit.name = new_name
    product_to_edit.price = new_price
    product_to_edit.stock = new_stock
    product_to_edit.status = new_status
    
    if update_product_file():
        print("\nProduct updated successfully!\n")
    else:
        print("\nError saving changes to file!")
    
    input("Press [ENTER] to continue.")
    filter_product_admin()

def restock_product(products, category):
    if not products:
        print("No products available to restock.")
        input("Press [ENTER] to continue.")
        return
        
    product_id = input("\nEnter the Product ID to restock: ")
    
    product_to_restock = None
    product_to_restock = jump_search(products, product_id, key='product_id')
    
    if not product_to_restock:
        print("No product found with that ID in this category!")
        input("\nPress [ENTER] to continue.")
        return
    
    print(f"\nRestocking product: {product_to_restock.name}")
    print(f"Current stock: {product_to_restock.stock}")

    while True:
        add_stock_input = input("\nEnter quantity to add: ").strip()
        try:
            add_stock = int(add_stock_input)
            if add_stock <= 0:
                print("Quantity must be positive!")
                continue
            break
        except:
            print("Invalid quantity! Please enter a whole number.")
    
    product_to_restock.stock += add_stock
    
    if update_product_file():
        print(f"\nProduct restocked successfully! New stock: {product_to_restock.stock}\n")
    else:
        print("\nError saving changes to file!")
        product_to_restock.stock -= add_stock
    
    input("Press [ENTER] to continue.")
    filter_product_admin()

def feedback_rating():
    if not logged_in_member:
        print("Error: No user logged in.")
        input("Press [ENTER] to continue.")
        return

    clear_screen()
    print("===========================================================================")
    print("|                              FEEDBACK & RATING                          |")
    print("===========================================================================")

    while True:
        rate_input = input("\nEnter your rating for our system (1 to 5), [R] to return: ").strip()

        if rate_input in ["R", "r"]:
            clear_screen()
            main_menu()

        if not rate_input:
            print("Invalid input. Rating cannot be empty.\n")
            continue

        only_digits = True
        for c in rate_input:
            if not ('0' <= c <= '9'):
                only_digits = False
                break

        if only_digits:
            rate = int(rate_input)
            if 1 <= rate <= 5:
                break
            else:
                print("Invalid rating. Please enter a number between 1 and 5.\n")
        else:
            print("Invalid input. Please enter a number between 1 and 5, or 'R' to return.\n")

    comment = input("\nEnter your comment (optional): ")
    print("\nThank you for your feedback!")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(RATING_FILE, "a", encoding="utf-8") as file:
        if comment == "":
            file.write(f"{logged_in_member.full_name},{rate},-,{now}\n")
        else:
            file.write(f"{logged_in_member.full_name},{rate},{comment},{now}\n")

    input("\nPress [ENTER] to return to main menu.")
    clear_screen()
    main_menu()

def display_product(product):
    if product.status == "Active":
        print("---------------------------------------------------------------------------")
        print(f"| Product ID: {product.product_id:<60}|")
        print("---------------------------------------------------------------------------")
        print(f"| Name      : {product.name:<60}|")
        print(f"| Category  : {product.category:<60}|")
        print(f"| Price     : RM {product.price:<57.2f}|")

        if product.stock <= 0:
            print("| WARNING   : SORRY! THIS PRODUCT IS CURRENTLY OUT OF STOCK!              |")
        else:
            print(f"| Stock     : {product.stock:<60}|")
        print("---------------------------------------------------------------------------")

def display_product_admin(products, selected_category):
    for product in products:
        if product.category == selected_category:
            print("---------------------------------------------------------------------------")
            print(f"| Product ID: {product.product_id:<60}|")
            print("---------------------------------------------------------------------------")
            print(f"| Name     : {product.name:<61}|")
            print(f"| Category : {product.category:<61}|")
            print(f"| Price    : RM {product.price:<58.2f}|")
            print(f"| Stock    : {product.stock:<61}|")
            print(f"| Status   : {product.status:<61}|")
            print("---------------------------------------------------------------------------")

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
                    product.price = 0.0

                try:
                    product.stock = int(stock_str) if stock_str else 0
                except ValueError:
                    product.stock = 0

                products.append(product)
        
        # Sort products by product_id
        bubble_sort(products, key='product_id')
        return True
    except FileNotFoundError:
        print(f"Error: Product file '{PRODUCT_FILE}' not found!")
        return False
    except IOError as e:
        print(f"Error: Could not read the product file: {e}")
        return False

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
    return SCRIPT_DIR + "/" + str(member_id) + "_cart.txt"

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

                parts = []
                temp = ""
                comma_count = 0
                for char in line:
                    if char == ',' and comma_count < 5:
                        parts.append(temp)
                        temp = ""
                        comma_count += 1
                    else:
                        temp += char
                parts.append(temp)

                if len(parts) != 6:
                    print(f"Skipping malformed line: {line}")
                    continue

                try:
                    item = CartItem()
                    item.product_id = parts[1].strip()
                    item.name = parts[2].strip()
                    item.price = float(parts[3].strip())
                    item.quantity = int(parts[4].strip())
                    item.total = float(parts[5].strip())
                except ValueError as e:
                    print(f"Skipping line due to conversion error: {line} - {e}")
                    continue

                # Attach latest product info
                for p in products:
                    if p.product_id == item.product_id:
                        item.product = p
                        item.status = p.status
                        break
                else:
                    print(f"Warning: Product ID {item.product_id} not found.")

                cart.append(item)

        return True

    except IOError as e:
        print(f"Error reading cart file: {e}")
        return False

def save_cart(cart):
    if not logged_in_member:
        print("Error: Cannot save cart. No user logged in.")
        return False

    cart_file = get_cart_filename(logged_in_member.member_id)

    try:
        with open(cart_file, 'w', encoding='utf-8') as file:
            for index, item in enumerate(cart, start=1):
                pid = item.product_id if item.product_id else (item.product.product_id if item.product else "")
                name = item.name if item.name else (item.product.name if item.product else "")
                price = item.price if item.price is not None else (item.product.price if item.product else 0.0)
                quantity = item.quantity
                total = item.total if item.total is not None else (price * quantity)

                file.write(f"{logged_in_member.member_id},{pid},{name},{price:.2f},{quantity},{total:.2f}\n")
        return True
    except IOError as e:
        print(f"Error: Could not update cart file: {e}")
        return False
    
def delete_cart(cart):
    while True:
        item_num_input = input("\nEnter item number to delete (or 0 to cancel): ").strip()

        if not is_integer(item_num_input):
            print("Invalid input. Please enter a number.")
            continue

        item_num = int(item_num_input)

        if item_num == 0:
            print("Cancel successful!\n")
            input("Press [ENTER] to refresh cart.")
            return False
        elif item_num < 1 or item_num > len(cart):
            if len(cart) == 1:
                print("Invalid item number. Please enter 1")
            else:
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
        print(f"\n'{deleted_item.name}' removed from cart successfully!\n")
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

    editable_items = []
    for i, item in my_enumerate(cart, 1):
        status = item.product.status if item.product else "N/A"
        if status == "Active":
            editable_items.append((i, item))

    if not editable_items:
        print("No editable items in your cart (all items are inactive).")
        input("Press [ENTER] to continue.")
        return False

    while True:
        item_num_input = input("\nEnter item number to edit (or 0 to cancel): ").strip()

        if not is_integer(item_num_input):
            print("Invalid input. Please enter a number.")
            continue

        item_num = int(item_num_input)

        if item_num == 0:
            print("Cancel successful!\n")
            input("Press [ENTER] to continue.")
            return False
        
        valid_numbers = [i for i, _ in editable_items]
        
        if item_num not in valid_numbers:
            if len(valid_numbers) == 1:
                print("Invalid item number. Please enter 1")
            else:
                print(f"Invalid item number. Please enter between {valid_numbers[0]} and {valid_numbers[-1]}")
            continue

        selected_item = None
        original_index = 0
        for i, item in editable_items:
            if i == item_num:
                selected_item = item
                original_index = i - 1  
                break

        if not selected_item:
            print("Item not found.")
            continue

        product_id = selected_item.product_id if selected_item.product_id else (
            selected_item.product.product_id if selected_item.product else "")
        
        product = None
        for p in products:
            if p.product_id == product_id:
                product = p
                break

        if not product:
            print("Product not found in inventory.")
            input("Press [ENTER] to continue.")
            return False

        while True:
            print(f"\nCurrent quantity: {selected_item.quantity}")
            print(f"Available stock: {product.stock + selected_item.quantity}\n")
            new_qty_input = input("Enter new quantity (or 0 to remove item): ").strip()

            if not is_integer(new_qty_input):
                print("Invalid input. Please enter a number.")
                continue

            new_qty = int(new_qty_input)

            if new_qty == 0:
                product.stock += selected_item.quantity
                cart.pop(original_index)
                
                if save_cart(cart) and update_product_file():
                    print("Item removed from cart successfully!\n")
                else:
                    product.stock -= selected_item.quantity
                    cart.insert(original_index, selected_item)
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
                    print("\nCart updated successfully!\n")
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

    has_inactive = False
    for item in cart:
        status = item.product.status if item.product else "Active"
        if status == "Inactive":
            has_inactive = True
            break
    
    if has_inactive:
        print("===========================================================================")
        print("|                             PAYMENT ERROR                               |")
        print("===========================================================================")
        print("| Your cart contains inactive/unavailable products.                       |")
        print("| Please remove these items or wait for them to become available          |")
        print("| before proceeding to payment.                                           |")
        print("===========================================================================")
        
        print("\nInactive products in your cart:")
        for i, item in my_enumerate(cart, 1):
            status = item.product.status if item.product else "Active"
            if status == "Inactive":
                print(f"{i}. {item.name} (Product ID: {item.product_id})")

        print(" ____________________________________")
        print("|                                    |")
        print("|    Options:                        |")
        print("|  1. Remove inactive items          |")
        print("|  2. Back to cart                   |")
        print("|  3. Back to main menu              |")
        print("|____________________________________|")
        
        while True:
            choice = input("\nEnter your choice: ")
            if choice == '1':
                items_to_delete = []
                for item in cart:
                    status = item.product.status if item.product else "Active"
                    if status == "Inactive":
                        items_to_delete.append(item)
                
                for item in items_to_delete:
                    for product in products:
                        if product.product_id == item.product_id:
                            product.stock += item.quantity
                            break
                    cart.remove(item)
                
                if save_cart(cart) and update_product_file():
                    print("\nInactive items removed successfully!")
                    input("Press [ENTER] to refresh cart.")
                    display_cart(cart)
                else:
                    print("\nError removing items. Please try again.")
                    input("Press [ENTER] to continue.")
                return
            elif choice == '2':
                display_cart(cart)
                return
            elif choice == '3':
                clear_screen()
                main_menu()
                return
            else:
                print("Invalid choice. Please try again.")
        return
    
    total_payment = 0.00
    
    print("===========================================================================")
    print("|                                 RECEIPT                                 |")
    print("===========================================================================")
    
    payable_items = []
    actual_total = 0.0
    
    for item in cart:
        status = item.product.status if item.product else "Active"
        if status == "Active":
            payable_items.append(item)
            actual_total += item.total
    
    for i, item in my_enumerate(cart, 1):
        status = item.product.status if item.product else "Active"
        
        print(" -------------------------------------------------------------------------")
        print(f"| Item {i:<67}|")
        print(f"| Title    : {item.product.name:<61}|")
        print(f"| Price    : RM {item.price:<58.2f}|")
        print(f"| Quantity : {item.quantity:<61}|")
        
        if status == "Inactive":
            print("| STATUS   : UNAVAILABLE (Not charged)                           |")
            print(f"| Total    : RM 0.00                                             |")
            print(" ---------------------------------------------------------------")
        else:
            print(f"| Total    : RM {item.total:<58.2f}|")
            print(" -------------------------------------------------------------------------")

    print("===========================================================================")
    print(f"| Payment Amount: RM {actual_total:<53.2f}|")
    print("===========================================================================")
    
    if logged_in_member:
        if actual_total >= 100 and actual_total < 120: 
            add_on = 0.00
            proceed = ''
            add_on = 120 - actual_total
            print(f"\nAdd-on RM {add_on:.2f} to get 5% discount!")
            proceed = input("\nEnter [0] to back to product list, enter [1] to proceed the payment: ").strip()
            
            while proceed != '0' and proceed != '1':
                print("Invalid input.")
                proceed = input("Enter 0 to back to product list, 1 to continue proceed to payment: ").strip()
            
            if proceed == '0':
                filter_products(products, cart)
                return
        
        if actual_total >= 120: 
            discount = 0.05
            discount_amount = actual_total * discount
            actual_total -= discount_amount
            print("\nCongratulations, you get 5% discount!")
            print(" _______________________")
            print("|                       |")
            print(f"| Discount: RM {discount_amount:.2f}\t|")
            print(f"| Total   : RM {actual_total:.2f}\t|")
            print("|_______________________|")
    
    payment_method = ''
    print("\nChoose your payment method")
    print("1. Cash")
    print("2. Debit card")
    
    payment_method = input("\nYour choice [0 to cancel payment]: ").strip()
    
    while payment_method != '0' and payment_method != '1' and payment_method != '2':
        payment_method = input("\nInvalid choice. Please enter again: ").strip()
    
    if payment_method == '0':
        print("Back to main menu...")
        input()
        clear_screen()
        main_menu()
    elif payment_method == '1':
        cash_payment(products, payable_items, actual_total)  
    elif payment_method == '2':
        debit_card_payment(payable_items, actual_total)

def debit_card_payment(cart, total_payment):
    card_number = input("\nCredit card number (13-16 digits): ").strip()
    
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
    
    purchase_history(cart, total_payment, "Debit Card")

    cart.clear()
    clear_cart(logged_in_member.member_id)
    
    print("\nYour cart has been cleared.")
    while True:
        more_purchase = input("\nDo you want to make more purchase [Y/N]?: ").strip()
        if more_purchase == 'Y' or more_purchase == 'y': 
            print("\nPress [ENTER] to continue...")
            input()
            clear_screen()
            main_menu()
            break
        elif more_purchase == 'N' or more_purchase == 'n': 
            print("\nPress [ENTER] to log out...")
            input()
            clear_screen()
            login_menu()
            break
        else:
            print("Invalid input. Please enter Y or N.")

def cash_payment(products, cart, total_payment):
    
    while True:
        cash_input = (input("\nCash  : RM ")).strip()
        if len(cash_input) == 0:
                print("Please enter a valid amount.")
                continue

        has_invalid_char = False
        dot_count = 0

        for i in range(len(cash_input)):
            char = cash_input[i]
            if char == '.':
                dot_count += 1
            elif char < '0' or char > '9': 
                has_invalid_char = True
                break

           
        if (has_invalid_char or dot_count > 1
            or (len(cash_input) > 0 and cash_input[0] == '.')
            or (len(cash_input) > 0 and cash_input[len(cash_input) - 1] == '.')):
            print("Only numbers and one decimal point allowed (e.g., 50 or 50.50).")
            continue

        try:
            cash = float(cash_input)
            if cash <= 0:
                print("Amount must be positive.")
            elif cash < total_payment:
                    print("Your cash is not enough!")
            else:
                    break
        except:
            print(" Invalid number format.")
    
    if cash > total_payment:
        change = cash - total_payment
        print(f"Change: RM {change:.2f}")
    
    print("\n\nProcessing payment...", end='')
    print("\n\nPayment successful! Thank you for your purchase.")
    
    purchase_history(cart, total_payment, "Cash")
    cart.clear()
    clear_cart(logged_in_member.member_id)
    
    print("\nYour cart has been cleared.")
    while True:
        more_purchase = input("\nDo you want to make more purchase [Y/N]?: ").strip()
        if more_purchase == 'Y' or more_purchase == 'y': 
            print("\nPress [ENTER] to continue...")
            input()
            clear_screen()
            main_menu()
            break
        elif more_purchase == 'N' or more_purchase == 'n': 
            print("\nPress [ENTER] to log out...")
            input()
            clear_screen()
            login_menu()
            break
        else:
            print("Invalid input. Please enter Y or N.")

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

def purchase_history(cart, total_payment, payment_method):
    global logged_in_member
    
    if not logged_in_member:
        print("Error: No member logged in to record purchase history.")
        return False
    
    if not cart:
        print("Cart is empty. No purchase to record.")
        return False
    
    try:
        from datetime import datetime
        purchase_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order_id = get_order_id()

        with open(PURCHASE_HISTORY_FILE, "a", encoding="utf-8") as file:
            file.write(f"{logged_in_member.member_id},{logged_in_member.full_name},{order_id},{purchase_time},{payment_method}\n")

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
        print("No member logged in to view purchase history.")
        input("Press [ENTER] to continue.")
        return

    try:
        clear_screen()
        print("===========================================================================")
        print("|                           YOUR PURCHASE HISTORY                         |")
        print("===========================================================================")

        if not os.path.exists(PURCHASE_HISTORY_FILE):
            with open(PURCHASE_HISTORY_FILE, "w", encoding="utf-8") as file:
                pass  

        with open(PURCHASE_HISTORY_FILE, "r", encoding="utf-8") as file:
            content = file.read()

        if not content.strip():
            print("|                                                                         |")
            print("|                         No purchase history found.                      |")
            print("|                                                                         |")
            print("===========================================================================")
            input("\nPress [ENTER] to continue.")
            return

        from datetime import datetime
        records = my_split(content.strip(), '\n\n')
        user_records = []

        for record in records:
            if not record.strip():
                continue

            lines = my_split(record.strip(), '\n')
            if len(lines) < 2:
                continue

            header = my_split(lines[0], ',')
            if len(header) < 5:
                continue

            member_id = header[0]
            if member_id != logged_in_member.member_id:
                continue

            try:
                order_id = header[2]
                purchase_time = header[3]
                payment_method = header[4]

                total_line = my_split(lines[-1], ',')
                total_payment = float(total_line[4]) if len(total_line) >= 5 and total_line[3] == "TOTAL" else 0.0

                user_records.append({
                    "lines": lines,
                    "datetime": purchase_time,
                    "datetime_obj": datetime.strptime(purchase_time, "%Y-%m-%d %H:%M:%S"),
                    "total": total_payment,
                    "order_id": order_id,
                    "payment_method": payment_method
                })

            except Exception as e:
                print(f"Error processing record: {e}")
                continue

        if not user_records:
            print("|                                                                         |")
            print("|                No purchase history found for your account.              |")
            print("|                                                                         |")
            print("===========================================================================")
            input("\nPress [ENTER] to return to main menu.")
            clear_screen()
            main_menu()
            return
        
        print("| How would you like to sort your purchase history?                       |")
        print(f"| {'1. By Date/Time (Latest First)':<72}|")
        print(f"| {'2. By Total Purchase Amount (Highest First)':<72}|")
        print(f"| {'3. Back To Main Menu':<72}|")
        print("===========================================================================")

        while True:
            choice = input("\nEnter your choice: ")
            try:
                choice = int(choice)  
                if choice == 3:
                    clear_screen()
                    main_menu()
                    return
                elif choice in (1, 2):
                    record_objects = [PurchaseRecord(rec) for rec in user_records]
                    if choice == 1:
                        bubble_sort(record_objects, key="datetime_obj", reverse=True)
                    elif choice == 2:
                        bubble_sort(record_objects, key="total", reverse=True)

                    user_records = [record.__dict__ for record in record_objects]
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid choice. Please try again.")


        clear_screen()

        print("===========================================================================")
        print("|                           YOUR PURCHASE HISTORY                         |")
        for record in user_records:
            print("===========================================================================")
            print(f"| Purchase Time : {record['datetime']:<56}|")
            print(f"| Payment Method: {record['payment_method']:<56}|")
            print("===========================================================================")

            for line in record["lines"][1:-1]:
                parts = my_split(line, ',')
                if len(parts) < 9:
                    continue

                product_id = parts[3]
                name = parts[4]
                category = parts[5]
                price = float(parts[6])
                quantity = int(parts[7])
                total = float(parts[8])

                print(" -------------------------------------------------------------------------")
                print(f"| Product ID : {product_id:<59}|")
                print(f"| Name       : {name:<59}|")
                print(f"| Category   : {category:<59}|")
                print(f"| Price      : RM {price:<56.2f}|")
                print(f"| Quantity   : {quantity:<59}|")
                print(f"| Total      : RM {total:<56.2f}|")

            print("===========================================================================")
            print(f"| Total Purchase: RM {record['total']:<53.2f}|")
            print("===========================================================================\n")

        input("\nPress [ENTER] to return.")
        clear_screen()
        view_purchase_history()

    except FileNotFoundError:
        print("Purchase history file not found. Creating a new one.")
        open(PURCHASE_HISTORY_FILE, "w", encoding="utf-8").close()
        input("Press [ENTER] to continue.")
        clear_screen()
        main_menu()
    except Exception as e:
        print(f"Error viewing purchase history: {str(e)}")
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
        print("===========================================================================")
        print("|                                  MY CART                                |")
        print("===========================================================================")
        print("|                                                                         |")
        print("|                             Your cart is empty.                         |")
        print("|                                                                         |")
        print("===========================================================================")
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
    
    bubble_sort(cart, key='product_id')

    print("===========================================================================")
    print("|                                 MY CART                                 |")
    print("===========================================================================")
    grand_total = 0.0

    for i, item in my_enumerate(cart, 1):
        pid = item.product_id if item.product_id else (item.product.product_id if item.product else "N/A")
        name = item.name if item.name else (item.product.name if item.product else "N/A")
        category = item.product.category if item.product and item.product.category else "N/A"
        price = item.price if item.price is not None else (item.product.price if item.product else 0.0)
        quantity = item.quantity
        total = item.total if item.total is not None else (price * quantity)
        status = item.product.status if item.product and item.product.status else "N/A"

        print(" -------------------------------------------------------------------------")
        print(f"| Item {str(i) + ':':<67}|")
        print(f"| Product ID : {pid:<59}|")
        print(f"| Name       : {name:<59}|")

        if status=="Inactive":
            total=0.0
            print("| SORRY! This product is currently unavailable :(                         |")
            print(" -------------------------------------------------------------------------")
        else:
            print(f"| Category   : {category:<59}|")
            print(f"| Price      : RM {price:<56.2f}|")
            print(f"| Quantity   : {quantity:<59}|")
            print(f"| Total      : RM {total:<56.2f}|")
            print(" -------------------------------------------------------------------------")
        grand_total += total
    print("===========================================================================")
    print(f"| Total Price: RM {grand_total:<56.2f}|")
    print("===========================================================================\n")

    print(" ____________________________________")
    print("|                                    |")
    print("|    Options:                        |")
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
    if not products:
        if not load_products():
            print("Error: Could not load products.")
            return

    # Sort products by product_id
    bubble_sort(products, key='product_id')

    # Search for product using the correct product_id
    selected_product = jump_search(products, product_id, key='product_id')

    if not selected_product:
        print(f"Error: Product with ID {product_id} not found.")
        return

    if selected_product.status == "Inactive":
        print("Error: This product is currently unavailable.\n")
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

    # Check if item is already in the cart
    bubble_sort(cart, key='product_id')
    item = jump_search(cart, product_id, key='product_id')

    if item:
        if selected_product.stock < item.quantity + quantity:
            print(f"Error: Adding {quantity} would exceed stock.")
            return
        item.quantity += quantity
        item.price = selected_product.price
        item.total = item.quantity * item.price
    else:
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
        # Revert stock if saving failed
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
        print("===========================================================================")
        print("|                        WELCOME TO OUR PASTRY PAN!                       |")
        print("===========================================================================")
        print("| Select a category:                                                      |")
        categories = {
            '1': 'Bread', '2': 'Pastries', '3': 'Cakes', '4': 'Donuts',
            '5': 'Cupcakes & Muffins', '6': 'Cookies', '7': 'Pies & Tarts',
            '8': 'Savories & Sandwiches'
        }
        for key, value in raw_items(categories):
            print(f"| {key}. {value:<69}|")
        print(f"| {'9. Back to Main Menu':<72}|")
        print("===========================================================================")

        choice = input("Enter your choice (1-9): ")
        if choice == '9':
            clear_screen()
            main_menu()
            return
        elif choice not in categories:
            print("Invalid choice. Please try again.\n")
            input("Press [ENTER] to continue.")
            continue

        selected_category = categories[choice]
        while True:
            clear_screen()
            print(f"Products in Category: {selected_category}                ")
            load_products()
            # Only show active products in this category
            filtered = [p for p in products if p.category.lower() == selected_category.lower() and p.status == "Active"]

            if not filtered:
                print(f"\nNo available products found in '{selected_category}' category.")
            else:
                for product in filtered:
                    display_product(product)
            print("\n---------------------------------------------------------------------------")

            print(" _________________________________")
            print("|                                 |")
            print("|    Options:                     |")
            print("| Enter Product ID to add to cart |")
            print("| [C] View Cart                   |")
            print("| [B] Back to Category Selection  |")
            print("| [M] Back to Main Menu           |")
            print("|_________________________________|")

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
            product = jump_search(products, selection, key='product_id')

            if not product:
                print(f"Product with ID '{product_id}' not found.\n")
                input("Press [ENTER] to continue.")
                continue

            # Check if product is inactive
            if product.status == "Inactive":
                print("\nThis product is currently unavailable.\n")
                input("Press [ENTER] to continue.")
                continue

            if product.stock <= 0:
                print("\nSorry, this product is out of stock!\n")
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
                        input("\nPress [ENTER] to continue.")
                        break
                except ValueError:
                    print("Invalid input. Please enter a number.")


# ==========================================VIEW DASHBOARD==========================================
def view_dashboard():
    product_count = 0
    active_product = 0
    inactive_product = 0
    out_of_stock = 0
    
    try:
        with open(PRODUCT_FILE, 'r') as file:
            content = file.read()
            lines = split_lines(content)
            for line in lines:
                line = line.strip()
                if line:
                    product_count += 1
                    parts = my_split(line, ',')
                    if len(parts) >= 6:
                        stock_str = parts[4].strip()    
                        stock = 0
                        is_all_digits = True
                        if stock_str:
                            for ch in stock_str:
                                if not ('0' <= ch <= '9'):
                                    is_all_digits = False
                                    break
                            if is_all_digits:
                                stock = int(stock_str)       
                        
                        status = parts[5].strip()
                        if status == "Active":
                            active_product += 1
                            if stock <= 0:
                                out_of_stock += 1
                        else: 
                            inactive_product += 1
    
    except FileNotFoundError:
        pass
    
    member_count = 0
    active_member = 0
    inactive_member = 0
    
    try:
        with open(MEMBERS_FILE, 'r') as file:
            content = file.read()
            lines = split_lines(content)
            
            member_count = len(lines) // 8
            for i in range(0, len(lines), 9):
                if i + 7 < len(lines) and lines[i+7].strip() == "Active":
                    active_member += 1
                elif i + 7 < len(lines) and lines[i+7].strip() == "Inactive":
                    inactive_member += 1
    except FileNotFoundError:
        pass
    
    order_count = 0
    total_sales = 0.0
    monthly_sale = {"01": 0.0, "02": 0.0, "03": 0.0, "04": 0.0, "05": 0.0, "06": 0.0, "07": 0.0, "08": 0.0, "09": 0.0, "10": 0.0, "11": 0.0, "12": 0.0, }
    month_name = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September" ,"10":"October" ,"11":"November", "12":"December"}
    
    try:
        with open(PURCHASE_HISTORY_FILE, 'r') as file:
            content = file.read()
            records = my_split(content.strip(), delimiter="\n\n")
            for record in records:
                if not record.strip():
                    continue
                lines = my_split(record.strip(), delimiter="\n")
                if len(lines) < 2:
                    continue

                date_line = my_split(lines[0], ',')
                if len(date_line) >= 4:
                    date_part = date_line[3].strip()
                    if len(date_part) >= 7 and date_part[5:7] in monthly_sale:
                        order_month = date_part[5:7]
                    else:
                        order_month = None
                else:
                    order_month = None

                for line in lines:
                    parts = my_split(line, ',')
                    if len(parts) >= 5 and parts[3] == "TOTAL":
                        total_str = parts[4]
                        total = 0.0
                        has_dot = False
                        is_float = True
                        for ch in total_str:
                            if ch == '.':
                                if has_dot:
                                    is_float = False
                                    break
                                has_dot = True
                            elif ch < '0' or ch > '9':
                                is_float = False
                                break
                        if is_float:
                            total = float(total_str)
                            total_sales += total
                            if order_month:
                                monthly_sale[order_month] += total
                            order_count += 1
    except FileNotFoundError:
        pass
    
    clear_screen()
    print("===========================================================================")
    print("|                             ADMIN DASHBOARD                             |")
    print("===========================================================================")
    print("|                                                                         |")
    print(f"| Total Products               : {product_count:<41}|")
    print(f"| Active Products              : {active_product:<41}|")
    print(f"| Inactive Products            : {inactive_product:<41}|")
    print(f"| Out of Stock                 : {out_of_stock:<41}|")
    print("|_________________________________________________________________________|")
    print("|                                                                         |")
    print(f"| Total Members                : {member_count:<41}|")
    print(f"| Active Members               : {active_member:<41}|")
    print(f"| Inactive Members             : {inactive_member:<41}|")
    print("|_________________________________________________________________________|")
    print("|                                                                         |")
    print(f"| Total Orders                 : {order_count:<41}|")
    print(f"| Total Sales                  : RM {total_sales:<38.2f}|")
    print("|_________________________________________________________________________|")
    print("|                                                                         |")
    print("| Monthly Sales Report                                                    |")
    print("|                                                                         |")
    month_keys = raw_keys(month_name)
    bubble_sort(month_keys)
    for key in month_keys:
        name = month_name[key]
        sale = monthly_sale[key]
        print(f"| {name:<71} |")
        print(f"| Sales for this month         : RM {sale:<38.2f}|")
        print("|                                                                         |")
    
    print("===========================================================================")
    input("\nPress [ENTER] to return to admin menu.")
# =======================================END OF VIEW DASHBOARD=======================================

# ===================================VIEW ORDER HISTORY===================================
def view_order_history():
    try:
        member_ids = []
        order_ids = []
        with open(PURCHASE_HISTORY_FILE, "r") as file:
            content = file.read()
            records = my_split(content.strip(), delimiter = "\n\n")
            
            for record in records:
                if not record.strip():
                    continue
                
                lines = my_split(record, '\n')
                if len(lines) >= 1:
                    header = my_split(lines[0], ',')
                    if len(header) >= 3:
                        if header[0] not in member_ids:
                            member_ids.append(header[0])
                        if header[2] not in order_ids:
                            order_ids.append(header[2])
        
        bubble_sort(member_ids)
        bubble_sort(order_ids)
        
        clear_screen()
        print("===========================================================================")
        print("|                    AVAILABLE MEMEBR ID WITH ORDERS                      |")
        print("===========================================================================")
        for member_id in member_ids:
            print(f"| ⨠ {member_id:<70}|")
        print("|_________________________________________________________________________|")
        
        search_id = None
        while True:
            search_input = input("Enter Member ID to filter (or press ENTER for all): ").strip().upper()
            
            if not search_input:
                break
                
            found_member = jump_search(member_ids, search_input)
            
            if found_member:
                search_id = found_member
                break
            else:
                print(f"\nMember ID {search_input} not found in order history.")
                print("___________________________________________________________________________")
                print("| Available Member IDs:                                                   |")
                for member_id in member_ids:
                    print(f"| ⨠ {member_id:<70}|")
                print("|_________________________________________________________________________|")
                continue
        
        search_order_id = None
        if search_id:
            member_order_ids = []
            with open(PURCHASE_HISTORY_FILE, "r") as file:
                content = file.read()
                records = my_split(content.strip(), delimiter="\n\n")
                
                for record in records:
                    if not record.strip():
                        continue
                    
                    lines = my_split(record, '\n')
                    if len(lines) >= 1:
                        header = my_split(lines[0], ',')
                        if len(header) >= 3 and header[0] == search_id:
                            member_order_ids.append(header[2])
            
            if member_order_ids:
                print(" _________________________________________________________________________")
                print("|                                                                         |")
                print(f"| Available Order IDs for {search_id:<48}|")
                for order_id in member_order_ids:
                    print(f"| ⨠ {order_id:<70}|")
                print("|_________________________________________________________________________|")
                
                while True:
                    order_input = input("| Enter Order ID to view order (or press ENTER for all): ").strip().upper()
                    
                    if not order_input:
                        break
                        
                    if order_input in member_order_ids:
                        search_order_id = order_input
                        break
                    else:
                        print(f"\nOrder ID {order_input} not found for this member.")
                        print("Available Order IDs:")
                        for order_id in member_order_ids:
                            print(f"⨠ {order_id}")
                        continue
        
        with open(PURCHASE_HISTORY_FILE, "r") as file:
            content = file.read()
            
        if not content:
            print("\nNo purchase history found.")
            input("\nPress [ENTER] to continue")
            return
        
        records = my_split(content.strip(), delimiter="\n\n")
        found_orders = False
        
        for record in records:
            if not record.strip():
                continue
            
            lines = my_split(record, '\n')
            if len(lines) < 2:
                continue
            
            header = my_split(lines[0], ',')
            if len(header) < 5:
                continue
            
            member_id = header[0]
            order_id = header[2]
            
            if search_id and member_id != search_id:
                continue
                
            if search_order_id and order_id != search_order_id:
                continue
                
            found_orders = True
            member_name = header[1]
            purchase_time = header[3]
            payment_method = header[4]
            
            print("\n _________________________________________________________________________")
            print("|                                                                         |")
            print(f"| Member ID       : {member_id:<54}|")
            print("|_________________________________________________________________________|")
            print(f"| Name            : {member_name:<54}|")
            print(f"| Order ID        : {order_id:<54}|")
            print(f"| Date n Time     : {purchase_time:<54}|")
            print(f"| Payment         : {payment_method:<54}|")
            print("|_________________________________________________________________________|")
            
            total_payment = 0.0
            has_discount = False
            
            for line in lines[1:-1]:
                parts = my_split(line, ',')
                if len(parts) < 9:
                    continue
                
                product_id   = parts[3]
                product_name = parts[4]
                category     = parts[5]
                price        = parts[6]
                quantity     = parts[7]
                total        = parts[8]
                
                print(f"| Product ID      : {product_id:<54}|")
                print(f"| Product Name    : {product_name:<54}|")
                print(f"| Category        : {category:<54}|")
                print(f"| Price           : RM {price:<51}|")
                print(f"| Quantity        : {quantity:<54}|")
                print(f"| Total           : RM {total:<51}|")
                print(" -------------------------------------------------------------------------")
                
                total_float = 0.0
                is_float = True
                has_decimal = False
                for ch in total:
                    if ch == '.':
                        if has_decimal:
                            is_float = False
                            break
                        has_decimal = True
                    elif ch < '0' or ch > '9':
                        is_float = False
                        break
                if is_float:
                    total_float = float(total)
                
                total_payment += total_float
                
                if total_float > 120.00:
                    has_discount = True
            
            total_line = my_split(lines[-1], ',')
            if len(total_line) >= 5 and total_line[3] == "TOTAL":
                total_str = total_line[4]
                total_payment = 0.0
                is_float = True
                has_decimal = False
                for ch in total_str:
                    if ch == '.':
                        if has_decimal:
                            is_float = False
                            break
                        has_decimal = True
                    elif ch < '0' or ch > '9':
                        is_float = False
                        break
                if is_float:
                    total_payment = float(total_str)
            
            if has_discount:
                print(f"| {'Total Purchase: RM ' + f'{total_payment:.2f}' + ' [after 5% discount]':<72}|")
            else:
                print(f"| Total Purchase: RM {total_payment:<53.2f}|")
            print("===========================================================================")
        if (search_id or search_order_id) and not found_orders:
            if search_order_id:
                print(f"\nNo orders found with Order ID: {search_order_id}")
            else:
                print(f"\nNo orders found for Member ID: {search_id}")
            
        input("\nPress [ENTER] to return to admin menu.")
        
    except FileNotFoundError:
        print("\nOrder history file not found.")
        input("Press [ENTER] to continue")
# ===================================END OF VIEW ORDER HISTORY===================================

# =======================================VIEW SALES REPORT=======================================
def view_sales_report():
    category_sales = {}
    category_count = {}
    
    try:
        products = {}
        with open(PRODUCT_FILE, 'r') as file:
            content = file.read()
            lines = split_lines(content)
            for line in lines:
                line = line.strip()
                if line:
                    parts = my_split(line, ',')
                    if len(parts) >= 3:
                        product_id = parts[0]
                        name = parts[1]
                        category = parts[2]
                        products[product_id] = (name, category)
        
        with open(PURCHASE_HISTORY_FILE, 'r') as file:
            content = file.read()
            records = my_split(content.strip(), delimiter="\n\n")

            for record in records:
                if not record.strip():
                    continue
                
                lines = my_split(record, '\n')
                if len(lines) < 2:
                    continue
                
                for line in lines[1:-1]:
                    parts = my_split(line, ',')
                    if len(parts) >= 9:
                        product_id = parts[3]
                        quantity_str = parts[7]
                        total_str = parts[8]
                        
                        quantity = 0
                        is_digit = True
                        for ch in quantity_str:
                            if ch < '0' or ch > '9':
                                is_digit = False
                                break
                        if is_digit:
                            quantity = int(quantity_str)
                        
                        total = 0.0
                        is_float = True
                        has_decimal = False
                        for ch in total_str:
                            if ch == '.':
                                if has_decimal:
                                    is_float = False
                                    break
                                has_decimal = True
                            elif ch < '0' or ch > '9':
                                is_float = False
                                break
                        if is_float:
                            total = float(total_str)
                        
                        if product_id in products:
                            category = products[product_id][1]
                            if category not in category_sales:
                                category_sales[category] = 0.0
                                category_count[category] = 0
                            category_sales[category] += total
                            category_count[category] += quantity
                            
        clear_screen()
        print("===========================================================================")
        print("|                             SALES REPORT                                |")
        print("===========================================================================")
        
        if not category_sales:
            print("No sales data available.")
        else:
            sorted_category = []
            for category in category_sales:
                inserted = False
                for i in range(len(sorted_category)):
                    if category_sales[category] > category_sales[sorted_category[i]]:
                        sorted_category.insert(i, category)
                        inserted = True
                        break
                if not inserted:
                    sorted_category.append(category)
                    
            for category in sorted_category:
                print(f"| Category: {category:<62}|")
                print(f"| Items Sold: {category_count[category]:<60}|")
                print(f"| Total Sales: RM {category_sales[category]:<56.2f}|")
                print("---------------------------------------------------------------------------")
            
        print("===========================================================================")
        input("\nPress [ENTER] to return to admin menu.")
        
    except FileNotFoundError:
        print("Required data files not found.")
        input("Press [ENTER] to continue.")
# ====================================END OF VIEW SALES REPORT===================================

# =======================================MANAGE MEMBER LIST======================================
def manage_member():
    while True:
        clear_screen()
        print("===========================================================================")
        print("|                            MANAGE MEMBER LIST                           |")      
        print("===========================================================================")
        print("| [1] View Active Members                                                 |")
        print("| [2] View Inactive Members                                               |")
        print("| [3] Change Member Status                                                |")
        print("| [4] Return to Admin Menu                                                |")
        print("===========================================================================")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            view_member_list("Active")
        elif choice == '2':
            view_member_list("Inactive")
        elif choice == '3':
            change_member_status()
        elif choice == '4':
            return
        else:
            input("Invalid choice, Press [ENTER] to try again. ")

def view_member_list(status_filter):
    try:
        members = []
        with open(MEMBERS_FILE, 'r') as file:
            lines = []
            for line in file:
                line = line.strip()
                if line:
                    lines.append(line)
            
            for i in range(0, len(lines), 8):
                if i + 7 < len(lines):
                    member = Member(
                        member_id=lines[i],
                        full_name=lines[i+1],
                        email=lines[i+2],
                        password=lines[i+3],
                        age=lines[i+4],
                        gender=lines[i+5],
                        contact=lines[i+6],
                        status=lines[i+7]
                    )
                    members.append(member)
        
        filtered_members = []
        for m in members:
            if m.status == status_filter:
                filtered_members.append(m)
        
        clear_screen()
        if status_filter == "Active":
            print("===========================================================================")
            print("|                         ACTIVE MEMBER LIST                              |")      
        else:
            print("===========================================================================")
            print("|                          INACTIVE MEMBER LIST                           |")      
        print("===========================================================================")
                
        if not filtered_members:
            print("|                                                                         | ")
            print(f"|                      No {status_filter.lower()+' members found.':<48}|")
            print("|                                                                         | ")
            print("---------------------------------------------------------------------------")
            input("\nPress [ENTER] to continue.")
            return
        
        for member in filtered_members:
            print(f"| Member ID         : {member.member_id:<52}|")
            print(f"| Name              : {member.full_name:<52}|")
            print(f"| Email             : {member.email:<52}|")
            print(f"| Age               : {member.age:<52}|")
            print(f"| Gender            : {member.gender:<52}|")
            print(f"| Contact           : {member.contact:<52}|")
            print("---------------------------------------------------------------------------")
        
        while True:
            search_choice = input("\nDo you want to search member by ID? (Y/N to return): ").upper().strip()
            
            if search_choice == 'N':
                return
            
            if search_choice == 'Y':
                bubble_sort(filtered_members, key='member_id')
                
                while True:
                    search_id = input("\nEnter Member ID to search (or 'C' to cancel): ").strip().upper()
                    
                    if search_id == 'C':
                        break
                    
                    found_member = jump_search(filtered_members, search_id, key='member_id')
                    
                    if found_member:
                        clear_screen()
                        print("===========================================================================")
                        print("|                                MEMBER DETAILS                           |")
                        print("===========================================================================")
                        print(f"| Member ID         : {found_member.member_id:<52}|")
                        print(f"| Name              : {found_member.full_name:<52}|")
                        print(f"| Email             : {found_member.email:<52}|")
                        print(f"| Age               : {found_member.age:<52}|")
                        print(f"| Gender            : {found_member.gender:<52}|")
                        print(f"| Contact           : {found_member.contact:<52}|")
                        print(f"| Status            : {found_member.status:<52}|")
                        print("===========================================================================")
                        input("\nPress [ENTER] to continue.")
                        break
                    else:
                        print(f"Member with ID {search_id} not found in {status_filter.lower()} members.")
                        continue
                
                clear_screen()
                break
            
            print("Invalid choice. Please enter Y (Yes), or N (No).")
            continue
            
    except FileNotFoundError:
        print("Member file not found.")
        input("Press [ENTER] to continue.")
        return

def change_member_status():
    try:
        clear_screen()
        print("===========================================================================")
        print("|                                 MEMBER LIST                             |")
        print("===========================================================================")
        print("| ID                 | Name                          | Status             |")
        print("===========================================================================")

        # Read member data manually
        with open(MEMBERS_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
            
        members_data = []
        current_member = []
        blank_line_count = 0
        
        for char in content:
            if char == '\n':
                blank_line_count += 1
                if blank_line_count == 2:
                    if current_member:
                        members_data.append(join_strings("", current_member))
                        current_member = []
                    blank_line_count = 0
            else:
                if blank_line_count == 1:
                    current_member.append('\n')
                    blank_line_count = 0
                current_member.append(char)
        
        if current_member:
            members_data.append(join_strings("", current_member))

        # Display all members
        for member_data in members_data:
            fields = split_lines(member_data)
            if len(fields) >= 8:
                member_id = fields[0]
                full_name = fields[1]
                status = fields[7]
                print(f"| {member_id:<18} | {full_name:<29} | {status:<18} |")

        print("===========================================================================")

        while True:
            chosen_id = input("\nEnter Member ID to change status (or 'C' to cancel): ").strip().upper()
            if chosen_id == 'C':
                print("\nOperation cancelled.")
                input("Press [ENTER] to continue.")
                return

            # Check if ID exists
            found = False
            for member_data in members_data:
                fields = split_lines(member_data)
                if fields and fields[0] == chosen_id:
                    found = True
                    break

            if not found:
                print(f"\nError: Member ID '{chosen_id}' not found. Please try again.")
                continue

            break
        
        print("___________________________________________________________________________")

        # Update status
        updated_members_data = []
        for member_data in members_data:
            fields = split_lines(member_data)
            if fields and fields[0] == chosen_id:
                current_status = fields[7]
                new_status = "Inactive" if current_status == "Active" else "Active"
                fields[7] = new_status
                updated_members_data.append(join_strings("\n", fields))
                print(f"\nMember {chosen_id} status changed from {current_status} to {new_status}.")
            else:
                updated_members_data.append(member_data)

        # Save changes
        with open(MEMBERS_FILE, 'w', encoding='utf-8') as file:
            file.write(join_strings("\n\n", updated_members_data))

        print("\n===========================================================================")
        input("Press [ENTER] to continue.")

    except FileNotFoundError:
        print("Member file not found.")
        input("Press [ENTER] to continue.")
        
# ===================================END OF MANAGE MEMBER LIST===================================

# ========================================VIEW ADMIN LIST========================================
def manage_admin():
    global logged_in_admin
    
    while True:
        clear_screen()
        print("===========================================================================")
        print("|                              MANAGE ADMIN LIST                          |")
        print("===========================================================================")
        print("| [1] View Active Admins                                                  |")
        print("| [2] View Inactive Admins                                                |")
        
        if logged_in_admin.position == "superadmin":
            print("| [3] Add New Admin                                                       |")
            print("| [4] Change Admin Status                                                 |")
            print("| [5] Return to Admin Menu                                                |")
            max_choice = '5'
        else: 
            print("| [3] Return to Admin Menu                                                |")
            max_choice = '3'
        print("===========================================================================")
        
        choice = input("Enter yout choice: ")
        if choice == '1':
            view_admin_list("Active")
        elif choice == '2':
            view_admin_list("Inactive")
        elif choice == '3' and logged_in_admin.position == "superadmin":
            add_new_admin()
        elif choice == '4' and logged_in_admin.position == "superadmin":
            change_admin_status()
        elif (choice == '3' and logged_in_admin.position != "superadmin") or (choice == '5' and logged_in_admin.position == "superadmin"):
            return
        else:
            input("Invalid choice, Press [ENTER] to try again.")
            
def view_admin_list(status_filter):
    try:
        admins = []
        with open(ADMINS_FILE, 'r') as file:
            lines = []
            for line in file:
                line = line.strip()
                if line:
                    lines.append(line)
                    
            for i in range(0, len(lines), 5):
                if i + 4 < len(lines):
                    try:
                        admin = Admin(
                            name=lines[i],
                            password=lines[i+1],
                            contact=lines[i+2],
                            position=lines[i+3],
                            status=lines[i+4]                        
                        )
                        admins.append(admin)
                    except ValueError as e:
                        print(f"Error creating admin from line {i}: {e}")
                        continue
                    
        filtered_admins = []
        for a in admins:
            if a.status == status_filter:
                filtered_admins.append(a)    
                
        clear_screen()
        if status_filter == "Active":
            print("===========================================================================")
            print("|                             ACTIVE ADMIN LIST                           |")
        elif status_filter == "Inactive":
            print("===========================================================================")
            print("|                            INACTIVE ADMIN LIST                          |")        
        print("===========================================================================")
        
        if not filtered_admins:
            print("|                                                                         | ")
            print(f"|                      No {status_filter.lower()+' admins found.':<48}|")
            print("|                                                                         | ")
            print("---------------------------------------------------------------------------")
        else:
            for admin in filtered_admins:
                print(f"| Name              : {admin.name:<52}|")    
                print(f"| Position          : {admin.position:<52}|")    
                print(f"| Contact           : {admin.contact:<52}|")  
                print("---------------------------------------------------------------------------")

            search_choice = input("\nDo you want to search admin by name? (Y/N): ").upper()
            if search_choice == 'Y':
                bubble_sort(filtered_admins, key='name')
                
                search_name = input("\nEnter Admin Name to search: ").strip()
                found_admin = jump_search(filtered_admins, search_name, key='name')
                
                if found_admin:
                    clear_screen()
                    print("===========================================================================")
                    print("|                               ADMIN DETAILS                             |")
                    print("===========================================================================")
                    print(f"| Name              : {found_admin.name:<52}|")
                    print(f"| Position          : {found_admin.position:<52}|")
                    print(f"| Contact           : {found_admin.contact:<52}|")
                    print(f"| Status            : {found_admin.status:<52}|")
                    print("===========================================================================")
                else:
                    print(f"Admin with name '{search_name}' not found in {status_filter.lower()} admins.")
                input("\nPress [ENTER] to continue.")
                return
        input("\nPress [ENTER] to continue")
    except FileNotFoundError:
        print("Admin file not found.")
        input("Press [ENTER] to continue.")

def add_new_admin():       
    clear_screen()
    print("===========================================================================")
    print("|                            ADD NEW ADMIN                                |")
    print("===========================================================================")
    print("| Requirment:                                                             |")
    print("| -> Name cannot be same                                                  |")
    print("| -> Password need at least 8 chars                                       |")
    print("| -> Password need one uppercase, lowercase, number                       |")
    print("| -> Contact format: 012-3456789 or 012-34567890                          |")
    print("===========================================================================")
    
    while True:
        name = input("Enter admin name (or 'C' to cancel): ").strip()
        if name.upper() == 'C':
            print("\nOperation cancelled.")
            input("Press [ENTER] to continue.")
            return
        
        if not name:
            print("Name cannot be empty.")
            continue
        
        try:
            with open(ADMINS_FILE, 'r') as file:
                content = file.read()
                if f"\n{name}\n" in content or content and content[0:len(name)+1] == name + "\n":
                    print("Name already exists.")
                    continue
        except FileNotFoundError:
            pass
        
        break
    
    while True:
        password = input("\nEnter password: ").strip()
        if len(password) < 8:
            print("Password must be at least 8 characters.")
            continue
        
        upper = False
        lower = False
        digit = False
        
        for char in password:
            if 'A' <= char <= 'Z':
                upper = True
            elif 'a' <= char < 'z':
                lower = True
            elif '0' <= char <= '9':
                digit = True 
                
        if not (upper and lower and digit):
              print("Password must contain at least one uppercase letter, one lowercase letter, and one number.")
              continue
          
        confirm = input("\nConfirm password: ").strip()
        if password != confirm:
            print("Password doesn't match.")
            continue
        
        break
    
    while True:
        contact = input("\nEnter contact number: ").strip()
        if len(contact) < 4 or contact[3] != '-':
            print("Format must be like 012-3456789 with a '-' .")
            continue
        
        part1 = contact[:3]
        part2 = contact[4:]
        
        if not (part1[0] == '0' and part1[1] == '1'):
            print("Phone number must start with '01'.")
            continue
        
        valid = True
        for c in part1 + part2:
            if not ('0' <= c <= '9'):
                valid = False
                break
        
        if not valid:
            print("Phone number can only contain digits and dash.")
            continue
        
        if len(part1 + part2) not in [10, 11]:
            print("Phone number must be 10 or 11 digits total.")
            continue
        
        break        

    position = "admin"
    status = "Active"
    
    try:
        with open(ADMINS_FILE, 'a') as file:
            file.write(f"\n\n{name}\n{password}\n{contact}\n{position}\n{status}")
            
            print(f"\nAdmin {name} added successfully!\n")
            input("Press [ENTER] to continue. ")
    except Exception as e:
        print(f"Error addinf admin: {e}")
        input("Press [ENTER] to continue. ")
            
            
def change_admin_status():
    global logged_in_admin
    
    try:
        clear_screen()
        print("===========================================================================")
        print("|                               ADMIN LIST                                |")
        print("===========================================================================")
        print("| Name                  | Position              | Status                  |")
        print("===========================================================================")
        
        # Read admin data manually
        with open(ADMINS_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
            
        admins_data = []
        current_admin = []
        blank_line_count = 0
        
        for char in content:
            if char == '\n':
                blank_line_count += 1
                if blank_line_count == 2:
                    if current_admin:
                        admins_data.append(join_strings("", current_admin))
                        current_admin = []
                    blank_line_count = 0
            else:
                if blank_line_count == 1:
                    current_admin.append('\n')
                    blank_line_count = 0
                current_admin.append(char)
        
        if current_admin:
            admins_data.append(join_strings("", current_admin))

        # Display all admins
        for admin_data in admins_data:
            fields = split_lines(admin_data)
            if len(fields) >= 5:
                name = fields[0]
                position = fields[3]
                status = fields[4]
                print(f"| {name:<22}| {position:<22}| {status:<24}|")

        print("===========================================================================")
        
        while True:
            name = input("| Enter admin name to change status (or 'C' to cancel): ").strip()
            
            if name.upper() == 'C':
                print("\nOperation cancelled")
                input("Press [ENTER] to continue. ")
                return
            
            if name == logged_in_admin.name and logged_in_admin.position == "superadmin":
                print("ERROR: Superadmin cannot change their own status.")
                input("Press [ENTER] to continue. ")
                return
            
            # Check if name exists
            found = False
            for admin_data in admins_data:
                fields = split_lines(admin_data)
                if fields and fields[0] == name:
                    found = True
                    break
            
            if not found:
                print(f"\nError: Admin '{name}' not found. Please try again.")
                continue
            
            break
        
        print("===========================================================================")
        
        # Update status
        updated_admins_data = []
        for admin_data in admins_data:
            fields = split_lines(admin_data)
            if fields and fields[0] == name:
                current_status = fields[4]
                new_status = "Inactive" if current_status == "Active" else "Active"
                fields[4] = new_status
                updated_admins_data.append(join_strings("\n", fields))
                print(f"Admin '{name}' status changed from {current_status} to {new_status}.")
            else:
                updated_admins_data.append(admin_data)
        
        # Save changes
        with open(ADMINS_FILE, 'w', encoding='utf-8') as file:
            file.write(join_strings("\n\n", updated_admins_data))
        
        input("Press [ENTER] to continue. ")
        
    except FileNotFoundError:
        print("Admin file not found.")
        input("Press [ENTER] to continue.")   
# ====================================END OF VIEW ADMIN LIST=====================================

def main_menu():
    global logged_in_member
    if not logged_in_member:
        return

    while True:
        clear_screen()
        print("===========================================================================")
        print(f"|                            Welcome {logged_in_member.full_name + ' !':<37}|")
        print("===========================================================================")
        print("|                               Main Menu                                 |")
        print("===========================================================================")
        print("| 1. Browse Products                                                      |")
        print("| 2. View My Cart                                                         |")
        print("| 3. My Profile                                                           |")
        print("| 4. Purchase History                                                     |")
        print("| 5. Rate Our System                                                      |")
        print("| 6. Log Out                                                              |")
        print("===========================================================================")

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
            feedback_rating()
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