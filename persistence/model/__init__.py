from abc import ABC, abstractmethod


class AbstractEntity(ABC):
    @property
    @abstractmethod
    def form(self):
        raise NotImplementedError()

    @form.setter
    @abstractmethod
    def form(self, data):
        raise NotImplementedError()

    @abstractmethod
    def update(self, data):
        raise NotImplementedError()

    @abstractmethod
    def validate(self):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def create(data):
        raise NotImplementedError()
