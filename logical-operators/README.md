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
   "cast":"Or hasson",
   "directors":"Rich Parker"
 }
 )
```
2. Second condition to get the movies of drama or crime genres:
```shell
 db.movies.find(
 {
   "cast":"Or hasson",
   "directors":"Rich Parker",
   "$or":[{"genres":"Drama","genres":"Crime"}]
   }
 )
```
3. Next we want only in the title and release year. For this, we will add the projection part:
```shell
 db.movies.find(
 {
   "cast":"Or hasson",
   "directors":"Rich Parker",
   "$or":[{"genres":"Drama","genres":"Crime"}]
   },
   {
     "title": 1, "year": 1, "_id":0
   }
 )
```