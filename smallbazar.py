from tkinter import *
from tkinter import ttk
import sqlite3
from PIL import ImageTk, Image



from tkinter import messagebox

from pyzbar.wrapper import ZBarSymbol


def connection():
    connectObj = sqlite3.connect("shopManagement.db")
    cur = connectObj.cursor()
    cur.execute('''
    create table if not exists products (
        productid string,
        product string,
        price int,
        quantity int
        )
    ''')
    connectObj.commit()


def select_all_tasks(text):
    connectObj = sqlite3.connect("shopManagement.db")
    cur = connectObj.cursor()
    cur.execute("SELECT * FROM products WHERE productid=?", (text,))
    rows = cur.fetchall()
    return rows



import cv2
from pyzbar.pyzbar import decode

# def scan_code():
#     camera = cv2.VideoCapture(0)
#
#     while True:
#         ret, frame = camera.read()
#
#         # Decode barcodes in the frame
#         barcodes = decode(frame)
#
#         # Check if any barcode is found
#         if barcodes:
#             for barcode in barcodes:
#                 # Get the barcode data
#                 barcode_data = barcode.data.decode('utf-8')
#
#                 # Check if the barcode data is 5 digits long
#                 if len(barcode_data) == 5 and barcode_data.isdigit():
#                     # Release the camera and return the barcode
#                     camera.release()
#                     cv2.destroyAllWindows()
#                     return barcode_data
#
#         # Display the camera feed
#         cv2.imshow("Scanning for 5-digit barcode", frame)
#
#         # Exit when 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     # Release the camera and close all windows
#     camera.release()
#     cv2.destroyAllWindows()
#




from pyzbar.pyzbar import decode, ZBarSymbol

def scan_code():
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        ret, frame = camera.read()

        # Decode Code 128 barcodes in the frame
        barcodes = decode(frame, symbols=[ZBarSymbol.CODE128])

        # Check if any Code 128 barcode is found
        if barcodes:
            for barcode in barcodes:
                # Get the barcode data
                barcode_data = barcode.data.decode('utf-8')

                # Release the camera and return the barcode
                camera.release()
                cv2.destroyAllWindows()
                return barcode_data

        # Display the camera feed
        cv2.imshow("Scanning for Code 128 barcode", frame)

        # Check if the window was closed
        if cv2.getWindowProperty("Scanning for Code 128 barcode", cv2.WND_PROP_VISIBLE) < 1:
            break

        # Check if the 'Esc' key is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break

        # Release the camera and close all windows
    camera.release()
    cv2.destroyAllWindows()


#
#
# def scan_code():
#     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#     cap.set(3, 640)
#     cap.set(4, 480)
#     camera = True
#     while camera == True:
#         success, frame = cap.read()
#         cv2.imshow('Testing-code-scan', frame)
#         for code in decode(frame, symbols=[ZBarSymbol.CODE128]):
#             cv2.imshow('Testing-code-scan', frame)
#             bar = code.data.decode('utf-8')
#             if bar != 0:
#                 cap.release()
#                 cv2.destroyAllWindows()
#                 return bar
#         cv2.waitKey(1)
#

def total_price():
    return int(price.get()) * int(quan.get())


def addtocart(pid, pname, mrp, q):
    if len(pid) == 0 or len(pname) == 0 or len(mrp) == 0 or len(q) == 0:
        prompt('Fill all the entries!')
    else:
        connectObj = sqlite3.connect("shopManagement.db")
        cur = connectObj.cursor()
        cur.execute("SELECT * FROM products WHERE productid=?", (pid,))
        rows = cur.fetchall()
        connectObj2 = sqlite3.connect("shopManagement.db")
        cur = connectObj2.cursor()
        cur.execute("SELECT quantity FROM products WHERE productid=?", (pid,))
        rows2 = cur.fetchall()
        if len(rows) == 0:
            prompt("No such product found!")
        else:
            if rows2[0][0] < int(q):
                prompt('OUT OF STOCK! only {} left'.format(rows2[0][0]))
            else:
                temp = [pid, pname, mrp, q, total_price()]
                tree.insert('', END, values=temp)
                addtolist(itemlist,pid, pname, mrp, q)
                productname.delete(0, END)
                product_id.delete(0, END)
                price.delete(0, END)
                quan.delete(0, END)


def addtolist(itemlist, pid, pname, mrp, q):
    temp = [pid, pname, mrp, q, total_price()]
    itemlist.append(temp)


def setTextid():
    text = scan_code()
    connectObj2 = sqlite3.connect("shopManagement.db")
    cur = connectObj2.cursor()
    cur.execute("SELECT quantity FROM products WHERE productid=?", (text,))
    rows2 = cur.fetchall()
    if len(rows2) == 0:
        prompt("No such product found!")
    else:
        setdata = select_all_tasks(text)
        setTextname(setdata[0][1])
        setTextprice(setdata[0][2])
        product_id.delete(0,"end")
        product_id.insert(0, str(text))


def setTextname(text):
    productname.delete(0,"end")
    productname.insert(0, str(text))


def setTextprice(text):
    price.delete(0,"end")
    price.insert(0, str(text))


def setTextidstock():
    text = scan_code()
    connectObj2 = sqlite3.connect("shopManagement.db")
    cur = connectObj2.cursor()
    cur.execute("SELECT quantity FROM products WHERE productid=?", (text,))
    rows2 = cur.fetchall()
    if len(rows2) == 0:
        prompt("No such product found!")
    else:
        stock_id.delete(0,"end")
        stock_id.insert(0, str(text))


def remove_item():
    curItem = tree.focus()
    for i in tree.item(curItem):
        if i == 'values':
            cur = tree.item(curItem)[i]
    for i in itemlist:
        curid = cur[0]
        if i[0] == str(curid):
            itemlist.remove(i)
    tree.delete(curItem)


def prompt(str):
    messagebox.askokcancel(title='ERROR', message=str)


def print_bill():
    billn = billno.get()
    phoneno = phone.get()
    cusn = cname.get()
    if  len(billn) == 0 or len(phoneno) == 0 or len(cusn) == 0:
        prompt("Fill all the entries!")
    else:
        filepath = cusn+billn+'.txt'
        with open(filepath , 'w') as filehandle:
            filehandle.writelines(
                "{:<20} {:<20} \n".format("CUSTUMER NAME:", cusn))
            filehandle.writelines(
                "{:<20} {:<20} \n".format("CONTACT NO.:", phoneno))
            filehandle.writelines(
                "{:<20} {:<20} \n".format("BILL NO.:", billn))
            filehandle.writelines("\n")
            filehandle.writelines(
                "{:<20} {:<20} {:<20} {:<20} {:20}\n".format("Product ID", "Product Name", "MRP", "Quantity", "Total"))
            filehandle.writelines(
                "{:<20} {:<20} {:<20} {:<20} {:20}\n".format(item[0], item[1], item[2], item[3], item[4]) for item in
                itemlist)
        billno.delete(0, "end")
        phone.delete(0, "end")
        cname.delete(0, "end")


def generate_bill():
    sum = 0
    for i in itemlist:
        sum = sum + i[4]
    temp = ["-", "-", "-", "Total:", sum]
    itemlist.append(temp)
    tree.insert('', END, values=temp)
    for i in itemlist:
        connectObj = sqlite3.connect("shopManagement.db")
        cur = connectObj.cursor()
        cur.execute("UPDATE products SET quantity=quantity-? WHERE productid = ? ", (i[3],i[0]))
        connectObj.commit()


def addstock(stk):
    pid = stock_id.get()
    connectObj2 = sqlite3.connect("shopManagement.db")
    cur = connectObj2.cursor()
    cur.execute("SELECT quantity FROM products WHERE productid=?", (pid,))
    rows2 = cur.fetchall()
    if len(rows2) == 0:
        prompt("No such product found!")
    else:
        connectObj = sqlite3.connect("shopManagement.db")
        cur = connectObj.cursor()
        cur.execute("UPDATE products SET quantity=quantity+? WHERE productid = ? ", (stk, pid))
        stock_id.delete(0,"end")
        stock.delete(0, "end")
        connectObj.commit()
        printinventory()
#    connectObj2 = sqlite3.connect("shopManagement.db")
#    cur = connectObj2.cursor()
#    cur.execute("SELECT * FROM products")
#    rows = cur.fetchall()
#   print(rows)


def setaddpid():
    text = scan_code()
    product_idadd.delete(0, "end")
    product_idadd.insert(0, str(text))


def printinventory():
    txt_stock.delete("1.0", "end")
    connectObj2 = sqlite3.connect("shopManagement.db")
    cur = connectObj2.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    txt_stock.insert(END, "{0:^20} \t".format('PRODUCT ID'))
    txt_stock.insert(END, "{0:^20} \t".format('PRODUCT NAME'))
    txt_stock.insert(END, "{0:^20} \t".format('PRICE(Rupees)'))
    txt_stock.insert(END, "{0:^20} \t\n".format('STOCK'))
    for i in rows:
        for k in i:
            txt_stock.insert(END, "{0:^20} \t".format(k))
        txt_stock.insert(END, "\n")


def addproducttoinv():
    paddid = product_idadd.get()
    pnameadd =productnameadd.get()
    priceadd = pricetoadd.get()
    quanadd = quantoadd.get()

    connectObj2 = sqlite3.connect("shopManagement.db")
    cur = connectObj2.cursor()
    cur.execute("SELECT productid FROM products WHERE productid = ? ", (paddid,))
    rows2 = cur.fetchall()
    print(rows2)
    if len(rows2) == 0:
        if len(paddid) == 0 or len(pnameadd) == 0 or len(priceadd) == 0 or len(quanadd) == 0 :
            prompt("Fill all the entries!")
        else:
            connectObj = sqlite3.connect("shopManagement.db")
            cur = connectObj.cursor()
            cur.execute("INSERT into products VALUES(?,?,?,?)", (paddid, pnameadd, priceadd, quanadd,))
            connectObj.commit()
            product_idadd.delete(0, "end")
            productnameadd.delete(0, "end")
            pricetoadd.delete(0, "end")
            quantoadd.delete(0, "end")
    else:
        prompt("Product allready present!")
        product_idadd.delete(0, "end")
        productnameadd.delete(0, "end")
        pricetoadd.delete(0, "end")
        quantoadd.delete(0, "end")
    #connectObj2 = sqlite3.connect("shopManagement.db")
    #cur = connectObj2.cursor()
    #cur.execute("SELECT * FROM products")
    #rows = cur.fetchall()
    #print(rows)

def removeproduct(rpid):
    connectObj2 = sqlite3.connect("shopManagement.db")
    cur = connectObj2.cursor()
    cur.execute("SELECT productid FROM products WHERE productid = ? ", (rpid,))
    rows2 = cur.fetchall()
    print(rows2)
    if len(rows2) == 0:
        prompt("NO PRODUCT FOUND!")
    else:
        connectObj = sqlite3.connect("shopManagement.db")
        cur = connectObj.cursor()
        cur.execute("DELETE FROM products WHERE productid = ?", (rpid,))
        connectObj.commit()
        product_idadd.delete(0, "end")
        stock_id.delete(0, "end")
        printinventory()

'''connectObj = sqlite3.connect("shopManagement.db")
cur = connectObj.cursor()
cur.execute("DROP table products")
connectObj.commit()'''
connection()
'''connectObj = sqlite3.connect("shopManagement.db")
cur = connectObj.cursor()
cur.execute("INSERT INTO products VALUES('11111', 'kurkure', 124, 23)")
connectObj.commit()'''

window = Tk()
window.title("SMALL BAZAR")
window.iconbitmap('favicon.ico')
window.geometry("1086x806")
tabs = ttk.Notebook(window)
tab1 = ttk.Frame(tabs)
tab2 = ttk.Frame(tabs)
tabs.add(tab1, text='Sell')
tabs.add(tab2, text='Stock')
tabs.pack(expand=1, fill="both")
itemlist = []
image=Image.open('shopping-cart.png')
img=image.resize((50, 50))
myimg=ImageTk.PhotoImage(img)
lab = Label(tab1, text="SMALL BAZAR",bg="#2b6777",fg='white', font=('Arial', 25, 'bold'))
lab.pack(fill=X)
lab["compound"] = LEFT
lab["image"] = myimg
# ////////costumer frame////////////
f1=LabelFrame(tab1,text="Cuntumer details", font=("times new roman",20,"bold"),fg="#fae5df",bg="#52ab98")
f1.place(x=0,y=80,relwidth=1)
custname = Label(f1,text="Custumer name",font=("times new roman",15,"bold"),bg="#52ab98",fg="white")
custname.grid(row=0,column=0)
cname = Entry(f1, font=('Times New Roman', 15, 'bold'),bg='white', fg="#86a3d9", width=15,bd=4,relief=RIDGE)
cname.grid(row=0,column=1,pady=5,padx=20)
number = Label(f1,text="Contact Number",font=("times new roman",15,"bold"),bg="#52ab98",fg="white")
number.grid(row=0,column=2)
phone = Entry(f1, font=('Times New Roman', 15, 'bold'),bg='white', fg="#86a3d9", width=15,bd=4,relief=RIDGE)
phone.grid(row=0,column=3,pady=5,padx=20)
bill = Label(f1,text="Bill No.",font=("times new roman",15,"bold"),bg="#52ab98",fg="white")
bill.grid(row=0,column=4)
billno = Entry(f1, font=('Times New Roman', 15, 'bold'),bg='white', fg="#86a3d9", width=15,bd=4,relief=RIDGE)
billno.grid(row=0,column=5,pady=5,padx=20)
# /////////////////////////////////////////////////////////
# fram2
f2 = LabelFrame(tab1,text="Product", font=("times new roman",20,"bold"),fg="#fae5df",bg="#52ab98")
f2.place(x=0, y=190)
name = Label(f2, text="Product Name",font=("times new roman",15,"bold"),bg="#52ab98",fg="white")
name.grid(row=0, column=0)
productname = Entry(f2, font=('Times New Roman', 15, 'bold'),bg='white', fg="#86a3d9", width=15,bd=4,relief=RIDGE)
productname.grid(row=0,column=1, pady=20, padx=10)
p_id = Label(f2,text="Product ID",font=("times new roman",15,"bold"),bg="#52ab98",fg="white")
p_id.grid(row=1,column=0)
product_id = Entry(f2, font=('Times New Roman', 15, 'bold'),bg='white', fg="#86a3d9", width=15,bd=4,relief=RIDGE)
product_id.grid(row=1,column=1, pady=20, padx=10)
pr = Label(f2,text="Price",font=("times new roman",15,"bold"),bg="#52ab98",fg="white")
pr.grid(row=2,column=0)
price = Entry(f2, font=('Times New Roman', 15, 'bold'),bg='white', fg="#86a3d9", width=15,bd=4,relief=RIDGE)
price.grid(row=2, column=1, pady=20, padx=10)
quantity = Label(f2,text="Quantity",font=("times new roman",15,"bold"),bg="#52ab98",fg="white")
quantity.grid(row=3,column=0)
quan = Entry(f2, font=('Times New Roman', 15, 'bold'),bg='white', fg="#86a3d9", width=15,bd=4,relief=RIDGE)
quan.grid(row=3, column=1, pady=25, padx=10)
scan = Button(f2, text="SCAN", command = lambda:setTextid(), width=12, bd=7, font=("Times New Roman",12), bg="#c8d8e4", activebackground='#2b6777', activeforeground='white',relief=RIDGE)
scan.grid(row=4, column=0, pady=25, padx=10)

add = Button(f2, text="ADD TO CART", command = lambda:addtocart(product_id.get(), productname.get(), price.get(), quan.get()), width=12, bd=7, font=("Times New Roman",12), bg="#c8d8e4", activebackground='#2b6777', activeforeground='white',relief=RIDGE)
add.grid(row=4, column=1, pady=20, padx=10)
# /////////////////////////////////////////////////
f3 = LabelFrame(tab1,text="Item List", font=("times new roman",20,"bold"),fg="#fae5df",bg="#52ab98")
f3.place(x=340, y=190)

columns = ('Pid', 'Pname', 'Mrp', 'quant', 'Total')
tree = ttk.Treeview(f3, columns=columns, show='headings',height=16)
# define headings
tree.heading('Pid', text='Pruduct Id',)
tree.column("Pid",minwidth=0,width=150, anchor=CENTER)
tree.heading('Pname', text='Name')
tree.column("Pname",minwidth=0,width=150, anchor=CENTER)
tree.heading('Mrp', text='MRP')
tree.column("Mrp",minwidth=0,width=150, anchor=CENTER)
tree.heading('quant', text='Quantity')
tree.column("quant",minwidth=0,width=150, anchor=CENTER)
tree.heading('Total', text='Total')
tree.column("Total",minwidth=0,width=150, anchor=CENTER)
tree.pack(side ='left')
verscrlbar = ttk.Scrollbar(f3,
                           orient="vertical",
                           command=tree.yview)
verscrlbar.pack(side='right', fill='y')
tree.configure(xscrollcommand=verscrlbar.set)
# /////////////////////////////////////////////////
f4 = LabelFrame(tab1, fg="#fae5df",bg="#52ab98")
f4.place(x=340, y=570)
delete = Button(f4, text="DELETE", command=lambda:remove_item() , width=20, bd=7, font=("Times New Roman",13), bg="#c8d8e4", activebackground='#2b6777', activeforeground='white',relief=RIDGE)
delete.grid(row=0, column=0, pady=3, padx=28)
bill = Button(f4,text="BILL", command=lambda:generate_bill(), width=20, bd=7, font=("times new roman",13), bg="#c8d8e4", activebackground='#2b6777', activeforeground='white',relief=RIDGE)
bill.grid(row=0, column =1, pady=3, padx=28)
printbill = Button(f4,text="PRINT BILL", command=lambda:print_bill(), width=20, bd=7, font=("times new roman",13), bg="#c8d8e4", activebackground='#2b6777', activeforeground='white',relief=RIDGE)
printbill.grid(row=0, column =2, pady=3, padx=28)
# /////////////////////////////////////////////////
lab = Label(tab2, text="SMALL BAZAR",bg="#2b6777",fg='white', font=('Arial', 25, 'bold'))
lab.pack(fill=X)
lab["compound"] = LEFT
lab["image"] = myimg
lab = Label(tab2, text="INVENTORY",bg="#2b6777",fg='white', font=('Arial', 15, 'bold'))
lab.pack(fill=X)
f5 = LabelFrame(tab2, fg="#fae5df",bg="#52ab98")
f5.place(x=0, y=100)
s_id = Label(f5,text="Product ID",font=("times new roman",15,"bold"),bg="#52ab98",fg="white")
s_id.grid(row=1,column=0)
s_id = Label(f5,text="Quantity",font=("times new roman",15,"bold"),bg="#52ab98",fg="white")
s_id.grid(row=1,column=2)
stock_id = Entry(f5, font=('Times New Roman', 15, 'bold'),bg='white', fg="#86a3d9", width=20,bd=4,relief=RIDGE)
stock_id.grid(row=1,column=1, pady=20)
stock = Entry(f5, font=('Times New Roman', 15, 'bold'),bg='white', fg="#86a3d9", width=20,bd=4,relief=RIDGE)
stock.grid(row=1,column=3, pady=20)
scan = Button(f5, text="SCAN", command = lambda:setTextidstock(), width=20, bd=7, font=("Times New Roman",12), bg="#c8d8e4", activebackground='#2b6777', activeforeground='white',relief=RIDGE)
scan.grid(row=2, column=0, pady=25, padx=10)
add = Button(f5, text="ADD STOCK", command = lambda:addstock((stock.get())), width=20, bd=7, font=("Times New Roman", 12), bg="#c8d8e4", activebackground='#2b6777', activeforeground='white',relief=RIDGE)
add.grid(row=2, column=1, pady=25, padx=10)
sub = Button(f5, text="REMOVE STOCK", command = lambda:addstock("-"+(stock.get())), width=20, bd=7, font=("Times New Roman", 12), bg="#c8d8e4", activebackground='#2b6777', activeforeground='white',relief=RIDGE)
sub.grid(row=2, column=2, pady=25, padx=10)
removwp = Button(f5, text="REMOVE PRODUCT", command = lambda:removeproduct(stock_id.get()), width=20, bd=7, font=("Times New Roman", 12), bg="#c8d8e4", activebackground='#2b6777', activeforeground='white',relief=RIDGE)
removwp.grid(row=2, column=3, pady=25, padx=10)
printinv = Button(f5, text="PRINT INVENTORY", command = lambda:printinventory(), width=20, bd=7, font=("Times New Roman", 12), bg="#c8d8e4", activebackground='#2b6777', activeforeground='white',relief=RIDGE)
printinv.grid(row=2, column=4, pady=25, padx=10)
f6 = LabelFrame(tab2,text="Add Products", font=("times new roman",20,"bold"),fg="#fae5df",bg="#52ab98")
f6.place(x=0, y=275)
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
name = Label(f6, text="Product Name",font=("times new roman",15,"bold"),bg="#52ab98",fg="white")
name.grid(row=0, column=0)
productnameadd = Entry(f6, font=('Times New Roman', 15, 'bold'),bg='white', fg="#86a3d9", width=15,bd=4,relief=RIDGE)
productnameadd.grid(row=0,column=1, pady=20, padx=10)
p_id = Label(f6,text="Product ID",font=("times new roman",15,"bold"),bg="#52ab98",fg="white")
p_id.grid(row=1,column=0)
product_idadd = Entry(f6, font=('Times New Roman', 15, 'bold'),bg='white', fg="#86a3d9", width=15,bd=4,relief=RIDGE)
product_idadd.grid(row=1,column=1, pady=20, padx=10)
pr = Label(f6,text="Price",font=("times new roman",15,"bold"),bg="#52ab98",fg="white")
pr.grid(row=2,column=0, padx=10)
pricetoadd = Entry(f6, font=('Times New Roman', 15, 'bold'),bg='white', fg="#86a3d9", width=15,bd=4,relief=RIDGE)
pricetoadd.grid(row=2, column=1, pady=20, padx=10)
quantity = Label(f6,text="Quantity",font=("times new roman",15,"bold"),bg="#52ab98",fg="white")
quantity.grid(row=3,column=0, padx=10)
quantoadd = Entry(f6, font=('Times New Roman', 15, 'bold'),bg='white', fg="#86a3d9", width=15,bd=4,relief=RIDGE)
quantoadd.grid(row=3, column=1, pady=25, padx=10)
scan = Button(f6, text="SCAN", command = lambda:setaddpid(), width=12, bd=7, font=("Times New Roman",12), bg="#c8d8e4", activebackground='#2b6777', activeforeground='white',relief=RIDGE)
scan.grid(row=4, column=0, pady=25, padx=10)
addproduct = Button(f6, text="Add Product", command = lambda:addproducttoinv(), width=12, bd=7, font=("Times New Roman",12), bg="#c8d8e4", activebackground='#2b6777', activeforeground='white',relief=RIDGE)
addproduct.grid(row=4, column=1, pady=25, padx=10)
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

f7 = LabelFrame(tab2, fg="#fae5df",bg="#52ab98")
f7.place(x=340, y=275)
txt_stock = Text(f7, height =24.5, width = 95)
l = Label(f7, text = "INVENTORY",bg="#52ab98", font =("Courier", 14))
l.pack()
txt_stock.pack()

window.mainloop()