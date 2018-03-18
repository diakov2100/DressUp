"""
Description: Create an outfit consisting of two items - bottom (pants/skirt) and top
"""
#from DressUp.algo.style_evaluator import evaluate_pure
from style_evaluator import evaluate_pure

TYPES = ['shoes', 'top', 'bottom']

def select_best(central_item, outfit, clothes):
    min_metric = float("inf")
    min_item = None
    for item in clothes:
        metric = 0
        metric += evaluate_pure(item['features'], central_item['features'])
        for outfit_item in outfit:
            metric += evaluate_pure(item['features'], outfit_item['features'])
        if metric < min_metric:
            min_metric = metric
            min_item = item
    return min_item

def get_outfit(central_item, clothes):
    """
        central_item: {
            features: result of preprocessing via load_and_preprocess_image_from_url 
                or load_and_preprocess_image,
            type: string
        }
        clothes: [{
            id: string : id from database,
            features: result of preprocessing via load_and_preprocess_image_from_url 
                or load_and_preprocess_imag,
            type: string
        }]
        return: list[int] : indexes of items in the outfit in a clothes array
    """
    left_types = TYPES[:]
    left_types.remove(central_item['type'])
    outfit = []
    for item_type in left_types:
        filtered_clothes = filter(lambda x: x['type'] == item_type, clothes)
        print('Left {} {}'.format(len(filtered_clothes), item_type))
        outfit.append(select_best(central_item, outfit, filtered_clothes))
    return [item['id'] for item in outfit]
