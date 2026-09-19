import sqlite3
from datetime import datetime
from database import get_conn
from validators import (
    get_phone,
    get_name,
    get_location,
    get_positive_number,
    get_text_input,
    get_choice,
    get_date,
)

#! FARMER MANAGEMENT


#! Adds a new farmer to the database
def add_farmer():
    print("\n>>> ADD FARMER <<<")
    name = get_name("Enter farmer name: ")
    phone = get_phone("Enter phone number: ")
    location = get_location("Enter location: ")

    connection = get_conn()
    cursor = connection.cursor()

    add_query = """INSERT INTO farmers (name, phone, location) VALUES (?, ?, ?)"""
    cursor.execute(add_query, (name, phone, location))
    connection.commit()
    connection.close()

    print("\nFarmer Added Successfully!")


#! Displays all farmers stored in the database
def view_farmers():
    connection = get_conn()
    cursor = connection.cursor()

    view_query = """SELECT farmer_id, name, phone, location FROM farmers"""
    cursor.execute(view_query)

    farmers = cursor.fetchall()
    connection.close()

    if not farmers:
        print("\nNo farmers Found.")
        return
    print("\n>>> FARMER LIST <<<")

    for farmer in farmers:
        print(
            f"Farmer_ID: {farmer[0]} |"
            f"Name: {farmer[1]} |"
            f"Phone: {farmer[2]} |"
            f"Location: {farmer[3]} |"
        )


#! Searches for a farmer by name or phone number
def search_farmer():
    print("\n>>> SEARCH FARMER <<<")
    search_value = input("Enter Farmer name or phone number: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    query = """ SELECT farmer_id, name, phone, location FROM farmers WHERE name LIKE ? OR phone LIKE ? """
    search_pattern = f"%{search_value}%"

    cursor.execute(query, (search_pattern, search_pattern))

    farmers = cursor.fetchall()

    connection.close()

    if not farmers:
        print("\nNo matching farmer found.")
        return
    for farmer in farmers:
        print(
            f"ID: {farmer[0]} | "
            f"Name: {farmer[1]} | "
            f"Phone: {farmer[2]} | "
            f"Location: {farmer[3]}"
        )


#! Updates an existing farmer's information
def update_farmer():
    print("\n>>> UPDATE FARMER <<<")
    farmer_id = input("Enter Farmer ID: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    query = (
        """SELECT farmer_id, name, phone, location FROM farmers WHERE farmer_id= ?"""
    )

    cursor.execute(query, (farmer_id,))

    farmer = cursor.fetchone()

    if not farmer:
        print("\nFarmer Not Found")
        connection.close()
        return
    print("\nCurrent Farmer Information:")
    print(f"ID: {farmer[0]}")
    print(f"Name: {farmer[1]}")
    print(f"Phone: {farmer[2]}")
    print(f"Location: {farmer[3]}")

    print("\nWhat would you like to update?")
    print("1. Name")
    print("2. Phone")
    print("3. Location")
    print("4. All Information")
    print("5. Cancel")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        name = get_name("Enter new farmer name: ")

        update_query = """
            UPDATE farmers
            SET name = ?
            WHERE farmer_id = ?
        """
        cursor.execute(update_query, (name, farmer_id))

        connection.commit()

        print("\nFarmer name updated successfully!")

    elif choice == 2:
        phone = get_phone("Enter new phone number: ")

        update_query = """ UPDATE farmers SET phone=? WHERE farmer_id=?"""

        cursor.execute(update_query, (phone, farmer_id))

        connection.commit()

        print("\nFarmer Phone number updated successfully!")

    elif choice == "3":
        location = get_location("Enter new location: ")

        update_query = """ UPDATE farmers SET location = ? WHERE farmer_id = ? """

        cursor.execute(update_query, (location, farmer_id))

        connection.commit()

        print("\nFarmer location updated successfully!")
    elif choice == "4":
        print("\nEnter new farmer information:")

        name = get_name("Enter new farmer name: ")
        phone = get_phone("Enter new phone number: ")
        location = get_location("Enter new location: ")

        update_query = """
            UPDATE farmers
            SET name = ?, phone = ?, location = ?
            WHERE farmer_id = ?
        """

        cursor.execute(update_query, (name, phone, location, farmer_id))

        connection.commit()

        print("\nFarmer information updated successfully!")

    elif choice == "5":
        print("\nUpdate cancelled.")
    else:
        print("\nInvalid choice. Please enter a number from 1 to 5.")

    connection.close()


#! Deletes an existing farmer from the database
def delete_farmer():
    print("\n>>> DELETE FARMER <<<")

    farmer_id = input("Enter farmer ID: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT farmer_id, name, phone, location
        FROM farmers
        WHERE farmer_id = ?
    """

    cursor.execute(query, (farmer_id,))

    farmer = cursor.fetchone()

    if not farmer:
        print("\nFarmer not found.")
        connection.close()
        return

    print("\nFarmer Information:")
    print(f"ID: {farmer[0]}")
    print(f"Name: {farmer[1]}")
    print(f"Phone: {farmer[2]}")
    print(f"Location: {farmer[3]}")

    confirmation = (
        input("\nAre you sure you want to delete this farmer? (y/n): ").strip().lower()
    )

    if confirmation != "y":
        print("\nDeletion cancelled.")
        connection.close()
        return

    delete_query = """ DELETE FROM farmers WHERE farmer_id=?"""
    cursor.execute(delete_query, (farmer_id,))

    connection.commit()
    print("\nFarmer deleted Successfully!")

    connection.close()


#!FIELD MANAGEMENT

area_units = [
    "Ropani",
    "Aana",
    "Bigha",
    "Kattha",
    "Dhur",
    "Hectare",
    "Square Meter",
]

soil_types = ["Sandy", "Clay", "Loamy", "Silty", "Sandy Loam", "Clay Loam"]

irrigation_types = [
    "Rainfed",
    "Canal",
    "Tube Well",
    "Borewell",
    "Drip",
    "Sprinkler",
    "Pond",
]


#! Adds a new field for an existing farmer
def add_field():
    print("\n>>> ADD FIELD <<<")

    farmer_id = input("Enter farmer ID: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    # Check whether the farmer exists
    query = """
        SELECT farmer_id, name
        FROM farmers
        WHERE farmer_id = ?
    """

    cursor.execute(query, (farmer_id,))
    farmer = cursor.fetchone()

    # Stop if farmer does not exist
    if not farmer:
        print("\nFarmer not found. Please enter a valid farmer ID.")
        connection.close()
        return

    # Display selected farmer
    print(f"\nFarmer selected: {farmer[1]}")

    # Get field information
    field_name = get_text_input("Enter field name: ")

    area = get_positive_number("Enter field area: ")

    area_unit = get_choice("Select area unit: ", area_units)

    soil_type = get_choice("Select soil type: ", soil_types)

    irrigation = get_choice("Select irrigation type: ", irrigation_types)
    # Insert field information into the database
    query = """
        INSERT INTO fields
        (farmer_id, field_name, area, area_unit, soil_type, irrigation)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    cursor.execute(
        query, (farmer_id, field_name, area, area_unit, soil_type, irrigation)
    )

    connection.commit()
    connection.close()

    print("\nField added successfully!")


#! Displays all fields stored in the database
def view_fields():
    connection = get_conn()
    cursor = connection.cursor()

    query = """SELECT f.field_id, fr.name, f.field_name,f.area, f.area_unit, f.soil_type, f.irrigation
            FROM fields AS f
            INNER JOIN farmers AS fr ON f.farmer_id = fr.farmer_id"""

    cursor.execute(query)
    fields = cursor.fetchall()

    connection.close()

    if not fields:
        print("\nNo fields found.")
        return
    print(">>> FIELD LIST <<<")
    for field in fields:
        print(
            f"ID: {field[0]} | "
            f"Farmer: {field[1]} | "
            f"Field: {field[2]} | "
            f"Area: {field[3]} {field[4]} | "
            f"Soil: {field[5]} | "
            f"Irrigation: {field[6]}"
        )


# Searches for a field by field name or farmer name
def search_fields():
    print("\n>>> SEARCH FIELD <<<")
    search_value = input("Enter Field Name or Farmer Name: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT f.field_id, fr.name, f.field_name, f.area, f.area_unit, f.soil_type, f.irrigation
        FROM fields AS f
        INNER JOIN farmers as fr
        ON f.farmer_id= fr.farmer_id
        WHERE f.field_name LIKE ?
        OR fr.name LIKE ?
    """
    search_pattern = f"%{search_value}%"

    cursor.execute(query, (search_pattern, search_pattern))
    fields = cursor.fetchall()

    connection.close()

    if not fields:
        print("\nNo matching field found.")
        return

    for field in fields:
        print(
            f"ID: {field[0]} | "
            f"Farmer: {field[1]} | "
            f"Field: {field[2]} | "
            f"Area: {field[3]} {field[4]} | "
            f"Soil: {field[5]} | "
            f"Irrigation: {field[6]}"
        )


#! Updates an existing field's information
def update_field():
    print("\n>>> UPDATE FIELD <<<")

    field_id = input("Enter field ID: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT f.field_id,
               fr.name,
               f.field_name,
               f.area,
               f.area_unit,
               f.soil_type,
               f.irrigation
        FROM fields AS f
        INNER JOIN farmers AS fr
            ON f.farmer_id = fr.farmer_id
        WHERE f.field_id = ?
    """

    cursor.execute(query, (field_id,))

    field = cursor.fetchone()

    if not field:
        print("\nField not found.")
        connection.close()
        return

    print("\nCurrent Field Information:")
    print(f"ID: {field[0]}")
    print(f"Farmer: {field[1]}")
    print(f"Field Name: {field[2]}")
    print(f"Area: {field[3]} {field[4]}")
    print(f"Soil Type: {field[5]}")
    print(f"Irrigation: {field[6]}")

    print("\nWhat would you like to update?")
    print("1. Field Name")
    print("2. Area")
    print("3. Area Unit")
    print("4. Soil Type")
    print("5. Irrigation")
    print("6. All Information")
    print("7. Cancel")

    choice = input("Enter your choice: ").strip()
    if choice == "1":
        field_name = get_text_input("Enter new field name: ")

        update_query = """
            UPDATE fields
            SET field_name = ?
            WHERE field_id = ?
        """

        cursor.execute(update_query, (field_name, field_id))

        connection.commit()

        print("\nField name updated successfully!")

    elif choice == "2":
        area = get_positive_number("Enter new field area: ")

        update_query = """
                UPDATE fields
                SET area = ?
                WHERE field_id = ?
            """

        cursor.execute(update_query, (area, field_id))

        connection.commit()

        print("\nField area updated successfully!")

    elif choice == "3":
        area_unit = get_choice("Select new area unit: ", area_units)
        update_query = """
            UPDATE fields
            SET area_unit = ?
            WHERE field_id = ?
        """

        cursor.execute(update_query, (area_unit, field_id))

        connection.commit()

        print("\nField area unit updated successfully!")

    elif choice == "4":
        soil_type = get_choice("Select new soil type: ", soil_types)

        update_query = """
            UPDATE fields
            SET soil_type = ?
            WHERE field_id = ?
        """

        cursor.execute(update_query, (soil_type, field_id))

        connection.commit()

        print("\nField soil type updated successfully!")

    elif choice == "5":
        irrigation = get_choice("Select new irrigation type: ", irrigation_types)

        update_query = """
            UPDATE fields
            SET irrigation = ?
            WHERE field_id = ?
        """

        cursor.execute(update_query, (irrigation, field_id))

        connection.commit()

        print("\nField irrigation updated successfully!")
    elif choice == "6":
        print("\nEnter new field information:")

        field_name = get_text_input("Enter new field name: ")
        area = get_positive_number("Enter new field area: ")
        area_unit = get_choice("Select new area unit: ", area_units)
        soil_type = get_choice("Select new soil type: ", soil_types)
        irrigation = get_choice("Select new irrigation type: ", irrigation_types)

        update_query = """
            UPDATE fields
            SET field_name = ?,
                area = ?,
                area_unit = ?,
                soil_type = ?,
                irrigation = ?
            WHERE field_id = ?
        """

        cursor.execute(
            update_query, (field_name, area, area_unit, soil_type, irrigation, field_id)
        )

        connection.commit()

        print("\nField information updated successfully!")
    elif choice == "7":
        print("\nUpdate cancelled.")
    else:
        print("\nInvalid choice. Please enter a number from 1 to 7.")
    connection.close()


#! Deletes an existing field from the database
def delete_field():
    print("\n>>> DELETE FIELD <<<")

    field_id = input("Enter field ID: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT f.field_id,
               fr.name,
               f.field_name,
               f.area,
               f.area_unit,
               f.soil_type,
               f.irrigation
        FROM fields AS f
        INNER JOIN farmers AS fr
            ON f.farmer_id = fr.farmer_id
        WHERE f.field_id = ?
    """

    cursor.execute(query, (field_id,))

    field = cursor.fetchone()

    if not field:
        print("\nField not found.")
        connection.close()
        return

    print("\nField Information:")
    print(f"ID: {field[0]}")
    print(f"Farmer: {field[1]}")
    print(f"Field Name: {field[2]}")
    print(f"Area: {field[3]} {field[4]}")
    print(f"Soil Type: {field[5]}")
    print(f"Irrigation: {field[6]}")

    confirmation = (
        input("\nAre you sure you want to delete this field? (y/n): ").strip().lower()
    )

    if confirmation != "y":
        print("\nDeletion cancelled.")
        connection.close()
        return
    delete_query = """
        DELETE FROM fields
        WHERE field_id = ?
    """

    cursor.execute(delete_query, (field_id,))

    connection.commit()

    print("\nField deleted successfully!")

    connection.close()


#!CROP PLANNING
seasons = ["Spring", "Summer", "Autumn", "Winter"]
crop_statuses = ["Planned", "Growing", "Harvested"]


#! Adds a new crop plan for an existing field
def add_crop_plan():
    print("\n>>> ADD CROP PLAN <<<")
    field_id = input("Enter Field ID: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT f.field_id, fr.name, f.field_name FROM fields AS f
        INNER JOIN farmers AS fr
        ON f.farmer_id=fr.farmer_id    
        WHERE f.field_id=?
    """
    cursor.execute(query, (field_id,))

    field = cursor.fetchone()

    if not field:
        print("\nField not found. Please enter a valid field ID.")
        connection.close()
        return

    print(f"\nFarmer: {field[1]}")
    print(f"Field: {field[2]}")
    crop_name = get_text_input("Enter crop name: ")
    variety = get_text_input("Enter crop variety: ")
    season = get_choice("Select season: ", seasons)
    planting_date = get_date("Enter planting date (YYYY-MM-DD): ")
    while True:
        expected_harvest_date = get_date("Enter expected harvest date (YYYY-MM-DD): ")
        planting = datetime.strptime(planting_date, "%Y-%m-%d")
        harvest = datetime.strptime(expected_harvest_date, "%Y-%m-%d")
        if harvest >= planting:
            break
        print("\nExpected harvest date cannot be earlier than planting date.")
    status = get_choice("Select crop status: ", crop_statuses)

    query = """
    INSERT INTO crop_plans(field_id, crop_name, variety, season, planting_date, expected_harvest_date, status ) VALUES (?,?,?,?,?,?,?)
    """
    cursor.execute(
        query,
        (
            field_id,
            crop_name,
            variety,
            season,
            planting_date,
            expected_harvest_date,
            status,
        ),
    )
    connection.commit()
    print("\nCrop plan added successfully!")


#! Displays all crop plans stored in the database
def view_crop_plans():
    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT cp.crop_id,
               fr.name,
               f.field_name,
               cp.crop_name,
               cp.variety,
               cp.season,
               cp.planting_date,
               cp.expected_harvest_date,
               cp.status
        FROM crop_plans AS cp
        INNER JOIN fields AS f
            ON cp.field_id = f.field_id
        INNER JOIN farmers AS fr
            ON f.farmer_id = fr.farmer_id
    """

    cursor.execute(query)

    crop_plans = cursor.fetchall()

    connection.close()

    if not crop_plans:
        print("\nNo crop plans found.")
        return

    print("\n>>> CROP PLAN LIST <<<")

    for crop in crop_plans:
        print(
            f"ID: {crop[0]} | "
            f"Farmer: {crop[1]} | "
            f"Field: {crop[2]} | "
            f"Crop: {crop[3]} | "
            f"Variety: {crop[4]} | "
            f"Season: {crop[5]} | "
            f"Planting: {crop[6]} | "
            f"Expected Harvest: {crop[7]} | "
            f"Status: {crop[8]}"
        )


#! Searches for a crop plan by crop name or farmer name
def search_crop_plans():
    print("\n>>> SEARCH CROP PLAN <<<")

    search_value = input("Enter Crop Name or Farmer Name: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT cp.crop_id,
               fr.name,
               f.field_name,
               cp.crop_name,
               cp.variety,
               cp.season,
               cp.planting_date,
               cp.expected_harvest_date,
               cp.status
        FROM crop_plans AS cp
        INNER JOIN fields AS f
            ON cp.field_id = f.field_id
        INNER JOIN farmers AS fr
            ON f.farmer_id = fr.farmer_id
        WHERE cp.crop_name LIKE ?
           OR fr.name LIKE ?
    """

    search_pattern = f"%{search_value}%"

    cursor.execute(query, (search_pattern, search_pattern))

    crop_plans = cursor.fetchall()

    connection.close()

    if not crop_plans:
        print("\nNo matching crop plan found.")
        return

    for crop in crop_plans:
        print(
            f"ID: {crop[0]} | "
            f"Farmer: {crop[1]} | "
            f"Field: {crop[2]} | "
            f"Crop: {crop[3]} | "
            f"Variety: {crop[4]} | "
            f"Season: {crop[5]} | "
            f"Planting: {crop[6]} | "
            f"Expected Harvest: {crop[7]} | "
            f"Status: {crop[8]}"
        )


#! Updates an existing crop plan
def update_crop_plan():
    print("\n>>> UPDATE CROP PLAN <<<")

    crop_id = input("Enter Crop ID: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT crop_id, crop_name, variety, season,
               planting_date, expected_harvest_date, status
        FROM crop_plans
        WHERE crop_id = ?
    """

    cursor.execute(query, (crop_id,))

    crop = cursor.fetchone()

    if not crop:
        print("\nCrop plan not found. Please enter a valid crop ID.")
        connection.close()
        return

    print("\nCurrent Crop Plan:")
    print(f"Crop Name: {crop[1]}")
    print(f"Variety: {crop[2]}")
    print(f"Season: {crop[3]}")
    print(f"Planting Date: {crop[4]}")
    print(f"Expected Harvest Date: {crop[5]}")
    print(f"Status: {crop[6]}")

    print("\nWhat would you like to update?")
    print("1. Crop Name")
    print("2. Variety")
    print("3. Season")
    print("4. Planting Date")
    print("5. Expected Harvest Date")
    print("6. Status")
    print("7. All Information")
    print("8. Cancel")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        new_crop_name = get_text_input("Enter new crop name: ")

        update_query = """
            UPDATE crop_plans
            SET crop_name = ?
            WHERE crop_id = ?
        """

        cursor.execute(update_query, (new_crop_name, crop_id))
        connection.commit()

        print("\nCrop name updated successfully!")
        connection.close()
        return
    elif choice == "2":
        new_variety = get_text_input("Enter new crop variety: ")

        update_query = """
            UPDATE crop_plans
            SET variety = ?
            WHERE crop_id = ?
        """

        cursor.execute(update_query, (new_variety, crop_id))
        connection.commit()

        print("\nCrop variety updated successfully!")
        connection.close()
        return
    elif choice == "3":
        new_season = get_choice("Select new season: ", seasons)

        update_query = """
            UPDATE crop_plans
            SET season = ?
            WHERE crop_id = ?
        """

        cursor.execute(update_query, (new_season, crop_id))
        connection.commit()

        print("\nCrop season updated successfully!")
        connection.close()
        return
    elif choice == "4":
        new_planting_date = get_date("Enter new planting date (YYYY-MM-DD): ")

        update_query = """
            UPDATE crop_plans
            SET planting_date = ?
            WHERE crop_id = ?
        """

        cursor.execute(update_query, (new_planting_date, crop_id))
        connection.commit()

        print("\nPlanting date updated successfully!")
        connection.close()
        return
    elif choice == "5":
        new_harvest_date = get_date("Enter new expected harvest date (YYYY-MM-DD): ")

        planting_date = datetime.strptime(crop[4], "%Y-%m-%d")
        harvest_date = datetime.strptime(new_harvest_date, "%Y-%m-%d")

        if harvest_date < planting_date:
            print("\nExpected harvest date cannot be earlier than planting date.")
            connection.close()
            return

        update_query = """
            UPDATE crop_plans
            SET expected_harvest_date = ?
            WHERE crop_id = ?
        """

        cursor.execute(update_query, (new_harvest_date, crop_id))
        connection.commit()

        print("\nExpected harvest date updated successfully!")
        connection.close()
        return
    elif choice == "6":
        new_status = get_choice("Select new crop status: ", crop_statuses)

        update_query = """
            UPDATE crop_plans
            SET status = ?
            WHERE crop_id = ?
        """

        cursor.execute(update_query, (new_status, crop_id))
        connection.commit()

        print("\nCrop status updated successfully!")
        connection.close()
        return
    elif choice == "7":
        print("\n>>> UPDATE ALL CROP INFORMATION <<<")

        new_crop_name = get_text_input("Enter new crop name: ")
        new_variety = get_text_input("Enter new crop variety: ")
        new_season = get_choice("Select new season: ", seasons)

        new_planting_date = get_date("Enter new planting date (YYYY-MM-DD): ")

        while True:
            new_harvest_date = get_date(
                "Enter new expected harvest date (YYYY-MM-DD): "
            )

            planting = datetime.strptime(new_planting_date, "%Y-%m-%d")

            harvest = datetime.strptime(new_harvest_date, "%Y-%m-%d")

            if harvest >= planting:
                break

            print("\nExpected harvest date cannot be earlier " "than planting date.")

        new_status = get_choice("Select new crop status: ", crop_statuses)

        update_query = """
            UPDATE crop_plans
            SET crop_name = ?,
                variety = ?,
                season = ?,
                planting_date = ?,
                expected_harvest_date = ?,
                status = ?
            WHERE crop_id = ?
        """

        cursor.execute(
            update_query,
            (
                new_crop_name,
                new_variety,
                new_season,
                new_planting_date,
                new_harvest_date,
                new_status,
                crop_id,
            ),
        )

        connection.commit()

        print("\nCrop plan updated successfully!")
        connection.close()
        return

    elif choice == "8":
        print("\nUpdate cancelled.")
        connection.close()
        return

    else:
        print("\nInvalid choice. Please select a number from 1 to 8.")
        connection.close()
        return


#! Deletes an existing crop plan
def delete_crop_plan():
    print("\n>>> DELETE CROP PLAN <<<")

    crop_id = input("Enter Crop ID: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT crop_id, crop_name, variety, season,
               planting_date, expected_harvest_date, status
        FROM crop_plans
        WHERE crop_id = ?
    """

    cursor.execute(query, (crop_id,))

    crop = cursor.fetchone()

    if not crop:
        print("\nCrop plan not found. Please enter a valid crop ID.")
        connection.close()
        return
    print("\nCrop Plan Details:")
    print(f"Crop Name: {crop[1]}")
    print(f"Variety: {crop[2]}")
    print(f"Season: {crop[3]}")
    print(f"Planting Date: {crop[4]}")
    print(f"Expected Harvest Date: {crop[5]}")
    print(f"Status: {crop[6]}")

    confirmation = (
        input("\nAre you sure you want to delete this crop plan? (yes/no): ")
        .strip()
        .lower()
    )

    if confirmation != "yes":
        print("\nDelete cancelled.")
        connection.close()
        return

    delete_query = """
        DELETE FROM crop_plans
        WHERE crop_id = ?
    """

    cursor.execute(delete_query, (crop_id,))
    connection.commit()

    print("\nCrop plan deleted successfully!")


#!Farming Activities

activity_types = [
    "Land Preparation",
    "Planting",
    "Irrigation",
    "Fertilization",
    "Weeding",
    "Pest Control",
    "Spraying",
    "Harvest Preparation",
    "Other",
]


#! Adds a new farming activity for an existing crop plan


def add_activity():
    print("\n>>> ADD FARMING ACTIVITY <<<")

    crop_id = input("Enter Crop ID: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    # Check whether the crop plan exists
    query = """
        SELECT cp.crop_id,
               fr.name,
               f.field_name,
               cp.crop_name
        FROM crop_plans AS cp
        INNER JOIN fields AS f
            ON cp.field_id = f.field_id
        INNER JOIN farmers AS fr
            ON f.farmer_id = fr.farmer_id
        WHERE cp.crop_id = ?
    """

    cursor.execute(query, (crop_id,))

    crop = cursor.fetchone()

    if not crop:
        print("\nCrop plan not found. Please enter a valid crop ID.")
        connection.close()
        return

    print(f"\nFarmer: {crop[1]}")
    print(f"Field: {crop[2]}")
    print(f"Crop: {crop[3]}")

    activity_type = get_choice("Select activity type: ", activity_types)

    activity_date = get_date("Enter activity date (YYYY-MM-DD): ")

    description = input("Enter description (optional): ").strip()

    query = """
        INSERT INTO activities
        (crop_id, activity_type, activity_date, description)
        VALUES (?, ?, ?, ?)
    """

    cursor.execute(query, (crop_id, activity_type, activity_date, description))

    connection.commit()

    print("\nFarming activity added successfully!")


#! Displays all farming activities stored in the database
def view_activities():
    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT a.activity_id,
               fr.name,
               f.field_name,
               cp.crop_name,
               a.activity_type,
               a.activity_date,
               a.description
        FROM activities AS a
        INNER JOIN crop_plans AS cp
            ON a.crop_id = cp.crop_id
        INNER JOIN fields AS f
            ON cp.field_id = f.field_id
        INNER JOIN farmers AS fr
            ON f.farmer_id = fr.farmer_id
    """

    cursor.execute(query)

    activities = cursor.fetchall()

    connection.close()

    if not activities:
        print("\nNo farming activities found.")
        return

    print("\n>>> FARMING ACTIVITY LIST <<<")

    for activity in activities:
        print(
            f"ID: {activity[0]} | "
            f"Farmer: {activity[1]} | "
            f"Field: {activity[2]} | "
            f"Crop: {activity[3]} | "
            f"Activity: {activity[4]} | "
            f"Date: {activity[5]} | "
            f"Description: {activity[6]}"
        )


#! Searches for a farming activity by crop, farmer, or activity type
def search_activities():
    print("\n>>> SEARCH FARMING ACTIVITY <<<")

    search_value = input("Enter Crop Name, Farmer Name, or Activity Type: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT a.activity_id,
               fr.name,
               f.field_name,
               cp.crop_name,
               a.activity_type,
               a.activity_date,
               a.description
        FROM activities AS a
        INNER JOIN crop_plans AS cp
            ON a.crop_id = cp.crop_id
        INNER JOIN fields AS f
            ON cp.field_id = f.field_id
        INNER JOIN farmers AS fr
            ON f.farmer_id = fr.farmer_id
        WHERE cp.crop_name LIKE ?
           OR fr.name LIKE ?
           OR a.activity_type LIKE ?
    """

    search_pattern = f"%{search_value}%"

    cursor.execute(query, (search_pattern, search_pattern, search_pattern))

    activities = cursor.fetchall()

    connection.close()

    if not activities:
        print("\nNo matching farming activity found.")
        return

    print("\n>>> SEARCH RESULTS <<<")

    for activity in activities:
        print(
            f"ID: {activity[0]} | "
            f"Farmer: {activity[1]} | "
            f"Field: {activity[2]} | "
            f"Crop: {activity[3]} | "
            f"Activity: {activity[4]} | "
            f"Date: {activity[5]} | "
            f"Description: {activity[6]}"
        )


#! Updates an existing farming activity
def update_activity():
    print("\n>>> UPDATE FARMING ACTIVITY <<<")

    activity_id = input("Enter Activity ID: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT activity_id, activity_type, activity_date, description
        FROM activities
        WHERE activity_id = ?
    """

    cursor.execute(query, (activity_id,))

    activity = cursor.fetchone()

    if not activity:
        print("\nFarming activity not found. Please enter a valid activity ID.")
        connection.close()
        return

    print("\nCurrent Activity:")
    print(f"Activity Type: {activity[1]}")
    print(f"Activity Date: {activity[2]}")
    print(f"Description: {activity[3]}")

    print("\nWhat would you like to update?")
    print("1. Activity Type")
    print("2. Activity Date")
    print("3. Description")
    print("4. All Information")
    print("5. Cancel")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        new_activity_type = get_choice("Select new activity type: ", activity_types)

        update_query = """
            UPDATE activities
            SET activity_type = ?
            WHERE activity_id = ?
        """

        cursor.execute(update_query, (new_activity_type, activity_id))
        print("\nActivity type updated successfully!")
    elif choice == "2":
        new_activity_date = get_date("Enter new activity date (YYYY-MM-DD): ")

        update_query = """
            UPDATE activities
            SET activity_date = ?
            WHERE activity_id = ?
        """
        cursor.execute(update_query, (new_activity_date, activity_id))
        print("\nActivity date updated successfully!")
    elif choice == "3":
        new_description = input("Enter new description: ").strip()

        update_query = """
            UPDATE activities
            SET description = ?
            WHERE activity_id = ?
        """
        cursor.execute(update_query, (new_description, activity_id))
        print("\nDescription updated successfully!")
    elif choice == "4":
        new_activity_type = get_choice("Select new activity type: ", activity_types)

        new_activity_date = get_date("Enter new activity date (YYYY-MM-DD): ")

        new_description = input("Enter new description: ").strip()

        update_query = """
            UPDATE activities
            SET activity_type = ?,
                activity_date = ?,
                description = ?
            WHERE activity_id = ?
        """

        cursor.execute(
            update_query,
            (new_activity_type, new_activity_date, new_description, activity_id),
        )
        print("\nFarming activity information updated successfully!")
    elif choice == "5":
        print("\nUpdate cancelled.")
        connection.close()
        return

    else:
        print("\nInvalid choice. Please select a number from 1 to 5.")
        connection.close()
        return

    connection.commit()


#! Deletes an existing farming activity
def delete_activity():
    print("\n>>> DELETE FARMING ACTIVITY <<<")

    activity_id = input("Enter Activity ID: ").strip()

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT activity_id, activity_type, activity_date, description
        FROM activities
        WHERE activity_id = ?
    """

    cursor.execute(query, (activity_id,))

    activity = cursor.fetchone()

    if not activity:
        print("\nFarming activity not found. Please enter a valid activity ID.")
        connection.close()
        return

    print("\nActivity Details:")
    print(f"Activity Type: {activity[1]}")
    print(f"Activity Date: {activity[2]}")
    print(f"Description: {activity[3]}")

    confirmation = (
        input("\nAre you sure you want to delete this activity? (yes/no): ")
        .strip()
        .lower()
    )

    if confirmation != "yes":
        print("\nDelete cancelled.")
        connection.close()
        return

    delete_query = """
        DELETE FROM activities
        WHERE activity_id = ?
    """

    cursor.execute(delete_query, (activity_id,))
    connection.commit()

    print("\nFarming activity deleted successfully!")

    connection.close()
