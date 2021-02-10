from random import randrange

from parse_stats import ChallengeRivals
from titan import Titan


def dice6():
    return randrange(1, 7, 1)


class Fight:

    def __init__(self, attacking: Titan, defending: Titan):
        self.attacking_titan = attacking
        self.defending_titan = defending

        self.count = 0

    @staticmethod
    def throws_check(amount, param, modifier=0, reverse=False):
        throws = [dice6() + modifier for _ in range(amount)]
        if not reverse:
            checks = [x for x in throws if x > param]
        else:
            checks = [x for x in throws if x < param]
        return throws, checks

    def basic(self):
        number_of_attacks = self.attacking_titan.attack + 1
        return self.basic_attack(number_of_attacks)

    def basic_attack(self, number_of_attacks, advanced=False):
        if number_of_attacks <= 0:
            return "no damage"
        attacking_weapon = self.attacking_titan.weapons[0]

        skill_check, successful_skill = self.throws_check(number_of_attacks, self.attacking_titan.skill)
        weapon_check, successful_weapon = self.throws_check(len(successful_skill), attacking_weapon.power)
        defence_check, failed_defence = self.throws_check(len(successful_weapon), self.defending_titan.armor,
                                                          modifier=attacking_weapon.breakthrough, reverse=True)
        total_damage = len(failed_defence) * attacking_weapon.damage
        if advanced and attacking_weapon.quality == 2:
            total_damage += len(failed_defence) * self.attacking_titan.weapons[1].damage
        death_checks_amount = total_damage - self.defending_titan.lives

        if death_checks_amount < 0:
            return "no damage"

        death_checks_amount += 1
        death_checks = [dice6() for _ in range(death_checks_amount)]

        return "death" if max(death_checks) >= 6 else "fall" if max(death_checks) >= 3 else "wound"

    @staticmethod
    def weapon_quality_check(weapon):
        if weapon.quality == 2:
            return -1
        if weapon.quality == 0:
            return -2
        return 0

    def advanced(self):
        attack_weapon = self.attacking_titan.weapons[0]
        defence_weapon = self.defending_titan.weapons[0]
        number_of_attacks = self.attacking_titan.attack + 1

        success_count = 0
        while number_of_attacks:
            number_of_attacks -= 1
            atd = dice6()
            ded = dice6()

            skill_diff = abs(self.attacking_titan.skill - self.defending_titan.skill)

            if self.attacking_titan.skill > self.defending_titan.skill:
                ded += skill_diff * 2
            else:
                atd += skill_diff * 2

            atd += self.weapon_quality_check(attack_weapon)
            ded += self.weapon_quality_check(defence_weapon)

            ded += 1

            if atd > ded:
                success_count = number_of_attacks + 1
                break

        return self.basic_attack(success_count, advanced=True)

    def old(self):
        attack_weapon = self.attacking_titan.weapons[0]
        defence_weapon = self.defending_titan.weapons[0]
        attack_number = self.attacking_titan.attack + (2 if attack_weapon.quality == 2 else 1)
        defence_number = self.defending_titan.attack + (2 if defence_weapon.quality == 2 else 1)
        attack_throws = [dice6() for _ in range(attack_number)]
        defence_throws = [dice6() for _ in range(defence_number)]

        atd = max(attack_throws)
        ded = max(defence_throws)

        skill_diff = abs(self.attacking_titan.skill - self.defending_titan.skill)
        if self.attacking_titan.skill > self.defending_titan.skill:
            ded += skill_diff
        else:
            atd += skill_diff

        atd += 1

        atd += len([x for x in attack_throws if x == 6])
        ded += len([x for x in defence_throws if x == 6])

        atd += len([x for x in defence_throws if x == 1])
        ded += len([x for x in attack_throws if x == 1])

        return self.basic_attack(atd - ded)


if __name__ == '__main__':

    def show_res(arr):
        return ({
                "death": round(len([x for x in arr if x == "death"]) / len(arr), 2) * 100,
                "fall": round(len([x for x in arr if x == "fall"]) / len(arr), 2) * 100,
                "wound": round(len([x for x in arr if x == "wound"]) / len(arr), 2) * 100,
                "no damage": round(len([x for x in arr if x == "no damage"]) / len(arr), 2) * 100,
            })

    titans = ChallengeRivals('stats.csv').titans
    for atk in range(len(titans)):
        for dnd in range(len(titans)):
            main_arena = Fight(attacking=titans[atk], defending=titans[dnd])
            basic_results = [main_arena.basic() for _ in range(100)]
            advanced_results = [main_arena.advanced() for _ in range(100)]
            old_results = [main_arena.old() for _ in range(100)]

            print(f'{titans[atk].name} hit {titans[dnd].name}')
            print(
                f'Basic: {show_res(basic_results)} \n'
                f'Advanced: {show_res(advanced_results)} \n'
                f'Old: {show_res(old_results)} \n'
                '______________________________________________'
            )
