# Redis_Clone
RESTful APIs using Django were built to replicate some Redis commands like GET, SET, ZADD, ZRANK, EXPIRE, ZRANGE. An in-memory data structure was created to efficiently store the caching information. 

For SET use POST /redis/, in request.form enter command=SET, key=<given_key>, value=<given_value>.

For GET use GET /redis/, in request params enter command=GET, key=<given_key>.

For EXPIRE use POST /redis/expire/, in request.form enter command=EXPIRE, key=<given_key>, timeout=<given_seconds>.

For ZADD use POST /redis/zadd/, in request.form enter command=ZADD, key=<given_key>, value=<given_value>, Eg- value=1 uno 1 one.

For ZRANK use GET /redis/zrank/, in request params enter command=ZRANK, key=<given_key>, value=<given_value>, Eg- value=uno.

For ZRANGE use GET /redis/zrange/, in request params enter command=ZRANGE, key=<given_key>, start=<given_start>, stop=<given_stop>, Eg- start=0 , stop=2, optionally you can add withscores=1 in request params to get the result with scores.

To clear the cache use GET /redis/clear/.
