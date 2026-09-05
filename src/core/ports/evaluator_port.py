from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.domain.entity.property import Property


@dataclass(frozen=True)
class EvaluationResult:
    """DTO/Value Object representing the outcome of an AI evaluation."""

    score: float  # e.g., 0.0 to 10.0
    reasoning: str  # AI explanation of why it gave this score
    is_opportunity: bool


class IEvaluatorPort(ABC):
    """
    Port interface for evaluating the profitability of a property.
    """

    @abstractmethod
    def evaluate_property(
        self, target: Property, market_comparables: list[Property]
    ) -> EvaluationResult:
        """
        Evaluates a property against similar properties to determine if it's a good
        deal.

        Args:
            target: The property to evaluate.
            market_comparables: A list of similar properties in the same area to use
                as a baseline.

        Returns:
            An EvaluationResult containing the score and reasoning.
        """
        pass
