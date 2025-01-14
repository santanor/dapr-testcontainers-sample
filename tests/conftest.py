import pytest
from testcontainers.core.container import DockerContainer
from testcontainers.core.image import DockerImage
from testcontainers.core.network import Network
from testcontainers.redis import RedisContainer

# These are the image names to be used in the tests
publisher_base = "publisher:latest"
processor_base = "processor:latest"
publisher = "publisher:integration"
processor = "processor:integration"
dapr = "dapr:integration"

@pytest.fixture
def base_publisher_url():
    return "http://localhost:8000"

@pytest.fixture(scope="session", autouse=True)
def images():
    def create_docker_image(path: str, tag: str) -> DockerImage:
        return DockerImage(path=path, tag=tag).build()

    # Build the base images as they'd be deployed in production
    create_docker_image("./order-processor", processor_base)
    create_docker_image("./order-publisher", publisher_base)
 
    # This uses the base images and extends them to include test-specific dependencies. In this case... just Dapr
    # but it could also include other things such as az cli or test volumes for sample payloads
    create_docker_image("./tests/docker-images/dapr", dapr)
    create_docker_image("./tests/docker-images/order-processor", processor)
    create_docker_image("./tests/docker-images/order-publisher", publisher)
    


@pytest.fixture(scope="function") 
def network():
    with Network() as network:
        yield network

@pytest.fixture(scope="function")
def redis(network):
    with (RedisContainer(image="redis:7.4.2-alpine").with_network(network).with_name("redis").with_bind_ports(6379, 6380)) as redis_container:
        yield redis_container

@pytest.fixture(scope="function")
def processor_container(network):
    with (DockerContainer(processor).with_network(network).with_name("processor")) as processor_container:
        yield processor_container


@pytest.fixture(scope="function")
def publisher_container(network):
    with (DockerContainer(publisher).with_network(network).with_name("publisher")) as publisher_container:
        yield publisher_container




# This pseudo code aims to showcase the order in which containers are created and used. Here we can see how the 
# network is created first, then redis and then both applications. Once the tests are finished the cleanup happens
# automatically (thanks to the 'with') but in reverse, first the apps, then Redis and lastly the network. 
# 
# We can also see how the network is passed down to every container so that they're all isolated from the local environment
# @pytest.fixture(scope="function")
# def containers(request, images):
#     with Network() as network:
#         with (RedisContainer(image="redis:7.4.2-alpine").with_network(network) as redis_container:
#             with (DockerContainer(publisher).with_network(network) as publisher_container:
#                 with (DockerContainer(processor).with_network(network) as processor_container:
#                     yield {
#                         "redis": redis_container,
#                         "publisher": publisher_container,
#                         "processor": processor_container
#                     }












