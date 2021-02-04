from clash_of_the_titans import *
wpn1 = Weapon(3, -2, 2, 2)
wpn2 = Weapon(4, 0, 1, 2)
TITANATTACC = Titan("Attack Titan", 3, 3, 2, 3)
TITANATTACC.weapons = [wpn1, wpn1]
TITANBEST = Titan("Beast Titan", 2, 3, 3, 4)
TITANBEST.weapons = [wpn1, wpn2]
main_arena = Fight(TITANATTACC, TITANBEST)

def show_res(arr):
	return {
		"death": round(len([x for x in arr if x == "death"]) / len(arr), 2) * 100,
		"fall": round(len([x for x in arr if x == "fall"]) / len(arr), 2) * 100,
		"wound": round(len([x for x in arr if x == "wound"]) / len(arr), 2) * 100,
		"no damage": round(len([x for x in arr if x == "no damage"]) / len(arr), 2) * 100,
	}