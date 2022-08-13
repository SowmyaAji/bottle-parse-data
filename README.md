## Backend Skills Tests

Implement an API.

You can use any framework or packages you like. 


### Base Requirements
- The first end point should accept a CSV file and parse the data into SOME storage mechanism (in memory would be fine). The csv file is in the root of this repo as `data.csv`.
- The second endpoint should allow the fetching of any row of that data by guid, or email. This endpoint should always return as an array. 
- The third endpoint should return the average, median, min, max, and sum of income for all rows with income values. You can return it as follows:

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


### Bonus
- Allow the second api (fetch) to grab multiple guids or emails at once. 


