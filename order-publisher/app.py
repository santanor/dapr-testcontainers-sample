from fastapi import FastAPI, Request
import json
from dapr.clients import DaprClient

app = FastAPI()

@app.post("/order")
async def publish_order(request: Request):
    order_data = await request.json()

    # Starting the client here uses the default values and the ones in the environment to 
    # create the client, Therefore there's no extra config here.
    with DaprClient() as client:
        client.publish_event(
            pubsub_name='orders-pubsub',
            topic_name='orders',
            data=json.dumps(order_data),
        )
    return {"status": "Order published"}


@app.post("/healthz")
def check_health():
    """Dapr calls this function to check if the service is ready"""
    return {"status": "healthy"}
