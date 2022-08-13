from bottle import run, route, request
import sqlite3
import statistics


@route("/")
def index():
    return "Welcome to bottle"


@route("/data", method="POST")
def get_csv():
    upload = request.files.get("upload_file")
    file_path = "saved_data.csv"
    upload.save(file_path)
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS person (id char PRIMARY KEY, first_name char(25) NOT NULL, last_name char(30) NOT NULL, email char(50) NOT NULL, gender char(15) NOT NULL, income INTEGER)")
  
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines[1:]:
            striped = line.strip()
            line_list = striped.split(",")
            salary = line_list[-1]
            
            c.execute("INSERT INTO person (id, first_name, last_name, email, gender, income) VALUES (?,?,?,?,?,?)",(line_list[0], line_list[1], line_list[2], line_list[3], line_list[4], salary))
    conn.commit()
    c.execute("SELECT * FROM person")
    results = c.fetchall()
    return { "msg" : "Got the file", "status": "1", "details": results}


@route("/data/<input>", method="GET")
# sample input data/7df64282-3ea0-437f-9142-58d3baf5a8bf,mstewart6d@europa.eu,ajanjic6e@4shared.com
# can take single string also
# all errors are ignored as there is no requirement to return errors
def get_rows(input):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    inputs = input.split(",")
    all_results = []
    for i in inputs:
        c.execute("SELECT * FROM person WHERE id=? OR email=?",(i, i))
        results = c.fetchall()
        all_results.extend(results)
       
    return { "results": all_results }

@route("/incomes", method="GET")
def get_income_details():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT income FROM person")
    results = c.fetchall()
    incomes = []
    for row in results:
        if row[0]:
            incomes.append(row[0])
    average = sum(incomes)/ len(incomes)
    median = statistics.median(incomes)
    get_min = min(incomes)
    get_max = max(incomes)
    get_sum = sum(incomes)
    
    deets = [ average, median, get_min, get_max, get_sum ]
    formatted_deets = []
    for i in deets:
        formatted_i = "{:,.2f}".format(i)
        formatted_deets.append(formatted_i)
    f_average, f_median, f_min, f_max, f_sum = formatted_deets
    
    json_obj = {
        "average": f_average,
        "median": f_median,
        "min": f_min,
        "max" : f_max,
        "sum" : f_sum
    }
    
    return json_obj
    

if __name__=="__main__":
    run(reloader=True, debug=True)