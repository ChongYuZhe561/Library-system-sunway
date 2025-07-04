
import os
from pathlib import Path
import pandas as pd
books_list = []
members_list = []
lending_list = []
colummn_names=['Book ID', 'Book Title', 'Book Author', 'availability']
members_names=['Member ID', 'Member Name', 'Member Contact']
lending_names=['Book ID', 'Member ID', 'Lending Date', 'return Date']

# Define column names for display
column_names_books = colummn_names
column_names_members = members_names
column_names_lending = lending_names
BOOKS_FILE = Path('Your path') #Add your path here
MEMBERS_FILE =Path('Your path')  #Add your path here
LENDING_FILE = Path('Your path')  #Add your path here

BOOKS_FILE.parent.mkdir(parents=True, exist_ok=True)
MEMBERS_FILE.parent.mkdir(parents=True, exist_ok=True)
LENDING_FILE.parent.mkdir(parents=True, exist_ok=True)

if os.path.exists(BOOKS_FILE):
    try:
        with open(BOOKS_FILE, 'r') as file:
            for line in file:
                book_data = line.strip().split(',')
                if len(book_data) == 4:  # Ensure it has all 4 elements
                    books_list.append(book_data)
    except Exception as e:
        print(f"Error reading books file: {e}")
else:
    # If books file does not exist, create it with a header
    open(BOOKS_FILE, 'w').write('Book ID,Book Title,Book Author,Availability\n')
        
if os.path.exists(MEMBERS_FILE):
    try:
        with open(MEMBERS_FILE, 'r') as file:
            for line in file:
                member_data = line.strip().split(',')
                if len(member_data) == 3:  # Ensure it has all 3 elements
                    members_list.append(member_data)
    except Exception as e:
        print(f"Error reading members file: {e}")
else:
    # If members file does not exist, create it with a header
    open(MEMBERS_FILE, 'w').write('Member ID,Member Name,Member Contact\n')
        
if os.path.exists(LENDING_FILE):
    try:
        with open(LENDING_FILE, 'r') as file:
            for line in file:
                lending_data = line.strip().split(',')
                if len(lending_data) == 4:  # Ensure it has all 4 elements
                    lending_list.append(lending_data)
    except Exception as e:
        print(f"Error reading lending file: {e}")
else:
    # If lending file does not exist, create it with a header
    open(LENDING_FILE, 'w').write('Book ID,Member ID,Lending Date,Return Date\n')

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

            # Check if book already exists (BEFORE collecting more info or appending)
            if any(book[0] == book_ID for book in books_list):
                print("Error: Book with this ID already exists. Please use a different ID.")
                continue # Go back to the menu loop

            book_title = input("Book title: ").strip()
            book_author = input("Book Author: ").strip()
            availability = "Available" # Consistent string value for availability

            # If no duplicate, then add the new book with 4 elements
            books_list.append([book_ID, book_title, book_author, availability])
            print(f"Book '{book_title}' added successfully with ID '{book_ID}'!")
            open(BOOKS_FILE, 'a').write(f"{book_ID},{book_title},{book_author},{availability}\n")
         
            
        # --- 2. Register New Member ---
        elif choice in ['2', 'add new member', 'register new member']:
            member_ID = input("Member ID: ").strip()
            # Optional: Add duplicate member ID check here as well
            if any(member[0] == member_ID for member in members_list):
                print("Error: Member with this ID already exists. Please use a different ID.")
                continue

            member_name = input("Member name: ").strip()
            member_contact = input("Member contact: ").strip()
            members_list.append([member_ID, member_name, member_contact])
            print("Member added successfully!")
            open(MEMBERS_FILE, 'a').write(f"{member_ID},{member_name},{member_contact}\n")

        # --- 3. Lend Book ---
        elif choice in ['3', 'lend book', 'lend a book']:
            lend_book_ID = input("Book ID to lend: ").strip()
            lend_member_ID = input("Member ID to lend: ").strip()

            # Optional: Check if member ID exists before proceeding with lending
            if not any(member[0] == lend_member_ID for member in members_list):
                print(f"Error: Member with ID '{lend_member_ID}' not found.")
                continue

            # First, try to find the book and check its availability
            book_found_in_inventory = False
            book_is_available = False
            for i, book in enumerate(books_list): # Use enumerate to get index for updating
                if book[0] == lend_book_ID:
                    book_found_in_inventory = True
                    # CORRECTED: Explicitly check for the string "Available"
                    if book[3] == "Available":
                        book_is_available = True
                        # CORRECTED: Set availability to the string "Borrowed"
                        books_list[i][3] = "Borrowed"
                        break # Book found and status checked, exit loop
                    
            if not book_found_in_inventory:
                print(f"Error: Book with ID '{lend_book_ID}' not found in inventory.")
            elif not book_is_available:
                # If book was found but not available, 'book' variable still holds its data
                print(f"Book '{lend_book_ID}' is currently not available for lending (Status: {book[3]}).")
            else:
                lend_date = input("Lending date (YYYY-MM-DD): ").strip()
                return_date_placeholder = "Not Returned" # Consistent placeholder for return date
                # If book is found and available, then record the lending transaction
                lending_list.append([lend_book_ID, lend_member_ID, lend_date, return_date_placeholder])
                print(f"Book '{lend_book_ID}' successfully lent to member '{lend_member_ID}' on {lend_date}.")
                open(LENDING_FILE, 'a').write(f"{lend_book_ID},{lend_member_ID},{lend_date},{return_date_placeholder}\n")
        # --- 4. Return Book ---
        elif choice in ['4', 'return book', 'return a book']:
            return_book_ID = input("Book ID to return: ").strip()
            return_member_ID = input("Member ID who returned the book: ").strip()
            return_date = input("Returning date (YYYY-MM-DD): ").strip()

            # Update the return date in the lending_list
            found_lending_record = False
            for i, record in enumerate(lending_list):
                # Match Book ID and Member ID, and check if it's currently 'Not Returned'
                if record[0] == return_book_ID and record[1] == return_member_ID and record[3] == "Not Returned":
                    lending_list[i][3] = return_date # Update 'Return Date'
                    found_lending_record = True
                    break

            if not found_lending_record:
                print("Warning: No active lending record found for this Book ID and Member ID, or it was already returned.")
            else:
                # Update book availability to 'Available' in books_list
                found_book_in_inventory = False
                for i, book in enumerate(books_list):
                    if book[0] == return_book_ID:
                        books_list[i][3] = "Available" # Set availability to the string "Available"
                        found_book_in_inventory = True
                        break
                if not found_book_in_inventory:
                    print(f"Warning: Book ID '{return_book_ID}' not found in inventory. Book status not updated.")
                print("Book return recorded and availability updated!")
                open(LENDING_FILE, 'w').write('\n'.join([','.join(record) for record in lending_list]) + '\n')
                open(BOOKS_FILE, 'w').write('\n'.join([','.join(book) for book in books_list]) + '\n')
                

        # --- 5. Display Books Inventory ---
        elif choice in ['5', 'display books inventory', 'show books inventory']:
            if not books_list:
                print("No books in inventory.")
            else:
                df_display_books = pd.DataFrame(books_list, columns=column_names_books)
                print("\n--- Books Inventory ---")
                print(df_display_books.to_string(index=False))

        # --- 6. Display Members Information ---
        elif choice in ['6', 'display members information', 'show members information']:
            if not members_list:
                print("No members registered.")
            else:
                df_display_members = pd.DataFrame(members_list, columns=column_names_members)
                print("\n--- Members Information ---")
                print(df_display_members.to_string(index=False))

        # --- 7. Exit ---
        elif choice in ['7', 'exit', 'quit']:         
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            

if __name__ == "__main__":
    menu() 
