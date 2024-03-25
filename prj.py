import time 

from colorama import Fore

import json 

#########################################################


#########################################################

def read_or_write_box(mode: str="read", dictionary: dict={}):
    
    if mode == "read":
        with open("box.json") as F:
            Dict = json.load(F)
        
        return Dict
    
    elif mode == "write":
        with open("box.json", "w") as F:
            json.dump(dictionary, F)

#########################################################

def read_or_write_inventory(mode: str="read", dictionary: dict={}):
    
    if mode == "read":
        with open("data.json") as F:
            Dict = json.load(F)
        
        return Dict
    
    elif mode == "write":
        with open("data.json", "w") as F:
            json.dump(dictionary, F)
        


#########################################################

def change_password():
    
    Dict = read_or_write_admin_data()
    
    old_password = input("Enter your old password: ")
    
    if old_password == Dict["password"]:
        
        new_password = input("Enter your new password: ")
        
        if check_password(new_password):
            
            Dict["password"] = new_password
            
            read_or_write_admin_data("write", Dict)
            
            print(Fore.GREEN + "\nyour password successfully changed.\n" + Fore.RESET)
        
        else:
            print(Fore.RED + "\nyour new password didn't set because it is not secure.\n" + Fore.RESET)
    
    else:
        print(Fore.RED + "\nyou didn't entered old password correctly\n" + Fore.RESET)
    
#########################################################

def add_product():
    
    product_name = input("Enter the name of product: ")
    
    product_buy_price = int(input(f"Enter the price of '{product_name}' that you bought: "))
    
    product_sell_price = int(input(f"Enter the price of '{product_name}' that you want to sell: "))
    
    product_quantity = int(input(f"Enter the quantity of the '{product_name}': "))
    
    Dict = read_or_write_admin_data()
    
    money = product_quantity * product_buy_price
    
    if money <= Dict["balance"]:
        
        new_balance = Dict["balance"] - money
        
        Dict["balance"] = new_balance
        
        with open("admin_data.json", "w") as F:
            json.dump(Dict, F)
        
        Dict = read_or_write_inventory()
        
        Dict[product_name] = {"buy":product_buy_price,
                              "price":product_sell_price,
                              "quantity":product_quantity}
        
        read_or_write_inventory("write", Dict)
        
        print(Fore.GREEN + f"\nYour product ({product_name}) successfully added .\n" + Fore.RESET)
        print(Fore.GREEN + f"you spend {money}$ . your remain balance: {new_balance}$\n" + Fore.RESET)
        
    else:
        print(Fore.RED + f"\nout of balance ! your current balance is: {Dict['balance']}$ .\n" + Fore.RESET) 
    
    
    

#########################################################

def remove_product():
    
    product_name = input("Enter the name of product that you want to remove: ")
    
    Dict = read_or_write_inventory()
    
    admin_dict = read_or_write_admin_data()
    
    if product_name in Dict:
        
        money = Dict[product_name]["quantity"]*Dict[product_name]["buy"]
        
        admin_dict["balance"] += money 
        
        read_or_write_admin_data("write", admin_dict)
        
        Dict.pop(product_name)
        
        read_or_write_inventory("write", Dict)
        
        print(Fore.GREEN + f"\nproduct '{product_name}' successfully removed from inventory.\n" + Fore.RESET)
        
    else:
        print(Fore.RED + f"\nproduct '{product_name}' is not available.\n" + Fore.RESET)
    

#########################################################

def change_quantity():
    
    product_name = input("Enter the name of product that you want to increase/decrease quantity: ")
    
    Dict = read_or_write_inventory()
    
    admin_dict = read_or_write_admin_data()
    
    if product_name in Dict:
        
        string = input("1. increase or 2. decrease ? ")
        
        if string in ["increase", "1"]:
            x = int(input("Enter the quantity that you want to increase: ")) 
            
            if x*Dict[product_name]["buy"] <= admin_dict["balance"]:
                Dict[product_name]["quantity"] += x 
                admin_dict["balance"] -= x*Dict[product_name]["buy"]
                read_or_write_inventory("write", Dict)
                read_or_write_admin_data("write", admin_dict)
                print(Fore.GREEN + f"\n'{product_name}' successfully increased.\n" + Fore.RESET)
            
            else:
                print(Fore.RED + f"\nout of balance. \ncurrent balance: {admin_dict['balance']}$\nneeded balance: {x*Dict[product_name]['buy']}\n" + Fore.RESET)
                
        elif string in ["decrease", "2"]:
            x = int(input("Enter the quantity that you want to decrease: "))
            
            if x <= Dict[product_name]["quantity"]:
                Dict[product_name]["quantity"] -= x 
                admin_dict["balance"] += x*Dict[product_name]["buy"]
                read_or_write_admin_data("write", admin_dict)
                read_or_write_inventory("write", Dict)
                print(Fore.GREEN + f"\n'{product_name}' successfully decreased.\n" + Fore.RESET)
                
            else:
                print(Fore.RED + f"\nwe dont have enough quantity of '{product_name}'. we have just: {Dict[product_name]['quantity']}\n" + Fore.RESET)
            
        
        else:
            print(Fore.RED + "\ninvalid input.\n" + Fore.RESET)
    
    else:
        print(Fore.RED + f"\nproduct '{product_name}' is not available.\n" + Fore.RESET)
    

#########################################################

def inventory(user: str="user"):
    
    Dict = read_or_write_inventory()
    
    print(Fore.GREEN + "\n*** inventory ***\n" + Fore.RESET)
    
    for key, value in Dict.items():
        
        print("product name:", key)
        print("quantity:", value["quantity"])
        print("price:", value["price"])
        if user == "admin":
            print("buy:", value["buy"])
        print("\n--------------\n")
        
#########################################################

def change_price():
    
    product_name = input("Enter the name of product that you want to change price: ")
    
    Dict = read_or_write_inventory()
    
    if product_name in Dict:
        new_price = int(input(f"Enter the new price of {product_name}: "))
        Dict[product_name]["price"] = new_price
        read_or_write_inventory("write", Dict)
        print(Fore.GREEN + f"\n'{product_name}' price successfully changed.\n" + Fore.RESET)
    
    else:
        print(Fore.RED + f"\nproduct '{product_name}' is not available.\n" + Fore.RESET)
    
#########################################################

def check_password(string: str) -> bool:
    
    lower_case, upper_case, digit_case, other_case = (0, 0, 0, 0)
    
    for ch in string:
        if ch.isupper():
            upper_case += 1
            
        elif ch.islower():
            lower_case += 1
        
        elif ch.isdigit():
            digit_case += 1
        
        else:
            other_case += 1
    
    if len(string) in range(8, 19):
        
        if (upper_case >= 1) and (lower_case >= 1) and (digit_case >= 1) and (other_case >= 1):
            return True
        
        else:
            return False

    else:
        return False
    

#########################################################

def read_or_write_admin_data(mode: str="read", dictionary: dict={}):
    
    if mode == "read":
        with open("admin_data.json") as F:
            Dict = json.load(F)
        
        return Dict
    
    elif mode == "write":
        
        with open("admin_data.json", "w") as F:
            json.dump(dictionary, F)
        
            
#########################################################

def get_password():
    
    global last_login_time
    
    Dict = read_or_write_admin_data()
    
    real_password = Dict["password"]
    
    counter = 3 
    
    while counter != 0:
        
        Pass = input("Enter your password: ")
        counter -= 1
        
        if Pass == real_password:
            print(Fore.GREEN + "\ncorrect password. welcome\n" + Fore.RESET)
            return True
            
        else:
            print(Fore.RED + f"\nincorrect password. you can try just {counter} time(s)\n" + Fore.RESET)
    
    last_login_time = time.time()
    return False

#########################################################

def add_to_box():
    
    box = read_or_write_box()
    Dict = read_or_write_inventory()
    
    
    inventory()
    
    product_name = input("Enter the name of product that you want to buy: ")
    
    if product_name in Dict:
        
        product_quantity = int(input(f"Enter the quantity of '{product_name}' that you want: "))
        
        if product_quantity <= Dict[product_name]["quantity"]:
            
            box[product_name] = {"quantity":product_quantity, "price":Dict[product_name]["price"]}
            Dict[product_name]["quantity"] -= product_quantity
            
            read_or_write_box("write", box)
            read_or_write_inventory("write", Dict)
            
            print(Fore.GREEN + f"\n'{product_name}' successfully added to your box.\n" + Fore.RESET)
        
        else:
            print(Fore.RED + f"\nwe dont have enough quantity of '{product_name}'. we have just: {Dict[product_name]['quantity']}\n" + Fore.RESET)
    
    else:
        print(Fore.RED + f"\nproduct '{product_name}' is not available.\n" + Fore.RESET)

#########################################################

def remove_from_box(product_name: str="", mode: str="default"):
    
    box = read_or_write_box()
    Dict = read_or_write_inventory()
    
    if mode == "default":
        product_name = input("Enter the name of product that you want to buy: ")
    
    if product_name in box:
        
        Dict[product_name]["quantity"] += box[product_name]["quantity"]
        
        box.pop(product_name)
        
        read_or_write_box("write", box)
        read_or_write_inventory("write", Dict)
    
    else:
        print(Fore.RED + f"\nproduct '{product_name}' is not available in your box.\n" + Fore.RESET)

#########################################################

def incr_decr_product():
    
    box = read_or_write_box()
    Dict = read_or_write_inventory()
    
    product_name = input("Enter the name of product that you want to increase/decrease the quantity: ")
    
    if product_name in box:
        
        string = input("1. increase / 2. decrease: ")
        
        if string in ["increase", "1"]:
            
            x = int(input("Enter the quantity that you want to increase: ")) 
            
            if x <= Dict[product_name]["quantity"]:
                
                box[product_name]["quantity"] += x 
                Dict[product_name]["quantity"] -= x
                read_or_write_inventory("write", Dict)
                read_or_write_box("write", box)
                print(Fore.GREEN + f"\n'{product_name}' successfully increased to your box.\n" + Fore.RESET)
            
            else:
                print(Fore.RED + f"\nwe dont have enough quantity of '{product_name}'. we have just: {Dict[product_name]['quantity']}\n" + Fore.RESET)
                
        elif string in ["decrease", "2"]:
            
            x = int(input("Enter the quantity that you want to decrease: "))
            
            if x <= box[product_name]["quantity"]:
                
                Dict[product_name]["quantity"] += x 
                box[product_name]["quantity"] -= x
                read_or_write_box("write", box)
                read_or_write_inventory("write", Dict)
                print(Fore.GREEN + f"\n'{product_name}' successfully decreased from your box.\n" + Fore.RESET)
                
            else:
                print(Fore.RED + f"\nyou dont have enough quantity of '{product_name}'. you have just: {box[product_name]['quantity']}\n" + Fore.RESET)
            
        
        else:
            print(Fore.RED + "\ninvalid input.\n" + Fore.RESET)
        
    
    else:
        print(Fore.RED + f"\nproduct '{product_name}' is not available in your box.\n" + Fore.RESET)

#########################################################

def check_box():
    
    box = read_or_write_box()
    
    print(Fore.GREEN + "\n*** box ***\n" + Fore.RESET)
    
    for key, value in box.items():
        
        print("product name:", key)
        print("quantity:", value["quantity"])
        print("price:", value["price"])
        
        print("\n--------------\n")

#########################################################

def accept_box():
    
    box = read_or_write_box()
    list_of_products = list(box)
    admin_dict = read_or_write_admin_data()
    
    string = input("do you want to accept your box(yes/no): ").lower()
    
    if string == "yes":
        
        Sum = 0
        
        for key, value in box.items():
            
            Sum += value["quantity"]*value["price"]
            
        admin_dict["balance"] += Sum
        
        read_or_write_box("write")
        
        read_or_write_admin_data("write", admin_dict)
        
        print(Fore.GREEN + "\npurches successfully completed.\n" + Fore.RESET)
        
    
    elif string == "no":
        print(Fore.GREEN + "\nok. have a good time.\n" + Fore.RESET)
        for name in list_of_products:
            remove_from_box(name, "custom")
    
    else:
        print(Fore.RED + "\ninvalid input.\n" + Fore.RESET)
        
    
    

#########################################################

def admin_panel():
    
    while True:
        
        print("admin menu:\n")
        print("1- change password")
        print("2- add product")
        print("3- remove product")
        print("4- increase/decrease product quantity")
        print("5- inventory")
        print("6- change price")
        print("7- log out\n")
        
        option = input("Enter your option: ")
        
        if option == "1":
            change_password()
        
        elif option == "2":
            add_product()
        
        elif option == "3":
            remove_product()
        
        elif option == "4":
            change_quantity()
        
        elif option == "5":
            inventory("admin")
        
        elif option == "6":
            change_price()
        
        elif option == "7":
            print(Fore.GREEN + "\nlog out successfully\n" + Fore.RESET)
            return None
        
        else:
            print(Fore.RED + "\n\n* invalid option. try again. *\n\n" + Fore.RESET)
        
        
#########################################################

def user_panel():
    
    while True:
        
        print("user menu:\n")
        print("1- inventory")
        print("2- add product to box")
        print("3- remove product from box")
        print("4- increase/decrease product to/from box")
        print("5- check the box")
        print("6- accept the purches")
        print("7- log out\n")
        
        option = input("Enter your option: ")
        
        if option == "1":
            inventory()
        
        elif option == "2":
            add_to_box()
        
        elif option == "3":
            remove_from_box()
        
        elif option == "4":
            incr_decr_product()
        
        elif option == "5":
            check_box()
        
        elif option == "6":
            accept_box()
        
        elif option == "7":
            print(Fore.GREEN + "\nlog out successfully\n" + Fore.RESET)
            return None
        
        else:
            print(Fore.RED + "\n\n* invalid option. try again. *\n\n" + Fore.RESET)

#########################################################

last_login_time = 0

while True:
    
    print("menu:\n")
    print("1- admin")
    print("2- user")
    print("3- exit\n\n")
    
    option = input("Enter your option: ")
    
    if option in ["1", "admin"]:
        now = time.time()
        if (now - last_login_time) >= 60:
            if get_password():
                admin_panel()
            else:
                pass
        
        else:
            remain = int(60 - (now - last_login_time))
            print(Fore.RED + f"\nyou can't login to admin panel . wait for {remain} second(s)\n" + Fore.RESET)
    
    elif option in ["2", "user"]:
        user_panel()
    
    elif option in ["3", "exit"]:
        print(Fore.GREEN + "\nEnd of Program\n" + Fore.RESET)
        break 
    
    else:
        print(Fore.RED + "\n\n* invalid option. try again. *\n\n" + Fore.RESET)
        