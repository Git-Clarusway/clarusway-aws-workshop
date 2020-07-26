# Import Flask modules
from flask import Flask, jsonify, abort, request, make_response,render_template
from flask_sqlalchemy import SQLAlchemy

# Cerate an object named app
app=Flask(__name__)
# Configure sglite database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./phone-list.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

def init_phones_db():
    drop_table = 'DROP TABLE IF EXISTS phones;'
    phone_table = """
    CREATE TABLE phones(
    person_id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    number VARCHAR ) ;
    """
    data = """
    INSERT INTO phones (name, number)
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

def find_person(id):
    query = f"""
    SELECT * FROM phones WHERE name like '%{id.title()}%';
    """
    row = db.session.execute(query)
    if row is not None:
        return row

def insert_person(name, number):
    insert = f"""
    INSERT INTO phones (name, number)
    VALUES ('{name}', '{number}');
    """
    result = db.session.execute(insert)
    db.session.commit()

    query = f"""
    SELECT * FROM phones WHERE person_id={result.lastrowid};
    """
    row = db.session.execute(query).first()

    return row[1],row[2]

def remove_person(name):
    delete = f"""
    DELETE FROM phones
    WHERE name like '{name.title()}';
    """
    result = db.session.execute(delete)
    db.session.commit()

    query = f"""
    SELECT * FROM phones WHERE name='{name.title()}';
    """
    row = db.session.execute(query).first()
    return True if row is None else False

def update_person(person,number):
    update = f"""
    UPDATE phones
    SET  number = '{number}'
    WHERE name = '{person.title()}';
    """
    result = db.session.execute(update)
    db.session.commit()

    query = f"""
    SELECT * FROM phones WHERE name='{person.title()}';
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
        if username:
            if username.isdecimal():
                return render_template('index.html',developer_name='SK',show_result=False,warning="Invalid input: Name of person should be text")    
            else:
                person=find_person(username)
                return render_template('index.html',developer_name='SK',keyword=username,persons=person,show_result=True)
        else:
            return  render_template('index.html',developer_name='SK',show_result=False,warning="Invalid input: Name can not be empty")                     
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
        except ValueError:
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
    app.run(debug=True)
    # app.run('0.0.0.0',port=80)
    