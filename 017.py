array = [
    [1, 1, 2],
    [1, 1, 2],
    [3, 3, 3],
]

value_coordinates = {}
square_dimensions = {}


def grid(arr):
    for y in range(len(arr)):
        for x in range(len(arr[y])):
            value = arr[y][x]
            if value not in value_coordinates:
                value_coordinates[value] = [(y, x), (y + 1, x + 1)]
            else:
                value_coordinates[value][1] = (y + 1, x + 1)

    for key, value in value_coordinates.items():
        square_dimensions[key] = [value[1][0] - value[0][0], value[1][1] - value[0][1]]


grid(array)
for key, value in square_dimensions.items():
    print(key, value)
