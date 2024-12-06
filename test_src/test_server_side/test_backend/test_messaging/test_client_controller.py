import pytest
from unittest.mock import patch

from src.server_side.backend.messaging.client_controller import ClientController


@pytest.fixture
def client_con_fix() -> ClientController:
    client_con_fix = ClientController()
    return client_con_fix


def test_ensure_singleton(client_con_fix: ClientController) -> None:
    """

    """
    client_con_2 = ClientController()
    assert client_con_fix is client_con_2


class TestClientController:

    @pytest.mark.parametrize("error", [RuntimeError, None])
    def test_start_client(self, client_con_fix: ClientController, error: bool) -> None:
        """

        """
        with patch.object(client_con_fix._process, "start") as patch_start:
            patch_start.side_effect = error
            client_con_fix.start_client()
            patch_start.assert_called()

    @pytest.mark.parametrize("alive", [True, False])
    def test_stop_client(self, client_con_fix: ClientController, alive: bool) -> None:
        """

        """
        with patch.object(client_con_fix._process, "is_alive") as patch_alive:
            with patch.object(client_con_fix._process, "terminate") as patch_terminate:
                with patch.object(client_con_fix._process, "join") as patch_join:
                    patch_alive.return_value = alive
                    client_con_fix.stop_client()
                    if patch_alive.return_value:
                        patch_terminate.assert_called()
                        patch_join.assert_called()
                    else:
                        patch_terminate.assert_not_called()
                        patch_join.assert_not_called()


if __name__ == "__main__":
    pass
