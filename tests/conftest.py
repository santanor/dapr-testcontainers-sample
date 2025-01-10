import os
from concurrent.futures import ThreadPoolExecutor, wait

import pytest
from testcontainers.core.container import DockerContainer
from testcontainers.core.image import DockerImage
from testcontainers.core.network import Network
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.redis import RedisContainer

# These are the image names to be used in the tests
publisher_base = "publisher:latest"
processor_base = "processor:latest"
publisher = "publisher:integration"
processor = "processor:integration"


@pytest.fixture
def base_publisher_url():
    return "http://localhost:8000"


@pytest.fixture(scope="session", autouse=True)
def images(request):
    # Build the images in parallel to save time
    def create_docker_image(path: str, tag: str) -> DockerImage:
        return DockerImage(path=path, tag=tag).build()

    # Build the base images as they'd be deployed in production
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(create_docker_image, "../order-processor", processor_base),
            executor.submit(create_docker_image, "../order-publisher", publisher_base),
        ]
        wait(futures)

    # This uses the base images and extends them to include test-specific dependencies. In this case... just Dapr
    # but it could also include other things such as az cli or test volumes for sample payloads
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(create_docker_image, "docker-images/order-processor", processor),
            executor.submit(create_docker_image, "docker-images/order-publisher", publisher),
        ]
        wait(futures)


@pytest.fixture
def containers(images):
    # This function structure showcases the workflow of the test containers. We can see how the dependencies are passed
    # "top down" with the network at the root. When the execution finishes this entire stack of nested 'withs' will
    # unravel and free up resources in order, essentially cleaning up the test environment for a new run.
    with Network() as network:
        with (RedisContainer(image="redis:7.4.2-alpine").with_network(network).with_name("redis").with_bind_ports(6379, 6380)) as redis_container:
            with (DockerContainer(publisher).with_network(network).with_name(publisher).with_bind_ports(8000,8000)) as publisher_container:
                with (DockerContainer(processor).with_network(network).with_name(processor)) as processor_container:
                    yield {
                        "redis": redis_container,
                        "publisher": publisher_container,
                        "processor": processor_container
                    }


