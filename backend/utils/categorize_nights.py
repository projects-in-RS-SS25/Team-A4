def categorize_nights(n):
    if n == 1:
        return 0
    elif n == 2:
        return 1
    elif 3 <= n <= 4:
        return 2
    elif 5 <= n <= 10:
        return 3
    else:
        return 4
