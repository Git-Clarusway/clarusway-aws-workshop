# Import Flask modules
from flask import Flask, jsonify, abort, request, make_response,render_template
from flask_sqlalchemy import SQLAlchemy

# Cerate an object named app
app=Flask(__name__)
# Configure sglite database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./phone-list.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

# # Name Format to convert 
#'Invalid input: Name can not be empty'
#'Invalid input: Name of person should be text'

# # Number Format to convert     
# Following is the format of data to be kept in db.
# id: unique identifier for the phone record, type is numeric.
# person: full name of person for the phone record, type is string.
# number: phone number of the person. type is numeric.

# Write a function named `init_todo_db` which initilazes the todo db
# Create phone table within sqlite db and populate with sample data
# Execute the code below only once.
def init_phones_db():
    drop_table = 'DROP TABLE IF EXISTS phones;'
    phone_table = """
    CREATE TABLE phones(
    task_id INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR ) ;
    """
    data = """
    INSERT INTO phones (title, description)
    VALUES
        ("Ahmet", 1234567890 ),
        ("Mehmet", 1234567890 ),
        ("Callahan", 1234567890 ),
        ("Vincenzo Altobelli",8993249797);
    """
    db.session.execute(drop_table)
    db.session.execute(phone_table)
    db.session.execute(data)
    db.session.commit()
# Write a function named `find_task` which finds task using task_id from the todos table in the db,
# and return result as list of dictionary 
# `[{'task_id': 1, 'title':'XXXX', 'description': 'XXXXXX', 'is_done': 'Yes' or 'No'} ]`.
def find_person(id):
    query = f"""
    SELECT * FROM phones WHERE title like '%{id.title()}%';
    """
    row = db.session.execute(query)
    if row is not None:
        return row
# Write a function named `insert_task` which inserts task into the todos table in the db,
# and return the newly added task as dictionary 
# `[{'task_id': 1, 'title':'XXXX', 'description': 'XXXXXX', 'is_done': 'Yes' or 'No'} ]`.
def insert_person(title, description):
    insert = f"""
    INSERT INTO phones (title, description)
    VALUES ('{title}', '{description}');
    """
    result = db.session.execute(insert)
    db.session.commit()

    query = f"""
    SELECT * FROM phones WHERE task_id={result.lastrowid};
    """
    row = db.session.execute(query).first()

    return row[1],row[2]
# Write a function named `remove_task` which removes task from the todos table in the db,
# and returns True if successfully deleted or False.
def remove_person(name):
    delete = f"""
    DELETE FROM phones
    WHERE title like '{name.title()}';
    """
    result = db.session.execute(delete)
    db.session.commit()

    query = f"""
    SELECT * FROM phones WHERE title='{name.title()}';
    """
    row = db.session.execute(query).first()
    return True if row is None else False

# Write a function named `find_phone` which finds phone using person_id from the phone table in the db,
# and return result as list of dictionary 
# `[{'person_id': 1, 'person_name':'XXXX', 'person_number': 'XXXXXX' ]`.
def update_person(person,number):
    update = f"""
    UPDATE phones
    SET  description = '{number}'
    WHERE title = '{person.title()}';
    """
    result = db.session.execute(update)
    db.session.commit()

    query = f"""
    SELECT * FROM phones WHERE title='{person.title()}';
    """
    row = db.session.execute(query).first()
    return row[1],row[2]
#html root
@app.route('/')
def index():
    return render_template('navigate.html',name='SK')
#html home page creating
@app.route('/index',methods=["POST","GET"])
def index_page():
    if request.method=='POST':
        username=request.form['username']
        try:
            if username:
                convert=username+1
                return render_template('index.html',developer_name='SK',show_result=False,warning="Invalid input: Name of person should be text")    
            else:
                return  render_template('index.html',developer_name='SK',show_result=False,warning="Invalid input: Name can not be empty")   
        except TypeError:
            person=find_person(username)
            return render_template('index.html',developer_name='SK',keyword=username,persons=person,show_result=True)           
    else:
        return render_template('index.html',developer_name="SK",show_result=False)
#html adding page creating
@app.route('/add',methods=["POST","GET"])
def add_page():
    if request.method=="POST":
        person=request.form["username"]
        number=request.form["phonenumber"]
        try:
            if not person.isdecimal():
                number=int(number)
                insert=insert_person(person,number)
                return render_template("add-update.html",developer_name="SK",action_name="ADD",not_valid=False,show_result=True,result=insert)
            else:
                return render_template("add-update.html",developer_name="SK",action_name="ADD",not_valid=True,warning="Invalid input: Name of person should be text",show_result=False)
        except ValueError as Val:
            return render_template("add-update.html",developer_name="SK",action_name="ADD",not_valid=True,warning="Invalid input: Phone number should be in numeric format",show_result=False)
    else:
        return render_template("add-update.html",developer_name="SK",action_name="ADD",not_valid=False,show_result=False)
#html update page creating
@app.route('/update',methods=["POST","GET"])
def update_page():
    if request.method=="POST":
        person=request.form["username"]
        number=request.form["phonenumber"]
        try:
            if not person.isdecimal():
                number=int(number)
                update=update_person(person,number)
                return render_template("add-update.html",developer_name="SK",action_name="Update",not_valid=False,show_result=True,result=update)
            else:
                return render_template("add-update.html",developer_name="SK",action_name="Update",not_valid=True,warning="Invalid input: Name of person should be text",show_result=False)
        except ValueError as Val:
            return render_template("add-update.html",developer_name="SK",action_name="Update",not_valid=True,warning="Invalid input: Phone number should be in numeric format",show_result=False)
    else:
        return render_template("add-update.html",developer_name="SK",action_name="Update",not_valid=False,show_result=False)
#html delete page creating
@app.route('/delete',methods=["POST","GET"])
def delete_page():   
    if request.method=='POST':
        username=request.form['username']
        try:
            if username:
                convert=int(username)
                return render_template('delete.html',developer_name='SK',show_result=False,not_valid=True,warning="Invalid input: Name of person should be text")    
            else:
                return  render_template('delete.html',developer_name='SK',show_result=False,not_valid=True,warning="Invalid input: Name can not be empty")   
        except ValueError:
            result=remove_person(username)
            return render_template("delete.html",developer_name="SK",not_valid=False,show_result=result,result="Succeedfully Deleted")
    else:
        return render_template("delete.html",developer_name="SK",not_valid=False,show_result=False)

#end of the code exacuting
if __name__ == '__main__':
    init_phones_db()
    # app.run(debug=True)
    app.run('0.0.0.0',port=80)
    