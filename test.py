import module as mod
import numpy as np

def test_1():
    """
    This function test make_damage function
    """
    #test only damage dice without modifiers
    res1 = []
    for i in range(100):
        res1.append(mod.make_damage(dmg_dice=['1d4'],dmg_modifier=0))
    res1 = np.array(res1)
    assert np.all(res1>0) #damage should be greater than 0
    assert np.all(res1<=4) #damage should not exceed the max possible roll of dice.
    
    #test single kind of damage dice with the modifier
    damage_modifier = np.random.randint(100) # set a random damage modifier
    dice_size = np.random.randint(1,100) # set a random dice size
    damage_dice = ['2d'+str(dice_size)]
    res2=[]
    for i in range(100):
        res2.append(mod.make_damage(dmg_dice=damage_dice,dmg_modifier=damage_modifier))
    res2 = np.array(res2)
    assert np.all(res2>=(damage_modifier+2)) #damage should be no less than the modifier+minimum dice roll
    assert np.all(res2<=(dice_size*2+damage_modifier)) #damage should be no more than the theoretical maximum
    
    #test multiple kinds of damage dice with potentially the negative modifier
    res3 = []
    damage_modifier = np.random.randint(-100,100) # set a random damage modifier
    dice_size = np.random.randint(1,100,10) # set 10 random dice sizes
    damage_dice =['1d'+str(i) for i in dice_size]
    for i in range(100):
        res3.append(mod.make_damage(dmg_dice=damage_dice,dmg_modifier=damage_modifier))
    res3 = np.array(res3)
    assert np.all(res3>=(damage_modifier+10))
    assert np.all(res3<=(damage_modifier+np.sum(dice_size)))
    
def test_2():
    """
    This function test sim_attack function
    """
    attack_1 = mod.sim_attack(10,9,['1d1'],0)
    # an attack with attack modifiter + minimum roll of dice equal to armor class is guaranteed to hit
    assert attack_1==1
    
    attack_2 = mod.sim_attack(10,0,['1d6'],0,True)
    # attack with advantage
    assert attack_2%1==0 #type is int or numpy.int
    assert attack_2>=0    
    
def test_3():
    """
    This function test sim_attack and sim_N functions
    """
    attack_1 = mod.sim_N(100,0,['1d8'],2,100) 
    assert len(attack_1)==100 # check cardinality
    # the armor class exceed the max possible attack roll, the attack is guaranteed to be missed
    assert np.all(np.array(attack_1)==0)

    attack_2 = mod.sim_N(10,-20,['1d8'],2,100)
    # the max possible sum of attack roll and attack modifier is below armor class,
    # miss guaranteed    
    assert np.all(np.array(attack_2)==0)
    
    attack_3 = mod.sim_N(0,0,['1d8'],2,100)
    assert np.all(np.array(attack_3)>0) # attacks on a target without armor class are guaranteed to hit
    assert np.all(np.array(attack_3)>2) # resulted damage should be greater than the damage modifier
