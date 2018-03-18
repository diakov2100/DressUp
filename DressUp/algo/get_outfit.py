"""
Description: Create an outfit consisting of two items - bottom (pants/skirt) and top
"""
from DressUp.algo.style_evaluator import evaluate_pure
#from style_evaluator import evaluate_pure

TYPES = ['shoes', 'top', 'bottom']

def select_best(outfit, clothes):
    min_metric = float("inf")
    min_id = 0
    for id, item in enumerate(clothes):
        metric = 0
        for outfit_item in outfit:
            metric += evaluate_pure(item['image'], outfit_item['image'])
        if metric < min_metric:
            min_metric = metric
            min_id = id
    return clothes[min_id]

def get_outfit(central_item,  clothes):
    """
        central_item: {
            image: instance of PIL.Image,
            type: string
        }
        clothes: [{
            image: instance of PIL.Image,
            type: string
        }]
        return: list[int] : indexes of items in the outfit in a clothes array
    """
    for i, item in enumerate(clothes):
        item['id'] = i
    left_types = TYPES[:]
    left_types.remove(central_item['type'])
    outfit = [central_item]
    for item_type in left_types:
        filtered_clothes = filter(lambda x: x['type'] == item_type, clothes)
        outfit.append(select_best(outfit, filtered_clothes))
    return [item['id'] for item in outfit[1:]]
