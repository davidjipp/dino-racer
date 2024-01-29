import random


class TrackHazard:
    def __init__(self, name, mod, desc):
        self.name = name
        self.mod = mod
        self.desc = desc

    def __repr__(self):
        return self.name


class TrackSegment:
    def __init__(self, district_name, segment_name):
        self.district_name = district_name
        self.segment_name = segment_name


# 1 Tiryki Anchorage, Dinosaur Pens
# 2 Market Ward Red Bazaar
# 3 Market Ward Dye Works
# 4 Market Ward Public Bathhouse
# 5 Merchant Ward Grand Souk
# 6 Merchant Ward Jewel Market
# 7 The Old City Executioner’s Run
# 8 Merchant Ward Grand Souk #yes again
# 9 Malar’s Throat Temple of Tymora
# 10 Tiryki Anchorage Dinosaur Pens #yes again


# For Segments 2-9
#         For each random hazard, RandInt 1-5.  Hazard =
#             0 Flooded -2 The track in this segment has become inundated by recent heavy rainfall and is flooded!
#             1 Insect Swarm -1 A swarm of insects has been spotted around this segment!
#             2 Blessed +1 A local priestly order has sent acolytes to bless the racers as they pass through this segment!
#             3 Wagon Jam -3 This segment is currently blocked by a traffic jam of wagons and carts!
#             4 Dancing Monkey Fruit +2 A local monkey fruit vendor has unwisely decided to set up their stall on this track segment!
#         Assign num_randomhazards to random segments to create the final race track that we can start running simulations on.

def generate_random_hazards(num_hazards):
    no_hazard = TrackHazard("no hazards", 0, "no hazards")
    hazards = [no_hazard] * 8

    hazard_choices = [
        TrackHazard("Flooded", -2,
                    "The track in this segment has become inundated by recent heavy rainfall and is flooded!"),
        TrackHazard("Insect Swarm", -1, "A swarm of insects has been spotted around this segment!"),
        TrackHazard("Blessed", 1,
                    "A local priestly order has sent acolytes to bless the racers as they pass through this segment!"),
        TrackHazard("Wagon Jam", -3, "This segment is currently blocked by a traffic jam of wagons and carts!"),
        TrackHazard("Dancing Monkey Fruit", 2,
                    "A local monkey fruit vendor has unwisely decided to set up their stall on this track segment!")
    ]

    # pick segments with hazards
    hazard_segments = []
    while len(hazard_segments) < num_hazards:
        # pick random segment to assign hazard to
        hazard_segment = random.randrange(8)
        if hazard_segment not in hazard_segments:
            hazard_segments.append(hazard_segment)

    for hazard_segment in hazard_segments:
        # pick a random hazard
        choice = random.randrange(5)
        hazard_choice = hazard_choices[choice]
        hazards[hazard_segment] = hazard_choice

    return hazards
