from database.database import DatabaseSpells

class SpellService:
    @staticmethod
    def get_spell_by_combo(combo: str) -> dict | None:
        """Ищет спелл в БД по отсортированной комбинации сфер (например 'EQW').
        Args:
            combo (str): Комбинация из 3 сфер
        Returns:
            dict | None: Словарь с данными спелла или None
        """
        sorted_combo = "".join(sorted(combo.upper()))

        spells = DatabaseSpells.get_all_spells()
        for spell in spells:
            if "".join(sorted(spell["combo"].upper())) == sorted_combo:
                return spell

        return None

