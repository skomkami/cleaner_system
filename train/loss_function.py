import random
from typing import List

# one cleaner
last_positions = [0]
dirt_states = [0.0, 0.0, 0.0]
sum_cost = 0
# amount of dirt one cleaner is removing in one time window
window_cleaning = 0.8
allowed_dirt_threshold = 3

random_dirt_deltas = [
    [0.365, 0.376, 0.379],
    [0.314, 0.394, 0.416],
    [0, 0.387, 0.324],
    [0, 0.434, 0.333],
    [0, 0.324, 0.402],
    [0, 0.395, 0.449],
    [0, 0.388, 0.344],
    [0.371, 0.439, 0.416],
    [0.486, 0, 0.448],
    [0.332, 0, 0.488],
    [0.405, 0, 0.43],
    [0.469, 0, 0.353],
    [0.372, 0, 0.421],
    [0.467, 0, 0.456],
    [0.486, 0.325, 0],
    [0.302, 0.305, 0],
    [0.304, 0.453, 0],
    [0.345, 0.362, 0]
]

current_time_window = 0


def loss_function(actual: List[int], predicted: List[int]):
    last_current_positions = zip(last_positions, predicted)
    move_cost = sum(map(lambda x: 0 if x[0] == x[1] else 1, last_current_positions))
    # subtract dirt where cleaner was
    new_dirt_states = []
    cost_acc = move_cost
    for r_no, dirt_state in enumerate(dirt_states):
        after_cleaning = max(0.0, dirt_state - window_cleaning * sum(1 for pos in last_positions if pos == r_no))
        over_the_limit = max(0.0, dirt_state - allowed_dirt_threshold)
        cost_acc += over_the_limit
        room_dirt_delta = random_dirt_deltas[current_time_window][r_no]
        new_dirt_states.append(after_cleaning + room_dirt_delta)
    sum_cost += cost_acc


example_predicted = [[random.randint(0, 2) for i in last_positions] for j in random_dirt_deltas]

while current_time_window < len(random_dirt_deltas):
    loss_function([0], example_predicted[current_time_window])
    current_time_window += 1

print(sum_cost)