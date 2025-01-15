import requests
import os

def test_order_publisher(base_publisher_url, redis, publisher_container):
    # We need to "request" the neccesary dependencies from the fixtures declared in conftest.py

    # First we check that there's nothing in the stream. We don't ever expect this to 
    # fail, and although it's redundant, it's here to prove a point for this sample
    client = redis.get_client()
    streams={'orders': '0'}
    result = client.xread(streams, count=1)
    assert len(result) == 0

    # And now we can run the test and check that something has been written to Redis
    requests.post(f"{base_publisher_url}/order", json={"order_id": "1", "item": "item1"})
    result = client.xread(streams, count=1)
    assert len(result) == 1
