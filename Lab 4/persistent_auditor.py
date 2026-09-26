def get_valid_input():
    failed_attempts = 0
    endme = 0

    while True:
        product_name = input("Enter Product Name or 'quit': ").strip()
        stock_quantity = input("Enter Quantity or 'quit': ").strip()
        order_data = ["INVALID DATA", 0, failed_attempts]

        if product_name.lower() == "quit":
            endme == 1
            return endme,order_data
        if stock_quantity.lower() == "quit":
            endme == 1
            return endme,order_data

        try:
            quantity = int(stock_quantity)
            if quantity >= 0:
                order_data[1] = quantity

            failed_attempts += 1
            print("Invalid input. Negative values not allowed.")

        except ValueError:
            failed_attempts += 1
            print("Invalid input. Please input only integers.")


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10

def report_decorator(func):
    def wrapper(total_units, failed_attempts):
        func(total_units, failed_attempts)

    def final(inventory, tax, total_deliveries, failed_attempts):
        print("=======FINAL REPORT=======")
        print(f"|| Current Inventory: {inventory}")
        print(f"|| Taxes To Pay: ${tax:.2f}")
        print(f"|| Total Deliveries Processed: {total_deliveries}")
        print(f"|| Number of Failed/Rejected Entries: {failed_attempts}")
        print("==========================")

    wrapper.final = final
    return wrapper

@report_decorator
def generate_report(total_units, failed_attempts):
    print(f"Deliveries Currently Processed: {total_units}")
    print(f"Current Number of Failed Attempts: {failed_attempts}")
    print("\n")


def load_inventory():
    global next_id
    inventory = []

    try:
        with open("inventory.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                data[0] = int(data[0])
                inventory.append(data)

            if len(inventory) > 0:
                next_id = max(i[0] for i in inventory) + 1

    except FileNotFoundError:
        inventory = []            

    #print(inventory)
    return inventory

def save_inventory(product, quantity):
    global next_id
    new_product = []
    
    order = [next_id, product, quantity] 
    new_product.append(order)
    
    with open("inventory.txt", "a") as file:
        file.write(",".join(map(str, order)) + "\n")

    next_id += 1





def main():
    total_deliveries = 0
    failed_attempts = 0
    total_tax = 0
    inventory = load_inventory()
    next_id = 1


    while True:
        stock, quantity, failures = get_valid_input()
        failed_attempts += failures

        print(stock, quantity, failures)

        if stock == "quit":
            break
        if quantity == "quit":
            break

        inventory = process_delivery(inventory, quantity)
        total_tax += calculate_tax(quantity)

        total_deliveries += 1
        generate_report(total_deliveries, failed_attempts)

    generate_report.final(inventory,total_tax,total_deliveries,failed_attempts)

get_valid_input()
# print(load_inventory())
# save_inventory("hello", 12)
# main()

# order_data = ["INVALID DATA", 0, 999]
# order_data[1] = 10
# print(order_data)