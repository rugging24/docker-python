from docker.errors import APIError
from docker.client import DockerClient


def is_container_still_running(docker_client: DockerClient, container_id: str) -> bool:
    try:
        return bool(docker_client.containers.get(container_id).short_id)
    except APIError:
        return False
