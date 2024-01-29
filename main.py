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
    with open("data/jockeys", "r") as f:
        for line in f:
            name, control = line.strip().split(",")
            jockey = Jockey(name, control)
            jockeys.append(jockey)


def load_dinos():
    with open("data/dinos", "r") as f:
        for line in f:
            name, dinotype, ferocity, speed = line.strip().split(",")
            dino = Dino(name, dinotype, ferocity, speed)
            dinos.append(dino)


def assign_racers():
    for jockey, dino in zip(jockeys, dinos):
        racer = Racer(jockey, dino)
        racers.append(racer)


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
    for race in range(NUM_RACES):

        for segment_num in range(NUM_SEGMENTS):
            for racer in racers:
                jockey = racer.jockey
                dino = racer.dino

                if control_check(jockey, dino, hazards[segment_num].mod):
                    racer.distance += dino.speed
                    racer.distances.append(racer.distance)

        # TODO: after 1 race, sort racers by distance and create placements
        for racer in racers:
            print(racer)

        input()

        # reset racers
        for racer in racers:
            racer.distance = 0
            racer.distances = []


    # race is over. calculate the placements
    input("calculating placements... ")

    # calculate percentages of placement


def reroll():
    print("reroll")


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
    # if choice == "y":
    #     return True
    # return False

    return choice == "y"


def main():
    # define the track
    hazards = generate_track()
    print(hazards)

    load_jockeys()
    load_dinos()
    assign_racers()

    # while True:
    #     # print jockey/dino pairings and track
    display_pairings()
    #     # prompt user to reroll stats
    #     prompt_user("do you want to reroll? [y/N]> ")
    #     if False:
    #         # if prompt_user("do you want to reroll? [y/N] >"):
    #         #     # start simulation? Y - simulation, N - reroll
    #         reroll()
    #     else:
    #         break

    run_simulation(hazards)

    # simulate control check for each jockey/dino for 10 rounds, add track bonus
    # order 1st, 2nd, 3rd place
    # perform this 100x, record results (record odds)

    # prompt user to start actual race
    prompt_user("do you want to start the race?")

    # pass


if __name__ == '__main__':
    # display_pairings()
    main()
