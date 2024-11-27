from machine import Pin, PWM, ADC
import time
from time import sleep_ms
import random
from neopixel import NeoPixel

### BOARD VARIABLES
xVal = ADC(Pin(5))
yVal = ADC(Pin(4))

xVal.atten(ADC.ATTN_11DB)
yVal.atten(ADC.ATTN_11DB)
xVal.width(ADC.WIDTH_12BIT)
yVal.width(ADC.WIDTH_12BIT)

roll_button = Pin(16, Pin.IN, Pin.PULL_UP)  # button to press when you want to roll the wheel(neopixel)
finished_button = Pin(17, Pin.IN, Pin.PULL_UP)  # button to press when you finished your turn

star_a_button = Pin(6, Pin.IN, Pin.PULL_UP)
star_b_button = Pin(7, Pin.IN, Pin.PULL_UP)
star_c_button = Pin(15, Pin.IN, Pin.PULL_UP)

buzzer = PWM(Pin(18), freq=100)

pin = Pin(8, Pin.OUT)
neo = NeoPixel(pin, 16)


### 7 SEGMENT DISPLAY
segments_score = {
    'a': Pin(35, Pin.OUT),
    'b': Pin(0, Pin.OUT),
    'c': Pin(45, Pin.OUT),
    'd': Pin(48, Pin.OUT),
    'e': Pin(47, Pin.OUT),
    'f': Pin(21, Pin.OUT),
    'g': Pin(36, Pin.OUT),
    'dp': Pin(19, Pin.OUT)
}

segments_player = {
    'a': Pin(3, Pin.OUT),
    'b': Pin(46, Pin.OUT),
    'c': Pin(9, Pin.OUT),
    'd': Pin(10, Pin.OUT),
    'e': Pin(11, Pin.OUT),
    'f': Pin(12, Pin.OUT),
    'g': Pin(13, Pin.OUT),
    'dp': Pin(14, Pin.OUT)
}

num_to_segments = {
    0: ['a', 'b', 'c', 'd', 'e', 'f'],
    1: ['b', 'c'],
    2: ['a', 'b', 'g', 'e', 'd'],
    3: ['a', 'b', 'g', 'c', 'd'],
    4: ['f', 'g', 'b', 'c'],
    5: ['a', 'f', 'g', 'c', 'd'],
    6: ['a', 'f', 'e', 'd', 'c', 'g'],
    7: ['a', 'b', 'c'],
    8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    9: ['a', 'b', 'c', 'd', 'f', 'g'],
}

### FUNCTIONS
def display_number_score(num):
    # Turn off all segments
    for seg in segments_score.values():
        seg.value(1)
    # Turn on the required segments
    for seg in num_to_segments[num]:
        segments_score[seg].value(0)


def display_number_player(num):
    # Turn off all segments
    for seg in segments_player.values():
        seg.value(1)
    # Turn on the required segments
    for seg in num_to_segments[num]:
        segments_player[seg].value(0)



### GAME VARIABLES
players = []

turn = 0
turn_count = 0
player_amount=0
'''while True:
    for num in range(10):
        display_number_score(num)
        sleep_ms(100)

        display_number_player(num)
        sleep_ms(100)'''  # to check the 7-segment display
waiting_for_the_player_choice = True
player_amount_choice_allowed = False
checkingdisplays = True
while True:
    while waiting_for_the_player_choice:
        # print('running')
        y_value = yVal.read()
        x_value = xVal.read()
        print('x:', x_value, '  y:', y_value)
        time.sleep(0.2)
        if player_amount_choice_allowed == True and x_value < 100:
            print('choice made')
            waiting_for_the_player_choice = False
            for i in range(player_amount):
                players.append([i + 1, 0])
            print(players)
        if x_value > 4050:
            print('up')
            player_amount_choice_allowed = True
            player_amount=3
        elif y_value < 100:
            print('left')
            player_amount_choice_allowed = True
            player_amount=4
        elif y_value > 4050:
            print('right')
            player_amount_choice_allowed = True
            player_amount=2
        display_number_player(player_amount)
    turn += 1
    turn_count += 1
    '''while checkingdisplays == True:
        score_or_player = int(input('score(1) or player(2)'))
        if score_or_player == 1:
            score = int(input('input: '))
            display_number_score(score)

        elif score_or_player == 2:
            player = int(input('input: '))
            display_number_player(player)

        else:
            print('skipping...')
            sleep_ms(1000)
            checkingdisplays = False'''
    if turn > player_amount:
        turn = 1
    display_number_player(turn)
    print("turn =", turn_count)
    for i in range(len(players)):
        if players[i][0] == turn:  # THE CODE HERE RUNS FOR THE PLAYER WHOS TURN IT IS
            print("player", i + 1, "is moving")
            print("player", i + 1, "has", players[i][1], "points")
            display_number_score(players[i][1])
            input("ROLL: ")
            roll = random.randint(1, 4)
            roll = random.randint(0, 15)
            circles=random.randint(8,10)
            sleeptime=10
            for x in range(circles):
                for spin in range(16):
                    neo.fill([0,0,0])
                    neo[spin] = [5,0,0]
                    sleep_ms(sleeptime)
                    neo.write()
                    spins=circles*16
                    if x>circles-5:
                        sleeptime+=1
                    if x>circles-3:
                        sleeptime+=2
            for y in range(roll):
                neo.fill([0,0,0])
                neo[y] = [5,0,0]
                sleeptime+=5
                sleep_ms(sleeptime)
                neo.write ()
            give_star = input("Give a star? ")
            if give_star == "y":
                players[i][1] += 1
            else:
                continue
    else:  # THE CODE HERE RUNS FOR THE PLAYERS WHOS TURN IT ISNT
        print("player", i + 1, "is NOT moving")
