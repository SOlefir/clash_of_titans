import csv

from titan import Titan
from weapon import Weapon


class ChallengeRivals:

    def __init__(self, file_name):

        self.titans = list()
        self._read_csv_into_dict(file_name)

    def _read_csv_into_dict(self, file_name):
        with open(file_name, 'r') as csv_file:
            for line in csv.DictReader(csv_file):
                self._get_titans(line)

    def __get_weapons(self, line: dict) -> list:
        weapons = list()
        for count in range(int(line['weapons'])):
            weapons.append(
                Weapon(
                    power=int(line[f'power_{count + 1}']),
                    breakthrough=int(line[f'breakthrough_{count + 1}']),
                    damage=int(line[f'damage_{count + 1}']),
                    quality=int(line[f'quality_{count + 1}']),
                )
            )
        return weapons

    def _get_titans(self, line: dict):
        self.titans.append(
            Titan(
                name=line['name'],
                lives=int(line['lives']),
                attack=int(line['attacks']),
                skill=int(line['skills']),
                armor=int(line['armor']),
                weapons=self.__get_weapons(line),
            )
        )

