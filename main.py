from flask import Flask,render_template,request,session,redirect,flash
import database
import review_analyser
import clarifi_tag_suggestions
import os
import json
import mailsender
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'my-secret-key'
app.config['UPLOAD_FOLDER'] = "/home/udaram/Desktop/DBMS/canteen/static/upload"

with open('config.json','r') as cc:
    params = json.load(cc)["params"]

@app.route('/')
def home():
    if 'user' in session:
        menu=database.mydatabase().get_menu()
        return render_template('index.html',user=session['user'],menu=enumerate(menu))
    else:
        return redirect("/login")

@app.route('/selectedmenu',methods=['GET','POST'])
def selectedmenu():
    if 'user' in session:
        if request.method=="POST":
            selected_menu_list = request.form.getlist('check')
            if(len(selected_menu_list)==0):
                flash("Select items before proceed further!!","danger")
                return redirect("/")
            #print(request.form.get('price_pizza')) 
            selected_item_slip = []
            menu = database.mydatabase().get_menu()
            total_amount=0
            for item in menu:
                temp ={}
                if item['item'] in selected_menu_list:
                    temp['item'] = item['item']
                    temp['price'] = item['price']
                    temp['quantity'] = request.form.get('quantity_'+item['item'])
                    temp['amount'] = temp['price']*int(temp['quantity'])
                    total_amount += temp['amount']
                    selected_item_slip.append(temp)
            return render_template('selectedmenu.html',user=session['user'],items=selected_item_slip,total_amount=total_amount,length=len(selected_item_slip))
        else:
            return redirect("/")
    else:
        return redirect("/login")

@app.route("/success")
def success():
    if 'user' in session:
        return render_template("success.html")
    return redirect("/login")

@app.route("/bookorder/<selected_menu>/<float:total_amount>", methods=["POST","GET"])
def bookorder(selected_menu,total_amount):         
    if 'user' in session:
        if request.method=="POST":
            database.mydatabase().bookorder(session['user'],eval(selected_menu),total_amount)
            #{'item': 'Burger', 'price': 11.0, 'quantity': '1', 'amount': 11.0}
            return redirect("/success")
    return redirect("/login")

@app.route("/postreview/<string:item>",methods=['GET','POST'])
def postreview(item):
    if 'user' in session:
        if request.method=='POST':
            review = request.form.get('review')
            if len(review)>2:
                sentiment = review_analyser.analyse(review)
                db = database.mydatabase()
                db.insertreview(item,review,sentiment,session['user'])
                flash("Thanks for submitting your review!!!","success")
        db = database.mydatabase()
        reviews = db.fetchreviews(item)
        return render_template('postreview.html',user=session['user'],reviews=enumerate(reviews),item=item)
    else:
        return redirect("/login")
 
# sign up 
@app.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method =='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        status = request.form.get('status')
        if password != repassword:
            flash("Passwords are not matching!!","danger")
            return redirect('/signup')
        elif len(mobile) != 10:
            flash("Enter Valid mobile number!!","danger")
        else:
            db = database.mydatabase()
            ss = db.signup(name,email,mobile,password,status)
            if ss==1:
                flash("We have sent you a mail Verify your account!!","success") 
                return redirect('/login')  
            elif ss==-1:
                flash("You are already registered!! We have sent you verification mail!!","success")
                return redirect('/login')
            elif ss==-2:
                flash("Provided Email doesn't exist!!!","danger")
                return redirect('/signup') 
            else:
                flash("User already exist!!!","danger")
                return redirect('/signup') 
        return redirect('/signup')        
    return render_template('signup.html')
#login route
@app.route('/login',methods=['POST','GET'])
def login():
    if 'user' in session:
        return redirect('/')
    if request.method== 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        ss = database.mydatabase().login(email,password)
        if ss==-1:
            flash("Account doesn't exist or not verified!!","danger")
        elif ss==0:
            flash("Wrong Password!!!","danger")
        else:
            session['user']=email.split('@')[0]
            return redirect("/")
    return render_template('login.html')

#account verification route
@app.route("/verification/<string:username>")
def account_verification(username):
    status = database.mydatabase().user_verification(username)
    if status == -1:
        return "Error occured"
    flash("Account has been verified successfully!!","success")
    return redirect("/login")

@app.route("/contact",methods=['POST','GET'])
def contact():
    if 'user' in session:
        if request.method=="POST":
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")
            message = request.form.get("message")
            database.mydatabase().contact_feedback(session['user'],name,email,phone,message)
            flash("We will get back to you soon!!","success")
        return render_template("contact.html",user=session['user'])
    return redirect("/login")    

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect("/login")

@app.route("/profile")
def userdashboard():
    if 'user' in session:
        info = database.mydatabase().get_user_info(session['user'])[0]
        #print(info)
        return render_template("userdashboard.html",info=info)
    return redirect("/login")

# @app.route("/hi")
# def jj():
#     return render_template("imagewithtag.html",photo="upload.jpeg",tags=tags)


@app.route("/generate_tag",methods=['POST','GET'])
def generate_tag():
    if request.method=="POST":
        file = request.files['img']
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        try:
            tags = clarifi_tag_suggestions.get_tags_suggestions(f"/home/udaram/Desktop/DBMS/canteen/static/upload/{filename}")
        except:
            pass
        return render_template("imagewithtag.html",photo=filename,tags=tags,user=session['user'])
    return redirect("/")

@app.route("/forgot-password",methods=['POST','GET'])
def forgot_password():
    if request.method=="POST":
        email = request.form.get("email")
        info = database.mydatabase().get_user_info(email.split("@")[0])
        if len(info)!=0:
            mailsender.password_reset_email(email)
            flash("Password Reset link has been sent to registered email!!","success")
        else:
            flash("Account doesn't exist!!","danger")
        return redirect("login")
    return render_template("forgot_password.html")

@app.route("/sendresetlink/<string:username>")
def sendresetpasswordlink(username):
    info = database.mydatabase().get_user_info(session['user'])[0]
    mailsender.password_reset_email(info['email'])
    flash("Reset link has been sent to registered email!!","success")
    return redirect("/profile")

@app.route("/resetpassword/<string:username>",methods=['POST','GET'])
def resetpassword(username):
    if request.method=="POST":
        password = request.form.get("password")
        repassword = request.form.get("repassword")
        if password != repassword:
            flash("passwords are not matching","danger")
            return redirect(f"/resetpassword/{username}")
        database.mydatabase().password_reset(username,password)
        return "Successfully updated password"
    return render_template("passwordreset.html",username=username)

@app.route("/profile/orders")
def user_orders():
    if 'user' in session:
        orders = database.mydatabase().get_user_orders(session['user'])
        print(orders)
        return render_template("userorders.html",orders=orders,no_orders=len(orders))
    return redirect("/login")

@app.route("/vieworder/<string:orderid>")
def vieworder(orderid):
    if 'user' in session:
        order = database.mydatabase().get_order_details(orderid)
        #print(order)
        # return "hi"
        return render_template("vieworder.html",order=order,length=len(order))
    elif 'admin' in session:
        order = database.mydatabase().get_order_details(orderid)
        return render_template("/admin/vieworder.html",order=order,length=len(order))
    else:
        return "Error 404 occured"


################
# ADMIN ROUTES #
################
@app.route("/admin")
def dashboard():
    if 'admin' in session:
        menu = database.mydatabase().get_menu()
        orders = database.mydatabase().get_all_orders()
        return render_template("/admin/dashboard.html",menu=enumerate(menu),orders=orders,no_orders=len(orders))
    return redirect("/admin_login")
@app.route("/menu")
def menu():
    if 'admin' in session:
        menu = database.mydatabase().get_menu()
        return render_template("/admin/menu.html",menu=enumerate(menu))
    return redirect("/admin_login")

@app.route("/orders")
def orders():
    if 'admin' in session:
        orders = database.mydatabase().get_all_orders()
        return render_template("/admin/orders.html",orders=orders,no_orders=len(orders))
    return redirect("/admin_login")

@app.route("/edit/<string:item>",methods=["POST","GET"])
def edit_menu(item):
    if 'admin' in session:
        if request.method=="POST":
            item_updated = request.form.get("item")
            price_updated = request.form.get("price")
            database.mydatabase().update_item_info(item,item_updated,price_updated)
            return redirect("/menu")
        item = database.mydatabase().get_item_info(item)[0]
        return render_template("/admin/edit.html",item=item)
    return redirect("/admin_login")

@app.route("/delete/<string:item>",methods=["POST","GET"])
def delete_menu(item):
    if 'admin' in session:
        database.mydatabase().delete_item_status(item)
        return redirect("/menu")
    return redirect("/admin_login")

@app.route("/addmenu",methods=["POST","GET"])
def addmenu():
    if 'admin' in session:
        if request.method=="POST":
            item = request.form.get('item')
            price = request.form.get('price')
            # print(item,price)
            database.mydatabase().add_menu(item,price)
            return redirect("/menu")
        menu = database.mydatabase().get_menu(0)
        return render_template("/admin/addmenu.html", menu=enumerate(menu))
    return redirect("/admin_login")
    
@app.route("/admin_logout")
def admin_logout():
    session.pop('admin')
    return render_template("/admin/admin_login.html")

@app.route("/admin_login",methods=["POST","GET"])
def admin_login():
    if 'admin' in session:
        return redirect("/admin")
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username==params["admin_username"] and password==params["admin_password"]:
            session['admin']=username
            return redirect("/admin")
    return render_template("/admin/admin_login.html")

@app.route("/confirmorder/<string:username>/<string:orderid>")
def confirmorder(username,orderid):
    if 'admin' in session:
        database.mydatabase().confirm_order(orderid,username)
        return redirect("/orders")
    return redirect("/admin_login")

#to automatically detecting changes and debugging
if __name__ == "__main__":
    app.debug=True
    app.run(host=params["ip"],port=8000)