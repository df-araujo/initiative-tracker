import math

def abilityMod(ability) :
    return math.floor((ability - 10)/2)

def sizeMod(size) :
    match(size) :
        case 'Tiny' :
            return 5
        case 'Small' :
            return 2
        case 'Medium' :
            return 0
        case 'Large' :
            return -2
        case 'Huge' :
            return -5
        case 'Gargantuan' :
            return -8
        
def speedMod(action) :
    if action.startswith('Fastest') :
        return 5
    if action.startswith('Fast') :
        return 2
    if action.startswith('Normal') :
        return 0
    if action.startswith('Slow') :
        return -2
    if action.startswith('Slowest') :
        return -5