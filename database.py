import MySQLdb
from datetime import date,datetime
import mailsender
# db = MySQLdb.connect("localhost","udaram","udardc@123","canteen" )

# # prepare a cursor object using cursor() method
# cursor = db.cursor()
# try:
#     #cursor.execute("insert into hi values(1,'udaram'),(2,'dayal')")
#     db.commit()
#     cursor.execute('select *from hi')
#     info= cursor.fetchall()
#     print(info)
# except:
#     pass
# # disconnect from server
# db.close()

class mydatabase:
    def __init__(self):
        self.db = MySQLdb.connect("localhost",
        "udaram",
        "udardc@123",
        "canteen")
        self.cursor = self.db.cursor()

    def get_menu(self,status=1):
        query=f"SELECT * FROM menu WHERE status = {status} "
        self.cursor.execute(query)
        return self.data_description(self.cursor.fetchall(),self.cursor.description)

    def get_item_info(self,item):
        try:
            query=f"SELECT *FROM menu WHERE item='{item}'"
            self.cursor.execute(query)
            return self.data_description(self.cursor.fetchall(),self.cursor.description)
        except:
            pass
    def update_item_info(self,item,item_updated,price_updated):
            try:
                query = f"UPDATE menu SET item='{item_updated}',price={price_updated},status=1 WHERE item='{item}'"
                self.cursor.execute(query)
                self.db.commit()
            except:
                pass
    def delete_item_status(self,item):
        try:
            query = f"UPDATE menu SET status=0 WHERE item='{item}'"
            self.cursor.execute(query)
            self.db.commit()
        except:
            pass
        
    def fetchreviews(self,item):
        query = f"SELECT distinct * FROM review WHERE item='{item}'"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        data = self.data_description(data,self.cursor.description)
        return data

    # insert reviews into the review table
    def insertreview(self,item,review,sentiment,c_name):
        try:
            query = f'''INSERT INTO review(username,item,review,sentiment,date)  VALUES('{c_name}','{item}','{review}','{sentiment}','{date.today()}')'''
            self.cursor.execute(query)
            self.db.commit()
        except:
            pass
    
    def add_menu(self,item,price):
        try:
            query=f"INSERT INTO menu VALUES('{item}',{price},{1})"
            self.cursor.execute(query)
            self.db.commit() 
        except:
            pass
    def contact_feedback(self,username,name,email,phone,message):
        try:
            contact_id = username+str(datetime.now())
            query = f"INSERT INTO contact VALUES('{contact_id}','{username}','{name}','{email}','{phone}','{message}')"
            self.cursor.execute(query)
            self.db.commit()
        except:
            pass
    
    def get_user_info(self,username):
        try:
            query = f"SELECT *FROM User WHERE username='{username}'"
            self.cursor.execute(query)
            return self.data_description(self.cursor.fetchall(),self.cursor.description)
        except:
            pass 

    def bookorder(self,username,selected_menu,total_amount):
        try:
            order_id = username+str(datetime.now())
            query = "INSERT INTO orders VALUES"
            for item in selected_menu:
                query = query + f"('{order_id}','{item['item']}',{item['price']},{item['quantity']}),"
            query = query[:-1]
            self.cursor.execute(query)
            self.cursor.execute(f"INSERT INTO orderInfo(orderID,amount,date,username) VALUES('{order_id}',{total_amount},'{date.today()}','{username}')")
            self.db.commit()
        except:
            pass

    def get_user_orders(self,username):
        try:
            query = f"SELECT * FROM orderInfo where username='{username}'"
            self.cursor.execute(query)
            return self.data_description(self.cursor.fetchall(),self.cursor.description)
        except:
            # print("hi")
            pass
    
    def get_all_orders(self):
        try:
            query = f"SELECT * FROM orderInfo"
            self.cursor.execute(query)
            return self.data_description(self.cursor.fetchall(),self.cursor.description)
        except:
            pass

    def get_order_details(self,orderid):
        try:
            query = f"SELECT * FROM orders O NATURAL JOIN (SELECT * FROM orderInfo WHERE orderID='{orderid}') I "
            self.cursor.execute(query)
            return self.data_description(self.cursor.fetchall(),self.cursor.description)
        except:
            pass

    def confirm_order(self,orderid,username):
        try:
            query = f"UPDATE orderInfo SET status='confirmed' WHERE orderID='{orderid}'"
            self.cursor.execute(query)
            self.db.commit()
            info = self.get_user_info(username)[0]
            order = self.get_order_details(orderid)
            mailsender.orderconfirmation(info['email'],order)
        except:
            pass

    def password_reset(self,username,password):
        try:
            query=f"UPDATE User SET password='{password}' WHERE username='{username}'"
            self.cursor.execute(query)
            self.db.commit()
        except:
            pass
    
    def signup(self,name,email,mobile,password,status):
        try:
            username = email.split("@")[0]
            query = f"""INSERT INTO User(username,name,email,mobile,password,status,verification) VALUES('{username}','{name}','{email}','{mobile}','{password}','{status}','{0}')"""
            self.cursor.execute(query)
            self.db.commit()
            #send email for verification
            s=mailsender.verification_email(email)
            #if mail is not valid
            if s == -1:
                return -2
            #user inserted successfully 
            return 1
        except:
            query = f"""SELECT *FROM User where email='{email}'"""
            self.cursor.execute(query)
            #get exact query result
            data=self.data_description(self.cursor.fetchall(),self.cursor.description)
            if data[0]['verification']==0:
                #user exist but email verification not done
                s=mailsender.verification_email(email)
                #send email for verification
                return -1 
            else:
                #user exist already
                return 0
            
    def login(self,email,password):
        try:
            query = f"""SELECT * FROM User WHERE email='{email}'"""
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            #user not exist
            if len(data) == 0:
                return -1 
            else:
                data = self.data_description(data,self.cursor.description)[0]
                #wrong password
                if data['password']!=password:
                    return 0
                #verification not done
                elif data['verification']==0:
                    return -1
                else:
                    return 1  
        except:
            return None

    def user_verification(self,username):
        try:
            query = f"""UPDATE User SET verification=1 WHERE username='{username}'"""
            self.cursor.execute(query)
            self.db.commit()
            return 1
        except:
            return -1 

    def data_description(self,result,des):
        field_name = [field[0] for field in des]
        data = []
        for d in result:
            temp = {}
            for i in range(len(d)):
                temp[field_name[i]]=d[i] 
            data.append(temp)
        return data





# h=mydatabase()
# x=h.login('udaramrdc@gmail.com','ssss')
# # query = f"""SELECT *FROM User where email='udaramrdc@gmail.com'"""
# # h.cursor.execute(query)
# # print(h.cursor.fetchall())
# print(x)
# 
# 

# x=h.login('udaramrdc@gmail.com')