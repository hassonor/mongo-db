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
