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
the client just keeps on waiting. After a certain threshold value for waiting is reached, the connection between the client and 
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
The MongoDB cursor provides the __skip()__ function, which accepts an integer and skips the specified number of documents
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
Another example, The next query should return 50 movies where the movie with the highest IMDb rating appearing at the top.
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
    
    const findMoviesByGenre = function(genre, pageNumber, pageSize) {
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
