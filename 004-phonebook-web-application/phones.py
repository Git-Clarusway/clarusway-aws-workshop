# Import Flask modules
from flask import Flask, jsonify, abort, request, make_response,render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
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
def find_person(name):
    query = f"""
    SELECT * FROM phones WHERE name like '%{name.title()}%';
    """
    row = db.session.execute(query)
    return row 
def insert_person(name,number):
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
def validate_name(name):
    if name=='' :
        return True,'Invalid input: Name can not be empty'
    elif name.isnumeric():
        return True,'Invalid input: Name of person should be text'
    else:
        return False,name.strip()
def validate_number(number):
    if number=='' : 
        return True,'Invalid input: Phone number can not be empty'
    elif  not number.isnumeric():
        return True,'Invalid input: Phone number should be in numeric format' 
    else:
        return False,number.strip()        
@app.route('/')
def index():
    return render_template('navigate.html',name='SK')
@app.route('/index',methods=["POST","GET"])
def index_page():
    if request.method=="POST":
        name=request.form['username']
        cond,msg=validate_name(name)
        if cond :    
            return render_template('index.html',developer_name='SK',show_result=False,warning=msg) 
        else:
            person=find_person(msg)
            return render_template('index.html',developer_name='SK',show_result=True,keyword=msg,warning=msg,persons=person)       
    return render_template('index.html',developer_name="SK")
@app.route('/add',methods=["POST","GET"])
def add_page():
    if request.method=="POST":
        name=request.form["username"]
        number=request.form["phonenumber"]
        cond,name_msg=validate_name(name)
        if cond:
            return render_template("add-update.html",developer_name="SK",action_name="ADD",not_valid=cond, message=name_msg,show_result=not cond)
        cond,number_msg=validate_number(number)
        if cond:
            return render_template("add-update.html",developer_name="SK",action_name="ADD",not_valid=cond, msg=number_msg,show_result=not cond)
        insert=insert_person(name_msg,number_msg)    
        return render_template("add-update.html",developer_name="SK",action_name="ADD",not_valid=False,show_result=True,result=f"{name_msg.title() } with phone {number} is successfully added")
    return render_template('add-update.html',developer_name='SK',action_name="add",show_result=False) 
@app.route('/update',methods=["POST","GET"])
def update_page():
    if request.method=="POST":
        name=request.form["username"]
        number=request.form["phonenumber"]
        cond,name_msg=validate_name(name)
        if cond:
            return render_template("add-update.html",developer_name="SK",action_name="ADD",not_valid=cond, message=name_msg,show_result=not cond)
        cond,number_msg=validate_number(number)
        if cond:
            return render_template("add-update.html",developer_name="SK",action_name="ADD",not_valid=cond, msg=number_msg,show_result=not cond)
        update=update_person(name_msg,number)   
        return render_template("add-update.html",developer_name="SK",action_name="ADD",not_valid=False,show_result=True,result=f"{name_msg.title() } with phone {number} is successfully Updated")
    return render_template('add-update.html',developer_name='SK',action_name="add",show_result=False) 
@app.route('/delete',methods=["POST","GET"])
def delete_page():   
    if request.method=="POST":
        name=request.form['username']
        cond,msg=validate_name(name)
        if cond :    
            return render_template('delete.html',developer_name='SK',show_result=False,not_valid=cond,message=msg) 
        else:
            result=remove_person(name)
            return render_template('delete.html',developer_name='SK',show_result=True,result=f"{msg.title()} is successfully deleted")       
    return render_template('delete.html',developer_name="SK")

if __name__ == '__main__':
    init_phones_db()
    app.run(debug=True)
    # app.run('0.0.0.0',port=80)
    