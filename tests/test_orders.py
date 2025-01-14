import requests
import os

def test_order_publisher(base_publisher_url, redis, publisher_container):
    client = redis.get_client()
    streams={'orders': '0'}
    result = client.xread(streams, count=1)
    assert len(result) == 0

    requests.post(f"{base_publisher_url}/order", json={"order_id": "1", "item": "item1"})
    result = client.xread(streams, count=1)
    assert len(result) == 1
