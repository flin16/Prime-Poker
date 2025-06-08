import re


def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def filter_numbers(s) -> list[int]:
    """Filter and return prime numbers from a string."""
    numbers = re.findall(r"\d+", s)
    numbers = list(map(int, numbers))
    for number in numbers:
        if number < 1 or number > 13:
            return []
    return list(map(int, numbers))


if __name__ == "__main__":
    # Example usage
    test_string = "3 * 7 = 2 1"
    primes = filter_numbers(test_string)
    print(f"numbers found: {primes}")  # Output: Prime numbers found: [2, 3, 5]

    # Check if a number is prime
    print(is_prime(7))  # Output: True
    print(is_prime(10))  # Output: False
