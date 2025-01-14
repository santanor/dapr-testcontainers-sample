import requests
import os

def test_order_publisher(base_publisher_url, redis, publisher):
    client = redis.get_client()
    result = client.xread("{orders}", 0)
    assert(len(result), 0)



    pass
