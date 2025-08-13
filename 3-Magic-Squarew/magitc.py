def generate_odd_magic_square(n):
    matrix = [[0] * n for _ in range(n)]
    row = n // 2
    col = n - 1

    for num in range(1, n * n + 1):
        matrix[row][col] = num

        if num % n == 0:
            col -= 1
        else:
            row -= 1
            col += 1

        row = (row + n) % n
        col = (col + n) % n

    return matrix


def generate_doubly_even_magic_square(n):
    matrix = [[0] * n for _ in range(n)]
    num = 1

    for i in range(n):
        for j in range(n):
            matrix[i][j] = num
            num += 1

    for i in range(n):
        for j in range(n):
            if (i % 4 == j % 4) or ((i % 4) + (j % 4) == 3):
                matrix[i][j] = n * n + 1 - matrix[i][j]

    return matrix


def generate_singly_even_magic_square(n):
    half_size = n // 2
    sub_square_size = half_size * half_size

    sub_square = generate_odd_magic_square(half_size)
    matrix = [[0] * n for _ in range(n)]

    for i in range(half_size):
        for j in range(half_size):
            value = sub_square[i][j]
            matrix[i][j] = value
            matrix[i + half_size][j + half_size] = value + sub_square_size
            matrix[i][j + half_size] = value + 2 * sub_square_size
            matrix[i + half_size][j] = value + 3 * sub_square_size

    k = (n - 2) // 4

    for i in range(half_size):
        for j in range(k):
            matrix[i][j], matrix[i + half_size][j] = matrix[i + half_size][j], matrix[i][j]

        for j in range(n - k + 1, n):
            matrix[i][j], matrix[i + half_size][j] = matrix[i + half_size][j], matrix[i][j]

    matrix[k][0], matrix[k + half_size][0] = matrix[k + half_size][0], matrix[k][0]
    matrix[k][k], matrix[k + half_size][k] = matrix[k + half_size][k], matrix[k][k]

    return matrix


def generate_magic_square(n):
    if n % 2 == 1:
        return generate_odd_magic_square(n)
    elif n % 4 == 0:
        return generate_doubly_even_magic_square(n)
    else:
        return generate_singly_even_magic_square(n)


def main():
    n = int(input("Enter order of magic square: "))

    if n < 3:
        print("Magic square not possible for n < 3")
        return

    magic_square = generate_magic_square(n)

    for row in magic_square:
        for num in row:
            print(num, end=" ")
        print()


if __name__ == "__main__":
    main()