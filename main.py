from database import create_tables
from services import (
    add_farmer,
    view_farmers,
    search_farmer,
    update_farmer,
    delete_farmer,
    add_field,
    view_fields,
    search_fields,
    update_field,
    delete_field,
    add_crop_plan,
    view_crop_plans,
    search_crop_plans,
    update_crop_plan,
    delete_crop_plan,
    add_activity,
    view_activities,
    search_activities,
    update_activity,
    delete_activity,
)


#! Displays the main menu of the application
def display_main_menu():
    print("\n" + "-" * 40)
    print(" SMART CROP PLANNING AND FARM RECORD SYSTEM ")
    print("\n" + "-" * 40)

    print("1. Farmer Management")
    print("2. Field Management")
    print("3. Crop Planning")
    print("4. Farming Activities")
    print("5. Expense Management")
    print("6. Harvest and Revenue")
    print("7. Reports and Analysis")
    print("8. Exit")
    print("\n" + "-" * 40)


#! Displays options available under Farmer Management
def display_farmer_menu():
    print("\n" + "-" * 40)
    print("\n>>> FARMER MANAGEMENT <<<")
    print("\n" + "-" * 40)
    print("1. Add Farmer")
    print("2. View Farmers")
    print("3. Search Farmer")
    print("4. Update Farmer")
    print("5. Delete Farmer")
    print("6. Back")
    print("\n" + "-" * 40)


#! Displays options available under Field Management
def display_field_menu():
    print("\n" + "-" * 40)
    print("\n>>> FIELD MANAGEMENT <<<")
    print("\n" + "-" * 40)

    print("1. Add Field")
    print("2. View Fields")
    print("3. Search Field")
    print("4. Update Field")
    print("5. Delete Field")
    print("6. Back")

    print("\n" + "-" * 40)


#! Displays options available under Crop Planning
def display_crop_menu():
    print("\n" + "-" * 40)
    print("\n>>> CROP PLANNING <<<")
    print("\n" + "-" * 40)

    print("1. Add Crop Plan")
    print("2. View Crop Plans")
    print("3. Search Crop Plan")
    print("4. Update Crop Plan")
    print("5. Delete Crop Plan")
    print("6. Back")

    print("\n" + "-" * 40)


#! Displays options available under Farming Activities
def display_activity_menu():
    print("\n" + "-" * 40)
    print("\n>>> FARMING ACTIVITIES <<<")
    print("\n" + "-" * 40)
    print("1. Add Activity")
    print("2. View Activities")
    print("3. Search Activity")
    print("4. Update Activity")
    print("5. Delete Activity")
    print("6. Back")
    print("\n" + "-" * 40)


#! Handles all Farmer Management operations
def farmer_management():
    while True:
        display_farmer_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            add_farmer()
        elif choice == "2":
            view_farmers()
        elif choice == "3":
            search_farmer()
        elif choice == "4":
            update_farmer()
        elif choice == "5":
            delete_farmer()
        elif choice == "6":
            print("\nReturning to Main Menu...")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 6.")


#! Handles all Field Management operations
def field_management():
    while True:
        display_field_menu()

        choice = input("Enter your choice: ")
        if choice == "1":
            add_field()
        elif choice == "2":
            view_fields()
        elif choice == "3":
            search_fields()
        elif choice == "4":
            update_field()
        elif choice == "5":
            delete_field()
        elif choice == "6":
            print("\nReturning to Main Menu...")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 6.")


#! Handles all Crop Planning operations
def crop_planning():
    while True:
        display_crop_menu()
        choice = input("Enter Your Choice: ").strip()

        if choice == "1":
            add_crop_plan()
        elif choice == "2":
            view_crop_plans()
        elif choice == "3":
            search_crop_plans()
        elif choice == "4":
            update_crop_plan()
        elif choice == "5":
            delete_crop_plan()
        elif choice == "6":
            print("\nReturning to Main Menu.......")
            break
        else:
            print("\nThis feature will be added soon.")


#! Handles all Farming Activities operations


def farming_activities():
    while True:
        display_activity_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_activity()
        elif choice == "2":
            view_activities()
        elif choice == "3":
            search_activities()
        elif choice == "4":
            update_activity()
        elif choice == "5":
            delete_activity()
        elif choice == "6":
            print("\nReturning to Main Menu...")
            break
        else:
            print("\nThis option is not available yet.")


#! Starts the application and controls the main menu flow
def main():
    create_tables()

    while True:
        display_main_menu()
        choice = input("Enter Your Choice: ")
        if choice == "1":
            farmer_management()
        elif choice == "2":
            field_management()
        elif choice == "3":
            crop_planning()
        elif choice == "4":
            farming_activities()
        elif choice == "5":
            print("\n>>> EXPENSE MANAGEMENT SELECTED <<<")
        elif choice == "6":
            print("\n>>> HARVEST AND REVENUE SELECTED <<<")
        elif choice == "7":
            print("\n>>> REPORTS AND ANALYSIS SELECTED <<<")
        elif choice == "8":
            print("\nThank you for using the system!")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
