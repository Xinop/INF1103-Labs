inventory = 0
rejected = 0

while True:
    stock = input("Enter stock quantity or type quit: ")


    if stock.lower() == "quit":
        print("Total Units Processed:", inventory)
        print("Number of Failed/Rejected Entries:", rejected)
        break


    if stock.startswith("-") and stock[1:].isdigit():
        print("Error: Negative numbers are not allowed.")
        rejected += 1
        continue


    elif not stock.isdigit():
        print("Error: Please enter a valid integer.")
        rejected += 1
        continue


    stock = int(stock)


    inventory += stock


    if inventory > 500:
        print("OVERSTOCK ALERT!")
        break