import docker
from .base_client import BaseClient
from testcompose.models.client import ClientFromEnv


class EnvClient(BaseClient):
    def __init__(self, client_param: ClientFromEnv) -> None:
        """Client environment parameters

        Args:
            client_param (ClientFromEnv): model class consisting of parameters for client connections with environment variables
        """
        super(EnvClient, self).__init__()
        self._version = client_param.version
        self._timeout = client_param.timeout or BaseClient.max_timeout
        self._max_pool_size = client_param.max_pool_size or BaseClient.max_pool_size
        self._use_ssh_client = client_param.use_ssh_client
        self._ssl_version = client_param.ssl_version
        self._assert_hostname = client_param.assert_hostname
        self._environment = client_param.environment

        # self.docker_client = self.initialise_client()

    def initialise_client(self) -> None:
        """Init docker client

        Returns:
            DockerClient: docker client
        """
        self.docker_client = docker.from_env(
            version=self._version,
            timeout=self._timeout,
            max_pool_size=self._max_pool_size,
            use_ssh_client=self._use_ssh_client,
            ssl_version=self._ssl_version,
            assert_hostname=self._assert_hostname,
            environment=self._environment,
        )
