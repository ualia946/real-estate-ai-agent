from abc import ABC, abstractmethod

from src.core.domain.entity.property import Property
from src.core.ports.evaluator_port import EvaluationResult


class INotifierPort(ABC):
    """
    Port interface for alerting the user about opportunities.
    """

    @abstractmethod
    def send_opportunity_alert(self, property: Property, evaluation: EvaluationResult) -> None:
        """
        Sends a notification (e.g., via Telegram) detailing a highly-rated property.

        Args:
            property: The property domain entity that triggered the alert.
            evaluation: The AI evaluation result containing the score and reasoning.
        """
        pass

