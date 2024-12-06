import sys
import pytest

from src.server_side.app.server_app import ServerApp


@pytest.fixture(scope="session")
def server_app() -> ServerApp:
    return ServerApp(sys.argv)


class TestServerApp:

    def test_init_success(self, server_app) -> None:
        """

        """
        assert server_app.init_success()


if __name__ == '__main__':
    pass
