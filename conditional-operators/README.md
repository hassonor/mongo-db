### Conditional Operators 
___
#### Equals ($eq)
The following queries find and return movies that have exactly 7 comments. Both queries have
the same effect:
```shell
db.movies.find({"num_mflix_comments": 7})
db.movies.find({"num_mflix_comments": {$eq : 7}})
```

#### Not Equals To ($ne)
The following query can be used to return movies whose count for comments is not equal to 7:
```shell
db.movies.find(
   {
     "num_mflix_comments": {$ne : 5}
   }
)
```

#### Greater Than ($gt) and Greater than or Equal to ($gte)
Find the number of movies released after __2017__:
```shell
db.movies.find(
  { year: {$gt : 2017}}
).count()
```
Find the number for movies that had released in or after __2017__:
```shell
db.movies.find(
  { year: {$gte : 2017}}
).count()
```
For Count movies that were released in the 21st century,
We want to include the movies that have been released since January 1, 2000:
```shell
db.movies.find(
  {"released":
     {$gte: new Date('2000-01-01')}
  }
).count()
```