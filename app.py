from bottle import run, route, request, HTTPError
import sqlite3
import statistics


@route("/")
def index():
    """
    The function `index()` returns the string "Welcome to bottle"
    :return: "Welcome to bottle"
    """
    
    return "Welcome to bottle"


@route("/data", method="POST")
def get_csv():
    """
    It takes a csv file, saves it to a file path, creates a database if it doesn't exist, creates a
    table if it doesn't exist, inserts the data from the csv file into the table, and returns the data
    from the table
    :return: A dictionary with three keys: msg, status, and details.
    """
    try:
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
    except HTTPError as e:
        return { "msg" : "Error getting file", "status": e}
    except sqlite3.DatabaseError as e:
        return { "msg": "Error connecting to database", "status": e}


@route("/data/<input>", method="GET")
# sample input data/7df64282-3ea0-437f-9142-58d3baf5a8bf,mstewart6d@europa.eu,ajanjic6e@4shared.com
# can take single string also
# all errors are ignored as there is no requirement to return errors
def get_rows(input):
    """
    It takes a string of comma separated values, splits them into a list, then loops through the list
    and returns a list of dictionaries containing the results of the query.
    
    :param input: The input string that we want to search for
    :return: A dictionary with a key of "results" and a value of all_results.
    """
    try:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        inputs = input.split(",")
        all_results = []
        for i in inputs:
            c.execute("SELECT * FROM person WHERE id=? OR email=?",(i, i))
            results = c.fetchall()
            all_results.extend(results)
        
        return { "results": all_results }
    except HTTPError as e:
        return { "msg" : "Error getting correct rows", "status": e}
    except sqlite3.DatabaseError as e:
        return { "msg": "Error connecting to database", "status": e}


@route("/incomes", method="GET")
def get_income_details():
    """
    It connects to the database, gets the income column, calculates the average, median, min, max, and
    sum of the incomes, formats the numbers, and returns a json object with the results
    :return: A JSON object containing the average, median, min, max, and sum of the incomes of all the
    people in the database.
    """
    try:
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
    except HTTPError as e:
        return { "msg" : "Error getting response", "status": e}
    except sqlite3.DatabaseError as e:
        return { "msg": "Error connecting to database", "status": e}
    

if __name__=="__main__":
    run(reloader=True, debug=True)