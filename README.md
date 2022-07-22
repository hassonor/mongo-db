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

### Query Arrays And Nested Documents
___
#### Finding an Array By An Element
The use wants to search for movies with the actors __Or Hasson__ and __Edna Purviance__ together:
```shell
db.movies.find(
    {$and: [
      {"cast": "Or Hasson"},
      {"cast": "Edna Purviance"}
    ]}
)
```

#### Finding an Array By An Array
The user wants to find movies that are available in both __English__ and __Hebrew__:
```shell
db.movies.find(
    {"languages": ["English","Hebrew"]}
)
  
// The order is matter here so next query will give up different results:
db.movies.find(
    {"languages": ["Hebrew","English"]}
)
```

#### Searching An Array With The $all Operator
The __$all__ operator finds all those documents where the value of the fields contains all the elements, irrespective of thier order or size:
```shell
db.movies.find(
    {"languages": { "$all": ["English","Hebrew"]}}
)
```

#### Projecting Array Elements
With next query, The array field will only contain the matching element;<br>
the rest of the elements will be skipped. <br>
Thus, the __languages__ array will only contain __Hebrew__ element. <br>
The MOST important thing to remember is that if more than one element is matched, the __$__ operator projects only
the first matching element.
```shell
db.movies.find(
    {"languages": "Hebrew"},
    {"languages.$": 1}
)
```

#### Projecting Matching Elements By their index position ($slice)
The __$slice__ operator is used to limit the array elements based on their index position.
This operator can be used with any array field, irrespective of the field being queried or not.
This means that we mary query a different field and still use this operator to limit the elements of the array fields.
In the following query, use __$slice__ to print only the first three elements of the array:
```shell
db.movies.find(
    {"title": "With Or Without You"},
    {"languages": {$slice: 4}}
).pretty()
```
Will return the results that match the title __With Or Without You__ and the __languages__ will
only contain the first four elements. <br>
The __$slice__ operator can be passed with two arguments, where the first argument indicates the number
of elements to be skipped and the second one indicates the number of elements to be returned.

####  Querying Nested Objects
The following query finds the __awards__ object by providing the complete object as its values:
```shell
db.movies.find(
      {
        "awards":
            {"wins":1, "nominations": 0, "text":"4 win."}
      }
)
  
// Previous query is NOT the same:
db.movies.find(
      {
        "awards":
            {"nominations": 0,"wins":1, "text":"4 win."}
      }
)
```

#### Querying Nested Object Fields
To finds movies that have won five awards, we can use __'.'__ notation like so:
```shell
db.movies.find(
      {
        {"awards.wins": 5 }
      }
)
```
The nested field search is performed independently on the given fields, irrespective of the
order of the elements. We can search by multiple fields and use any of the conditional or logical query operators.
For example the next query uses a combination of two conditions on two different nested fields.
```shell
db.movies.find(
      {
        {"awards.wins": {$gte: 5}},
        "awards.nominations":5
      }
)
```

#### Projecting Nested Object Fields
1. This query return all the records and project only the __awards__ field:
```shell
db.movies.find(
      {},
      {
        "awards":1,
        "_id":0
      }
)
```
2. To project specific fields from embedded objects, we can refer to a field of anm embedded object
   using __'.'__ notation. For example:
```shell
 db.movies.find(
      {},
      {
        "awards.wins":1,
        "awards.nominations":1,
        "_id":0
      }
)
```

### Limiting, Skipping and Sorting Documents
___

#### Limiting the result
To limit the number of records a query returns, the resulting cursor provides a function called __limit()__.
For example to get titles of movies starring __Or Hasson__ and restrict the result size to __5__:
```shell
db.movies.find(
    {"cast": "Or Hasson"},
    {"title": 1, "_id":0}
).limit(5)
```

#### Limit and batch size
One of the main purpose of batching is to avoid high resource utilization,
which may happen while processing a large number of record sets. <br>
Also, it keeps the connection between the client and server active,
because of which timeout errors are avoided. <br>
For large queries, when the db takes linger to find and return the result,
the client just keeps on waiting. After a certain threshold value for waiting is reached, the connection between the client and
server is broken and the query is failed with a timeout exception.<br>
Using batching avoids such timeouts as the server keeps returning the individual batches continuously. <br>
For example without limit:
```shell
db.movies.find(
    {"cast": "Or Hasson"},
    {"title": 1, "_id":0}
).batchSize(5)
```
For example with limit:
```shell
db.movies.find(
    {"cast": "Or Hasson"},
    {"title": 1, "_id":0}
).limit(5).batchSize(5)
```

#### Skipping Documents
Skipping is used to exclude some documents in the result set and return the rest. <br>
The MongoDB cursor provides the __skip()__ function, which accepts an integer and skips the specified number of documents
from the cursor, returning the rest. <br>
The following example uses the same query with __skip__ function:
```shell
db.movies.find(
    {"cast": "Or Hasson"},
    {"title": 1, "_id":0}
).skip(3)
```
Since the __skip()__ function have been provided with the value __3__, the first three documents will be excluded
from the output.

#### Sorting Documents
The MongoDB cursor provides a __sort()__ function that accepts an argument of the document type,
where the documents define a sort order for specific fields.
The following query we are calling the __sort()__ function on the resulting cursor. <br>
The argument to the function is a document where the __title__ field has a value of __1__.<br>
This specifies that the given field should be sorted in ASC order.
```shell
// ASC order
db.movies.find(
    {"cast": "Or Hasson"},
    {"title": 1, "_id":0}
).sort({"title": 1})
  
// DESC order
db.movies.find(
    {"cast": "Or Hasson"},
    {"title": 1, "_id":0}
).sort({"title": -1})
```
Another example, The next query should return 50 movies where the movie with the highest IMDb rating appearing at the top.
If two movies have the same ratings, then the older movie should take precedence.<br>
The following query can be used to implement this:
```shell
// ASC order
db.movies.find()
    .limit(50)
    .sort({"imdb.rating": -1, "year": 1})
```

More Examples:
Finding Movies by Genre and Paginate Results:
```javascript

    const genre = "Comedy"
    const pageNumber = 4
    const pageSize = 7
    
    const findMoviesByGenre = function(genre, pageNumber, pageSize) {
        const toSkip = 0;
        if (pageNumber < 2) {
            toSkip = 0;
        } else {
            toSkip = (pageNumber - 1) * pageSize;
        }

        const movies = db.movies.find(
            {"genres": genre},
            {"_id": 0, "title": 1})
            .sort({"imdb.rating": -1})
            .skip(toSkip)
            .limit(pageSize)
            .toArray()
    }
```

### Updating with Aggregation Pipelines and Arrays
___
#### Updating with an Aggregation Pipeline
// Step 1 Creating the documents
```shell

db.users.insertMany ([
  { full_name: "Or Hasson" },
  { full_name: "Arya Stark" }
])


```
// Step 2 update the documents
```shell


db.users.updateMany(
  {},
  [
      {
        $set : {"name_array": {$split: ["full_name"," "]}},
      },
      {
        $set: {
              "first_name": {"arrayElemAt" :["$name_array",0]},
              "last_name": {"arrayElemAt" :["$name_array",1]},
        }
      },
      {
        $project: {
          "first_name": 1,
          "last_name": 1,
          "full_name": {
              $concat : [{$toUpper: "$first_name"}, " ", "$last_name"]
          }
        }
      }
  ]
)
```

// Step_3 Get The new Data
```shell
db.users.find({}, {_id: 0})

{
  "first_name": "Or", "last_name": "Hasson", "full_name": "OR Hasson"
}
{
   "first_name": "Arya", "last_name": "Stark", "full_name": "ARYA Stark"
}
```

#### Updating Array Fields

// Insert **movies** collection:
```shell
db.movies.inset({ _id: 123,"title": "The hasson" })
```
// Adding array field:
```shell
    db.movies.findOneAndUpdate(
    {_id: 123},
    {$set: {"genre":["Unknown"]}},
    {"returnNewDocument": true}
    )
```
// Uses $unset we can remove the **genre** field.
```shell
db.movies.findOneAndUpdate(
  {_id: 123},
  {$unset: {"genre": ""}},
  {"returnNewDocument": true}
)
```

#### Adding Elements to Arrays
Adding an elements to Array:
```shell
db.movies.findOneAndUpdate(
  {_id: 123},
  {$push: {"genre": "unknown"}},
  {"returnNewDocument": true}
)
  
  db.movies.findOneAndUpdate(
  {_id: 123},
  {$push: {"genre": "Drama"}},
  {"returnNewDocument": true}
)
```

#### Adding Multiple Elements to Arrays
```shell
db.movies.findOneAndUpdate(
  {_id: 123},
  {
    $push: {
      "genre": {
        $each: ["History","Action"]
      }}
  },
  {"returnNewDocument": true}
)
```
#### Sort Array
Sort the array alphabetically (ASC =  sort => 1) or (DESC = sort => -1)
```shell
db.movies.findOneAndUpdate(
  {_id: 123},
  {
    $push: {
      "genre": {
        $each: [],
        $sort: 1
      }}
  },
  {"returnNewDocument": true}
)
```

#### An Array As a Set
Using $addToSet to add element to array and using $each to add few elements:
```shell
db.movies.findOneAndUpdate(
  {_id: 123},
  {$addToSet:{
    "genres": {
        $each : ["History","Thriller","Drama"]
      }}
    },
    {"returnNewDocument": true}
)

```
Update documents with filter and addToSet:
```shell
    db.movies.updateMany(
      {
        "cat.viewer.meter" : {$gt: 90},
        "cat.viewer.critic" : {$gt: 90},
      },
      {
        $addToSet: {"genres": "Classic"}
      }
    )
```

#### Removing Array Elements
___
#### Removing the first or last element ($pop)
The **$pop** operator, when used in an update command, allows us remove the first or last element
in an array. It removes one element at a time and can only be used with the values 1 (for the last element),<br>
or -1 (for the first element).<br>
For example removing the last element on "genre":
```shell
db.movies.findOneAndUpdate(
  {_id: 123},
  {$pop: {"genre": 1}},
  {"returnNewDocument": true}
)
```
For example removing the first element on "genre":
```shell
db.movies.findOneAndUpdate(
  {_id: 123},
  {$pop: {"genre": -1}},
  {"returnNewDocument": true}
)
```
#### Removing all elements
When we only need to remove certain elements from an array,
We can use the `$pullAll` operator.<br>
We provide one or more elements to the operator, which
then removes all occurrences of those elements from the array. <br>
For example:
```shell
db.movies.findOneAndUpdate(
  {_id: 123},
  {$pullAll: {"genre": ["Action","Crime"]}},
  {"returnNewDocument": true}
)
```
#### Removing Matched Elements
Query to update the array with `$pull`. it allows us to use combinations of logical and conditional operators to
prepare a query condition, just like any **find** query.
The following example will remove the elements that have `quantity` 4 and `name` ends with `tr`:
```shell
db.items.findOneAndUpdate(
  {_id: 123},
  {$pull: {
      "items": {
          "quantity": 4,
          "name": {$regex: "tr$"}
      }
  }},
  {"returnNewDocument": true }
)
```

#### Updating Array Elements
The **genres** array has two elements, and we will update both of them using the following command:
```shell
db.movies.findOneAndUpdate(
  {_id: 123},
  {$set: {"genre.$[]":"Or Hasson"}},
  {"returnNewDocument": true}
)
```
Let's assume we have an element on Array `items` array without only `name` field, but it should have<br>
`quantity` and `price` fields too. We can filter by elements with `null` value on a field and add them<br>
to the elements that doesn't have a value there:
```shell
    db.items.findOneAndUpdate(
      {_id: 123},
      {$set: {
        "items.$[myElements]" :{
            "quantity": 9,
            "price":5.5,
            "name":"Hasson"
        }
      }},
      {
        "returnNewDocument": true,
        "arrayFilters":[{"myElements.quantity":null}]
      }
    )
```
Another example, we want to update directors array to `Or Hasson` director and change it from another value:
```shell
    db.movies.updateMany(
      {"directors": "Unknown Director"},
      {$set: {
          "directors.${elem}" : "Or Hasson"
      }},
      {
        "arrayFilters": [{elem: "Unknown Director"}]
      }
    )
```




