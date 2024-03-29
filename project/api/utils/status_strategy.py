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

    def execute_filtering(self, user_type, id) -> list:
        result = self._strategy.filter_status(user_type, id)
        return result


class Strategy(ABC):
    @abstractmethod
    def filter_status(self, user_type, id):
        pass


class InitiatedStrategy(Strategy):
    def filter_status(self, user_type, id) -> list:
        pax = utils.filter_by_status('I', user_type, id)
        return pax


class CanceledStrategy(Strategy):
    def filter_status(self, user_type, id) -> list:
        pax = utils.filter_by_status('C', user_type, id)
        return pax


class PendentStrategy(Strategy):
    def filter_status(self, user_type, id) -> list:
        pax = utils.filter_by_status('P', user_type, id)
        return pax


class FinalizedStrategy(Strategy):
    def filter_status(self, user_type, id) -> list:
        pax = utils.filter_by_status('F', user_type, id)
        return pax
