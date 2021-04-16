# Amazon S3

## Bacis

### Buckets

__A bucket is a container for objects stored in Amazon S3.__ Every object is contained in a bucket. For example, if the object named `photos/puppy.jpg` is stored in the `awsexamplebucket1 bucket` in the US West (Oregon) Region, then it is addressable using the URL `https://awsexamplebucket1.s3.us-west-2.amazonaws.com/photos/puppy.jpg`.

数据桶的概念与形式。

### Objects

__Objects are the fundamental entities stored in Amazon S3.__ Objects consist of object data and metadata. The data portion is opaque to Amazon S3. __`The metadata is a set of name-value pairs that describe the object`. These include some default metadata, such as the date last modified, and standard HTTP metadata, such as Content-Type. You can also specify custom metadata at the time the object is stored.__

`An object is uniquely identified within a bucket by a key (name) and a version ID.`

对象及对象信息。

### keys

`A key is the unique identifier for an object within a bucket.` Every object in a bucket has exactly one key. __The combination of a `bucket`, `key`, and `version ID` uniquely identify each object.__ 

So you can think of Amazon S3 as a basic data map between "bucket + key + version" and the object itself. Every object in Amazon S3 can be uniquely addressed through the combination of the web service endpoint, bucket name, key, and optionally, a version. For example, in the URL https://doc.s3.amazonaws.com/2006-03-01/AmazonS3.wsdl, "doc" is the name of the bucket and "2006-03-01/AmazonS3.wsdl" is the key.

键的构成与含义。

### Regions

选择数据存储的区域。不同区域的数据并不共享。


### Amazon S3 data consistency model

数据一致性。

__Amazon S3 does not support object locking for concurrent writers.__ If two PUT requests are simultaneously made to the same key, the request with the latest timestamp wins. If this is an issue, you will need to build an object-locking mechanism into your application

__Updates are key-based.__ There is no way to make atomic updates across keys. For example, you cannot make the update of one key dependent on the update of another key unless you design this functionality into your application.


## Metadata

You can set object metadata in Amazon S3 at the time you upload the object. Object metadata is a set of name-value pairs. After you upload the object, you cannot modify object metadata. The only way to modify object metadata is to make a copy of the object and set the metadata.


### System-defined object metadata

1. Metadata such as object creation date is system controlled, where only Amazon S3 can modify the value.

### User-defined object metadata

When uploading an object, you can also assign metadata to the object. __You provide this optional information as a name-value (key-value) pair when you send a PUT or POST request to create the object. When you upload objects using the REST API, the optional user-defined metadata names must begin with `"x-amz-meta-"` to distinguish them from other HTTP headers. When you retrieve the object using the REST API, this prefix is returned.__

 


























