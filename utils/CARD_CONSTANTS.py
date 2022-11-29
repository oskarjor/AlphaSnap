import Card

NONCOLLECTIBLE_CARD_DICT = {

    "0-cost": 
    {
        
    }, 

    "1-cost": 
    {

    }, 


    "2-cost": 
    {

    },

    "3-cost": 
    {

    },

    "4-cost": 
    {

    }, 

    "5-cost": 
    {

    },


    "6-cost": 
    {

    },

}

CARD_DICT = {

    "0-cost": 
    {
        "wasp": Card.Wasp, 
        "yellowjacket": Card.Yellowjacket,
    }, 

    "1-cost": 
    {
        "mistyKnight": Card.MistyKnight, 
        "antMan": Card.AntMan, 
        "elektra": Card.Elektra, 
        "mantis": Card.Mantis, 
    }, 

    "2-cost": 
    {
        "shocker": Card.Shocker, 
        "starLord": Card.StarLord,
    }, 

    "3-cost": 
    {
        "cyclops": Card.Cyclops, 
        "groot": Card.Groot, 
    }, 

    "5-cost": 
    {
        "theThing": Card.TheThing, 
    }, 

}

def getFlatCardDict(CARD_DICT):
    FLAT_CARD_DICT = {}
    for _, COST_CARD_DICT in CARD_DICT.items():
        for key, val in COST_CARD_DICT.items():
            FLAT_CARD_DICT[key] = val
    return FLAT_CARD_DICT



FLAT_CARD_DICT = getFlatCardDict(CARD_DICT)
FLAT_NONCOLLECTIBLE_CARD_DICT = getFlatCardDict(NONCOLLECTIBLE_CARD_DICT)