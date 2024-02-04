import random
from Jockey import Jockey
from Dino import Dino
from Racer import Racer
from Track import TrackHazard, TrackSegment, generate_random_hazards

# user defined variables. set this before running program
num_participants = 5
num_hazards = 3

# constants
NUM_SEGMENTS = 10
NUM_RACES = 100

# program variables
jockeys = []
dinos = []
racers = []


def load_jockeys():
    with open("data/jockeys", "r", encoding="utf-8") as f:
        for line in f:
            name, control = line.strip().split(",")
            jockey = Jockey(name, control)
            jockeys.append(jockey)


def load_dinos():
    with open("data/dinos", "r", encoding="utf-8") as f:
        for line in f:
            name, dinotype, ferocity, speed = line.strip().split(",")
            dino = Dino(name, dinotype, ferocity, speed)
            dinos.append(dino)


def assign_racers():
    # truncate jockey/dino lists to only num_participants
    global jockeys, dinos

    # randomize jockey/dino pairing
    random.shuffle(jockeys)
    random.shuffle(dinos)

    jockeys, dinos = jockeys[:num_participants], dinos[:num_participants]
    for jockey, dino in zip(jockeys, dinos):
        racer = Racer(jockey, dino)
        racers.append(racer)
        racer.placements = [0] * (num_participants + 1)  # one-indexed
        racer.placements[0] = -1  # sentinel value, there should not be a 0th place


def generate_track():
    starting_hazard = TrackHazard("And They’re Off", 1, "The gates go up and the dinosaurs take off!")
    ending_hazard = TrackHazard("Final Stretch", 1, "The dinosaurs race to the finish")
    random_hazards = generate_random_hazards(num_hazards)
    hazards = [starting_hazard] + random_hazards + [ending_hazard]

    return hazards


def control_check(jockey, dino, track_modifier=0) -> bool:
    """
    Rolls a control check and returns control result,
    then compares it against the dinosaur's ferocity value.

    If control check is >= the dinosaur's ferocity value, it
    succeeds.
    """

    # roll 1d20
    roll = random.randint(1, 20)
    # check critical success/failure
    if roll == 1:
        return False
    if roll == 20:
        return True

    # add result to jockey's control value
    control_check_value = roll + jockey.control + track_modifier

    # compare to dino's ferocity value
    if control_check_value >= dino.ferocity:
        return True

    return False


def run_simulation(hazards):
    run_race(hazards)


def run_race(hazards, num_races=NUM_RACES, verbose=False):
    for race in range(num_races):
        for segment_num in range(NUM_SEGMENTS):
            if verbose:
                print(f"segment {segment_num+1}, hazard: {hazards[segment_num].name}, desc: {hazards[segment_num].desc}")
            for racer in racers:
                jockey = racer.jockey
                dino = racer.dino

                if control_check(jockey, dino, hazards[segment_num].mod):
                    racer.distance += dino.speed
                racer.distances.append(racer.distance)

                if verbose:
                    print(racer)
            if verbose:
                input()

        # selection sort - sort racers list in place
        for i in range(len(racers)):
            max_index = i
            for j in range(i + 1, len(racers)):
                if racers[max_index] < racers[j]:
                    max_index = j

            # swap max_index with position of newest max
            racers[i], racers[max_index] = racers[max_index], racers[i]

        if verbose:
            print("race results:")
            for i, racer in enumerate(racers):
                print(f"    place {i+1}: {racer}")

        # update placement and reset racers
        for i in range(len(racers)):
            racer = racers[i]
            racer.placements[i + 1] += 1
            racer.distance = 0
            racer.distances = []

    # simulation over. calculate percentages of placement
    for racer in racers:
        s = f"{racer.jockey.name} {racer.dino.name}"
        for placement in range(1, num_participants + 1):
            s += f", {placement}: {racer.placements[placement] / NUM_RACES * 100:.0f}%"

        print(s)


def reroll():
    global jockeys, dinos, racers
    jockeys = []
    dinos = []
    racers = []

    load_jockeys()
    load_dinos()
    assign_racers()


def display_pairings():
    columns = {}
    headings = (
        "Jockey",
        "Control",
        "Dinosaur",
        "Type",
        "Ferocity",
        "Speed"
    )

    columns["headings"] = headings
    columns["widths"] = [-1] * len(headings)

    # save the max column width from the heading names
    for i, heading in enumerate(headings):
        columns["widths"][i] = len(columns["headings"][i])

    # save the max column width from the jockey/dino names
    for jockey in jockeys:
        if len(jockey.name) > columns["widths"][0]:
            columns["widths"][0] = len(jockey.name)
        if len(str(jockey.control)) > columns["widths"][1]:
            columns["widths"][1] = len(str(jockey.control))
    for dino in dinos:
        if len(dino.name) > columns["widths"][2]:
            columns["widths"][2] = len(dino.name)
        if len(dino.dinotype) > columns["widths"][3]:
            columns["widths"][3] = len(dino.dinotype)
        if len(str(dino.ferocity)) > columns["widths"][4]:
            columns["widths"][4] = len(str(dino.ferocity))
        if len(str(dino.speed)) > columns["widths"][5]:
            columns["widths"][5] = len(str(dino.speed))

    hsep = "+"
    for width in columns["widths"]:
        hsep += f"""{"".center(width + 2, "-")}+"""

    heading_line = "|"
    for i, heading in enumerate(columns["headings"]):
        heading_line += f"""{heading.center(columns["widths"][i] + 2)}+"""

    header = hsep + "\n" + heading_line + "\n" + hsep + "\n"

    roster_lines = ""
    for racer in racers:
        racer_line = "|"
        for i, entry in enumerate((
                racer.jockey.name,
                racer.jockey.control,
                racer.dino.name,
                racer.dino.dinotype,
                racer.dino.ferocity,
                racer.dino.speed,
        )):
            racer_line += f""" {str(entry).ljust(columns["widths"][i])} |"""
        roster_lines += racer_line + "\n"

    # +----------------+---------+------------------+----------------------+----------+-------+
    # |         Jockey | Control |     Dinosaur     |         Type         | Ferocity | Speed |
    # +----------------+---------+------------------+----------------------+----------+-------+
    # | Fipya Ngore    |       2 | Big Honker       | Allosaurus, young    |       80 |    50 |
    # | Azaka Imbogoro |       1 | Ubtao’s Favorite | Deinonychus          |       60 |    40 |
    # | Yapa Sahandi   |       0 | Banana Candy     | Dimetrodon           |       50 |    30 |
    # | Wadizi Dawa    |       1 | Bonecruncher     | Hadrosaurus          |       50 |    40 |
    # | U'lolo Talro'a |       2 | Grung Stomper    | Stegosaurus, young   |       60 |    40 |
    # | Vazul O'tamu   |       2 | Scarback         | Triceratops, young   |       75 |    50 |
    # | Zaidi Imbogoro |       3 | Nasty Boy        | Tyrannosaurus, young |      100 |    50 |
    # +----------------+---------+------------------+----------------------+----------+-------+
    footer = hsep

    roster = header + roster_lines + footer
    print(roster)


def prompt_user(param):
    choice = input(param)
    return choice == "y"


def main():
    # define the track
    hazards = generate_track()
    print(hazards)

    load_jockeys()
    load_dinos()
    assign_racers()

    while True:
        # print jockey/dino pairings and track
        display_pairings()
        # prompt user to reroll stats
        if prompt_user("do you want to reroll? [y/N] > "):
            # start simulation? Y - simulation, N - reroll
            reroll()
        else:
            break

    run_simulation(hazards)

    # simulate control check for each jockey/dino for 10 rounds, add track bonus
    # order 1st, 2nd, 3rd place
    # perform this 100x, record results (record odds)

    # prompt user to start actual race
    while True:
        if prompt_user("do you want to start the race? [y/N] > "):
            break

    run_race(hazards, 1, True)


if __name__ == '__main__':
    main()
