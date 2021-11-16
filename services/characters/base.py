class Character:
    level: int
    base_attack: int  # Attack from character level
    weapon_attack: int  # Weapon attack
    attack: int  # Whole attack (base + weapon + artifacts)
    crit_rate: float
    crit_dmg: float
    defense: int
    elemental_mastery: int
    elemental_dmg_bonus: float
    physical_dmg_bonus: float
    artifacts: dict
