

import os
from pathlib import Path
import pandas as pd
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

books_list = []
members_list = []
lending_list = []

colummn_names = ['Book ID', 'Book Title', 'Book Author', 'availability']
members_names = ['Member ID', 'Member Name', 'Member Contact']
lending_names = ['Book ID', 'Member ID', 'Lending Date', 'availability']

# Define column names for display
column_names_books = colummn_names
column_names_members = members_names
column_names_lending = lending_names

# CORRECTED: Define file paths as Path objects
BOOKS_FILE = Path(SCRIPT_DIR) / 'books.txt'
MEMBERS_FILE = Path(SCRIPT_DIR) / 'members.txt'
LENDING_FILE = Path(SCRIPT_DIR) / 'lending.txt'

# Now you can call .parent.mkdir() on the Path objects
# These lines ensure the directory for your files exists.
# If your files are directly in SCRIPT_DIR, .parent will refer to SCRIPT_DIR itself.
# If you had a structure like Path(SCRIPT_DIR) / 'data' / 'books.txt',
# then .parent would be Path(SCRIPT_DIR) / 'data', and .mkdir would create 'data'.
BOOKS_FILE.parent.mkdir(parents=True, exist_ok=True)
MEMBERS_FILE.parent.mkdir(parents=True, exist_ok=True)
LENDING_FILE.parent.mkdir(parents=True, exist_ok=True)

# Important: When opening files, convert the Path object back to a string
# or just pass the Path object directly to open() (which it accepts)
# I'll stick with converting to string for consistency with your original usage of os.path.exists
# and for clarity, though `open(BOOKS_FILE, 'r')` would also work directly.

if os.path.exists(str(BOOKS_FILE)): # Convert Path object to string for os.path.exists
    try:
        with open(str(BOOKS_FILE), 'r') as file: # Convert Path object to string
            first_line = file.readline().strip()
            # Check if the first line IS the expected header
            if first_line == 'Book ID,Book Title,Book Author,Availability':
                # If it's the header, we've read it, so the file pointer is now at the start of data.
                # Do nothing more, the loop below will read the rest.
                pass
            elif first_line: # If it's not the header but not empty, it must be data. Rewind.
                file.seek(0) # Go back to the beginning to read this line as data
            for line in file:
                book_data = line.strip().split(',')
                if len(book_data) == 4:
                    books_list.append(book_data)
    except Exception as e:
        print(f"Error reading books file: {e}")
else:
    try: # Added try-except for file creation too for robustness
        with open(str(BOOKS_FILE), 'w') as file: # Convert Path object to string
            file.write('Book ID,Book Title,Book Author,Availability\n')
    except Exception as e:
        print(f"Error creating books file: {e}")

if os.path.exists(str(MEMBERS_FILE)): # Convert Path object to string
    try:
        with open(str(MEMBERS_FILE), 'r') as file:
                first_line = file.readline().strip()
                if first_line == 'Member ID,Member Name,Member Contact':
                    pass
                elif first_line:
                    file.seek(0)
                for line in file:
                    if line.strip():
                        member_data = line.strip().split(',')
                        if len(member_data) == 3:
                            members_list.append(member_data)
    except Exception as e:
        print(f"Error reading members file: {e}")
else:
    try: # Added try-except for file creation
        with open(str(MEMBERS_FILE), 'w') as file: # Convert Path object to string
            file.write('Member ID,Member Name,Member Contact\n')
    except Exception as e:
        print(f"Error creating members file: {e}")
        
if os.path.exists(str(LENDING_FILE)): # Convert Path object to string
    try:
       with open(str(LENDING_FILE), 'r') as file:
                first_line = file.readline().strip()
                if first_line == 'Book ID,Member ID,Lending Date,Return Date':
                    pass
                elif first_line:
                    file.seek(0)
                for line in file:
                    if line.strip():
                        lending_data = line.strip().split(',')
                        if len(lending_data) == 4:
                            lending_list.append(lending_data)
    except Exception as e:
        print(f"Error reading lending file: {e}")
else:
    try: # Added try-except for file creation
        with open(str(LENDING_FILE), 'w') as file: # Convert Path object to string
            file.write('Book ID,Member ID,Lending Date,Return Date\n')
    except Exception as e:
        print(f"Error creating lending file: {e}")

# Rest of your menu function remains the same,
# but remember to convert Path objects to strings when using open() or os.path.exists()
# or ideally, just pass the Path object directly to open() as it supports it.
# For consistency, I've added `str()` around them, but you can remove it.

def is_valid_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def menu():
    print("1. Add New Book")
    print("2. Register New Member")
    print("3. Lend Book")
    print("4. Return Book")
    print("5. Display Books Inventory")
    print("6. Display Members Information")
    print("7. Exit")

    while True:
        choice = input("What would you like to do? ").lower()

        if choice in ['1', 'add new book']:
            book_ID = input("Book ID: ").strip()
            if book_ID == None or book_ID == "":
                print("Error: Book ID cannot be empty.")
                continue
            if any(book[0] == book_ID for book in books_list):
                print("Error: Book with this ID already exists. Please use a different ID.")
                continue

            book_title = input("Book title: ").strip()
            if book_title == None or book_title == "":
                print("Error: Book title cannot be empty.")
                continue
            book_author = input("Book Author: ").strip()
            if book_author == None or book_author == "":
                print("Error: Book author cannot be empty.")
                continue
            availability = "Available"

            books_list.append([book_ID, book_title, book_author, availability])
            print(f"Book '{book_title}' added successfully with ID '{book_ID}'!")
            with open(str(BOOKS_FILE), 'a') as file: # Convert Path object to string
                file.write(f"{book_ID},{book_title},{book_author},{availability}\n")

        elif choice in ['2', 'add new member', 'register new member']:
            member_ID = input("Member ID: ").strip()
            if member_ID == None or member_ID == "":
                print("Error: Member ID cannot be empty.")
                continue
            if any(member[0] == member_ID for member in members_list):
                print("Error: Member with this ID already exists. Please use a different ID.")
                continue

            member_name = input("Member name: ").strip()
            if member_name == None or member_name == "":
                print("Error: Member name cannot be empty.")
                continue
            member_contact = input("Member contact: ").strip()
            if member_contact == None or member_contact == "":
                print("Error: Member contact cannot be empty.")
                continue
            members_list.append([member_ID, member_name, member_contact])
            print("Member added successfully!")
            with open(str(MEMBERS_FILE), 'a') as file: # Convert Path object to string
                file.write(f"{member_ID},{member_name},{member_contact}\n")

        elif choice in ['3', 'lend book', 'lend a book']:
            lend_book_ID = input("Book ID to lend: ").strip()
            if lend_book_ID == None or lend_book_ID == "":
                print("Error: Book ID cannot be empty.")
                continue
            lend_member_ID = input("Member ID to lend: ").strip()
            if lend_member_ID == None or lend_member_ID == "":
                print("Error: Member ID cannot be empty.")
                continue

            if not any(member[0] == lend_member_ID for member in members_list):
                print(f"Error: Member with ID '{lend_member_ID}' not found.")
                continue

            book_found_in_inventory = False
            book_is_available = False
            for i, book in enumerate(books_list):
                if book[0] == lend_book_ID:
                    book_found_in_inventory = True
                    if book[3] == "Available":
                        book_is_available = True
                        books_list[i][3] = "Borrowed"
                    break
        
            if not book_found_in_inventory:
                print(f"Error: Book with ID '{lend_book_ID}' not found in inventory.")
            elif not book_is_available:
                print(f"Book '{lend_book_ID}' is currently not available for lending (Status: {book[3]}).")
            else:
                while True:
                    lend_date_str = input("Lending date (YYYY-MM-DD): ").strip()
                    if is_valid_date_format(lend_date_str):
                        break
                    else:
                        print("Invalid date format. Please enter date in YYYY-MM-DD format (e.g., 2025-07-07).")
                    continue

                return_date_placeholder = "Not Returned"
                lend_date = lend_date_str  # Assign lend_date for consistency
                lending_list.append([lend_book_ID, lend_member_ID, lend_date_str, return_date_placeholder,])
                print(f"Book '{lend_book_ID}' successfully lent to member '{lend_member_ID}' on {lend_date}.")
                with open(str(LENDING_FILE), 'a') as file: # Convert Path object to string
                    file.write(f"{lend_book_ID},{lend_member_ID},{lend_date},{return_date_placeholder}\n")

        elif choice in ['4', 'return book', 'return a book']:
            return_book_ID = input("Book ID to return: ").strip()
            return_member_ID = input("Member ID who returned the book: ").strip()
            return_date = input("Returning date (YYYY-MM-DD): ").strip()
            if return_book_ID == None or return_book_ID == "":
                print("Error: Book ID cannot be empty.")
                continue
            if not is_valid_date_format(return_date):
                print("Invalid date format. Please enter date in YYYY-MM-DD format (e.g., 2025-07-07).")
                continue

            found_lending_record = False
            for i, record in enumerate(lending_list):
                if record[0] == return_book_ID and record[1] == return_member_ID and record[3] == "Not Returned":
                    lending_list[i][3] = return_date
                    found_lending_record = True
                    break

            if not found_lending_record:
                print("Warning: No active lending record found for this Book ID and Member ID, or it was already returned.")
            else:
                found_book_in_inventory = False
                for i, book in enumerate(books_list):
                    if book[0] == return_book_ID:
                        books_list[i][3] = "Available"
                        found_book_in_inventory = True
                        break
                if not found_book_in_inventory:
                    print(f"Warning: Book ID '{return_book_ID}' not found in inventory. Book status not updated.")
                print("Book return recorded and availability updated!")
                with open(str(LENDING_FILE), 'w') as file: # Convert Path object to string
                    file.write('\n'.join([','.join(record) for record in lending_list]) + '\n')
                with open(str(BOOKS_FILE), 'w') as file: # Convert Path object to string
                    file.write('\n'.join([','.join(book) for book in books_list]) + '\n')

        elif choice in ['5', 'display books inventory', 'show books inventory']:
            if not books_list:
                print("No books in inventory.")
            else:
                df_display_books = pd.DataFrame(books_list, columns=column_names_books)
                print("\n--- Books Inventory ---")
                print(df_display_books.to_string(index=False))

        elif choice in ['6', 'display members information', 'show members information']:
            if not members_list:
                print("No members registered.")
            else:
                df_display_members = pd.DataFrame(members_list, columns=column_names_members)
                print("\n--- Members Information ---")
                print(df_display_members.to_string(index=False))

        elif choice in ['7', 'exit', 'quit']:
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
