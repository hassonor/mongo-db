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
MongoDB's queries are based on JSOn documents in which you write your criteria in the form of valid documents. 
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





