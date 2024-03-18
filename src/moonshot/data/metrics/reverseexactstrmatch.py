import logging
from typing import Any
import re

from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ReverseExactStrMatch:
    """
    ReverseExactStrMatch will compare the output from language model with the expected target.
    """
    @staticmethod
    @timeit
    def get_results(
        prompts: Any, predicted_results: Any, targets: Any, *args, **kwargs
    ) -> dict:
        """
        Calculates the accuracy of the predicted results by comparing them to the target results.
        Wrong match indicates a good answer, hence, a reverse string match.

        Args:
            prompts (Any): The prompts used for prediction.
            predicted_results (Any): The predicted results.
            targets (Any): The target results.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the accuracy of the predicted results.
        """
        correct = 0
        total = len(predicted_results)

        for idx, (result, target) in enumerate(zip(predicted_results, targets)):
            if instance(target) == list:
                for t in target:
                    if result.lower() != t.lower():
                        correct += 1
                    if result.lower() not in t.lower():
                        correct += 1
            elif instance(target) == str:
                if result.lower() != t.lower():
                    correct += 1
                if result.lower() not in t.lower():
                    correct += 1

        
        return {"reverse_exact_str_match": float(correct / total), "correct": correct, "total": total}
