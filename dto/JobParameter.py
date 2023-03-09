from dataclasses import dataclass


@dataclass
class JobParameter:
    name: str
    type: str
    value: str
    availableValues: []
