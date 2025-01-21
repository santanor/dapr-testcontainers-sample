import requests
import os
from testcontainers.core.waiting_utils import wait_for_logs

def test_order_publisher(base_publisher_url, redis, publisher_container):
    # We need to "request" the neccesary dependencies from the fixtures declared in conftest.py
    # First we check that there's nothing in the stream. We don't ever expect this to 
    # fail, and although it's redundant, it's here to prove a point for this sample
    client = redis.get_client()
    streams={'orders': '0'}
    result = client.xread(streams, count=1)
    assert len(result) == 0

    # And now we can run the test and check that something has been written to Redis
    response = requests.post(f"{base_publisher_url}/order", json={"order_id": "1", "item": "item1"})
    assert response.status_code == 200

    result = client.xread(streams, count=1)
    assert len(result) == 1

def test_order_publisher_processor(base_publisher_url, redis, publisher_container, processor_container):
    # To simplify this sample, we won't be testing the publisher side of things, we'll simply fire a request 
    # at the publisher and test that the processor has received the message

    response = requests.post(f"{base_publisher_url}/order", json={"order_id": "1", "item": "item1"})
    assert response.status_code == 200

    # For this sample we'll just wait for the log to indicate that the processor has received the message
    wait_for_logs(processor_container, "Received order: {\"order_id\": \"1\", \"item\": \"item1\"}")

    # If the log is found, the test passes
    assert True