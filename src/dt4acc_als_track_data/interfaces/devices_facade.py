from abc import ABCMeta, abstractmethod


class DevicesFacadeInterface(metaclass=ABCMeta):
    @abstractmethod
    def get(self, name: str):
        """
        Args:
            * name: the name of the device

        returns the device needed
        """
        raise NotImplementedError
