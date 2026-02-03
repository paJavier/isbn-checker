def clean_isbn(isbn):
    return isbn.replace("-", "").replace(" ", "")

def compute_check_digit(isbn9):
    total = 0
    weight = 10

    for digit in isbn9:
        total += int(digit) * weight
        weight -= 1

    check_digit = (11 - (total % 11)) % 11
    return "X" if check_digit == 10 else str(check_digit)

def is_valid_isbn10(isbn):
    isbn = clean_isbn(isbn)

    if len(isbn) != 10 or not isbn[:9].isdigit():
        return False

    total = 0
    weight = 10

    for i in range(10):
        value = 10 if isbn[i] == "X" else int(isbn[i])
        total += value * weight
        weight -= 1

    return total % 11 == 0

def single_test():
    isbn = input("\nEnter ISBN-10: ")
    cleaned = clean_isbn(isbn)

    if len(cleaned) != 10 or not cleaned[:9].isdigit():
        print("\nInvalid ISBN format.")
        input("\nPress Enter to return to the menu...")
        return

    if is_valid_isbn10(isbn):
        print("\nResult: VALID ISBN ✅")
    else:
        correct_digit = compute_check_digit(cleaned[:9])
        print("\nResult: INVALID ISBN ❌")
        print("Correct check digit is:", correct_digit)
        print("Correct ISBN-10 is:", cleaned[:9] + correct_digit)

    input("\nPress Enter to return to the menu...")

def batch_test():
    print("\nBatch ISBN-10 Testing")
    print("Enter ISBN-10 numbers one per line.")
    print("Press ENTER on an empty line to finish.\n")

    isbns = []

    while True:
        isbn = input("ISBN: ").strip()
        if isbn == "":
            break
        isbns.append(isbn)

    if not isbns:
        print("\nNo ISBNs entered.")
        input("\nPress Enter to return to the menu...")
        return

    print("\n--- Batch Test Results ---")
    for isbn in isbns:
        cleaned = clean_isbn(isbn)

        if len(cleaned) != 10 or not cleaned[:9].isdigit():
            print(f"{isbn} → Invalid format")
            continue

        if is_valid_isbn10(isbn):
            print(f"{isbn} → VALID")
        else:
            correct_digit = compute_check_digit(cleaned[:9])
            print(f"{isbn} → INVALID (correct digit: {correct_digit})")

    input("\nPress Enter to return to the menu...")

def main():
    print("ISBN-10 Checker and Fixer")
    print("--------------------------")

    while True:
        print("\nOptions:")
        print("1. Check single ISBN-10")
        print("2. Batch ISBN-10 testing")
        print("3. Exit")

        choice = input("Choose an option (1, 2, or 3): ").strip()

        if choice == "1":
            single_test()

        elif choice == "2":
            batch_test()

        elif choice == "3":
            print("\nProgram terminated. Thank you!")
            break

        else:
            print("\nInvalid option.")
            input("Press Enter to try again...")

if __name__ == "__main__":
    main()

