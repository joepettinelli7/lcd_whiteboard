import traceback
from multiprocessing import Process

from src.client_side.client_app import client_process_target


def ensure_singleton(cls):
    """
    Decorator to ensure that the client controller
    is a singleton. Should make running the multiprocessing
    module without if __name__ == "__main__" guard safer

    Args:
        cls: The class of object wrapped

    Returns:
        Original ClientController instance
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@ensure_singleton
class ClientController:
    """
    Used to control the Client process / app.
    Not best practice to start this process outside
    an if __name__ == "__main__" guard

    """

    def __init__(self) -> None:
        super().__init__()
        self._process: Process = Process(target=client_process_target)

    def start_client(self) -> None:
        """
        Client app started after server app starts.

        Returns:

        """
        try:
            # spawn process
            self._process.start()
        except RuntimeError:
            traceback.print_exc()

    def stop_client(self) -> None:
        """
        Stop the client app

        Returns:

        """
        if self._process.is_alive():
            # Nothing to handle in client process
            self._process.terminate()
            self._process.join()
        else:
            pass


if __name__ == "__main__":
    pass
