from database import create_tables
import services


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


#! Displays options available under Expense Management
def expense_management_menu():
    print("\n" + "-" * 40)
    print("\n>>> EXPENSE MANAGEMENT <<<")
    print("\n" + "-" * 40)

    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Search Expense")
    print("4. Update Expense")
    print("5. Delete Expense")
    print("6. Back")
    print("\n" + "-" * 40)


#! Displays options available under Harvest and Revenue Management
def harvest_revenue_menu():
    while True:
        print("\n===== HARVEST AND REVENUE =====")
        print("1. Harvest Management")
        print("2. Revenue Management")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            harvest_management()
        elif choice == "2":
            revenue_management()
        elif choice == "3":
            break
        else:
            print("\nInvalid choice. Please try again.")


#! Handles all Farmer Management operations
def farmer_management():
    while True:
        display_farmer_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            services.add_farmer()
        elif choice == "2":
            services.view_farmers()
        elif choice == "3":
            services.search_farmer()
        elif choice == "4":
            services.update_farmer()
        elif choice == "5":
            services.delete_farmer()
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
            services.add_field()
        elif choice == "2":
            services.view_fields()
        elif choice == "3":
            services.search_fields()
        elif choice == "4":
            services.update_field()
        elif choice == "5":
            services.delete_field()
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
            services.add_crop_plan()
        elif choice == "2":
            services.view_crop_plans()
        elif choice == "3":
            services.search_crop_plans()
        elif choice == "4":
            services.update_crop_plan()
        elif choice == "5":
            services.delete_crop_plan()
        elif choice == "6":
            print("\nReturning to Main Menu.......")
            break
        else:
            print("\nInvalid choice. Please select a number from 1 to 6.")


#! Handles all Farming Activities operations
def farming_activities():
    while True:
        display_activity_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            services.add_activity()
        elif choice == "2":
            services.view_activities()
        elif choice == "3":
            services.search_activities()
        elif choice == "4":
            services.update_activity()
        elif choice == "5":
            services.delete_activity()
        elif choice == "6":
            print("\nReturning to Main Menu...")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 6.")


#! Handles all Expense Management operations
def expense_management():
    while True:
        expense_management_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            services.add_expense()
        elif choice == "2":
            services.view_expenses()
        elif choice == "3":
            services.search_expense()
        elif choice == "4":
            services.update_expense()
        elif choice == "5":
            services.delete_expense()
        elif choice == "6":
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 6.")


#! Handles all Harvest Management operations
def harvest_management():
    while True:
        print("\n===== HARVEST MANAGEMENT =====")
        print("1. Add Harvest")
        print("2. View Harvests")
        print("3. Search Harvest")
        print("4. Update Harvest")
        print("5. Delete Harvest")
        print("6. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            services.add_harvest()
        elif choice == "2":
            services.view_harvests()
        elif choice == "3":
            services.search_harvest()
        elif choice == "4":
            services.update_harvest()
        elif choice == "5":
            services.delete_harvest()
        elif choice == "6":
            break
        else:
            print("\nInvalid choice. Please try again.")


#! Handles all Revenue Management operations
def revenue_management():
    while True:
        print("\n===== REVENUE MANAGEMENT =====")
        print("1. Add Revenue")
        print("2. View Revenues")
        print("3. Search Revenue")
        print("4. Update Revenue")
        print("5. Delete Revenue")
        print("6. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            services.add_revenue()
        elif choice == "2":
            services.view_revenues()
        elif choice == "3":
            services.search_revenue()
        elif choice == "4":
            services.update_revenue()
        elif choice == "5":
            services.delete_revenue()
        elif choice == "6":
            break
        else:
            print("\nInvalid choice. Please try again.")


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
            expense_management()
        elif choice == "6":
            harvest_revenue_menu()
        elif choice == "7":
            print("\n>>> REPORTS AND ANALYSIS SELECTED <<<")
        elif choice == "8":
            print("\nThank you for using the system!")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
