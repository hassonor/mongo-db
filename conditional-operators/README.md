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
#### Less Than ($lt) and less than or equal to ($lte)
Find how many movies have __less__ than 2 comments, enter the following query:<br>
```shell
db.movies.find(
  {"num_mflix_comments":
      {$lt: 2}
  }
).count()
```
Similarly to find the number of movies that have a maximum of two comments, enter the following query:
<br>
```shell
db.movies.find(
  {"num_mflix_comments":
      {$lte: 2}
  }
).count()
```
To count the movies that were _released_ in the previous century, simply use $lt:
```shell
db.movies.find(
    {"released":
     {$lt: new Date('2000-01-01')}
    }
).count()
```

#### In ($in) and not In ($nin)
A query that returns movies rated as either of 'G','PG' or 'PG-13': <br>
```shell
db.movies.find(
  {"rated":
    {$in : ["G","PG","PG-13"]}
  }
) 
```
The __$nin__ operator stands for __Not In__ and matches all the documents where the value of the field does not match 
with any of the array elements:<br>
```shell
db.movies.find(
  {"rated":
    {$nin : ["G","PG","PG-13"]}
  }
)
```

More queries examples: <br>
1. count Movies in which _Or Hasson_ appears by using the __cast__ field: <br>
`db.movies.countDocuments({"cast":"Or Hasson"})`
2. The genres of the movies in the collection are represented by the __genres__ field. <br>
Use the __distinct()__ function to fond the unique __genres__:<br>
`db.movies.distinct("genres",{"cast":Or Hasson"})`
3. Using movie titles, we can now find the year of release for each of the actor's movies. <br>
As we are only interested in the titles and release years of his movies, <br>
add a projection clause to the query:<br>
```shell
db.movies.find(
  {"cast": "Or Hasson"},
  {"title": 1, "year":1, "_id:": 0}
) 
```
4. Query that counts the movies that match the preceding query:<br>
`db.movies.countDocuments({"directors": "Or Hasson"})`
