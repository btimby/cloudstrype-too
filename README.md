# cloudstrype-too

Next gen.

# Services

```
+-----+-----+-----------------------------------------------------+-----+-----+
|     |     |                        Auth                         |     |     |
|  R  |  P  +--------------------------+--------------------------+     |     |
|  E  |  G  |           Cloud          |          Array           |     |     |
|  D  |  S  +--------------------------+--------------------------+ API | web |
|  I  |  Q  |                        Chunk                        |     |     |
|  S  |  L  +-----------------------------------------------------+     |     |
|     |     |                     Filesystem                      |     |     |
+-----+-----+-----------------------------------------------------+-----+-----+
```

## Auth

 - User registration
 - User / group management
 - Login
 - Token validation (JWT)
 - Authorization

Notes:

Written using aiohttp & aiopg.sa.

## Array

 - Handles connections from desktop software.
 - Provides simple REST interface for reading / writing chunks.

Notes:

Accepts JWT, validates via auth.
Written in aiohttp & aioredis.
Provides following urls:

POST http://array/<chunk_id>
* Uses user information to locate array member(s), writes chunk member(s). Can
  accept a replica count. Records the association of the chunk_id <-> member(s).
GET http://array/<chunk_id>
* Looks up array members containing given chunk. Reads chunk from available
  member(s) and returns it.


## Cloud

 - Handles OAuth registration of cloud providers.
 - Internal OAuth key management.
 - Provides simple REST interface for reading / writing chunks.

Notes:

Accepts JWT, validates via auth.
Written in aiohttp & aioredis.
Provides following urls:

POST http://cloud/<chunk_id>
* Uses user information to locate cloud storages, writes chunk cloud(s). Can
  accept a replica count. Records the association of the chunk_id <-> cloud(s).
GET http://cloud/<chunk_id>
* Looks up cloud storages containing given chunk. Reads chunk from available
  cloud(s) and returns it.

## Chunk

 - Front-end for Cloud / Array services.
 - Provides simple REST interface for reading / writing chunks.

Notes:

Accepts JWT, validates via auth.
Written in aiohttp & aioredis.
Provides following urls:

POST http://cloud/
* Uses cloud / array services to store a chunk. Generates and returns the chunk
  id. Can accept replica and encryption algorithm. Records location(s) of the
  chunk.

```
POST /
Content-Type: multipart/form-data; boundary="--foo"

--foo
Content-Disposition: name=encryption

aes256-md5

--foo
Content-Disposition: name=durability

raid1(3)

--foo
<chunk_data>
```

GET http://cloud/<chunk_id>
* Looks up chunk location and reads it from cloud / array services.

## Filesystem

 - Provides hierarchial file system on top of chunk system.

Notes:

Accepts JWT, validates via auth.
Written in Django.
Uses model such as:

```python
    class Directory(models.Model):
        name = models.TextField()
        depth = models.IntegerField()

    class File(models.Model):
        name = models.CharField(max_length=200)
        directory = models.ForeignKey(Directory)
```

Provides following URLs:

GET http://filesystem/info?path=/&depth=1
* Builds hierarchy.
GET http://filesystem/info/<file_id>
* Returns metadata for a file.
POST http://filesystem/info/<file_id>
* Saves metadata for a file.
POST http://filesystem/data
* Uploads a file. Accepts parameters as multipart/form-data. Required parameter
  is directory path and file name.
GET http://filesystem/data/<file_id>
* Retrieves file's data.

## API Gateway

nginx exposes various services at a unified url:

 - http://cloudstrype/api/filesystem/ -> http://filesystem/
 - http://cloudstrype/api/array/ -> http://array/
 - http://cloudstrype/api/cloud/ -> http://cloud/
 - http://cloudstrype/api/chunk/ -> http://chunk/
 - http://cloudstrype/api/auth/ -> http://auth/


## Web interface

Jekyll generated site. Static HTML and JS using handlebars, AJAX calls to above
services.
