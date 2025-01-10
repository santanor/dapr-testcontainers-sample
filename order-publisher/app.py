from fastapi import FastAPI, Request
import json
import uvicorn
from dapr.clients import DaprClient

app = FastAPI()

@app.post("/order")
async def publish_order(request: Request):
    order_data = await request.json()
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)