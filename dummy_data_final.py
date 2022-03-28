import pyodbc
import names
import random
import datetime
import time
from random_address import real_random_address_by_state
from random_username.generate import generate_username

##Util functions
def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))

def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y%m%d %H:%M:%S', prop)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

##insert into Complaints
def create_dummy_complaints(commit):
    print("Creating dummy Complaints")
    lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean et nunc nec libero dictum porta quis quis sem. Maecenas vulputate elit vel tellus congue porta. Integer sed mollis sapien. Donec euismod ipsum nec dui ultricies imperdiet. Vivamus finibus porta lectus a vulputate. Donec vulputate elementum odio, sed cursus massa euismod congue. Sed placerat, augue at ultrices condimentum, orci lectus pretium turpis, quis vestibulum neque eros id dui. Maecenas condimentum ex sit amet volutpat consectetur. Curabitur placerat leo quis mauris molestie dignissim. Proin finibus felis eget ante vulputate vestibulum. Vivamus arcu massa, vulputate non nibh sit amet, finibus faucibus risus. Mauris feugiat neque et velit mollis dignissim. Sed non varius ligula. Cras venenatis lorem ut blandit luctus. Vestibulum libero sapien, interdum eget enim eu, consectetur accumsan magna. Ut in ex suscipit, luctus quam non, sagittis turpis.".split(" ")
    status = ["Pending", "Being handled", "Addressed"]
    uid_count = list(cursor.execute("select COUNT(*) from Users"))[0][0]
    eid_count = list(cursor.execute("select COUNT(*) from Employees"))[0][0]
    if commit:
        start = time.time()
        for i in range(10000):
            try:
                text = " ".join(random.sample(lorem_ipsum, 5))
                handled_date = random_date("20210101 00:00:00", "20220101 00:00:00", random.random())
                filed_date = datetime.datetime.strptime(handled_date, '%Y%m%d %H:%M:%S') - datetime.timedelta(days=random.randint(1,30))
                is_handled = True #random.randint(0,10) > 3
                none = None
                cursor.execute(f"insert into Complaints(FilledDateTime, HandledDateTime, Text, Status, EID, UID) values ('{filed_date}','{handled_date if is_handled else none}','{text}','{status[0] if not is_handled else random.choice(status[1:])}','{random.randint(1,eid_count)}','{random.randint(1,uid_count)}')")
            except Exception as e:
                print(e)
        cursor.commit()
        print(f"Time taken: {time.time() - start} seconds")

##insert into ComplaintsOnOrders
def create_dummy_complaints_on_orders(commit):
    print("Creating dummy ComplaintsOnOrders")
    complaints = list(cursor.execute("select * from Complaints"))
    orders = list(cursor.execute("select * from Orders"))
    if commit:
        start = time.time()
        for i in range(len(orders)):
            try:
                cursor.execute(f"insert into ComplaintsOnOrders(CID, OID) values ('{random.choice(complaints)[0]}', '{random.choice(orders)[0]}')")
            except Exception as e:
                print(e)
        cursor.commit()
        print(f"Time taken: {time.time() - start} seconds")

##insert into ComplaintsOnShops
def create_dummy_complaints_on_shops(commit):
    print("Creating dummy ComplaintsOnShops")
    complaints = list(cursor.execute("select * from Complaints"))
    shops = list(cursor.execute("select * from Shops"))
    if commit:
        start = time.time()
        for i in range(1000):
            try:
                cursor.execute(f"insert into ComplaintsOnShops(CID, Sname) values ('{random.choice(complaints)[0]}', '{random.choice(shops)[0]}')")
            except Exception as e:
                print(e)
        cursor.commit()
        print(f"Time taken: {time.time() - start} seconds")

##insert into Employees
def create_dummy_employees(commit):
    print("Creating dummy Employees")
    if commit:
        start = time.time()
        random_names = [names.get_full_name() for i in range(1000)]
        for i in range(len(random_names)):
            cursor.execute(f"insert into Employees(Name,SALARY) values ('{random_names[i]}','{random.randint(1000,9000)}')")
        cursor.commit()
        print(f"Time taken: {time.time() - start} seconds")

##insert into Feedback
def create_dummy_feedback(commit):
    print("Creating dummy Feedback")
    lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean et nunc nec libero dictum porta quis quis sem. Maecenas vulputate elit vel tellus congue porta. Integer sed mollis sapien. Donec euismod ipsum nec dui ultricies imperdiet. Vivamus finibus porta lectus a vulputate. Donec vulputate elementum odio, sed cursus massa euismod congue. Sed placerat, augue at ultrices condimentum, orci lectus pretium turpis, quis vestibulum neque eros id dui. Maecenas condimentum ex sit amet volutpat consectetur. Curabitur placerat leo quis mauris molestie dignissim. Proin finibus felis eget ante vulputate vestibulum. Vivamus arcu massa, vulputate non nibh sit amet, finibus faucibus risus. Mauris feugiat neque et velit mollis dignissim. Sed non varius ligula. Cras venenatis lorem ut blandit luctus. Vestibulum libero sapien, interdum eget enim eu, consectetur accumsan magna. Ut in ex suscipit, luctus quam non, sagittis turpis.".split(" ")
    products_in_orders = list(cursor.execute("select * from ProductsInOrders"))
    uid_count = list(cursor.execute("select COUNT(*) from Users"))[0][0]
    rating = [1,2,3,3,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
    if commit:
        start = time.time()
        for i in range(len(products_in_orders)):
            try:
                text = " ".join(random.sample(lorem_ipsum, 6))
                date = products_in_orders[i][3] + datetime.timedelta(days=random.randint(1,30)) #if random.randint(1,10) < 4 and products_in_orders[i][3] < datetime.datetime.strptime(random_date("20210801 00:00:00", "20210801 00:00:01", random.random()), '%Y%m%d %H:%M:%S')else datetime.datetime.strptime(random_date("20210801 00:00:00", "20210801 00:00:01", random.random()), '%Y%m%d %H:%M:%S') + datetime.timedelta(days=random.randint(1,30))
                cursor.execute(f"insert into Feedback(UID, OPID, Comment, DateTime, RATING) values ('{random.randint(1,uid_count)}','{products_in_orders[i][0]}','{text}','{date}','{random.choice(rating)}')")
            except Exception as e:
                print(e)
        cursor.commit()
        print(f"Time taken: {time.time() - start} seconds")

##insert into Orders
def create_dummy_orders(commit):
    print("Creating dummy Orders")
    uid_count = list(cursor.execute("select COUNT(*) from Users"))[0][0]
    if commit:
        start = time.time()
        for i in range(20000):
            try:
                address = real_random_address_by_state("CA")["address1"]
                r_date = random_date("20210101 00:00:00", "20220101 00:00:00", random.random()) if random.randint(1,10) < 3 else random_date("20210801 00:00:00", "20210801 00:00:01", random.random())
                cursor.execute(f"insert into Orders(DateTime, ShippingAddress, ShippingCost, UID) values ('{r_date}', '{address}', '{random.randint(0,100)}','{random.randint(1,uid_count)}')")
            except Exception as e:
                print("ERROR: ", end="")
                print(e)
        cursor.commit()
        print(f"Time taken: {time.time() - start} seconds")

##insert into PriceHistory
def create_dummy_price_history(commit):
    print("Creating dummy PriceHistory")
    spid_count = list(cursor.execute("select COUNT(*) from ProductListings"))[0][0]
    if commit:
        start = time.time()
        start_date = datetime.date(2021, 1, 1)
        end_date = datetime.date(2022, 1, 1)
        for single_date in daterange(start_date, end_date):
            for spid in range(spid_count):
                try:
                    cursor.execute(f"insert into PriceHistory(SPID, StartDate, EndDate, Price) values ('{spid}','{single_date}','{single_date}','{random.randint(1000,2000)}')")
                except Exception as e:
                    print(e)
        cursor.commit()
        print(f"Time taken: {time.time() - start} seconds")

##insert into ProductListings
def create_dummy_product_listings(commit):
    print("Creating dummy ProductListings")
    if commit:
        start = time.time()
        products = list(cursor.execute("select * from Products"))
        shops = list(cursor.execute("select * from Shops"))
        for i in range(200):
            try:
                cursor.execute(f"insert into ProductListings(SPrice, SQuantity, PName, SName) values ('{random.randint(1000,2000)}','{random.randint(10,200)}','{random.choice(products)[0]}','{random.choice(shops)[0]}')")
            except Exception as e:
                print(e)
        cursor.commit()
        print(f"Time taken: {time.time() - start} seconds")

##insert into Products
def create_dummy_products(commit):
    print("Creating dummy Products")
    if commit:
        start = time.time()
        phones = ["Samsung Galaxy S", "iPhone ", "Xiaomi Mi ", "Huawei P"]
        maker_dict = {
            "Samsung Galaxy S":"Samsung",
            "iPhone ":"Apple Inc.",
            "Xiaomi Mi ":"Xiaomi",
            "Huawei P":"Huawei"
        }

        for i in range(1000):
            phone = random.choice(phones)
            maker = maker_dict[phone]
            try:
                version_number = str(random.randint(8,11))
                if phone == phones[1]:
                    if int(version_number) == 10:
                        version_number = 'X'
                cursor.execute(f"insert into Products(Pname, Maker, Category) values ('{phone+version_number}','{maker}','Smartphone')")
            except Exception as e:
                print(e)
        cursor.commit()
        print(f"Time taken: {time.time() - start} seconds")

##insert into ProductsInOrders
def create_dummy_productsinorders(commit):
    print("Creating dummy ProductsInOrders")
    products = list(cursor.execute("select * from Products"))
    shops = list(cursor.execute("select * from Shops"))
    orders = list(cursor.execute("select * from Orders"))
    if commit:
        start = time.time()
        for i in range(len(orders)):
            try:
                quantity = random.randint(1,10)
                order_selected = orders[i]
                order_date = order_selected[1]
                delivery_date = order_date + datetime.timedelta(days=random.randint(1,30))
                print(f"{order_date} {delivery_date}")
                status = ["Being processed", "Shipped", "Delivered", "Returned"]
                cursor.execute(f"insert into ProductsInOrders( OPrice, OQuantity, DeliveryDate, Status, PName, Sname, OID) values ('{random.randint(1000,2000)*quantity}','{quantity}','{delivery_date}','{random.choice(status)}','{random.choice(products)[0]}','{random.choice(shops)[0]}','{order_selected[0]}')")
            except Exception as e:
                print(e)
        cursor.commit()
        print(f"Time taken: {time.time() - start} seconds")
        return

##insert into Shops
def create_dummy_shops(commit):
    print("Creating dummy Shops")
    if commit:
        start = time.time()
        for i in range(1000):
            cursor.execute(f"insert into Shops(Sname) values ('PhoneShop{i+1}')")
        cursor.commit()
        print(f"Time taken: {time.time() - start} seconds")

##insert into Users
def create_dummy_users(commit):
    print("Creating dummy Users")
    if commit:
        start = time.time()
        usernames = generate_username(1000)
        for i in range(len(usernames)):
            cursor.execute(f"insert into Users(UName) values ('{usernames[i]}')")
        cursor.commit()
        print(f"Time taken: {time.time() - start} seconds")

if __name__ == "__main__":
    server = '155.69.100.36'
    database = 'ss8g2DB'
    username = 'ss8g2'
    password = 'P@ssw0rd!'

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()
    delete = True
    if delete:
        try:
            print("Deleting previous entries")
            cursor.execute("DELETE FROM Feedback")
            cursor.execute("DELETE FROM PriceHistory")
            cursor.execute("DELETE FROM ComplaintsOnOrders")
            cursor.execute("DELETE FROM ComplaintsOnShops")
            cursor.execute("DELETE FROM ProductsInOrders")
            cursor.execute("DELETE FROM ProductListings")
            cursor.execute("DELETE FROM Complaints")
            cursor.execute("DELETE FROM Users")
            cursor.execute("DELETE FROM Shops")
            cursor.execute("DELETE FROM Employees")
            cursor.execute("DELETE FROM Orders")
            cursor.execute("DELETE FROM Products")
            cursor.execute("DBCC CHECKIDENT (Users, RESEED, 0)")
            cursor.execute("DBCC CHECKIDENT (Employees, RESEED, 0)")
            cursor.execute("DBCC CHECKIDENT (Orders, RESEED, 0)")
            cursor.execute("DBCC CHECKIDENT (Complaints, RESEED, 0)")
            cursor.execute("DBCC CHECKIDENT (ProductListings, RESEED, 0)")
            cursor.execute("DBCC CHECKIDENT (ProductsInOrders, RESEED, 0)")
            cursor.commit()
            print("Deletion completed")
        except Exception as e:
            print(e)
    create_dummy_employees(True)
    create_dummy_users(True)
    create_dummy_shops(True)
    create_dummy_products(True)
    create_dummy_orders(True)
    create_dummy_complaints(True)
    create_dummy_product_listings(True)
    create_dummy_productsinorders(True)
    create_dummy_price_history(True)
    create_dummy_complaints_on_orders(True)
    create_dummy_complaints_on_shops(True)
    create_dummy_feedback(True)
