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






