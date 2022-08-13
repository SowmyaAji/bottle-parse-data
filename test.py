import statistics
incomes = [ 2300, 4567, 8999, 21345]



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
print(formatted_deets)

json_obj = {
    "average": f_average,
    "median": f_median,
    "min": f_min,
    "max" : f_max,
    "sum" : f_sum
}
print(json_obj)