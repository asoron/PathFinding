import numpy as np
import turtle as t
import random as r

screen = t.Screen()
screen.setup(800,800)

mapSize = 11

q_values = np.zeros((mapSize, mapSize, 4))

actions = ['up', 'right', 'down', 'left']

rewards = np.full ((mapSize, mapSize), -100.)

colons = {}
#Bitis Konumu
rx,ry = 0,5
rewards [rx, ry] = 100


#Harita Olusturma
aisles = {}
for i in range(mapSize-1):
    aisles[i]=[]
    for a in range(mapSize):
        colon = t.Turtle ()
        colon.penup ()
        colon.speed (10)
        colon.shape ("square")
        if (r.randint (0,3) <= 2):
            aisles[i].append(a)
            cor = str(a) + str(i)
            print(cor)
            colons[int(cor)] = colon
            colon.shape ("square")
            colon.setpos (a*40-200,-i*40+200)
            colon.color("cyan")
        else:
            colon.setpos (a * 40 - 200, -i * 40 + 200)
            colon.color ("red")
        if(a == ry and i == rx):
            colon.color("LightGreen")

for Y in range (1, 10):
    for X in aisles [Y]:
        rewards [Y, X] = -1

for row in rewards:
    print (row)




def is_terminal_state(current_row_index, current_column_index):
  if rewards[current_row_index, current_column_index] == -1.:
    return False
  else:
    return True

def get_starting_location():
  current_row_index = np.random.randint(mapSize)
  current_column_index = np.random.randint(mapSize)
  while is_terminal_state(current_row_index, current_column_index):
    current_row_index = np.random.randint(mapSize)
    current_column_index = np.random.randint(mapSize)
  return current_row_index, current_column_index

def get_next_action(current_row_index, current_column_index, epsilon):
  if np.random.random() < epsilon:
    return np.argmax(q_values[current_row_index, current_column_index])
  else:
    return np.random.randint(4)

def get_next_location(current_row_index, current_column_index, action_index):
  new_row_index = current_row_index
  new_column_index = current_column_index
  if actions[action_index] == 'up' and current_row_index > 0:
    new_row_index -= 1
  elif actions[action_index] == 'right' and current_column_index < mapSize - 1:
    new_column_index += 1
  elif actions[action_index] == 'down' and current_row_index < mapSize - 1:
    new_row_index += 1
  elif actions[action_index] == 'left' and current_column_index > 0:
    new_column_index -= 1
  return new_row_index, new_column_index

def get_shortest_path(start_row_index, start_column_index):
  if is_terminal_state(start_row_index, start_column_index):
    return []
  else:
    current_row_index, current_column_index = start_row_index, start_column_index
    shortest_path = []
    shortest_path.append([current_row_index, current_column_index])
    cor = int(str(start_column_index)+str(start_row_index))
    colons[cor].color("green")
    while not is_terminal_state(current_row_index, current_column_index):
        action_index = get_next_action(current_row_index, current_column_index, 1.)
        current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
        shortest_path.append([current_row_index, current_column_index])
        cor = int (str (current_column_index) + str (current_row_index))
        if(colons[cor] != None):
            colons [cor].color ("yellow")
    return shortest_path


epsilon = 0.9
discount_factor = 0.9
learning_rate = 0.9

for episode in range (1000):
    row_index, column_index = get_starting_location ()

    while not is_terminal_state (row_index, column_index):
        action_index = get_next_action (row_index, column_index, epsilon)

        old_row_index, old_column_index = row_index, column_index
        row_index, column_index = get_next_location (row_index, column_index, action_index)

        reward = rewards [row_index, column_index]
        old_q_value = q_values [old_row_index, old_column_index, action_index]
        temporal_difference = reward + (discount_factor * np.max (q_values [row_index, column_index])) - old_q_value

        new_q_value = old_q_value + (learning_rate * temporal_difference)
        q_values [old_row_index, old_column_index, action_index] = new_q_value

print ('Training complete!')

print(get_shortest_path(7, 9))


t.done()