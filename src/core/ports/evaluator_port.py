from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from src.core.domain.entity.property import Property


@dataclass(frozen=True)
class MathValuation:
    """Result of the deterministic math homogenization phase."""
    math_score: float
    confidence_mad: float
    rent_yield: float


@dataclass(frozen=True)
class EvaluationResult:
    """Final outcome after both Math and LLM filtering."""
    math_valuation: MathValuation
    final_score: float
    red_flags: list[str] = field(default_factory=list)
    qualitative_adjustment: float = 0.0
    llm_reasoning: str = ""
    is_opportunity: bool = False


class IEvaluatorPort(ABC):
    """
    Port interface for evaluating properties in a two-stage process:
    1. Mathematical Homogenization
    2. Qualitative LLM Judgment
    """

    @abstractmethod
    def calculate_math_valuation(
        self, target: Property, active_comparables: list[Property]
    ) -> MathValuation:
        """
        Applies elasticity and coefficients to calculate the raw score and confidence.
        """
        pass

    @abstractmethod
    def judge_qualitative_factors(
        self, target: Property, math_val: MathValuation
    ) -> EvaluationResult:
        """
        Passes the property prose to the LLM to find red flags and apply qualitative adjustments.
        """
        pass
