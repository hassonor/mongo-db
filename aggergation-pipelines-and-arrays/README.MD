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