import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

with open('config.json','r') as cc:
    params = json.load(cc)["params"]

def verification_email(email):
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    # start TLS for security 
    s.starttls() 
    # Authentication 
    s.login(params["SENDER_EMAIL"],params["SENDER_PASS"]) 
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Email verification for Shiva Canteen"
        message["From"] = params["SENDER_EMAIL"]
        message["To"] = email
        link = "http://"+params["ip"]+":8000/verification/"+email.split('@')[0]
        html = '''
            <html>
            <head>
                <style>
                .button {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                -webkit-transition-duration: 0.4s; /* Safari */
                transition-duration: 0.4s;
                }

                .button1 {
                box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
                }
            </style>
            </head>
            <body>
                <p>Congratulations!!!<br>
                Your account has been created succesfully on Shiva Canteen</p>
                <p> <b>Click on below to verify your account</b> </p>
                <a href="'''+link+'''"><button class="button button1">Verify Account</button></a> 
                <br>
                <p>---<br>Thanks and Regards <br>Shiva Canteen</p> 
            </body>
            </html>
            '''
        part = MIMEText(html, "html")
        message.attach(part)
            # subject = "Email verification for Shiva Canteen"
            # body = " \nYour account has been created succesfully on Shiva Canteen\nClick on below link to verify your account\n{link}\n Thanks and Regards \nShiva Canteen"
            # message = f'Subject: {subject}\n\n{body}'
        s.sendmail(params["SENDER_EMAIL"], email, message.as_string()) 
            # terminating the session 
        s.quit()
        return 1
    except:
        #provided mail is not valid
        # terminating the session 
        s.quit()
        return -1   


def password_reset_email(email):
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    # start TLS for security 
    s.starttls()
    # Authentication 
    s.login(params["SENDER_EMAIL"],params["SENDER_PASS"]) 
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Reset Password Shiva Canteen"
        message["From"] = params["SENDER_EMAIL"]
        message["To"] = email
        link = "http://"+params["ip"]+":8000/resetpassword/"+email.split('@')[0]
        html = '''
            <html>
            <head>
                <style>
                .button {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                -webkit-transition-duration: 0.4s; /* Safari */
                transition-duration: 0.4s;
                }

                .button1 {
                box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
                }
            </style>
            </head>
            <body>
                <p>Dear Customer!!!<br>
                Click on below link to reset your password on Shiva Canteen</p>
                <p> <b>Click Here</b> </p>
                <a href="'''+link+'''"><button class="button button1">Reset Account Password</button></a> 
                <br>
                <p>---<br>Thanks and Regards <br>Shiva Canteen</p> 
            </body>
            </html>
            '''
        part = MIMEText(html, "html")
        message.attach(part)
            # subject = "Email verification for Shiva Canteen"
            # body = " \nYour account has been created succesfully on Shiva Canteen\nClick on below link to verify your account\n{link}\n Thanks and Regards \nShiva Canteen"
            # message = f'Subject: {subject}\n\n{body}'
        s.sendmail(params["SENDER_EMAIL"], email, message.as_string()) 
            # terminating the session 
        s.quit()
        return 1
    except:
        #provided mail is not valid
        # terminating the session 
        s.quit()
        return -1  


def orderconfirmation(email,order):
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    # start TLS for security 
    s.starttls() 
    # Authentication 
    s.login(params["SENDER_EMAIL"],params["SENDER_PASS"]) 
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Order Confirmation"
        message["From"] = params["SENDER_EMAIL"]
        message["To"] = email
        html = '''
            <html>
            <head>
            <style>
                #tablelayout {
                  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif
                  border-collapse: collapse;
                  width: 100%;
                }

                #tablelayout td, #tablelayout th {
                  border: 1px solid #ddd;
                  padding: 8px;
                }

                #tablelayout th {
                  padding-top: 12px;
                  padding-bottom: 12px;
                  text-align: left;
                  background-color: #4CAF50;
                  color: white;
                }
            </style>
            </head>
            <body>
                <p>Dear Customer!!!<br>
                Your order has been placed successfully at Shiva Canteen</p>
                
                <p style="font-weight: bold;">Your order details are as below:</p>
                '''

        html = html + f'''
            <p><span style="color:blue;"> Order ID :</span> {order[0]['orderID']}</p>
            <p><span style="color:blue;"> Username :</span> {order[0]['username']}</p>
            <p><span style="color:blue;"> Date :</span> {order[0]['date']}</p>
            <p><span style="color:blue;"> Status :</span> {order[0]['status']}</p>
            <hr>
            <table border="1">
                <tr>
                    <th>S.No.</th>
                    <th>Item</th>
                    <th>Qty</th>
                    <th>Price</th>
                    <th>Amount</th>
                </tr>'''
        for i,item in enumerate(order):
            html = html +f''' <tr>
            <td>{i+1}</td>
            <td>{item['item']}</td>
            <td>{item['quantity']}</td>
            <td>{item['price']}</td>
            <td>{item['price']*item['quantity']}</td>
            </tr>'''
        html=html +f''' <tr>
            <td></td>
            <td></td>
            <td></td>
            <td><b>Total(Rs.):</b></td>
            <td><b>{order[0]['amount']}</b></td>
            </tr>
            </table>
            
            <p>Please Pick up your order from canteen counter after 15 minutes</p>
            <p>---<br>Thanks and Regards <br>Shiva Canteen</p> 
            </body>
            </html>
            '''
        part = MIMEText(html, "html")
        message.attach(part)
            # subject = "Email verification for Shiva Canteen"
            # body = " \nYour account has been created succesfully on Shiva Canteen\nClick on below link to verify your account\n{link}\n Thanks and Regards \nShiva Canteen"
            # message = f'Subject: {subject}\n\n{body}'
        s.sendmail(params["SENDER_EMAIL"], email, message.as_string()) 
            # terminating the session 
        s.quit()
        return 1
    except:
        #provided mail is not valid
        # terminating the session 
        s.quit()
        return -1  

#verification_email("udaram@iitjammu.ac.in") 
    