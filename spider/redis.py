import redis

redis_host = '127.0.0.1'
redis_port = 6379
redis_db = 1
redis_pwd = ''
redisConnect = redis.Redis(redis_host, redis_port, redis_db, redis_pwd)
