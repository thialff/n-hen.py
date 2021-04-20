import math


def slice_array(array, num_of_slices):
    """Slices `array` into `num_of_slices` parts of equal length and returns an array containing those parts.
    Should the number of elements in `array` not be divisible by `num_of_slices` the last entry of the returned array will have fewer elements."""
    length = len(array)
    segment_length = int(math.ceil(length / num_of_slices))
    slices = []
    for i in range(num_of_slices):
        lower = segment_length * i
        upper = min(segment_length * (i + 1), length + 1)
        slices.append(array[lower:upper])
    return slices
