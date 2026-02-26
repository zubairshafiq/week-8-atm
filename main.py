import json  # Import the JSON module to work with JSON files
import os    # Import the OS module to interact with the operating system


DATA_FILE = "users.json"  # The filename where user data is stored


def load_users():
    """
    Load user records from the JSON file.
    Returns a dictionary of users.
    """
    # Check if the data file exists
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        # Open the file and load the data
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
    except (json.JSONDecodeError, OSError):
        pass  # If there's an error, return an empty dictionary

    return {}


def save_users(users):
    """
    Save user records to the JSON file.
    """
    # Write the users dictionary to the file
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=2)


def create_user(users):
    """
    Create a new user account by asking for a username and PIN.
    """
    # Ask the user to enter a username
    username = input("Create username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return None

    # Check if the username already exists
    if username in users:
        print("Username already exists.")
        return None

    # Ask the user to enter a 4-digit PIN
    pin = input("Create 4-digit PIN: ").strip()
    if not (pin.isdigit() and len(pin) == 4):
        print("PIN must be exactly 4 digits.")
        return None

    # Add the new user to the users dictionary
    users[username] = {"pin": pin, "balance": 0.0}
    save_users(users)
    print("Account created successfully.")
    return username


def login(users):
    """
    Authenticate an existing user by checking username and PIN.
    """
    # Ask for username and PIN
    username = input("Username: ").strip()
    pin = input("PIN: ").strip()

    user = users.get(username)
    # Check if the username exists and the PIN matches
    if not user or user.get("pin") != pin:
        print("Invalid username or PIN.")
        return None

    print(f"Login successful. Welcome, {username}!")
    return username


def deposit(balance):
    """
    Add money to the account balance.
    """
    # Ask the user for the deposit amount
    amount_text = input("Enter amount to deposit: $").strip()

    try:
        amount = float(amount_text)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return balance

    # Check if the amount is positive
    if amount <= 0:
        print("Deposit amount must be greater than 0.")
        return balance

    # Add the amount to the balance
    balance += amount
    print(f"Deposit successful. New balance: ${balance:.2f}")
    return balance


def withdraw(balance):
    """
    Remove money from the account balance.
    """
    # Ask the user for the withdrawal amount
    amount_text = input("Enter amount to withdraw: $").strip()

    try:
        amount = float(amount_text)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return balance

    # Check if the amount is positive
    if amount <= 0:
        print("Withdrawal amount must be greater than 0.")
        return balance

    # Check if there are enough funds
    if amount > balance:
        print("Insufficient funds.")
        return balance

    # Subtract the amount from the balance
    balance -= amount
    print(f"Withdrawal successful. New balance: ${balance:.2f}")
    return balance


def check_balance(balance):
    """
    Display the current account balance.
    """
    print(f"Current balance: ${balance:.2f}")


def run_atm_session(users, username):
    """
    Run ATM operations for a logged-in user.
    Allows deposit, withdrawal, balance check, and logout.
    """
    # Get the user's current balance
    balance = float(users[username].get("balance", 0.0))

    while True:
        # Show the ATM menu
        print(f"\n=== ATM Menu ({username}) ===")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Logout")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            balance = deposit(balance)
            users[username]["balance"] = balance
            save_users(users)
        elif choice == "2":
            balance = withdraw(balance)
            users[username]["balance"] = balance
            save_users(users)
        elif choice == "3":
            check_balance(balance)
        elif choice == "4":
            print("Logged out.")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


def main():
    # Load users from the data file
    users = load_users()

    while True:
        # Show the main menu
        print("\n=== Welcome to ATM ===")
        print("1. Login")
        print("2. Create New User")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            # Login and start ATM session if successful
            username = login(users)
            if username:
                run_atm_session(users, username)
        elif choice == "2":
            # Create a new user and start ATM session
            username = create_user(users)
            if username:
                run_atm_session(users, username)
        elif choice == "3":
            print("Thank you for using the ATM. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    # Start the program
    main()
