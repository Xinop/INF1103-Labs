def get_valid_input():
    failed_attempts = 0

    while True:
        user_input = input("Enter stock quantity or 'quit': ").strip()

        if user_input.lower() == "quit":
            return "quit", failed_attempts

        try:
            value = int(user_input)

            if value >= 0:
                return value, failed_attempts

            failed_attempts += 1
            print("Invalid input. Negative values not allowed.")

        except ValueError:
            failed_attempts += 1
            print("Invalid input. Please input only integers.")


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10



def generate_report(total_units, failed_attempts):
    print(f"Deliveries Currently Processed: {total_units}")
    print(f"Current Number of Failed Attempts: {failed_attempts}")
    print("\n")


def main():
    inventory = 0
    total_deliveries = 0
    failed_attempts = 0

    while True:
        value, failures = get_valid_input()
        failed_attempts += failures

        if value == "quit":
            break

        inventory = process_delivery(inventory, value)
        tax = calculate_tax(value)

        total_deliveries += 1
        generate_report(total_deliveries, failed_attempts)

    print("=======FINAL REPORT=======")
    print(f"||Current Inventory: {inventory} ")
    print(f"||Taxes To Pay: ${tax:.2f} ")
    print(f"||Total Deliveries Processed: {total_deliveries}")
    print(f"||Number of Failed/Rejected Entries: {failed_attempts}")
    print("==========================")


main()