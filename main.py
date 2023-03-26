# Module Imports

import getpass
import re
import tkinter as t
from tkinter import messagebox

import mysql.connector as mc

con = mc.connect(host="localhost", user="root", passwd="root", database="adp_project")
k = con.cursor()


# Functions


def admin_login():
    # Getting User Details
    email = input("Enter your Username: ")
    user_password = getpass.getpass("Enter your Password: ")

    # Verifying User Details
    k.execute(f"select password from admin where username='{email}'; ")
    info = k.fetchall()
    print(info)

    if info[0][0] == user_password:
        print("success")
        return True
    else:
        return False


def add_product():
    product_name = input("Enter product Name: ").lower()
    product_category = input("Enter Product Category").lower()
    k.execute(f"insert into stock (name,Category) values('{product_name}', '{product_category}')")
    con.commit()


def customer_login(a, b):
    # Getting User Details
    email = a.get().lower()
    password = b.get()

    # Verifying User Details
    k.execute(f"select password from customer where email='{email}'; ")
    info = k.fetchall()
    if not info:
        return False
    elif str(info[0][0]) == password:
        return True
    else:
        return False


def del_product():
    product_id = input("Enter Product ID: ")
    k.execute(f"delete from stock where productID='{product_id}'")
    con.commit()


def get_current_stock():
    k.execute("select * from stock;")
    t_stock = k.fetchall()
    print(t_stock)


def search(col, aug):
    k.execute(f"select * from stock where {col} like '%{aug}%' order by '{col}';")
    t_stock = k.fetchall()
    return t_stock


def buy_item_logic(product):
    item_bought = product
    k.execute(f"update stock set quantity=quantity-1, where name='{item_bought}';")
    # con.commit()


# Tkinter
bg_color = "#9ea1a0"
window = t.Tk()
window.geometry("1000x600")
window.maxsize(width=1000, height=600)
window.minsize(width=1000, height=600)
window.config(background=bg_color)
WIDTH = 1000
HEIGHT = 600
lb_wd = 50
BASKET = []
PRICE = []


# Page Funcs


def main_page(c=None):
    global BASKET
    global PRICE
    BASKET, PRICE = [], []
    try:
        for i in c.winfo_children():
            i.destroy()
    except:
        print("Error detected")
    else:
        pass

    title_text = ("comic sans", 70)
    button_text = ("comic sans", 20)

    ls_page_label = t.Label(window, text="El-mart", font=title_text, bg=bg_color, fg="#000000", highlightcolor="black")
    login_button = t.Button(window, text="Login", font=button_text, bg="#f0671d", border=4,
                            command=lambda: login_page(window))
    signup_button = t.Button(window, text="SignUp", font=button_text, bg="#f0671d", border=4,
                             command=lambda: signup_page(window))

    # Widgets Placement

    ls_page_label.place(y=HEIGHT * 0.2, x=(WIDTH * 0.50))
    login_button.place(x=WIDTH * 0.30, y=HEIGHT * 0.55)
    signup_button.place(x=WIDTH * 0.60, y=HEIGHT * 0.55)
    window.update()
    ls_page_label.place(y=HEIGHT * 0.2, x=(WIDTH * 0.50) - ls_page_label.winfo_width() / 2)
    window.mainloop()


def signup_page(screen):
    try:
        for i in screen.winfo_children():
            i.destroy()
    except:
        print("Error detected")
    else:
        pass

    def customer_signup():
        # Getting User Details
        name = name_entry.get().lower()
        email = email_entry.get().lower()
        password = password_entry.get()

        # Adding UserData to To Database
        k.execute(f"insert into customer (name, email, password) values('{name}', '{email}', '{password}')")
        con.commit()

        print('''
            User added Successful
            ''')

    def checkpass():
        regex = r'\b[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Z|a-z]{2,7}\b'
        mail_flag = True
        k.execute("select email from customer;")
        emails = k.fetchall()
        if repeat_password_entry.get() != password_entry.get():
            messagebox.showerror(title="Error", message="Entered Passwords do not Match.")
        elif name_entry.get() == "":
            messagebox.showerror(title="Error", message="Invalid Username")
        elif email_entry.get() == "":
            messagebox.showerror(title="Error", message="Invalid Email")
        elif not re.fullmatch(regex, email_entry.get()):
            messagebox.showerror(title="Error", message="Invalid Email")
        else:
            for mail in emails:
                if email_entry.get() == mail[0]:
                    messagebox.showerror(title="Error", message="Account With This Email Already Exists.")
                    mail_flag = False
                    break
            if mail_flag is True:
                print("Success!")
                customer_signup()
                main_page(window)

    # Tkinter Widgets
    signup_font = "Helvetica 25"
    title = t.Label(window, text="Sign Up", font=signup_font, bg=bg_color, highlightcolor="Red")
    name_entry = t.Entry(window, font=signup_font, highlightcolor="#000000")
    name_label = t.Label(window, text="Name:", font=signup_font, bg=bg_color)
    email_entry = t.Entry(window, font=signup_font, highlightcolor="#000000")
    email_label = t.Label(window, text="Email:", font=signup_font, bg=bg_color)
    password_entry = t.Entry(window, font=signup_font, highlightcolor="#000000", show="*")
    password_label = t.Label(window, text="Password: ", font=signup_font, bg=bg_color)
    repeat_password_entry = t.Entry(window, font=signup_font, highlightcolor="#000000", show="*")
    repeat_password_label = t.Label(window, text="Confirm Passwords: ", font=signup_font, bg=bg_color)
    submit = t.Button(text="submit", command=checkpass, bg='#f0671d', font=signup_font)
    back = t.Button(window, text="<--", command=lambda: main_page(window))
    back.place(x=0, y=0)

    # Tkinter Widget Placement
    lb_ls = [name_label, email_label, password_label, repeat_password_label]
    en_ls = [name_entry, email_entry, password_entry, repeat_password_entry]
    w = 0.1
    h = 0.1
    for i in lb_ls:
        i.place(x=WIDTH * w, y=HEIGHT * h)
        h += 0.1
    h = 0.1
    w = 0.5
    for i in en_ls:
        i.place(x=WIDTH * w, y=HEIGHT * h)
        h += 0.1
    submit.place(y=HEIGHT * 0.8, x=(WIDTH * 0.5))
    title.place(x=(WIDTH * 0.5))
    window.update()
    title.place(x=(WIDTH * 0.5) - (title.winfo_width() * 0.5))
    submit.place(y=HEIGHT * 0.8, x=(WIDTH * 0.5) - submit.winfo_width())


def login_page(screen):
    for i in screen.winfo_children():
        i.destroy()

    def login():
        if customer_login(email_entry, password_entry):
            print("Success")
            user_page(window)
        else:
            messagebox.showerror(title="Error", message="Invalid login details")

    login_font = "Helvetica 25"
    email_entry = t.Entry(window, font=login_font)
    email_label = t.Label(window, text="Email:", font=login_font, bg=bg_color)
    password_entry = t.Entry(window, font=login_font, show="*")
    password_label = t.Label(window, text="Password ", font=login_font, bg=bg_color)
    submit = t.Button(text="submit", command=login, font=login_font, bg="#f0671d")
    back = t.Button(window, text="<--", command=lambda: main_page(window))
    back.place(x=0, y=0)
    title = t.Label(window, text="Sign Up", font=login_font, bg=bg_color, highlightcolor="Red")
    # Tkinter Widget Placement

    lb_ls = [email_label, password_label]
    en_ls = [email_entry, password_entry]
    w = 0.1
    h = 0.1
    for i in lb_ls:
        i.place(x=WIDTH * w, y=HEIGHT * h)
        h += 0.1
    h = 0.1
    w = 0.5
    for i in en_ls:
        i.place(x=WIDTH * w, y=HEIGHT * h)
        h += 0.1
    submit.place(y=HEIGHT * 0.8, x=(WIDTH * 0.5))
    title.place(x=(WIDTH * 0.5))
    window.update()
    title.place(x=(WIDTH * 0.5) - (title.winfo_width() * 0.5))
    submit.place(y=HEIGHT * 0.8, x=(WIDTH * 0.5) - submit.winfo_width())


def user_page(screen):
    for i in screen.winfo_children():
        i.destroy()

    def search_button(col=None):
        if col == "All Deals":
            items = search("name", "")
            search_page(screen, items)
        elif col is not None:
            items = search("category", col.lower())
            search_page(screen, items)
        else:
            if search_entry.get().strip() == "":
                messagebox.showerror(title="Error", message="No Item Searched")
            else:
                items = search("name", search_entry.get())
                search_page(screen, items)

    # Widgets
    t.Label(window, text="El-Mart", bg=bg_color, font="Helvetica 20").place(x=0, y=0)
    sp_font = "Helvetica 20"
    search_btn = t.Button(window, text="Search", command=search_button, font="Helvetica 13")
    search_entry = t.Entry(window, font=sp_font, width=50 + 3)
    search_entry.place(x=WIDTH * 0.10, y=0)
    search_btn.place(x=WIDTH * 0.9 + 2, y=2)
    # Menu
    menubar = t.Menu(window, bg="Grey", fg='Red', activebackground="Yellow", )
    categories = t.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Categories", menu=categories, )
    categories.add_command(label='Fruits & Vegetables', command=lambda: search_button('Fruits & Vegetables'))
    categories.add_command(label='Food-grains, Oil & Masala',
                           command=lambda: search_button('Food-grains, Oil & Masala'))
    categories.add_command(label='Bakery, Cakes & Dairy', command=lambda: search_button('Bakery, Cakes & Dairy'))
    categories.add_command(label='Beverages', command=lambda: search_button('Beverages'))
    categories.add_command(label='Snacks & Branded Foods', command=lambda: search_button('Snacks & Branded Foods'))
    categories.add_command(label='Beauty & Hygiene', command=lambda: search_button('Beauty & Hygiene'))
    categories.add_command(label='Cleaning & Household', command=lambda: search_button('Cleaning & Household'))
    categories.add_command(label='Kitchen, Garden & Pets', command=lambda: search_button('Kitchen, Garden & Pets'))
    categories.add_command(label='Eggs, Meat & Fish', command=lambda: search_button('Eggs, Meat & Fish'))
    categories.add_command(label='Gourmet & World Food', command=lambda: search_button('Gourmet & World Food'))
    categories.add_command(label='Baby Care', command=lambda: search_button('Baby Care'))
    menubar.add_command(label="View All", command=lambda: search_button("All Deals"))
    menubar.add_command(label="Hot Deals")
    menubar.add_command(label="Best Sellers")
    menubar.add_command(label="Logout", command=lambda: main_page(window))
    window.config(menu=menubar)


def search_page(screen, itm):
    try:
        for i in screen.winfo_children():
            i.destroy()
    except:
        print("Error detected")
    else:
        pass

    def search_button(col=None):
        if col == "All Deals":
            items = search("name", "")
            search_page(screen, items)
        elif col is not None:
            items = search("category", col.lower())
            search_page(screen, items)
        else:
            if search_entry.get().strip() == "":
                messagebox.showerror(title="Error", message="No Item Searched")
            else:
                items = search("name", search_entry.get())
                search_page(screen, items)

    def add2basket(pd, pc):
        PRICE.append(pc[lb.curselection()[0]])
        BASKET.append(pd[lb.curselection()[0]])

    sp_font = "Helvetica 20"
    search_btn = t.Button(window, text="Search", command=search_button, font="Helvetica 13")
    search_entry = t.Entry(window, font=sp_font, width=50 + 3)
    search_btn.place(x=WIDTH * 0.9 + 2, y=2)
    menubar = t.Menu(window, bg="Grey", fg='Red', activebackground="Yellow", )
    categories = t.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Categories", menu=categories, )
    t.Label(window, text="El-Mart", bg=bg_color, font="Helvetica 20").place(x=0, y=0)
    categories.add_command(label='Fruits & Vegetables', command=lambda: search_button('Fruits & Vegetables'))
    categories.add_command(label='Food-grains, Oil & Masala',
                           command=lambda: search_button('Food-grains, Oil & Masala'))
    categories.add_command(label='Bakery, Cakes & Dairy', command=lambda: search_button('Bakery, Cakes & Dairy'))
    categories.add_command(label='Beverages', command=lambda: search_button('Beverages'))
    categories.add_command(label='Snacks & Branded Foods', command=lambda: search_button('Snacks & Branded Foods'))
    categories.add_command(label='Beauty & Hygiene', command=lambda: search_button('Beauty & Hygiene'))
    categories.add_command(label='Cleaning & Household', command=lambda: search_button('Cleaning & Household'))
    categories.add_command(label='Kitchen, Garden & Pets', command=lambda: search_button('Kitchen, Garden & Pets'))
    categories.add_command(label='Eggs, Meat & Fish', command=lambda: search_button('Eggs, Meat & Fish'))
    categories.add_command(label='Gourmet & World Food', command=lambda: search_button('Gourmet & World Food'))
    categories.add_command(label='Baby Care', command=lambda: search_button('Baby Care'))

    menubar.add_command(label="View All", command=lambda: search_button('All Deals'))
    menubar.add_command(label="Hot Deals")

    menubar.add_command(label="Best Sellers")
    menubar.add_command(label="print basket", command=lambda: print(BASKET))
    menubar.add_command(label="Logout", command=lambda: main_page(window))
    window.config(menu=menubar)

    search_entry.place(x=WIDTH * 0.10, y=0)
    lb = t.Listbox(window, font="Courier 20 bold", width=lb_wd, height=15)
    products = []
    price = []
    for i in itm:
        products.append(i[1])
        price.append(i[3])
    long = len(max(products, key=len))
    for i in itm:
        lb.insert("end", f"{i[1].ljust(long)} {str(i[3]).rjust(lb_wd - len(i[1].ljust(long)) - 3)}rs")
    lb.place(x=WIDTH * 0.1, y=HEIGHT * 0.1)
    lb.yview()
    window.update()
    t.Button(window, font="helvetica 15", text="Add Item", command=lambda: add2basket(products, price)).place(
        x=WIDTH * 0.1, y=lb.winfo_height() + HEIGHT * 0.110)
    t.Button(window, font="helvetica 15", text="Basket", command=basket_page).place(
        x=(WIDTH * 0.85) - 22, y=lb.winfo_height() + HEIGHT * 0.110)


def basket_page():
    for i in window.winfo_children():
        i.destroy()

    # tkinter Widgets
    title = t.Label(window, text="Your Basket", bg=bg_color, font="Helvetica 40")
    basket = t.Listbox(window, font="Courier 20 bold", width=lb_wd, height=10)
    basket.xview()
    basket.place(x=WIDTH * 0.1, y=HEIGHT * 0.1)
    long = len(max(BASKET, key=len))
    for i, j in zip(BASKET, PRICE):
        basket.insert("end", f"{i.ljust(long)} {str(j).rjust(lb_wd - len(str(i).ljust(long)) - 3)}rs")
    total = sum(PRICE)
    total = t.Label(window, text=f"Total:{total}rs", bg=bg_color, font="Helvetica 40")
    total.place(x=WIDTH * 0.1, y=HEIGHT * 0.1 + (basket.winfo_height() + 15))
    window.update()
    total.place(x=WIDTH * 0.1, y=HEIGHT * 0.1 + (basket.winfo_height() + 15))
    # Widget placement
    title.place(x=WIDTH * 0.40)
    back = t.Button(window, text="<--", command=lambda: user_page(window))
    back.place(y=0, x=0)



main_page()
