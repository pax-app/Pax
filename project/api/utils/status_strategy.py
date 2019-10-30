from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from project.api.utils.creation_utils import Utils
from project.api.models import Pax

utils = Utils()


class Context():
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def execute_filtering(self, id) -> list:
        result = self._strategy.filter_status(id)
        return result


class Strategy(ABC):
    @abstractmethod
    def filter_status(self, id):
        pass


class InitiatedStrategy(Strategy):
    def filter_status(self, user_type, id) -> list:
        pax = utils.filter_by_status('I', self.user_type, self.id)
        return pax


class CanceledStrategy(Strategy):
    def filter_status(self, user_type, id) -> list:
        pax = utils.filter_by_status('C', self.user_type, self.id)
        return pax


class PendentStrategy(Strategy):
    def filter_status(self, user_type, id) -> list:
        pax = utils.filter_by_status('P', self.user_type, self.id)
        return pax


class FinalizedStrategy(Strategy):
    def filter_status(self, user_type, id) -> list:
        pax = utils.filter_by_status('F', self.user_type, self.id)
        return pax
