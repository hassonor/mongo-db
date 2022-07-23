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
The most basic implementation of a __$group__ stage accepts only an **_id** key, with the value being an expression. <br>
For example, the folliwng code will group all movies by their rating, outputting a single record for each rating category:
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
 }

```

