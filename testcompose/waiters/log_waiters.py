from datetime import datetime
from logging import Logger
import re
from time import sleep
from typing import Optional, Match
from docker.models.containers import Container
from testcompose.models.bootstrap.container_log_wait_parameter import ContainerLogWaitParameter
from testcompose.log_setup import stream_logger
from testcompose.waiters.waiting_utils import is_container_still_running
from docker.client import DockerClient


logger: Logger = stream_logger(__name__)


class LogWaiter:
    @staticmethod
    def search_container_logs(
        docker_client: DockerClient, container: Container, log_parameter: ContainerLogWaitParameter
    ) -> None:
        """Search for a given predicate in the container log. Useful to check if a
        container is running and healthy

        Args:
            search_string (str): predicate to search in the log
            timeout (float, optional): Defaults to 300.0.
            interval (int, optional): Defaults to 1.

        Raises:
            ValueError: if a non string predicate is passed

        Returns:
            bool: True if the log contains the provided predicate
        """
        if not log_parameter:
            return

        if not isinstance(log_parameter.log_line_regex, str):
            raise ValueError

        prog = re.compile(log_parameter.log_line_regex, re.MULTILINE).search
        start: datetime = datetime.now()
        output: Optional[Match[str]] = None
        while (datetime.now() - start).total_seconds() < (log_parameter.wait_timeout_ms / 1000):
            if not is_container_still_running(docker_client, container.id):  # type: ignore
                return
            output = prog(container.logs().decode())
            if output:
                return
            if (datetime.now() - start).total_seconds() > (log_parameter.wait_timeout_ms / 1000):
                raise TimeoutError(
                    "container %s did not emit logs satisfying predicate in %.3f seconds"
                    % (container.name, float(log_parameter.wait_timeout_ms or 60000))
                )
            sleep(log_parameter.poll_interval_ms / 1000)
        logger.info(container.logs().decode())
