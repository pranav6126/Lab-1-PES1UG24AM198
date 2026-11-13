import re


def average_marks(marks_csv):
    """Return the average of integer marks (0-100), or None if invalid."""
    if not isinstance(marks_csv, str) or not marks_csv.strip():
        return None
    marks = []
    for token in marks_csv.split(','):
        token = token.strip()
        if re.fullmatch(r'[0-9]{1,3}', token) is None:
            return None
        mark = int(token)
        if mark > 100:
            return None
        marks.append(mark)
    return round(sum(marks) / len(marks), 2)


def parse_srn(srn):
    """Parse PES<campus>UG<year><department><number>; invalid input returns None."""
    if not isinstance(srn, str):
        return None
    match = re.fullmatch(r'(PES[0-9])UG([0-9]{2})([A-Z]{2})[0-9]{3}', srn.strip())
    if match is None:
        return None
    return match.group(1), int(match.group(2)), match.group(3)


def short_name(full_name):
    """Abbreviate a two-part alphabetic name, or return None if invalid."""
    if not isinstance(full_name, str):
        return None
    parts = full_name.split()
    if len(parts) != 2 or not all(part.isalpha() for part in parts):
        return None
    first, last = parts
    return first[0].upper() + ". " + last.capitalize()


def main():
    print("==== Running average_marks ====")
    user_input = input("Enter marks as CSV (e.g. 78,85,92): ")
    result = average_marks(user_input)
    print("Average Marks:", result if result is not None else "Invalid marks")

    print("\n==== Running parse_srn ====")
    user_input = input("Enter an SRN (e.g. PES1UG23CS123): ")
    result = parse_srn(user_input)
    print("Campus, Year and Dept:", result if result is not None else "Invalid SRN")

    print("\n==== Running short_name ====")
    user_input = input("Enter first and last name (e.g. ravi kumar): ")
    result = short_name(user_input)
    print("Short Name:", result if result is not None else "Invalid name")


if __name__ == "__main__":
    main()
