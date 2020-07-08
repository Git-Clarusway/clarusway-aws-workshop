from flask import *
import datetime
app = Flask('__name__')
@app.route('/')

def home():
    return render_template('index.html',developer_name='S_Kaplan',not_valid=False,today=str(datetime.date.today()))    
@app.route('/',methods=['POST','GET'])
def convt():
    if request.method=='POST':
        number=request.form['number']
        if   not number.isdigit():
            return render_template('index.html',developer_name='S_Kaplan',not_valid=True) 
        if  int(number)< 1 or int(number)> 3999:
            return render_template('index.html',developer_name='S_Kaplan',not_valid=True)    
        box = {1000: "M", 900: 'CM', 500: "D", 400: 'CD', 100: "C", 90: 'XC', 50: "L", 40: 'XL', 10: "X", 9: 'IX', 5: "V", 4: 'IV', 1: "I"}
        # number = int(input ("enter a number :")) # 1994 "MCMXCIV"
        number=int(number)
        result = ""
        for k,v in box.items() : # k =1000
                value = number // k # 1
                result += v * value # M *1
                number%=k # 994
        return render_template('result.html',number_decimal=request.form['number'],number_roman=result,developer_name='S_Kaplan',not_valid=False)
if __name__ == '__main__':
    app.run(debug=True)
    # app.run('0.0.0.0',port=80)