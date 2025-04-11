import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

# Create a database if it doesn't already exists
def database():
    conn = sqlite3.connect("library.db") # Connect to the database
    c = conn.cursor() # Create a cursor
    c.execute("""
        CREATE TABLE IF NOT EXISTS "books"(
            "id" INTEGER,
            "title" TEXT NOT NULL,
            "author" TEXT NOT NULL,
            "status" TEXT NOT NULL CHECK("status" IN ('read', 'unread')) DEFAULT 'unread',
            "page" INTEGER NOT NULL,
            PRIMARY KEY("id")
        )
    """) # Create the books table
    conn.commit() # To commit the table
    conn.close() # Close connection

# Add books to the library database
def add_books(title, author, status, page):
    try:
        conn = sqlite3.connect("library.db") # Connect to the database
        c = conn.cursor() # Create a cursor
        c.execute('INSERT INTO "books"("title", "author", "status", "page") VALUES (?, ?, ?, ?)', 
                  (title, author, status, page)) # Add a book
        conn.commit() # To commit the insert
    except sqlite3.Error as e:
        print("Error adding book:", e) # Check for Errors when adding a book
    finally:
        conn.close() # Close connection

# Update books 
def update_books(title, author, status=None, page=None):
    conn = sqlite3.connect("library.db") # Connect to the database
    c = conn.cursor() # Create a cursor

    updates = [] # It will hold the values from the table
    values = [] # It will hold the values that will be inserted into the placeholders

    # Check if the status have change, to update it
    if status is not None:
        updates.append('"status" = ?')
        values.append(status)
    # Check if the pages where change, to update it
    if page is not None:
        updates.append('"page" = ?')
        values.append(page)
    # Execute the updates
    if updates:
        query = f'UPDATE "books" SET {', '.join(updates)} WHERE "title" = ? AND "author" = ?'
        values.extend([title, author])
        c.execute(query, values)
    
    conn.commit() # To commit the update
    conn.close() # Close connection

# Delete books
def delete_books(title, author):
    conn = sqlite3.connect("library.db") # Connect to the database
    c = conn.cursor() # Create a cursor
    c.execute('DELETE FROM "books" WHERE "title" = ? AND "author" = ?', (title, author)) # Delete a book
    conn.commit() # To commit deleting the book
    conn.close() # Close connection

# Add Books window 
def add_window():
    window = tk.Toplevel(root) # Child window for the root
    window.title("Add Book") # Title
    window.geometry("300x350") # Size
    window.iconbitmap("images/main_icon.ico") # Icon

    window.resizable(False, False) # Prevent resizing 

    background = Image.open("images/add_book.jpg") # Background
    background = background.resize((300, 350), Image.LANCZOS) # Resize
    tk_background = ImageTk.PhotoImage(background) # Convert

    background_label = tk.Label(window, image = tk_background) # Label
    background_label.image = tk_background # Remains in memory
    background_label.place(relwidth=1, relheight=1) # Fully cover the window

    # Create the Title label and entry
    tk.Label(window, text="Title:", bg="#f8c1b2").place(x=60, y=20)
    title_entry = tk.Entry(window)
    title_entry.place(x=110, y=20)

    # Create the Author label and entry
    tk.Label(window, text="Author:", bg="#f8c1b2").place(x=60, y=60)
    author_entry = tk.Entry(window)
    author_entry.place(x=110, y=60)

    # Create the Page label and entry
    tk.Label(window, text="Page:", bg="#f8c1b2").place(x=60, y=100)
    page_entry = tk.Entry(window)
    page_entry.place(x=110, y=100)

    # Create the Status label and dropdown menu 
    tk.Label(window, text="Status:", bg="#f8c1b2").place(x=60, y=140)
    status_var = tk.StringVar(value="unread")
    status_dropdown = ttk.Combobox(window, textvariable=status_var, values=["read", "unread"]) # Set 2 values for the dropdown
    status_dropdown.place(x=110, y=140)

    # Save the book in the database
    def save():
        try:
            page_number = int(page_entry.get())  # Convert page number to integer
            add_books(title_entry.get(), author_entry.get(), status_var.get(), page_number)
            window.destroy() # Close the window
            display_books() # Update the list of books on the main window
        except ValueError:
            messagebox.showerror("Invalid Input", "Page number must be a valid integer.") # Error message box

    tk.Button(window, text="Add Book", command=save).place(x=120, y=290) # Button to trigger the save

# 'Update Books' window
def update_window():
    window = tk.Toplevel(root) # Child window for the root
    window.title("Update Book") # Title
    window.geometry("300x350") # Size
    window.iconbitmap("images/main_icon.ico") # Icon

    window.resizable(False, False) # Prevent resizing 

    background = Image.open("images/update_book.jpg") # Background
    background = background.resize((300, 350), Image.LANCZOS) # Resize
    tk_background = ImageTk.PhotoImage(background) # Convert

    background_label = tk.Label(window, image = tk_background) # Label
    background_label.image = tk_background # Remains in memory
    background_label.place(relwidth=1, relheight=1) # Fully cover the window

    # Create the Title label and entry
    tk.Label(window, text="Title:", bg="#f8c1b2").place(x=60, y=20)
    title_entry = tk.Entry(window)
    title_entry.place(x=110, y=20)

    # Create the Author label and entry
    tk.Label(window, text="Author:", bg="#f8c1b2").place(x=60, y=60)
    author_entry = tk.Entry(window)
    author_entry.place(x=110, y=60)

    # Create the Page label and entry
    tk.Label(window, text="Page:", bg="#f8c1b2").place(x=60, y=100)
    page_entry = tk.Entry(window)
    page_entry.place(x=110, y=100)

    # Create the Status label and dropdown menu 
    tk.Label(window, text="Status:", bg="#f8c1b2").place(x=60, y=140)
    status_var = tk.StringVar(value="unread")
    status_dropdown = ttk.Combobox(window, textvariable=status_var, values=["read", "unread"]) # Set 2 values for the dropdown
    status_dropdown.place(x=110, y=140)

    # Save the changes in the database
    def save():
        try:
            page_number = int(page_entry.get()) if page_entry.get() else None  # Convert only if not empty
            update_books(title_entry.get(), author_entry.get(), status_var.get(), page_number)
            window.destroy() # Close the window
            display_books() # Update the list of books on the main window
        except ValueError:
            messagebox.showerror("Invalid Input", "Page number must be a valid integer.")

    tk.Button(window, text="Update Book", command=save).place(x=110, y=250) # Button to trigger the save

# 'Delete Books' window
def delete_window():
    window = tk.Toplevel(root) # Child window for the root
    window.title("Delete Book") # Title
    window.geometry("300x250") # Size
    window.iconbitmap("images/main_icon.ico") # Icon

    window.resizable(False, False) # Prevent resizing 

    background = Image.open("images/delete_book.jpg") # Background
    background = background.resize((300, 250), Image.LANCZOS) # Resize
    tk_background = ImageTk.PhotoImage(background) # Convert

    background_label = tk.Label(window, image = tk_background) # Label
    background_label.image = tk_background # Remains in memory
    background_label.place(relwidth=1, relheight=1) # Fully cover the window

    # Create the Title label and entry
    tk.Label(window, text="Title:", bg="#f8c1b2").place(x=60, y=20)
    title_entry = tk.Entry(window)
    title_entry.place(x=110, y=20)

    # Create the Author label and entry
    tk.Label(window, text="Author:", bg="#f8c1b2").place(x=60, y=60)
    author_entry = tk.Entry(window)
    author_entry.place(x=110, y=60)

    # Delete the book from the database
    def delete():
        delete_books(title_entry.get(), author_entry.get())
        window.destroy() # Close the window
        display_books() # Update the list of books on the main window

    tk.Button(window, text="Delete", command=delete).place(x=130, y=100) # Button to trigger the delete

# Search Books on main window
def search_books():
    search_query = search_entry.get().strip().lower()  # Convert input to lowercase, strip spaces
    books_listbox.delete(0, tk.END)  # Clear the listbox so it will only show the results

    conn = sqlite3.connect("library.db") # Connect to the database
    c = conn.cursor() # Create a cursor
    
    # Search both the title and author sections 
    if search_query:  
        c.execute('SELECT * FROM "books" WHERE LOWER("title") LIKE ? OR LOWER("author") LIKE ?', 
                  ('%' + search_query + '%', '%' + search_query + '%'))
    # If the search bar is empty, then show all the books
    else:  
        c.execute("SELECT * FROM books")
    
    results = c.fetchall() # Fetch all the results of the query
    conn.close() # Close connection

    # Loop through all the results and insert the books in the listbox
    for book in results:
        books_listbox.insert(tk.END, f"{book[1]} - {book[2]} ({book[3]}, {book[4]} pages)")

# Display all the books in listbox
def display_books():
    books_listbox.delete(0, tk.END)  # Clear listbox

    conn = sqlite3.connect("library.db") # Connect to the database
    c = conn.cursor() # Create a cursor
    c.execute("SELECT * FROM books") 
    books = c.fetchall() # Retrieve all the results from the query
    conn.close() # Close connection

    # Loop through each book and insert them into the listbox
    for book in books:
        books_listbox.insert(tk.END, f"{book[1]} - {book[2]} ({book[3]}, {book[4]} pages)")

# The main window
def main():
    global root, books_listbox
    root = tk.Tk() # Creates the main application window
    root.title("Digital Home Library") # Window title
    root.geometry("1000x600") # Size
    root.iconbitmap("images/main_icon.ico") # Icon

    root.resizable(False, False) # Prevent resizing 

    database()

    background = Image.open("images/background.jpg") # Background
    background = background.resize((1000, 600), Image.LANCZOS) # Resize
    tk_background = ImageTk.PhotoImage(background) # Convert

    background_label = tk.Label(root, image = tk_background) # Label
    background_label.image = tk_background # Remains in memory
    background_label.place(relwidth=1, relheight=1) # Fully cover the window

    title_label = tk.Label(root, text="My Library", font=("Arial", 30, "bold"), fg="#e4b29f", bg="black") # Display the title
    title_label.place(x=400, y=50) # Placement

    # Add Book Button
    tk.Button(root, text="Add Book", command=add_window, bg="#f1d0c1").place(x=370, y=150)

    # Update Book Button
    tk.Button(root, text="Update Book", command=update_window, bg="#e4b29f").place(x=463, y=150)

    # Delete Book Button
    tk.Button(root, text="Delete Book", command=delete_window, bg="#d59e8e").place(x=570, y=150)

    # Search Section button and entry
    search_frame = tk.Frame(root,bg="#c88b7a")
    search_frame.pack(pady=10)
    search_frame.place(x=410, y=200)

    global search_entry  # So other functions can access it
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, padx=10)
    search_button = tk.Button(search_frame, text="Search", command=search_books, bg="#c88b7a")
    search_button.pack(side=tk.LEFT)

    # Listbox to show books which are added to the database
    global books_listbox 
    books_listbox = tk.Listbox(root, width=50, height=15, bg="#fdf0e4")
    books_listbox.pack(pady=10)
    books_listbox.place(x=350, y=250)

    # Automatically update search as the user types
    search_entry.bind("<KeyRelease>", lambda event: search_books())

    display_books() # Load books after making sure the database exists

    root.mainloop() # Run it

if __name__ == "__main__":
    main()