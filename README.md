<p align="center" style="margin: 0 0 10px">
  <img width="350" height="208" src="https://github.com/rugging24/python-testcompose/blob/main/docs/images/testcompose.png" alt='Testcompose'>
</p>

<h1 align="center" style="font-size: 3rem; margin: -15px 0">
Testcompose
</h1>

<p align="center"><strong>Testcompose</strong> <em>- A clean and better way to test your Python containerized applications.</em></p>

<p align="center">
<a href="https://github.com/rugging24/python-testcompose/actions">
    <img src="https://github.com/rugging24/python-testcompose/workflows/RunningTests/badge.svg" alt="RunningTests">
</a>
<a href="https://pypi.org/project/testcompose/">
    <img src="https://badge.fury.io/py/testcompose.svg" alt="Testcompose version">
</a>
</p>

---

**Testcompose** provides an easy way of using docker containers for functional and integration testing. It allows for combination of more than one containers and allows for interactions with these containers from your test code without having to write extra scripts for such interactions. I.e providing a docke compose kind of functionality with the extra benefit of being abale to fully control the containers from test codes.

This is inspired by the  [testcontainers-python](https://testcontainers-python.readthedocs.io/en/latest/index.html#) project and goes further to add a few additional functionality to imporve software integration testing while allowing the engineer control every aspect of the test.

---

Install testcompose using pip:

```shell
$ pip install testcompose
```

testcompose requires Python 3.7+.

Using a config file. See the [Quickstart](https://github.com/rugging24/python-testcompose/blob/main/docs/quickstart.md) for other options

```yaml
network:
  name: some_network_name
  auto_create: False
  use_random_network: True
services:
  - name: db1
    image: "postgres:13"
    auto_remove: True
    command: ""
    environment:
      POSTGRES_USER: postgres
      POSTGRES_DB: postgres
      POSTGRES_PASSWORD: a
    exposed_ports:
      - 5432
    volumes:
      - host: "data_volume"
        container: "/data"
        mode: "rw"
        source: "docker" # possible values are `docker` or `local`
    log_wait_parameters:
      log_line_regex: "database system is ready to accept connections"
      wait_timeout: 30
      poll_interval: 2
```

Verify it as follows:

```python
from testcompose.parse_config import TestConfigParser
from testcompose.configs.service_config import Config
from testcompose.run_containers import RunContainers

my_test_service = TestConfigParser.parse_config(
    file_name='some-file-name'
)
my_config =  Config(test_services=my_test_service)
print(my_config.ranked_itest_config_services)

with RunContainers(
        services=running_config.ranked_itest_config_services
) as runner:
    # Interract with the running containers

    assert runner.containers

    # Use some special parameters of the running containers

    app_container = runner.extra_envs["app_container_config_name"]

    # Get the host port a certain exposed container port is mapped to
    mapped_port = app_container.get("DOCKER_PYTHON_MAPPED_PORTS", {}).get("port")

    # where `port` is the exposed port of the container


```


## Documentation

[Quickstart](https://github.com/rugging24/python-testcompose/blob/main/docs/quickstart.md)

[Special-Variables](https://github.com/rugging24/python-testcompose/blob/main/docs/environment_variables.md)

[Full-Doc](https://rugging24.github.io/python-testcompose/)
