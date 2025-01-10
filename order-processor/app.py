import json
from dapr.clients import DaprClient
from dapr.ext.grpc import App, BindingRequest

app = App()

@app.subscribe(pubsub_name='orders-pubsub', topic='orders')
def orders_subscriber(event: BindingRequest):
    data = json.loads(event.Data())
    print(f"Received order: {data}")

def check_health():
    """Dapr calls this function to check if the service is ready"""
    return True


if __name__ == '__main__':
    app.register_health_check(check_health)
    app.run(50051)