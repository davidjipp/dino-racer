import random
from Jockey import Jockey
from Dino import Dino
from Track import TrackHazard, TrackSegment, generate_random_hazards

# user defined variables. set this before running program
num_participants = 5
num_hazards = 3

# constants
NUM_SEGMENTS = 10
NUM_RACES = 100

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


def run_simulation():
    for race in range(NUM_RACES):
        for segment_num in range(NUM_SEGMENTS):
            for racer in racers:
                jockey = racer.jockey
                dino = racer.dino

                if control_check(jockey, dino, hazards[segment_num]):
                    racer.distance += dino.speed
                    racer.distances.append(racer.distance)

    # race is over. calculate the placements




    # calculate percentages of placement





def reroll():
    print("reroll")


def display_pairings():
    roster = f"""
+----------------+---------+------------------+----------------------+----------+-------+
|     Jockey     | Control |     Dinosaur     |         Type         | Ferocity | Speed |
+----------------+---------+------------------+----------------------+----------+-------+
| Fipya Ngore    |       2 | Big Honker       | Allosaurus, young    |       80 |    50 |
| Azaka Imbogoro |       1 | Ubtao’s Favorite | Deinonychus          |       60 |    40 |
| Yapa Sahandi   |       0 | Banana Candy     | Dimetrodon           |       50 |    30 |
| Wadizi Dawa    |       1 | Bonecruncher     | Hadrosaurus          |       50 |    40 |
| U'lolo Talro'a |       2 | Grung Stomper    | Stegosaurus, young   |       60 |    40 |
| Vazul O'tamu   |       2 | Scarback         | Triceratops, young   |       75 |    50 |
| Zaidi Imbogoro |       3 | Nasty Boy        | Tyrannosaurus, young |      100 |    50 |
+----------------+---------+------------------+----------------------+----------+-------+
    """

    # roster = heading

    print(roster)


def prompt_user(param):
    choice = input(param)
    # if choice == "y":
    #     return True
    # return False

    return choice == "y"

def main():
    # define number of participants

    # define the track
    starting_hazard = TrackHazard("And They’re Off", 1, "The gates go up and the dinosaurs take off!")
    ending_hazard = TrackHazard("Final Stretch", 1, "The dinosaurs race to the finish")
    random_hazards = generate_random_hazards(num_hazards)
    hazards = [starting_hazard] + random_hazards + [ending_hazard]

    print(hazards)

    # for now have program assign jockeys to dinos. stretch goal: manually perform this later

    # racers = [
    #     alice x tyrannosaurus,
    #     david x triceratops
    #
    #
    # ]
    #
    # racers[0]
    #
    #
    #
    # jockeys = (
    #     "Alice",
    #     "David",
    #     "Kenneth",
    #     "Michael"
    # )
    #
    # dinos = (
    #     "tyrannosaurus",
    #     "triceratops",
    #     "stegosaurus",
    #     "pteradactyl"
    # )

    # print jockey/dino pairings and track

    # prompt user to reroll stats
    while True:
        display_pairings()
        if prompt_user("do you want to reroll? [y/N]"):
            #     # start simulation? Y - simulation, N - reroll
            reroll()
        else:
            break

    run_simulation()

    # simulate control check for each jockey/dino for 10 rounds, add track bonus
    # order 1st, 2nd, 3rd place
    # perform this 100x, record results (record odds)

    # prompt user to start actual race
    prompt_user("do you want to start the race")

    # pass


if __name__ == '__main__':
    # display_pairings()
    main()
