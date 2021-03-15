import numpy as np

def sim_attack(ac,attack_modifier,dmg_dice,dmg_modifier,advantage=False):
    """
    Return the damage result of an attack, 0 if missed.
    An attack requires rolling an attack roll to determine if the target is hit,
    and then a damage roll to determine the damaged dealt to the target.
    Attack Roll = roll of a 20-sided dice + attack modifier
    Damage Roll = Roll of all damage dice + damage modifier
    
    Parameters:
    ----------
    ac: armor class of the target, an attack roll >= armor class guarantees a hit.
    
    attack_modifier: the value to be added to the attack dice roll;
    it can be negative or 0.
    
    dmg_dice: a list of string representing dice to roll to determine damage,
    dice are represented in 'xdy' way in which x is the number of dice and y
    is the number of side, for instance '2d8' means two eight-sided dice.
    
    dmg_modifier: the value to be added to the damage dice roll;
    it can be negative or 0.
    
    advantage: an attack with advantage can roll 2 instead of 1 attack dice,
    and choose the highest as the result. Default False.
    
    Output:
    ------
    The damage(int) as an result of the attack, 0 if missed;
    the total value of damage is the sum of rolls of each damage dice 
    plus the damage modifier.
    """
    #calculate attack roll
    if advantage:
        dice_roll = np.amax([np.random.randint(1,21),np.random.randint(1,21)])
    else:
        dice_roll = np.random.randint(1,21)
    attack_roll = dice_roll + attack_modifier
    # validate if target is hit
    if attack_roll<ac:
        return 0
    else:
        return make_damage(dmg_dice,dmg_modifier) #calculate damage if hit
    
def make_damage(dmg_dice,dmg_modifier):
    """
    Calculate the damage based on damage dice and damage modifier/
    
    Parameters:
    ----------
    dmg_dice: a list of string representing dice to roll to determine damage,
    dice are represented in 'xdy' way in which x is the number of dice and y
    is the number of side, for instance '2d8' means two eight-sided dice.
    
    dmg_modifier: the value to be added to the damage dice roll;
    it can be negative or 0.
    
    Output:
    ------
    an interger representing the damage dealt
    """
    #calculate damage
    num_roll = [] #store the number of damage dice
    num_roll_point = [] #store the size/number of sides of each dice
    #split dmg_dice
    for i in dmg_dice:
        num_roll.append(int(i.split('d')[0]))
        num_roll_point.append(int(i.split('d')[1]))
    #calculate the value of each damage dice roll
    num_roll = np.array(num_roll)
    num_roll_point = np.array(num_roll_point)
    dmg = num_roll*np.array([np.random.randint(1,i+1) for i in num_roll_point])
    # sum all damage dice roll, add damage modifier to the result
    return np.sum(dmg)+dmg_modifier

def sim_N(ac,attack_modifier,dmg_dice,dmg_modifier,N,advantage=False):
    """
    simulate attack N times
    
    Parameters:
    ----------
    N: the number of attack to simmulate, default 1.
    
    other arguments: see the sim_attack function
    
    Output:
    ------
    resulted damages as an array of each attack
    """
    arr = []
    for i in range(N):
        arr.append(sim_attack(ac
                              ,attack_modifier
                              ,dmg_dice
                              ,dmg_modifier
                              ,advantage))
    return arr

