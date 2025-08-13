import math

jug_x_capacity = 0
jug_y_capacity = 0
current_x = 0
current_y = 0


def fill_jug_x():
    global current_x
    current_x = jug_x_capacity


def fill_jug_y():
    global current_y
    current_y = jug_y_capacity


def empty_jug_x():
    global current_x
    current_x = 0


def empty_jug_y():
    global current_y
    current_y = 0


def pour_x_into_y():
    global current_x, current_y
    pour_amount = min(current_x, jug_y_capacity - current_y)
    current_x -= pour_amount
    current_y += pour_amount


def pour_y_into_x():
    global current_x, current_y
    pour_amount = min(current_y, jug_x_capacity - current_x)
    current_y -= pour_amount
    current_x += pour_amount


def goal_reached(target):
    return current_x == target or current_y == target


def solve_water_jug(target):
    global current_x, current_y
    current_x = 0
    current_y = 0

    while not goal_reached(target):
        if current_x == 0:
            fill_jug_x()
        elif current_y == jug_y_capacity:
            empty_jug_y()
        else:
            pour_x_into_y()

        print(f"({current_x}, {current_y})")


def main():
    global jug_x_capacity, jug_y_capacity, current_x, current_y

    jug_x_capacity = int(input("Enter capacity of jug x: "))
    jug_y_capacity = int(input("Enter capacity of jug y: "))
    target_volume = int(input("Enter goal volume: "))

    gcd_value = math.gcd(jug_x_capacity, jug_y_capacity)

    if target_volume > max(jug_x_capacity, jug_y_capacity) or target_volume % gcd_value != 0:
        print("Goal not achievable with given jug sizes.")
        return

    print("Starting state:")
    print(f"({current_x}, {current_y})")

    solve_water_jug(target_volume)
    print(f"Goal {target_volume} reached.")


if __name__ == "__main__":
    main()