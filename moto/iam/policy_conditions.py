from typing import Dict, Iterator, List, Union

from .exceptions import ValidationError


def string_equals_operation(
    expected_value: Union[List[str], str], actual_value: Union[List[str], str]
) -> bool:
    if not isinstance(expected_value, str) or not isinstance(actual_value, str):
        return False

    return expected_value == actual_value


CONDITION_OPERATIONS = {"StringEquals": string_equals_operation}


class TrustCondition:
    """Single condition object"""

    def __init__(
        self,
        condition: str,
        expected_value: Union[List[str], str],
        expected_value_source: str,
    ) -> None:
        if condition not in CONDITION_OPERATIONS:
            raise NotImplementedError(f"Unsupported condition: {condition}")

        self._condition = condition

        self._expected_value_source = expected_value_source
        self._expected_value = expected_value

    @property
    def value_source_key(self) -> str:
        return self._expected_value_source

    def verify_condition(self, actual_value: Union[List[str], str]) -> bool:
        verify_action = CONDITION_OPERATIONS[self._condition]

        return verify_action(actual_value, self._expected_value)


ConditionData = Dict[str, Dict[str, Union[str, List[str]]]]


class TrustRelationShipConditions:
    """Trust relationship conditions segment model"""

    def __init__(self, conditions: ConditionData) -> None:
        self._conditions: List[TrustCondition] = []

        for conditions_operation, condition_values in conditions.items():
            condition_values_items: List[Union[str, List[str]]] = list(
                *condition_values.items()
            )
            if len(condition_values_items) != 2:
                raise ValidationError("Invalid condition values format")

            expected_value_source = condition_values_items[0]
            expected_value = condition_values_items[1]
            self._conditions.append(
                TrustCondition(
                    conditions_operation, expected_value, expected_value_source
                )
            )

    def __iter__(self) -> Iterator[TrustCondition]:
        return self._conditions.__iter__()
