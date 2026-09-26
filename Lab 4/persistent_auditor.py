inventory_file = "inventory.txt"

def get_valid_input():
    failed_attempts = 0
    invalid_characters = "[](),"

    while True:
        product_name = input("Enter Product Name or 'quit': ").strip()
        if product_name.lower() == "quit":
            return True, None
        if not product_name:
            failed_attempts += 1
            print("Product Name cannot be empty.")
            continue
        if any(char in product_name for char in invalid_characters):
            failed_attempts += 1
            print("Product name contains invalid characters.")
            continue
        break

    while True:
        stock_quantity = input("Enter Quantity or 'quit': ").strip()
        if stock_quantity.lower() == "quit":
            return True, None
        if not stock_quantity:
            failed_attempts += 1
            print("Quantity cannot be empty.")
            continue
        try:
            quantity = int(stock_quantity)
            if quantity < 0:
                failed_attempts += 1
                print("Invalid input. Negative values not allowed.")
                continue
            break
        except ValueError:
            failed_attempts += 1
            print("Invalid input. Please input only integers.")
            continue

    order_data = [product_name, quantity, failed_attempts]

    return False, order_data


def unit_transactions():
    inventory = load_inventory()
    transactions = len(inventory) 
    return transactions

def processed_units():
    inventory = load_inventory()
    total = 0
    for x in inventory:
        try:
            total += int(x[2])
        except (ValueError, IndexError):
            print("Invalid inventory record skipped.")
    return total


def report_decorator(func):
    def wrapper(total_processed,total_transactions,failed_attempts):
        func(total_processed,total_transactions,failed_attempts)

    def final(total_processed,total_transactions,failed_attempts):
        print("=======AUDIT REPORT=======")
        print(f"|| Total Transactions Recorded: {total_transactions}")
        # print(f"|| Taxes To Pay: ${tax:.2f}")
        print(f"|| Total Units Processed: {total_processed}")
        print(f"|| Number of Failed/Rejected Entries: {failed_attempts}")
        print("==========================")

    wrapper.final = final
    return wrapper

@report_decorator
def generate_report(total_processed,total_transactions,failed_attempts):
    print(f"Deliveries Currently Processed: {total_processed}")
    print(f"Current Number of Transactions: {total_transactions}")
    print(f"Current Number of Failed Attempts: {failed_attempts}")
    print("\n")

def load_inventory_decorator(func):
    def wrapper():
        inventory = func()
        return inventory
    def start():
        inventory = func()
        print("=====Current Orders=====")
        print("ID| Product | Quantity")
        for i in inventory:
            order_line = " | ".join(map(str,i))
            print(order_line)
        print("========================")

        return inventory

    wrapper.start = start
    return wrapper


@load_inventory_decorator
def load_inventory():
    global next_id
    inventory = []

    try:
        with open(inventory_file, "r") as file:
            for line in file:
                data = line.strip().split(",")
                data[0] = int(data[0])
                inventory.append(data)

            if len(inventory) > 0:
                next_id = max(i[0] for i in inventory) + 1
            else:
                next_id = 1

    except FileNotFoundError:
        inventory = []  
        next_id = 1       

    return inventory



def save_inventory(product, quantity):
    global next_id
    new_product = []
    
    order = [next_id, product, quantity] 
    new_product.append(order)
    
    with open(inventory_file, "a") as file:
        file.write(",".join(map(str, order)) + "\n")

    next_id += 1

    return order




def main():
    total_deliveries = 0
    failed_attempts = 0
    total_tax = 0
    next_id = 1
    inventory = load_inventory.start()
    

    while True:
        endme,order_data = get_valid_input()
        if endme:
            print("Order successfully saved to " + str(inventory_file))
            break
        failed_attempts += int(order_data[2])

        product = str(order_data[0])
        quantity = int(order_data[1])
        saved_order = save_inventory(product, quantity)
        product_id = saved_order[0]
        print("Record Added!")
        print(product_id, product, quantity)
        total_deliveries += 1
        #generate_report(total_processed,total_transactions,failed_attempts)

    total_processed = processed_units()
    total_transactions = unit_transactions()
    
    generate_report.final(total_processed,total_transactions,failed_attempts)


#main()
#generate_report(processed_units(), unit_transactions(), 0)