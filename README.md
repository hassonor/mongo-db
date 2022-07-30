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

This technique is called __projection__. Projection is expressed as a second argument to the __find()__ or __findOne()__
functions.
In the projection expression, we can explicitly exclude a field by setting it to 0 or include one by setting it to 1.
Thus, in the last example above it will find all comments posted by the user `Or Hasson` and returns only
the __name__ and __date__ fields without __id__. (**_id** included by default, so we must exclude it explicitly)
. <br><br>
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

When the function is provided with a query, the count of documents that match the given query is returned. For example,
the following
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

This query will return all the movies that do not have 5 or more comments and the movies that do not contain the __
num_mflix_comments__ field.

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

The __$all__ operator finds all those documents where the value of the fields contains all the elements, irrespective of
thier order or size:

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

#### Querying Nested Objects

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
the client just keeps on waiting. After a certain threshold value for waiting is reached, the connection between the
client and
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
The MongoDB cursor provides the __skip()__ function, which accepts an integer and skips the specified number of
documents
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

Another example, The next query should return 50 movies where the movie with the highest IMDb rating appearing at the
top.
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

const findMoviesByGenre = function (genre, pageNumber, pageSize) {
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

Sort the array alphabetically (ASC = sort => 1) or (DESC = sort => -1)

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

### Data Aggregation

___
There are two parameters used for aggregation. The **pipeline** parameter contains all the logic to find,
sort,project,limit,transform,
and aggregate our data. <br>
The **pipeline** parameter itself is passed in as array of JSON documents.<br>
The second parameter is the __options'__ parameter. This is optional and allows us to specify the details of the
configuration, such as how the aggregation should execute or some flags that are required during debugging and building
our pipelines.<br>

#### Pipeline Syntax

The pipeline is an array, witch each item in the array being an object:

```shell
const pipeline = [
    { . . . },
    { . . . },
    { . . . },
]
```

Each of the objects in the array represents a single stage in the overall pipeline, with
the stages being executed in their array order (top to bottom). <br>
Each stage object takes the form of the following

```shell
{$stage: parameters}
```

The stage represents the action we want to perform on the data (such as __limit__ or __sort__)
and the parameters can be either a single value or another object, depending on the stage.<br><br>
Example: _Pipeline passed as a variable_:

```shell
const pipeline = [
        { $match: {"location.address.state":"IL"} },
        { $project: {"location.address.city": 1} },
        { $sort: {"location.address.city": 1} },
        { $limit: 5  },
        ]
```

#### Creating Aggregations

Match the theater collection to get a list of all theaters in __IL__ state.<br>
Project only by the city.<br>
Sort the list by __city__ name. <br>
Limit the result to the first __5__ theaters.

```shell
const simpleFind = () =>{
  //Find command using filter, project, sort and limit.
  print("Find Result:")
  db.thearters.find(
     {"location.address.state":"IL"},
     {"location.address.city": 1})
     .sort({"location.address.city": 1})
     .limit(5)
     .forEach(printjson);
  )
}
simpleFind();
```

Rebuild the previous example by __aggregation__:

```shell
const simpleFindAsAggregate = () =>{
#  Aggregation using match, project, sort and limit.
  print("Aggregation Result:")
  const pipeline = [
        { $match: {"location.address.state":"IL"} },
        { $project: {"location.address.city": 1} },
        { $sort: {"location.address.city": 1} },
        { $limit: 5  },
        ];
        db.theaters.aggregate(pipeline).forEach(printjson);

}
simpleFindAsAggregate();
```

The __$match__ and __$project__ stages execute first because these will reduce the size of the result set at each
stage. <br>
It is generally good practice to try and reduce the number of documents that will add excessive loads to the server.
<br>
Another example to Find Top Actions Movies with aggregation:

```shell
 const findTopActionMovies = () =>{
   print("Finding top Action movies...")
   const pipeline = [
    { $match: {
      geres: {$in: ["Action"]}, //Action movies only
      released: {$lte: new ISODate("2000-01-01T00:00:00Z")} //Movies Before 2000-01-01
    }},
    { $sort: {"imdb.rating": -1}} // Sort by IMDB rating.
        { $limit: 3 }, // Limit to 3 results.
        { $project: title: 1, genres: 1, released: 1, "imdb.rating": 1} //  (Last Stage)
   ]
 }
findTopActionMovies();
```

### Manipulating Data

___

#### The Group Stage

The __$group__ stage allows up to group documents based on specific condition. <br>
The __$group__ stage serves as the cornerstone of the most powerful queries.  <br>
The most basic implementation of a __$group__ stage accepts only an **_id** key, with the value being an
expression. <br>
For example, the folliwng code will group all movies by their rating, outputting a single record for each rating
category:

```shell
const pipeline = [
  {$group: {
    _id:"$rated"
  }}
  ];
  db.movies.aggregate(pipeline).forEach(printjson);
]

Output:
  {"_id": "NC-16"}
  {"_id": "G"}
  {"_id": "R"}
  {"_id": "TV-Y7"}
  {"_id": "PG-13"}
```

#### Accumulator Expressions

The $group command can accept more than just one argument. It can also accept any number of additional arguments in the
following format:<br>
`field: { accumulator: expression}` <br>

* __field__ will define the key of our newly computed field for each group.
* __accumulator__ must be a supported accumulator operator. There are a group
  of operators.
* __expression__: in this context will be passed to the __accumulator__ operator as the input
  of what field in each document it should be accumulating.<br><br>
  _Example_: Identify the total number of movies in each group:

```shell
const pipeline = [
  {$group:{
    _id: "$rated",
    "numMovies": { $sum: 1}
  }}
];
db.movies.aggregate(pipeline).forEach(printjson);

//Output
{"_id": "NC-17","numMovies": 45}
{"_id": "PG","numMovies": 11}
{"_id": "OPEN","numMovies": 455}
```

_Example_ Find the total runtime of every single film in rating
,group the __rating__ field and accumulate the runtime of each film:

```shell
const pipeline = [
  {$group: {
    _id: "$rated",
    "sumRuntime": { $sum: "$runtime"}
  }}
];
db.movies.aggregate(pipeline).forEach(printjson);

//Output
{"_id": "Not Rated", "sumRuntime": 111}
{"_id": "OPEN", "sumRuntime": 87}
{"_id": "PASSED", "sumRuntime": 515}
```

_Example_: Get the avg runtime of the titles for each group.<br>
Change the __$sum__ to __$avg__ and return the avg runtime across each group: <br>:

```shell
const pipeline = [
  {$group: {
    _id: "$rated",
    "avgRuntime": { $avg: "$runtime"}
  }}
];
db.movies.aggregate(pipeline).forEach(printjson);

//Output
{"_id": "Not Rated", "avgRuntime": 105.754}
{"_id": "OPEN", "avgRuntime": 114.1}
{"_id": "PASSED", "avgRuntime": 91.55555}
```

_Example_: Get the avg runtime of the titles for each group.<br>
Change the __$sum__ to __$avg__ and return the avg runtime across each group <br>
Adding __$trunc__ stage to get integer avg value:

```shell
const pipeline = [
  {$group: {
    _id: "$rated",
    "sumRuntime": { $avg: "$runtime"}
  }},
  {$project: {
      "roundedAvgRuntime": { $trunc: "$avgRuntime"}
  }}
];
db.movies.aggregate(pipeline).forEach(printjson);

//Output
{"_id": "Not Rated", "avgRuntime": 105}
{"_id": "OPEN", "avgRuntime": 114}
{"_id": "PASSED", "avgRuntime": 91}
```

#### Manipulating Data Example_1:

* Match movies that were released before 1997.
* Find the average popularity of each genre.
* Sort genres by popularity.
* Output the adjusted runtime of each movie.
  Translate to steps: <br>
* Match movies that were released before 1997.
* Group all movies by their first genre and accumulate the average and maximum IMDb ratings.
* Sort by the average popularity of each genre.
* Project the adjusted runtime as __total_runtime__.

```shell
 const findGenrePopularity = () =>{
   print("Finding popularity of each genre");
   const pipeline = [
        {$match: {
          released: {$lte: new ISODate("1997-01-01T00:00:00Z")}
        }},
        {$group: {
          _id:{"$arrayElemAt":["$genres", 0]}
          "popularity": { $avg: "$imdb.rating"},
          "top_movie": {$max: "$imdb.rating"},
          "longest_runtime":{$max: "$runtime"}
        }},
        {$sort: {popularity: -1 }},
        {$project: {
          _id: 1,
          popularity: 1,
          top_movie: 1,
          adjusted_runtime: {$add: ["$longest_runtime", 15 ] } } }, //Adding 15 minutes of trailers
   ];
   db.movies.aggregate(pipeline).forEach(printjson);
 }
 findGenrePopularity();
 
 //Output 
 {
   "id": "Action",
   "popularity": 8.73,
   "top_movie": 8.7,
   "adjusted_runtime": 111
 }
 {
   "id": "Short",
   "popularity": 8.13,
   "top_movie": 9.1,
   "adjusted_runtime": 1112
 }
 {
   "id": "Documentary",
   "popularity": 7.43,
   "top_movie": 8.6,
   "adjusted_runtime": 1254
 }
```

#### Manipulating Data Example_2 - Selecting the title from each movie Category:

```shell
 const findGenrePopularity = () => {
   print("Finding popularity of each genre");
   const pipeline = [
        {$match: {
          released: {$lte: new ISODate("1997-01-01T00:00:00Z")}, //Filter out movies after 1997-01-01.
          runtime: {$lte: 220} //Filter out movies longer than 220 minutes.
          "imdb.rating": {$gte: 7.5} //Filter out movies with lower than 7.5 rating.
        }},
        {$sort: {"imdb.rating": -1 }},
        {$group: {
          _id:{"$arrayElemAt":["$genres", 0]},
          "recommended_title": {$first: "$title"},
          "recommended_rating": {$first: "$imdb.rating"},
          "recommended_raw_runtime": {$first: "$runtime"},
          "popularity": { $avg: "$imdb.rating"},
          "top_movie": {$max: "$imdb.rating"},
          "longest_runtime":{$max: "$runtime"}
        }},
        {$sort: {popularity: -1 }},
        {$project: {
          _id: 1,
          popularity: 1,
          top_movie: 1,
          recommended_title: 1,
          recommended_rating: 1,
          recommended_raw_runtime: 1,
          adjusted_runtime: {$add: ["$longest_runtime", 15 ] } } }, //Adding 15 minutes of trailers
   ];
   db.movies.aggregate(pipeline).forEach(printjson);
 }
 findGenrePopularity();


//Output
 {
   "id": "Action",
   "recommended_title": "Or Hasson was Here",
   "recommended_rating": 9.1,
   "recommended_raw_runtime": 95,
   "popularity": 8.13,
   "top_movie": 9.1,
   "adjusted_runtime": 1112
 }
 {
   "id": "Documentary",
   "popularity": 7.43,
   "top_movie": 8.6,
   "adjusted_runtime": 1254
 }``
```

#### Joining Collections With $lookup

In production queries, we may sometimes need to write queries that ar operating across multiple
collections. In MongoDB, these collection joins are done using the $lookup aggregation step.

```javascript
const lookupExample = () => {
    const pipeline = [
        {
            $match: {
                $or: [{"name": "Catelyn Stark"},
                    {"name": "Or Hasson"}]
            }
        },
        {
            $lookup: {
                from: "comments",
                localfield: "name",
                foreignField: "name",
                as: "comments"
            }
        },
        {$limit: 3},
    ];
    db.users.aggregate(pipeline).forEach(printjson);
}
lookupExample();
```

First, we are running a __$match__ against the __users__ collection to get
only two users named __Catelyn Stark__ and __Or Hasson__. <br>
Once we have these two records, wer perform our lookup. The four parameters of
__$lookup__ are as follows:<br>

* __from__: The collection we are joining to our current aggregation. In this case, we are
  joining **comments** to **users**.
* __localField__: The field name that we are going to use to join our documents in the local collection
  (The collection we are running the aggregation on). In our case, the name of our user.
* __foreignField__: The field name that links to __localField__ in the __from__ collection.
  These may have different names, but in our scenario, it is the same field: __name__.
* __as__: This is how our new joined data will be labeled.<br><br>
  If we were to run the pipeline as it is, the beginning of the output would look something like this:

```shell
 {
   "_id": ObjectId("5bf142459b72e12b2b1b2cd"),
   "name":"Or Hasson",
   "email":"hassonor@gmail.com",
   "password": "$124987ufmfklfsdnurt284359sdkjh82435hsfdi8423h5fdsbjk31259/Vu",
   "comments":[
        {
          "_id": ObjectId("5bf142459b72e12b3b1b2cd"),
          "name": "Or Hasson",
          "email": "hassonor@gmail.com",
          "movie_id": ObjectId("5bf142459b72e12b3b1b243"),
          "text": "This is a very good movie."
          "date": ISO("2020-02-21T03:17:06Z")
        },
         {
          "_id": ObjectId("5bf142459b72e12b3b1b2cb"),
          "name": "Or Hasson",
          "email": "hassonor@gmail.com",
          "movie_id": ObjectId("5bf142459b72e12b3b1b241"),
          "text": "This is a very good movie 2."
          "date": ISO("2020-02-21T03:17:06Z")
        },
          {
          "_id": ObjectId("5bf142459b72e12b3b1b2ba"),
          "name": "Or Hasson",
          "email": "hassonor@gmail.com",
          "movie_id": ObjectId("5bf142459b72e12b3b1b225"),
          "text": "This is a very good movie 3."
          "date": ISO("2020-02-21T03:17:06Z")
        }
   ]
 }
```

In our example, users have made many comments, so the embedded array becomes quite substantial and challenging
to view. This issue presents an excellent place to introduce the __$unwind__ operator, as these joins can often
result in large arrays of related documents. __$unwind__ is a relatively simple stage. It
deconstructs an array field from an input document to output a new document for each element in the array.
For example, if you $unwind this document:<br>
`{a: 1, b: 2, c: [1,2,3,4]`<br>
The output will be the following documents:

```shell
{"a": 1, "b": 2, "c":1}
{"a": 1, "b": 2, "c":2}
{"a": 1, "b": 2, "c":3}
{"a": 1, "b": 2, "c":4}
```

We can add this new stage to our join and try running it:

```javascript
const lookupExample = () => {
    const pipeline = [
        {
            $match: {
                $or: [{"name": "Catelyn Stark"},
                    {"name": "Or Hasson"}]
            }
        },
        {
            $lookup: {
                from: "comments",
                localfield: "name",
                foreignField: "name",
                as: "comments"
            }
        },
        {$unwind: "$comments"},
        {$limit: 3},
    ];
    db.users.aggregate(pipeline).forEach(printjson);
}
lookupExample();
```

We will see output like this:

```shell
 {
   "_id": ObjectId("5bf142459b72e12b2b1b2cd"),
   "name":"Or Hasson",
   "email":"hassonor@gmail.com",
   "password": "$124987ufmfklfsdnurt284359sdkjh82435hsfdi8423h5fdsbjk31259/Vu",
   "comments":
        {
          "_id": ObjectId("5bf142459b72e12b3b1b2cd"),
          "name": "Or Hasson",
          "email": "hassonor@gmail.com",
          "movie_id": ObjectId("5bf142459b72e12b3b1b243"),
          "text": "This is a very good movie."
          "date": ISO("2020-02-21T03:17:06Z")
        },
}
{
   "_id": ObjectId("5bf142459b72e12b2b1b2cd"),
   "name":"Or Hasson",
   "email":"hassonor@gmail.com",
   "password": "$124987ufmfklfsdnurt284359sdkjh82435hsfdi8423h5fdsbjk31259/Vu",
   "comments":
            {
                "_id": ObjectId("5bf142459b72e12b3b1b2cb"),
                "name": "Or Hasson",
                "email": "hassonor@gmail.com",
                "movie_id": ObjectId("5bf142459b72e12b3b1b241"),
                "text": "This is a very good movie 2."
                "date": ISO("2020-02-21T03:17:06Z")
              },
}
{
   "_id": ObjectId("5bf142459b72e12b2b1b2cd"),
   "name":"Or Hasson",
   "email":"hassonor@gmail.com",
   "password": "$124987ufmfklfsdnurt284359sdkjh82435hsfdi8423h5fdsbjk31259/Vu",
   "comments":
            {
                "_id": ObjectId("5bf142459b72e12b3b1b2ba"),
                "name": "Or Hasson", 
                "email": "hassonor@gmail.com",
                "movie_id": ObjectId("5bf142459b72e12b3b1b225"),
                "text": "This is a very good movie 3."
                "date": ISO("2020-02-21T03:17:06Z")
              }
}
```

#### EX: Listing the most user-comments movies

In this ex, we will help the cinema company to obtain a list of movies that generate the most comments from users.
Perform the following steps to complete this ex: <br>

Outline the stages in our pipeline; they appear in the following order:

* __$group__ the comments by the movie for which they are targeted.
* __$sort__ the result by the number of total comments.
* __$limit__ the result to the top five movies by comments.
* __$lookup__ the movie that matches each document.
* __$project__: just the movie title and rating.
* __$merge__: the result into a new collection.

Step 1:

```shell
const findMostCommentedMovies = () =>{
    print("Finding the most commented on movies.")
    const pipeline = [
        {$group: {
          _id: "$movie_id",
          "sumComments": {$sum: 1}  // sum the total comments each movie
        }},
        {$sort: {"sumComments": -1 }}, // sort by highest __sumComments__ value are first
        {$limit: 5},
    ];
    db.comments.aggregate(pipeline).forEach(printjson);  
} 
findMostCommentedMovies();
```

Output will appear as follows:

```shell
    {"_id": ObjectId("5bf142459b72e12b2b1b2cd"),"sumComments": 45}
    {"_id": ObjectId("5bf142459b72e12b2b1b2ab"),"sumComments": 40}
    {"_id": ObjectId("5bf142459b72e12b2b1b4cd"),"sumComments": 35}
    {"_id": ObjectId("5bf142459b72e12b2b1b5cd"),"sumComments": 27}
    {"_id": ObjectId("5bf142459b72e32b2b1b5ad"),"sumComments": 21}
```

Step 2:
Perform a lookup into the __movies__ collection to match our
comment group with the movie documents:

```shell
const findMostCommentedMovies = () =>{
    print("Finding the most commented on movies.")
    const pipeline = [
        {$group: {
          _id: "$movie_id",
          "sumComments": {$sum: 1}  // sum the total comments each movie
        }},
        {$sort: {"sumComments": -1 }}, // sort by highest __sumComments__ value are first
        {$limit: 5},
        {$lookup:{
          from: "movies",
          localfield: "_id",
          foreignField: "_id",
          as: "movie"
        }}
    ];
    db.comments.aggregate(pipeline).forEach(printjson);  
} 
findMostCommentedMovies();
```

Output will appear as follows:

```shell
    {"_id": ObjectId("5bf142459b72e12b2b1b2cd"),"sumComments": 45,
      "movie":[
      {
        "_id": ObjectId("5bf142459b72e12b2b1b2cd"),
        "fullplot": "lorem ipsum dolor sit amet, consectetur adipiscing elit"
        "imdb"{
          "rating": 8.4,
          "votes": 156344,
          "id": 11555056
        }
      }]
    }
    {"_id": ObjectId("5bf142459b72e12b2b1b2ab"),"sumComments": 40,
     "movie":[
      {
        "_id": ObjectId("5bf142459b72e12b2b1b2ab"),
        "fullplot": "lorem ipsum dolor sit amet, consectetur adipiscing elit"
        "imdb"{
          "rating": 8.1,
          "votes": 156144,
          "id": 11555051
        }
      }]
    }
    ....
```

There is only one movie in each __movie__ array, so unwind those arrays to simplify the structure.
Once it is unwound, we can project out all the fields we don't care to see.
In Addition, we still need to output this result into a collection.
Add the __$out__ step at the end:
Step 3:

```shell
const findMostCommentedMovies = () =>{
    print("Finding the most commented on movies.")
    const pipeline = [
        {$group: {
          _id: "$movie_id",
          "sumComments": {$sum: 1}  // sum the total comments each movie
        }},
        {$sort: {"sumComments": -1 }}, // sort by highest __sumComments__ value are first
        {$limit: 5},
        {$lookup:{
          from: "movies",
          localfield: "_id",
          foreignField: "_id",
          as: "movie"
        }},
        {$unwind: "$movie"},
        {$project: {
          "movie.title": 1,
          "movie.imdb.rating":1,
          "sumComments": 1
        }},
        {$output: "most_commented_movies"}
    ];
    db.comments.aggregate(pipeline).forEach(printjson);  
} 
findMostCommentedMovies();
```

After running this query we should be able to check the newly created collection using
__find()__ and see our results: <br>
`findMostCommentedMovies()`<br>
`db.most_commented_movies.find({})`<br><br>
Output should looks like:

```shell
    {"_id": ObjectId("5bf142459b72e12b2b1b2cd"),"sumComments": 45, "movie": {"imdb": {"rating": 8.5}, "title": "Gladiator"}}
    {"_id": ObjectId("5bf142459b72e12b2b1b2ab"),"sumComments": 40, "movie": {"imdb": {"rating": 7.8}, "title": "Lord Of The Ring"}}
    {"_id": ObjectId("5bf142459b72e12b2b1b4cd"),"sumComments": 35, "movie": {"imdb": {"rating": 7.1}, "title": "The Ring"}}
    {"_id": ObjectId("5bf142459b72e12b2b1b5cd"),"sumComments": 27, "movie": {"imdb": {"rating": 7.3}, "title": "American X"}}
    {"_id": ObjectId("5bf142459b72e32b2b1b5ad"),"sumComments": 21, "movie": {"imdb": {"rating": 6.5}, "title": "Shrek"}}


```

#### Filter Early and filter often`

A common way to first filter stage in our pipeline be a __$match__, which matches only documents we need later in the
pipeline.
Example:

```shell
const wellOrderedQuery = () =>{
  print("Running query in a good order")
  const pipeline = [
    { $match: {
      genres: {$in: ["Action"]}, // Action movies only.
      released: {$lte: new ISODate("2002-01-01T00:00:00Z")}}}, // movies before 2002
    { $sort: {"imdb.rating": -1}}, // Sort by imdb rating.
    { $limit: 1}, // Limit to 1 result.
    { $project: { title: 1, genres: 1, released: 1, "imdb.rating":1}},
    ];
  db.movies.aggregate(pipeline).forEach(printjson);
}
wellOrderedQuery();

```

Output will be:

```shell
{
   "_id": ObjectId("5bf142459b72e12b2b1b2cd"),
   "genres": ["Action","Drama"],
   "title": "Men in black 2",
   "released": ISODate("1998-01-01T00:00:00Z"),
   "imdb":{
     "rating": 9.2
   }
}
```

#### Finding Award-Winning Documentary Movies

We need to find a few award-winning documentary movies and then list the movies that have won the most awards

```shell
const findAwardWinningDocumentaries = () =>{
  print("Finding award winning documentary Movies....")
  const pipeline = [
      { $match: {"awards.wins": {$gte: 1}, genres: {$in: ["Documentary"]},
      }},
      { $project: {title: 1, genres:1, awards: 1}},
      { $limit: 5},
      { $sort: {"awards.wins":-1}} // Sort by award wins.
  ];
  const options = {
    maxTimeMS: 3000,
    allowDistUse: true,
    comment: "Find Award Winning Documentary Films"
  }
  db.movies.aggregate(pipeline, options).forEach(printjson);
}
findAwardWinningDocumentaries();
```

Output will be:

```shell
{
     "_id": ObjectId("5bf142459b72e12b2b1b2cd"),
     "genres": ["Action","Documentary"],
     "title": "Cizenfour",
     "awards":{
       "wins": 63,
       "nomination": 30,
       "text": "Nominated for 1 Oscar. Another 62 wins & 30 nominations."
     }
}
....
```

#### EX: Putting Aggregation Into Practice

___
Our aim to design, test, and run an aggregation pipeline that will create unified view. <br>
We should ensure that the final output of the aggregation answers the following business problems:

* For each genre, which movie has the most award nominations, given that they have won at least one of these
  nominations?
* For each of these movies, what is their appended runtime, given that each movie has 12 minutes of trailers before it?
* An example of the sorts of things users are saying about this film.
* Because this is a classic movie marathon, only movies released before 1999 are eligible.
* Across all genres, list all the genres that have the highest number of award wins.

The following steps will help us to complete the task:

1. Filter out any documents that were not released before 1999.
2. Filter out any documents that do not have at least one award win.
3. Sort the documents by awards nominations.
4. Group the documents into a genre.
5. Take the first film in each group.
6. Take the total number of award wins for each group.
7. Join with the __comments__ collection to get a list of comments for each film.
8. Reduce the number of comments for each film to one using projection. (use the __$slice__ operator to reduce array
   length).
9. Append the trailer time of 12 minutes to each film's runtime.
10. Sort our result by the total number of award wins.
11. Impose a limit of 3 documents.

```shell
const findTopAwardWinningByGenre = () =>{
  print("Finding award winning documentary Movies....")
  const pipeline = [
      { $match: 
      {released: {$lte: new ISODate("1999-01-01T00:00:00Z")},"awards.wins": {$gte: 1},
      }},
      { $sort: {"awards.nomination":-1}} // Sort by award nomination.
      { $group: {
          _id: {"$arrayElemAt": ["$genres",0]},
          "film_id": {$first: "$_id"},
          "film_title": {$first: "$title"},
          "film_awards": {$first: "$awards"},
          "film_runtime": {$first: "$runtime"},
          "genre_award_wins": {$sum: "$awards.wins"},
        }},
        {$lookup: {
            from: "comments",
            localField: "film_id",
            foreignField: "movie_id",
            as: "comments"
          }},
      {$project: 
      {
        film_id: 1, 
        film_title:1, 
        film_awards: 1,
        film_runtime: {$add: ["$film_runtime",12]},
        genre_award_wins: 1, 
        "comments": {$slice: ["$comments",1 ]}
      }},
      {sort: {
        "genre_award_wins": -1}},
      { $limit: 3},
  ];
 
  db.movies.aggregate(pipeline).forEach(printjson);
}
findTopAwardWinningByGenre();
```

Output will be as follows:

```shell
{
    "_id": "Drama",
    "film_id":   ObjectId("5bf142459b72e12b2b1b2cd"),
    "film_title": "Almost Famous",
    "film_awards": {
      "wins": 58,
      "nominations": 95,
      "text": "Won 1 Oscar. Another 57 wins & 95 nominations."
    },
    "genre_award_wins": 14021,
    "film_runtime": 134,
    "comments": ["some movie comment"]
}
{
      "_id": "Comedy",
      ...
}
```








