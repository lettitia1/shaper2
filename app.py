from flask import Flask, render_template, url_for, redirect, request
import psycopg2
import os
from sqlalchemy import create_engine
from flask_cors import CORS
# from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lettiemokubung'  
#Making sure we don't get errors
CORS(app)


try: 
    #Connecting to database
    con = psycopg2.connect(
        database="lettie",
        user="lettie",
        password="password",
        port="5430"
    )
    cur = con.cursor()
   #Creating admin table
#     create_table_query = '''
#     Create Table adminstrator(
#     id  Serial Primary key, 
#     admin_username VARCHAR(20),
#     admin_password VARCHAR(20)
#     );
# '''

#     create_table_query = '''
#      Create Table employee(
#      emp_num  Serial Primary key, 
#      emp_name VARCHAR(20),
#      emp_surname VARCHAR(20),
#      datehired date,
#      emp_position VARCHAR(20) 

#      );
#  '''
#     cur.execute(create_table_query)
#     con.commit()
    
#     cur.close()
#     con.close()

   

   #Creating Registration form
    class Registerform(FlaskForm):
      admin_username = StringField(validators=[InputRequired(), Length(min=5, max=20)],
      render_kw={"placeholder":"Username"})
      admin_password = PasswordField(validators=[InputRequired(), Length(min=5, max=20)],render_kw={"placeholder":"Password"})

      submit = SubmitField("Register")
  
         
         

    #Creating Login form
    class Loginform(FlaskForm):
      admin_username = StringField(validators=[InputRequired(), Length(min=5, max=20)],
      render_kw={"placeholder":"Username"})
      admin_password = PasswordField(validators=[InputRequired(), Length(min=5, max=20)],render_kw={"placeholder":"Password"})

      submit = SubmitField("Login")  
   
      
    #login
    @app.route('/', methods=['GET','POST'])
    def login():
        form=Loginform()
        if request.method == 'POST':
                admin_username = request.form['admin_username']
                admin_password = request.form['admin_password']

                cur.execute("SELECT * FROM adminstrator WHERE admin_username=%s AND admin_password=%s", (admin_username,admin_password))
                existing_user = cur.fetchone()

                if existing_user is None:
                   return redirect(url_for('registration'))
                else:
                   return redirect(url_for('dashboard'))
        return render_template('login.html' , form=form)
      
    # Signing in 
    
    @app.route('/registration', methods=['GET','POST'])
      
    def registration():
         form=Registerform()
         if form.validate_on_submit():
               if request.method == 'POST':
                admin_username = request.form['admin_username']
                admin_password = request.form['admin_password']

                cur.execute("SELECT * FROM adminstrator WHERE admin_username=%s", (admin_username,))
                existing_user = cur.fetchone()

                if existing_user is None:
                # Insert the new admin
                 cur.execute("INSERT INTO adminstrator (admin_username, admin_password) VALUES (%s, %s)", (admin_username, admin_password))
                 con.commit()

                return redirect(url_for('success'))
               else:
                return "Username already exists. Please choose a different one."

    

        
         return render_template('registration.html' , form=form)
    

    @app.route('/success')
    def success():
       return redirect(url_for('login'))
#dashboard page
    @app.route('/dashboard', methods =['GET'])
    def dashboard():

        cur.execute("Select * From employee ")
        row =cur.fetchall()
        print(row[0][0])
    
        return render_template('dashboard.html', row=row)
    
    @app.route('/search', methods = ['Post'])
    def fetch_id():
       request.method==['Get']
       emp_num = request.form['emp_num']
       cur.execute("Select * From employee WHERE emp_num=%s", (emp_num,))
       rows = cur.fetchall()
       print(rows[0][0])
       return render_template('dashboard.html', rows=rows)

    @app.route('/Add_emp', methods=['GET','POST']) 
    def Add_emp():
         if request.method == 'POST':
                 emp_name = request.form['T2']
                 emp_surname = request.form['T3']
                 date_hired = request.form['SB1']
                 emp_pos = request.form['LB1']

                # Insert the new employee
                 cur.execute("INSERT INTO employee (emp_name, emp_surname, datehired, emp_position) VALUES (%s,%s, %s, %s)", (emp_name, emp_surname, date_hired, emp_pos))
                 con.commit()
                 if ('form submission success'):
                     return redirect(url_for('dashboard'))
         else:
                 if ('form submission failed'):
                     return render_template('add.html')
                 

    @app.route('/delete_employee', methods=['POST','DELETE'])
    def delete_emp():
        if request.method == 'POST':
            emp_num = int(request.form['emp_num'])
            cur.execute("Delete From employee Where emp_num = %s", (emp_num,))
            con.commit()
            return redirect(url_for('dashboard'))
        else:
            return render_template('delete_employee.html')
        

    @app.route('/update_employee2', methods=['POST'])
    def employee_update2():

        if request.method == 'POST':
                 emp_name = request.form['T2']
                 emp_surname = request.form['T3']
                 emp_pos = request.form['LB1']
                 cur.execute( 'UPDATE employee SET emp_name = %s, emp_surname = %s, emp_position = %s WHERE emp_num= 1',(emp_name,emp_surname,emp_pos))
                 con.commit()
                 return render_template('dashboard.html')
                #  return redirect(url_for('dashboard'))
        # else:
        
        #      return redirect(url_for('update_employee'))
         
    @app.route('/update_employee', methods=['POST'])
    def employee_update():

            if request.method == 'POST':
                return render_template('update.html')
                
  
except Exception as e:
    print(f'Error: {e}')
if __name__ == '__main__':
    app.run(debug=True, port=5638)