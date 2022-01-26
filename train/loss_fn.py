from typing import List


class CostCalculator:
    def __init__(self, random_dirt_deltas: List[List[float]]):
        # amount of dirt one cleaner is removing in one time window
        self.window_cleaning = 0.3
        self.allowed_dirt_threshold = 3
        self.random_dirt_deltas = random_dirt_deltas

    def calc_cost(self, positions: List[List[int]]):
        last_positions = [i for i in range(0, len(positions[0]))]
        sum_cost = 0
        dirt_states = [0.0, 0.0, 0.0]
        for idx, time_window_positions in enumerate(positions):
            last_current_positions = zip(last_positions, time_window_positions)
            move_cost = sum(map(lambda x: 0 if x[0] == x[1] else 1, last_current_positions))
            # subtract dirt where cleaner was
            new_dirt_states = []
            cost_acc = move_cost
            for r_no, dirt_state in enumerate(dirt_states):
                after_cleaning = max(0.0, dirt_state - self.window_cleaning * sum(
                    1 for pos in last_positions if pos == r_no))
                over_the_limit = max(0.0, dirt_state - self.allowed_dirt_threshold)
                cost_acc += over_the_limit
                room_dirt_delta = self.random_dirt_deltas[idx][r_no]
                new_dirt_states.append(after_cleaning + room_dirt_delta)
            dirt_states = new_dirt_states
            sum_cost += cost_acc
            last_positions = time_window_positions
        return sum_cost


random_dirt_deltas = [
    [0.365, 0.376, 0.379],  # 0
    [0.314, 0.394, 0.416],  # 0
    [0, 0.387, 0.324],  # 0
    [0, 0.434, 0.333],  # 2
    [0, 0.324, 0.402],  # 2
    [0, 0.395, 0.449],  # 2
    [0, 0.388, 0.344],  # 1
    [0.371, 0.439, 0.416],  # 1
    [0.486, 0, 0.448],  # 1
    [0.332, 0, 0.488],  # 0
    [0.405, 0, 0.43],  # 0
    [0.469, 0, 0.353],  # 2
    [0.372, 0, 0.421],  # 2
    [0.467, 0, 0.456],  # 2
    [0.486, 0.325, 0],  # 0
    [0.302, 0.305, 0],  # 0
    [0.304, 0.453, 0],  # 1
    [0.345, 0.363, 0]  # 2
]

cost_calculator = CostCalculator(random_dirt_deltas)

positions = [[0], [2], [2], [2], [1], [1], [1], [0], [0], [2], [2], [2], [0], [0], [1], [2]]

sum_cost = cost_calculator.calc_cost(positions)

print(sum_cost)
