from flask import *
app=Flask(__name__)
@app.route('/')
def home():
    return redirect('home')
@app.route('/home')
def index():
    return render_template('index.html',developer_name='S_Kaplan',not_valid=False)
@app.route('/',methods=['POST','GET'])    
def result():
    if request.method=='POST':
        number=request.form['number']
        if number.isdigit():
            a=int(number)
            if   not a  :
                return render_template('index.html',developer_name='S_Kaplan',not_valid=True)
        else:
            return render_template('index.html',developer_name='S_Kaplan',not_valid=True)
        x=''
        if a>999:
            while a>999:    
                    if a>=3600000:
                        b,a=divmod(a,3600000)
                        x+=f'{b} hour/s'
                    elif a>=60000:
                        b,a=divmod(a,60000)
                        x+=f' {b} minute/s'
                    else:
                        b,a=divmod(a,1000)
                        x+=f' {b} second/s'
        else:
                x+=f'just {a} millisecond/s'    
        return render_template('result.html',milliseconds=request.form['number'],result=x,developer_name='S_Kaplan',not_valid=False)

if __name__=='__main__':
    # app.run(debug=True)
    app.run('0.0.0.0',port=80)
