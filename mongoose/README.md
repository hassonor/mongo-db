### Schema
___
#### Defining our Schema
```javascript
import mongoose from 'mongoose';
const { Schema } = mongoose;

const blogSchema = new Schema({
  title:  String, // String is shorthand for {type: String}
  author: String,
  body:   String,
  comments: [{ body: String, date: Date }],
  date: { type: Date, default: Date.now },
  hidden: Boolean,
  meta: {
    votes: Number,
    favs:  Number
  }
});
```

Permitted Schema Types are:
The permitted SchemaTypes are:
* String
* Number
* Date
* Buffer
* Boolean
* Mixed
* ObjectId
* Array
* Decimal128
* Map

By default, Mongoose adds an **_id** property to your schemas.
```javascript
const Model = mongoose.model('Test', schema);

const doc = new Model();
doc._id instanceof mongoose.Types.ObjectId; // true
```

#### Virtuals
Virtuals are document properties that you can get and set but that do not get persisted to MongoDB. The getters are useful for formatting or combining fields, while setters are useful for de-composing 
a single value into multiple values for storage.
```javascript
// define a schema
const personSchema = new Schema({
  name: {
    first: String,
    last: String
  }
});

// compile our model
const Person = mongoose.model('Person', personSchema);

// create a document
const axl = new Person({
  name: { first: 'Or', last: 'Hasson' }
});
```
Suppose We want to print out the person's full name. We could do it ourselves: <br>
```javascript
console.log(axl.name.first + ' ' + axl.name.last); // Or Hasson
```
A virtual property getter lets you define a fullName property that won't get persisted to MongoDB.
```javascript
personSchema.virtual('fullName').get(function() {
  return this.name.first + ' ' + this.name.last;
});
```

Now, mongoose will call your getter function every time you access the `fullName` property:
```javascript
console.log(axl.fullName); // Or Hasson
```

### SchemaType
___
#### What is SchemaType?
You can think of a Mongoose schema as the configuration object for a Mongoose model. 
A SchemaType is then a configuration object for an individual property. 
A SchemaType says what type a given path should have, 
whether it has any getters/setters, and what values are valid for that path.
```javascript
const schema = new Schema({ name: String });
schema.path('name') instanceof mongoose.SchemaType; // true
schema.path('name') instanceof mongoose.Schema.Types.String; // true
schema.path('name').instance; // 'String'
```
A SchemaType is different from a type. In other words,`mongoose.ObjectId !== mongoose.Types.ObjectId`.
A SchemaType is just a configuration object for Mongoose. An instance of the `mongoose.ObjectId`
SchemaType doesn't actually create MongoDB ObjectIds, it is just a configuration for a path in a schema.

#### Example
```javascript
const schema = new Schema({
  name:    String,
  binary:  Buffer,
  living:  Boolean,
  updated: { type: Date, default: Date.now },
  age:     { type: Number, min: 18, max: 65 },
  mixed:   Schema.Types.Mixed,
  _someId: Schema.Types.ObjectId,
  decimal: Schema.Types.Decimal128,
  array: [],
  ofString: [String],
  ofNumber: [Number],
  ofDates: [Date],
  ofBuffer: [Buffer],
  ofBoolean: [Boolean],
  ofMixed: [Schema.Types.Mixed],
  ofObjectId: [Schema.Types.ObjectId],
  ofArrays: [[]],
  ofArrayOfNumbers: [[Number]],
  nested: {
    stuff: { type: String, lowercase: true, trim: true }
  },
  map: Map,
  mapOfString: {
    type: Map,
    of: String
  }
})

// example use

const Thing = mongoose.model('Thing', schema);

const m = new Thing;
m.name = 'Statue of Liberty';
m.age = 125;
m.updated = new Date;
m.binary = Buffer.alloc(0);
m.living = false;
m.mixed = { any: { thing: 'i want' } };
m.markModified('mixed');
m._someId = new mongoose.Types.ObjectId;
m.array.push(1);
m.ofString.push("strings!");
m.ofNumber.unshift(1,2,3,4);
m.ofDates.addToSet(new Date);
m.ofBuffer.pop();
m.ofMixed = [1, [], 'three', { four: 5 }];
m.nested.stuff = 'good';
m.map = new Map([['key', 'value']]);
m.save(callback);
```

#### The `type` Key
`type` is a special property in Mongoose schemas. When Mongoose finds a nested property named `type` in your schema,
Mongoose assumes that it needs to define a SchemaType with the given type.
```javascript
// 3 string SchemaTypes: 'name', 'nested.firstName', 'nested.lastName'
const schema = new Schema({
  name: { type: String },
  nested: {
    firstName: { type: String },
    lastName: { type: String }
  }
});
```
When Mongoose sees type: String, it assumes that you mean asset should be a string, not an object with a property type. 
The correct way to define an object with a property type is shown below.
```javascript
const holdingSchema = new Schema({
  asset: {
    // Workaround to make sure Mongoose knows `asset` is an object
    // and `asset.type` is a string, rather than thinking `asset`
    // is a string.
    type: { type: String },
    ticker: String
  }
});
```

#### SchemaType Options


