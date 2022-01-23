import random
from typing import List


class LstmState:
    def __init__(self, random_dirt_deltas: List[List[float]]):
        # one cleaner
        self.last_positions = [0]
        self.dirt_states = [0.0, 0.0, 0.0]
        self.sum_cost = 0
        # amount of dirt one cleaner is removing in one time window
        self.window_cleaning = 0.8
        self.allowed_dirt_threshold = 3
        self.current_time_window = 0
        self.random_dirt_deltas = random_dirt_deltas

    def update_loss(self, predicted: List[int]):
        last_current_positions = zip(self.last_positions, predicted)
        move_cost = sum(map(lambda x: 0 if x[0] == x[1] else 1, last_current_positions))
        # subtract dirt where cleaner was
        new_dirt_states = []
        cost_acc = move_cost
        for r_no, dirt_state in enumerate(self.dirt_states):
            after_cleaning = max(0.0, dirt_state - self.window_cleaning * sum(
                1 for pos in self.last_positions if pos == r_no))
            over_the_limit = max(0.0, dirt_state - self.allowed_dirt_threshold)
            cost_acc += over_the_limit
            room_dirt_delta = self.random_dirt_deltas[self.current_time_window][r_no]
            new_dirt_states.append(after_cleaning + room_dirt_delta)
        self.dirt_states = new_dirt_states
        self.sum_cost += cost_acc
        self.current_time_window += 1
        return self.sum_cost


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

state = LstmState(random_dirt_deltas)


def loss_function(actual: List[int], predicted: List[int]):
    return state.update_loss(predicted)


example_predicted = [[random.randint(0, 2) for i in state.last_positions] for j in random_dirt_deltas]

while state.current_time_window < len(random_dirt_deltas):
    loss_function([0], example_predicted[state.current_time_window])

print(state.sum_cost)
