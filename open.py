import csv
import os
import locale
from time import sleep
import uuid


def load_data(filename): 
    products = [] 
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = int(row['id'])
                name = row['name']
                desc = row['desc']
                price = float(row['price'])
                quantity = int(row['quantity'])

                products.append(        #list
                    {                    #dictionary
                        "id": id,       
                        "name": name,
                        "desc": desc,
                        "price": price,
                        "quantity": quantity
                    }
                )
    except ValueError:
        print("Kan inte hitta filen")
        sleep(1.5)
    
    return products





#gör en funktion som hämtar en produkt

def add_product(products, name, desc, price, quantity):
    max_id = max(products, key = lambda x: x['id'])
    
    new_id = max_id['id'] + 1


    new_product = {                    
        "id": new_id,       
        "name": name,
        "desc": desc,
        "price": price,
        "quantity": quantity
    }
    products.append(new_product)

    with open('db_products.csv','a') as fd:
        fd.write(f"\n{new_id},{name},{desc},{price},{quantity}")

    return f"Du lade till {name}, id = {new_id}"

  
def get_product(products):
    while True:
        answer = int(input("\nVilken plats är varan du vill ändra på?  "))

        if answer <= len(products) and answer >= 0:
               return answer
                        
        
        else:
            print("Felaktigt värde")
            sleep(1)
    


def change_product(products, number, id, name, desc, price, quantity):
    product_to_edit = None

    for product in products:
        if product['id'] == number:
            product_to_edit = product

    product_to_edit['id'] = id
    product_to_edit['name'] = name
    product_to_edit['desc'] = desc
    product_to_edit['price'] = price
    product_to_edit['quantity'] = quantity

    return f"Ändrade: {number}"

 
def save_info(products):
    csv_file_path = "db_products.csv"

        # Write the products data to a CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
        writer.writeheader()  # Write the header row
        writer.writerows(products)  # Write the product data
    
    print(f"Data successfully saved to {csv_file_path}")
    sleep(1)

    os.system('cls' if os.name == 'nt' else 'clear')







def remove_product(products, id):
    temp_product = None

    for product in products:
        if product["id"] == id:
            temp_product = product
            break  # Avsluta loopen så snart produkten hittas

    if temp_product:
        products.remove(temp_product)
        return f"Product: {id} {temp_product['name']} was removed"
    else:
        return f"Product with id {id} not found"




def view_product(products, id):
    # Go through each product in the list
    for product in products:
        # Check if the product's id matches the given id
        if product["id"] == id:
            # If it matches, return the product's name and description
            return f"Visar produkt: {product['name']} {product['desc']}"
    
    # If no matching product is found, return this message
    return "Produkten hittas inte"


def view_products(products):
    # skapa sidhuvudet av tabellen:
    header = f"{'#':<6} {'NAMN':<26} {'BESKRIVNING':<51} {'PRIS':<15} {'KVANTITET':<10}"
    separator = "-" * 110           #linje
    
    # rader för varje produkt:
    rows = []

    for index, product in enumerate(products, 1):
        name = product['name']
        desc = product['desc']
        price = product['price']
        quantity = product['quantity']
        
        price = locale.currency(price, grouping=True)
        row = f"{index:<5} {name:<35} {desc:<70} {price:<14} {quantity:<10}"

        rows.append(row)
    
    # kombinera sidhuvud och rader:
    inventory_table = "\n".join([header, separator] + rows)
    
    return f"{inventory_table}"

#TODO: gör om så du slipper använda global-keyword (flytta inte "product = []")
#TODO: skriv en funktion som returnerar en specifik produkt med hjälp av id


locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')  

os.system('cls' if os.name == 'nt' else 'clear')

products = load_data('db_products.csv')

while True:

    try:
       
        os.system('cls' if os.name == 'nt' else 'clear')

        print(view_products(products))  # Show ordered list of products

        choice = input("\nVill du (V)isa, (L)ägga till, (F)örändra eller (T)a bort en produkt? ").strip().upper()
        
        if choice == "L":
            
            name = input("Namn: ")
            desc = input("Beskrivning: ")
            price = float(input("Pris: "))
            quantity = int(input("Kvantitet: "))

            print(add_product(products, name, desc, price, quantity))
            sleep(1.5)
            save_info(products)
        
        elif choice == "F":
            number = get_product(products)

            id = input("Nytt ID: ")
            name = input("Nytt namn: ")
            desc = input("Ny beskrivning: ")
            price = float(input("Nytt pris: "))
            quantity = int(input("Ny kvantitet: "))


            
            print(change_product(products, number, id, name, desc, price, quantity))
            sleep(1.5)
            save_info(products)



        elif choice in ["V", "T"]:
            index = int(input("Enter product Number: "))
            
            if choice == "V":   #visa
                if 1 <= index <= len(products):  # Ensure the index is within the valid range
                    selected_product = products[index - 1]  # Get the product using the list index
                    id = selected_product['id']  # Extract the actual ID of the product
                    print(view_product(products, id))  # Remove product using the actual ID
                    done = input()

                    
                else:
                    print("Ogiltig produkt")
                    sleep(0.3)
                    

            elif choice == "T": #ta bort
                if 1 <= index <= len(products):  # Ensure the index is within the valid range
                    selected_product = products[index - 1]  # Get the product using the list index
                    id = selected_product['id']  # Extract the actual ID of the product

                    print(remove_product(products, id))  # Remove product using the actual ID
                    sleep(0.5)    
                    save_info(products)
        

                else:
                    print("Ogiltig produkt")
                    sleep(0.3)

    
        
    except ValueError:
        print("Välj en produkt med siffor")
        sleep(0.5)

        
    