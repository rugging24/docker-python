from abc import ABC, abstractmethod
import pathlib
from typing import Any, Dict, List, Optional
from docker.client import DockerClient
from testcompose.models.container import ContainerParam
from testcompose.models.volume import VolumeMapping
from docker.errors import ImageNotFound
from testcompose.models.volume import VolumeSourceTypes


class ContainerBuilder(ABC):
    """Container Builder

    Args:
        ABC ([type]):
    """

    def __init__(self, container_param: ContainerParam) -> None:
        self._environments: Dict[str, Any] = dict()
        self._ports: Dict[int, Any] = dict()
        self._volumes: Dict[str, Dict[str, str]] = dict()
        self._docker_host: Optional[str] = None
        self.generic_container_param = container_param

    @property
    def generic_container_param(self) -> ContainerParam:
        """Container parameter

        Returns:
            ContainerParam: parameter model
        """
        return self._container_param

    @generic_container_param.setter
    def generic_container_param(self, param: ContainerParam) -> None:
        self._container_param = param

    @property
    def docker_client(self) -> DockerClient:
        """Docker Client

        Returns:
            DockerClient: client object
        """
        return self._docker_client

    @docker_client.setter
    def docker_client(self, client: DockerClient):
        self._docker_client = client

    def with_exposed_ports(self, ports: Optional[List[str]]):
        """List of exposed port to be assigned random port
        numbers on the host. Random ports are exposed to the
        host. A fixed port can be assigned on the host by providing
        the port in the format **[host_port:container_port]**

        Args:
            ports (Optional[List[str]]): list of container exposed ports
        """
        if ports:
            for port in ports:
                _ports = str(port).split(":")
                if len(_ports) == 2:
                    self._ports[int(_ports[1])] = int(_ports[0])
                else:
                    self._ports[int(port)] = None

    def with_volumes(self, volumes: Optional[List[VolumeMapping]]) -> None:
        """A list of volume mappings to be mounted in the container.

            VolumeMapping:
                host: host volume path or a docker volume name
                container: path to mount the host volume in the container
                mode: volume mode [ro|rw]
                source: source of the volume [local|docker]
                        local: a file or directory to be mounted
                        docker: a docker volume (existing or to be created)

        Args:
            volumes (Optional[List[VolumeMapping]]): Optional list of volumes to mount on the container
        """
        if volumes:
            for vol in volumes:
                host_bind: Optional[str] = None
                if vol.source == VolumeSourceTypes.DOCKER_SOURCE:
                    host_bind = vol.host
                elif vol.source == VolumeSourceTypes.LOCAL_SOURCE:
                    host_bind = str(pathlib.Path(vol.host).absolute())
                if not host_bind:
                    raise ValueError("Volume source can only be one of local|docker")
                self._volumes[host_bind] = {"bind": vol.container, "mode": vol.mode}

    def with_environment(self, env: Optional[Dict[str, Any]]):
        """Environment variables for running containers

        Args:
            env (Optional[Dict[str, Any]]): [description]
        """
        if env:
            for k, v in env.items():
                self._environments[k] = v

    def pull_image(self, image_pull_policy="Always_Pull"):
        """Pull image of registry
        Pull polic can be one of the following:

            image_pull_policy:
                - Always_Pull [default]
                - Never

        Args:
            image_pull_policy (str, optional): Image pull policy for the test.
        """
        # TODO: Allow pull toggle
        try:
            self.docker_client.images.get(name=self.generic_container_param.image)
        except ImageNotFound:
            self.docker_client.images.pull(repository=self.generic_container_param.image)

    def build(self, docker_client: DockerClient) -> None:
        """Container parameters

        Args:
            docker_client (DockerClient): docker client
        """
        self.docker_client = docker_client
        self.with_environment(self._container_param.environment_variables)
        self.with_volumes(self._container_param.volumes)
        self.with_exposed_ports(self._container_param.exposed_ports)
        if self.generic_container_param.registry_login_param.username:
            login = self.docker_client.login(**self.generic_container_param.registry_login_param.dict())
            print(login)
        print(f"Pulling image {self.generic_container_param.image}")
        self.pull_image()

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def stop(self):
        ...
