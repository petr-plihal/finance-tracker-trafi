from dataclasses import dataclass

# TODO: This dataclass could later contain a name of the employment type, since there are more than 2 types.
@dataclass
class NetSalaryInfo:
    gross: float
    net: float

@dataclass
class ComparedEmploymentTypes:
    employee: NetSalaryInfo
    self_employed: NetSalaryInfo