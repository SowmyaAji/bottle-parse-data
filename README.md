## How to use this repo:

- clone it and cd into it
- run ```pipenv shell``` (requires pipenv installed)
- run ```pipenv install```
- run ```python app.py``` (to start the bottle server)

end points are as listed below: 


- The first end point /data accepts a CSV file and parses the data. A test csv file is in the root of this repo as `data.csv`. Please use Thunder Client or Postman to upload the file as a POST request. The file variable is "upload_file".
- The second endpoint /data allows the fetching of any row of that data by guid, or email. This endpoint always returns as an array. This is a get request from the url. Format is data/abcdefg,xxxyy,random@example.com (will also take a single request without commas). Will not show or return any erroneous inputs. 
- The third endpoint /incomes returns the average, median, min, max, and sum of income for all rows with income values. This is also a get request and requires no inputs.
Sample return value: 
```
{
    average: number
    median: number
    min: number
    max: number
    sum: number
}
```

The expected values for each are listed below. 

```
Average: 152,218.21
Median: 155,788.00
Max: 249,925.00
Min: 50,005.00
Sum: 145,977,259.00
```





