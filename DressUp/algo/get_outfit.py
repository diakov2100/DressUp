"""
Description: Create an outfit consisting of two items - bottom (pants/skirt) and top
"""

def get_outfit(img, clothes):
    """
        img: instance of PIL.Image : start point of img
        clothes: [{
            img: instance of PIL.Image,
            type: string
        }]
        return: list[int] : indexes of items in the outfit in a clothes array
    """
    return [1, 2]