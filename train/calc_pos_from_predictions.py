from typing import List

predictions = [
    [-0.092668],
    [-0.10471054],
    [-0.08102176],
    [-0.0713949],
    [-0.07959006],
    [-0.08777147],
    [-0.09291182],
    [-0.08826579],
    [-0.10431632],
    [-0.09256671],
    [-0.08969969],
    [-0.09710778],
    [-0.09112241],
    [-0.0865535],
    [-0.08653311],
    [-0.09429237],
    [-0.07833327],
    [-0.08242852]
]


def calc_pos_from_pred(predictions: List[List[float]], no_classes: int):
    minp = min(min(predictions, key=min))
    print(minp)
    maxp = max(max(predictions, key=max))
    print(maxp)
    diff = maxp - minp
    class_distance = diff / (no_classes - 1)
    to_class = lambda pred: round((pred - minp) / class_distance)
    return [[to_class(ix) for ix in x] for x in predictions]



result = calc_pos_from_pred(predictions, 3)

print(result)
