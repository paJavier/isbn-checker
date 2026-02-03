# ISBN-10 Checker and Correct Check Digit Generator (Loop Version)

def clean_isbn(isbn):
    """Remove hyphens and spaces"""
    return isbn.replace("-", "").replace(" ", "")

def compute_check_digit(isbn9):
    """Compute the correct ISBN-10 check digit"""
    total = 0
    weight = 10

    for digit in isbn9:
        total += int(digit) * weight
        weight -= 1

    check_digit = (11 - (total % 11)) % 11
    return "X" if check_digit == 10 else str(check_digit)

def is_valid_isbn10(isbn):
    """Check if ISBN-10 is valid"""
    isbn = clean_isbn(isbn)

    if len(isbn) != 10 or not isbn[:9].isdigit():
        return False

    total = 0
    weight = 10

    for i in range(10):
        if isbn[i] == "X":
            value = 10
        else:
            value = int(isbn[i])

        total += value * weight
        weight -= 1

    return total % 11 == 0

def main():
    print("ISBN-10 Checker and Fixer")
    print("--------------------------")

    while True:
        print("\nOptions:")
        print("1. Check ISBN-10")
        print("2. Exit")

        choice = input("Choose an option (1 or 2): ").strip()

        if choice == "2":
            print("\nProgram terminated. Thank you!")
            break

        elif choice == "1":
            isbn = input("\nEnter ISBN-10: ")
            cleaned = clean_isbn(isbn)

            if len(cleaned) != 10 or not cleaned[:9].isdigit():
                print("Invalid ISBN format. Please try again.")
                continue

            if is_valid_isbn10(isbn):
                print("\nResult: VALID ISBN ✅")
            else:
                correct_digit = compute_check_digit(cleaned[:9])
                print("\nResult: INVALID ISBN ❌")
                print("Correct check digit is:", correct_digit)
                print("Correct ISBN-10 is:", cleaned[:9] + correct_digit)

        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
