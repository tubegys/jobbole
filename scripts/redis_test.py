#!/home/gys/anaconda3/bin/python
# 脚本功能：测试python连接redis脚本

import redis

conn = redis.StrictRedis()
keys = conn.keys()
for key in keys:
    print(key)


