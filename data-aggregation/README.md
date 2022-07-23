### Data Aggregation
___
There are two parameters used for aggregation. The **pipeline** parameter contains all the logic to find, sort,project,limit,transform, 
and aggregate our data. <br>
The **pipeline** parameter itself is passed in as array of JSON documents.<br>
The second parameter is the __options'__ parameter. This is optional and allows us to specify the details of the configuration, such as how the aggregation should execute or some flags that are required during debugging and building our pipelines.<br>

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
    { $sort: {"imdb.rating": -1}} // Sort by IMDB rating.
    { $match: {
      geres: {$in: ["Action"]}, //Action movies only
      released: {$lte: new ISODate("2000-01-01T00:00:00Z")} //Movies Before 2000-01-01
    }},
        { $limit: 3 }, // Limit to 3 results.
        { $project: genres: 1, released: 1, "imdb.rating": 1} //  (Last Stage)
   ]
 }
findTopActionMovies();
```
