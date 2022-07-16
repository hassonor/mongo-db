#### Mongo DB Data Types
___
* Strings
* Numbers
    * __double__: 64-bit floating point
    * __int__: 32-bit signed integer
    * __long__: 64-bit unsigned integer
    * __decimal__: 128-bit floating point - which IEE 754-compliant
* Booleans
* Objects
* Arrays
* Null
* ObjectId
* Dates
* Timestamps
* Binary Data / BinData

#### MongoDB Query Structure
___
MongoDB's queries are based on JSON documents in which you write your criteria in the form of valid documents. 
With the data stored in the form of JSON-like documents, the queries seem more natural and readable. 
The following query is an example of simple MongoDB query that finds all the documents where the __name__
field contains the value __Hasson__ on collections name __users__:
`db.users.find({"name": "Hasson"})`

### Basic MongoDB Queries
___
#### Findings Documents:
The most basic query in MongoDB is performed with the __find()__ function on the collection.
When this function is executed without any argument, it returns all the documents in a collection. <br>
e.g.: `db.comments.find()` <br><br>
If we only want to find comment that have been added by a specific user, __Or Hasson__,
The query should be written as follows: <br>`db.comments.find({"name": "Or Hasson"})` <br>
If we want to get well-formatted result: <br>
`db.comments.find({"name": "Or Hasson"}).pretty()`
#### Using FindOne():
__findOne()__,
Returns only one matching record. This function is very useful when you are looking to isolate a specific record.
The syntax of this function is similar to the syntax of the __find()__ function,
as follows: <br>
`db.comments.findOne()` -> Will returning only the first <br>

```shell
// All of the quries have the same behavior - will bring the first 20 documents:
db.comments.find()
db.comments.find({})
db.comments.find({"a_non_existent_field": null})
```

```shell
// All of the quries have same behavior - will bring the first document
db.comments.findOne()
db.comments.findOne({})
db.comments.findOne({"a_non_existent_field": null})
```

#### Choosing the fields for the output
```shell
db.comments.find(
  {"name": "Or Hasson"},
  {"name": 1, "date":1, "_id":0}

)
```
This technique is called __projection__. Projection is expressed as a second argument to the __find()__ or __findOne()__ functions.
In the projection expression, we can explicitly exclude a field  by setting it to 0 or include one by setting it to 1.
Thus, in the last example above it will find all comments posted by the user `Or Hasson` and returns only 
the __name__ and __date__ fields without __id__. (**_id** included by default, so we must exclude it explicitly). <br><br>
It is important to note the three behaviors of field projects, listed as follows:
* The **_id** field will always be included, unless excluded explicit.
* When one or more fields are explicitly included, the other fields (expect **_id**) get excluded automatically.
* Explicitly excluding one or more fields will automatically include the rest of the fields, along with **_id**

#### Finding the Distinct Fields
The __distinct()__ function is used to get the distinct or unique values of a field with or without query criteria. 
For the purpose of this example, we will use the __movies__ collection. 
Each movie is assigned an audience suitability rating that is based on the content and viewers' age. 
Let's find the unique ratings that exist in our collection with the help of the following query: <br>
`db.movies.distinct("rated")` <br>
This query gives us all the __unique__ ratings from the __movies__ collection. <br><br>

The __distinct()__ function can also be used along with a query condition. 
The following example finds all the unique ratings
the films that were released in 1987 have received: <br>
`db.movies.distinct("rated",{"year": 1987})`

The result of __distinct__ is always returned as array.
### Counting the Documents
___
#### count()
This function is used to return the count of the documents 
within a collection or a count of the documents that match the given query.
When executed without any query argument, it returns the total count of documents in the collection
, as follows:
```shell
// Count of all movies
db.movies.count()
```
When the function is provided with a query, the count of documents that match the given query is returned. For example, the following
query will return count of movies that have exactly six comments:
```shell
// Counting movies that have 6 comments
db.movies.count("num_mflix_comments": 6)
```
#### countDocuments()
This function returns the count of documents that are matched by the given condition.
The following is an example query that returns the count of movies released in 2001: <br>
`db.movies.countDocuments({"year":2001})` <br>
Unlike the `count()` function, a query argument is a mandatory for `countDocuments()`. <br>
To count all the documents in the collection, we can pass an empty query to the function 
as follows: `db.movies.countDocuments({})`

#### estimatedDocumentCount()
This function returns the approximate or estimated count of documents in a collection.
It does not accept any query and always returns the count of all documents in the collection.
The count is always based on the _collection's **metadata**_.
`db.movies.estimatedDocumentCount()` <br>
As the count is based on metadata, the results are less accurate, but the performance is better.
The function should be used when performance is more important that accuracy.

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

### Logical Operators
___

#### $and Operator
Using the __$and__ operator, you can have any number of conditions wrapped in an array
and the operator will return only the documents that satisfy all the conditions. <br>
When a documents fails a condition check, the next conditions are skipped.
That is why the operator is called a short-circuit operator. <br>
For example, If we want to determine the count of _unrated_ movies that were released in 1987. This
query must have two conditions:
* The field rated should have value of __UNRATED__
* The field year must be equal to __1987__
```shell
db.movies.countDocuments (
  { $and:
    [{"rated":"UNRATED"},{"year":1987}]
  }
) 
```

#### $or Operator
```shell
db.movies.find(
  { $or: [
   {"rated": "G"},
   {"rated": "PG"},
   {"rated": "PG-13"}
  ]}
)
```
Query that will find movies are three conditions:
* {"rated" : "G"}
* {"year": 1987}
* {"num_mflix_comments" :{$gte: 5}}
```shell
db.movies.find(
  {$or:[
     {"rated":"G"},
     {"year":1987},
     {"num_mflix_comments" :{$gte: 5}}
     ]}
) 
```

#### $nor Operator
The $nor operator is syntactically like $or but behaves in opposite way.
The __$nor__ operator accepts multiple conditions expressions in the form of an array and returns
the documents that do not satisfy any of the given conditions. The conditions. <br><br>
The following is the same query we wrote above,expect that __$or__ operator is replaced with __$nor__:
```shell
db.movies.find(
  {$nor:[
     {"rated":"G"},
     {"year":1987},
     {"num_mflix_comments" :{$gte: 5}}
     ]}
) 
```
This query will match and return all the movies that are __not__ rated __G__, were not released
in __1987__ and do not have more than __5__ comments.

#### $not Operator
The __$not__ operator represents the logical NOT operation that negated the given condition.<br>
The following query finds movies with __5__ or more comments:
```shell
db.movies.find(
    {"num_mflix_comments":{$gte: 5}}
) 
```
Use the __$not__ operator in the same query and negate the given condition:
```shell
db.movies.find(
    {"num_mflix_comments":{$not: {$gte: 5}}}
) 
```
This query will return all the movies that do not have 5 or more comments and the movies that do not contain the __num_mflix_comments__ field.

More examples:
1. The first condition is that Or Hasson must be one of the actors and that Rich Parker must be the director:
```shell
 db.movies.find(
 {
   "cast":"Or Hasson",
   "directors":"Rich Parker"
 }
 )
```
2. Second condition to get the movies of drama or crime genres:
```shell
 db.movies.find(
 {
   "cast":"Or Hasson",
   "directors":"Rich Parker",
   "$or":[{"genres":"Drama","genres":"Crime"}]
   }
 )
```
3. Next we want only in the title and release year. For this, we will add the projection part:
```shell
 db.movies.find(
 {
   "cast":"Or Hasson",
   "directors":"Rich Parker",
   "$or":[{"genres":"Drama","genres":"Crime"}]
   },
   {
     "title": 1, "year": 1, "_id":0
   }
 )
```

### Regular Expressions
___
In MongoDB queries, regular expressions can be used with the __$regex__ operator. <br>
For example, we typed __Hasson__ into the search box, and we want to find all the movies whose title
contain this character pattern:
```shell
db.movies.find(
  {"title": {$regex: "Hasson"}}
)
```

#### Using the Caret [^] Operator
To find only the strings that start with the given regular expression, the caret operator (^) can be used. <br>
To find only those movies whose titles start with the word __Hasson__:
```shell
db.movies.find(
  {"title": {$regex: "^Hasson"}}
)
```

#### Using the Dollar [$] Operator
To find only movies with title end with the word "Hasson":
```shell
db.movies.find(
  {"title": {$regex: "Hasson$"}}
)
```

#### Case-Insensitive Search
To do Case-Insensitive search, prove the __$options__ argument with a value of __i__,
where __i__ stands for Case-Insensitive:
```shell
db.movies.find(
  {"title": {$regex: "Hasson", $options: "i"}}
)
```




