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