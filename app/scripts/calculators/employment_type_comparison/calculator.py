from config import EmployeeConfig, OSVCConfig, CommonConfig

# NOTE: Kalkulace jsou platné pouze v souvislosti s daty a zákony České Republiky.
# NOTE: Samostatná výdělečná činnost může být hlavní nebo vedlejší. Tento skript počítá pouze s hlavní (takže placení důchodového pojištění je povinné).

class Zamestnanec:
    def __init__(self, mesicni_hruba_mzda):
        """
        Pro výpočet čisté měsíční mzdy je třeba od měsíční hrubé mzdy:
        - odečíst sociální a zdravotní pojištění
        - odečíst zálohu na daň
        - přičíst slevy na daních

        Sociální a zdravotní pojištění:
        Ty jsou vypočteny každá zvlášť jako procento z hrubé mzdy.
        Sociální pojištění - skládá se z nemocenského a důchodového pojištění

        Záloha na daň:
        Záloha na daň = průběžná platba, která se v průběhu roku hradí na účet budoucí, celkové daňové povinnosti, která se definitivně určí až po skončení zdaňovacího období (zpravidla na konci roku).

        Slevy na daních:
        Pro většinu případů se uplatňuje typicky pouze "Sleva na poplatníka".
        """

        socialni = round(EmployeeConfig().SOCIALNI_POJISTENI_SAZBA * mesicni_hruba_mzda)
        zdravotni = round(EmployeeConfig().ZDRAVOTNI_POJISTENI_SAZBA * mesicni_hruba_mzda)

        # Pokud je hrubá mzda více než 139 671 Kč (3x minimální mzda): daní se PŘESAH této hodnoty vyšší/progresivní sazbou (23%), zbytek "normálně" základní (15%).
        if mesicni_hruba_mzda > CommonConfig().HRANICE_VYSSIHO_PRIJMU:
            zaloha_zakladni_cast = CommonConfig().HRANICE_VYSSIHO_PRIJMU * CommonConfig().ZAKLADNI_DANOVA_SAZBA_FYZI_OSOB
            zaloha_progresivni_cast = (mesicni_hruba_mzda - CommonConfig().HRANICE_VYSSIHO_PRIJMU) * CommonConfig().PROGRESIVNI_DANOVA_SAZBA_FYZI_OSOB

            zaloha_na_dan_pred_slevami = zaloha_zakladni_cast + zaloha_progresivni_cast
        else:
            zaloha_na_dan_pred_slevami = mesicni_hruba_mzda * CommonConfig().ZAKLADNI_DANOVA_SAZBA_FYZI_OSOB
        zaloha_na_dan_pred_slevami = round(zaloha_na_dan_pred_slevami)

        # Daňové slevy - pro většinu případů má smysl pouze "Sleva na poplatníka"
        zaloha_na_dan_po_slevach = zaloha_na_dan_pred_slevami - (CommonConfig().SLEVA_NA_POPLATNIKA)

        mesicni_cista_mzda = mesicni_hruba_mzda - (socialni + zdravotni + zaloha_na_dan_po_slevach)
        self.mesicni_cista_mzda = mesicni_cista_mzda

    def get_mesicni_cista_mzda(self):
        return self.mesicni_cista_mzda

class OSVC:
    def __init__(self, mesicni_hruba_mzda):
        pass


def main():
    hruba_mzda_OSVC = 41000
    hruba_mzda_zamestnanec = 27000

    zamestnanec = Zamestnanec(hruba_mzda_zamestnanec)
    osvc = OSVC(hruba_mzda_OSVC)

if __name__=="__main__":
    main()