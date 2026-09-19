from datetime import datetime
# Gets text input and ensures that it is not empty
def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


# Gets and validates a farmer's name
def get_name(prompt):
    while True:
        name = get_non_empty_input(prompt)

        if name.replace(" ", "").isalpha():
            return name

        print("Please enter a valid name.")


# Gets and validates a 10-digit phone number
def get_phone(prompt):
    while True:
        phone = get_non_empty_input(prompt)

        if phone.isdigit() and len(phone) == 10:
            return phone

        print("Please enter a valid 10-digit phone number.")


def get_location(prompt):
    while True:
        location = get_non_empty_input(prompt)
        if any(char.isalpha() for char in location):
            return location
        print("Please enter a valid location.")


def get_positive_number(prompt):
    while True:
        value = get_non_empty_input(prompt)
        try:
            number = float(value)
            if number > 0:
                return number
            else:
                print("Please enter a number greater than 0.")
        except ValueError:
            print("Please enter a valid number.")


# Gets text input and ensures it contains at least one letter
def get_text_input(prompt):
    while True:
        text = get_non_empty_input(prompt)

        if any(char.isalpha() for char in text):
            return text

        print("Please enter valid text.")


# Gets a value from a predefined list of choices
def get_choice(prompt, choices):
    while True:
        print()

        for index, choice in enumerate(choices, start=1):
            print(f"{index}. {choice}")
        value = get_non_empty_input(prompt)

        if value.isdigit():
            choice_number = int(value)
            if 1 <= choice_number <= len(choices):
                return choices[choice_number - 1]

        print("Please select a valid option.")

# Gets and validates a date in YYYY-MM-DD format
def get_date(prompt):
    while True:
        date= get_non_empty_input(prompt)
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print("Please Enter a valid date in YYYY-MM-DD format.")