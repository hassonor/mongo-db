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
