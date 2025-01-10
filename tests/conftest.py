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

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(create_docker_image, "../order-processor", processor_base),
            executor.submit(create_docker_image, "../order-publisher", publisher_base),
        ]
        wait(futures)

def containers():
    with Network() as network:
        with (
            RedisContainer(image="redis:7.4.1-bookworm")
            .with_network(network)
            .with_bind_ports(6379, 6380) as redis_container
        ):
            yield redis_container
