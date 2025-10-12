from dataclasses import dataclass

@dataclass
class NetSalaryInfo:
    gross: float
    net: float

@dataclass
class ComparedEmploymentTypes:
    employee: NetSalaryInfo
    self_employed: NetSalaryInfo