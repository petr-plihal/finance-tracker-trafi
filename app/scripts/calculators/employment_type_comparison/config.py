from dataclasses import dataclass

@dataclass(frozen=True)
class EmployeeConfig:
    # Skládá se z nemocenského (0,6%) a důchodového (6,5%) pojištění. Státní politiku zaměstnanosti řeší zaměstnavatel.
    SOCIALNI_POJISTENI_SAZBA: float = 0.071
    ZDRAVOTNI_POJISTENI_SAZBA: float = 0.045

@dataclass(frozen=True)
class OSVCConfig:
    SOCIALNI_POJISTENI_SAZBA: float = 0.292
    ZDRAVOTNI_POJISTENI_SAZBA: float = 0.135

@dataclass(frozen=True)
class CommonConfig:
    ZAKLADNI_DANOVA_SAZBA_FYZI_OSOB: float = 0.15
    PROGRESIVNI_DANOVA_SAZBA_FYZI_OSOB: float = 0.23

    # TODO: Neměla by tato konstanta být vždy tří násobek minimální mzdy?
    HRANICE_VYSSIHO_PRIJMU: int = 139671

    # Daňové slevy
    # Měsíční částka slevy
    SLEVA_NA_POPLATNIKA = 2570
    
