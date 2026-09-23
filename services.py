from datetime import datetime
from database import get_conn
import validators

#! FARMER MANAGEMENT


#! Adds a new farmer to the database
def add_farmer():
    print("\n>>> ADD FARMER <<<")
    name = validators.get_name("Enter farmer name: ")
    phone = validators.get_phone("Enter phone number: ")
    location = validators.get_location("Enter location: ")

    connection = get_conn()
    cursor = connection.cursor()
    check_query = """
        SELECT farmer_id
        FROM farmers
        WHERE phone = ?
    """

    cursor.execute(check_query, (phone,))

    existing_farmer = cursor.fetchone()

    if existing_farmer:
        print("\nThis phone number is already registered.")
        connection.close()
        return

    add_query = """INSERT INTO farmers (name, phone, location) VALUES (?, ?, ?)"""
    cursor.execute(add_query, (name, phone, location))
    connection.commit()
    connection.close()

    print("\nFarmer added successfully!")


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
    search_value = validators.get_non_empty_input("Enter Farmer name or phone number: ")

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
            f"Farmer_ID: {farmer[0]} | "
            f"Name: {farmer[1]} | "
            f"Phone: {farmer[2]} | "
            f"Location: {farmer[3]}"
        )


#! Updates an existing farmer's information
def update_farmer():
    print("\n>>> UPDATE FARMER <<<")
    farmer_id = validators.get_positive_integer("Enter Farmer ID: ")

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
        name = validators.get_name("Enter new farmer name: ")

        update_query = """
            UPDATE farmers
            SET name = ?
            WHERE farmer_id = ?
        """
        cursor.execute(update_query, (name, farmer_id))

        connection.commit()

        print("\nFarmer name updated successfully!")

    elif choice == "2":
        phone = validators.get_phone("Enter new phone number: ")
        check_query = """
            SELECT farmer_id
            FROM farmers
            WHERE phone = ?
            AND farmer_id != ?
        """

        cursor.execute(check_query, (phone, farmer_id))

        existing_farmer = cursor.fetchone()

        if existing_farmer:
            print("\nThis phone number is already registered.")
            connection.close()
            return

        update_query = """ UPDATE farmers SET phone=? WHERE farmer_id=?"""

        cursor.execute(update_query, (phone, farmer_id))

        connection.commit()

        print("\nFarmer Phone number updated successfully!")

    elif choice == "3":
        location = validators.get_location("Enter new location: ")

        update_query = """ UPDATE farmers SET location = ? WHERE farmer_id = ? """

        cursor.execute(update_query, (location, farmer_id))

        connection.commit()

        print("\nFarmer location updated successfully!")
    elif choice == "4":
        print("\nEnter new farmer information:")

        name = validators.get_name("Enter new farmer name: ")
        phone = validators.get_phone("Enter new phone number: ")
        location = validators.get_location("Enter new location: ")
        check_query = """
            SELECT farmer_id
            FROM farmers
            WHERE phone = ?
            AND farmer_id != ?
        """

        cursor.execute(check_query, (phone, farmer_id))

        existing_farmer = cursor.fetchone()

        if existing_farmer:
            print("\nThis phone number is already registered.")
            connection.close()
            return
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

    farmer_id = validators.get_positive_integer("Enter farmer ID: ")
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
    print(f"Farmer_ID: {farmer[0]}")
    print(f"Name: {farmer[1]}")
    print(f"Phone: {farmer[2]}")
    print(f"Location: {farmer[3]}")

    print("\nWARNING:")
    print("Deleting this farmer will also delete all fields")
    print("and all crop-related records belonging to those fields.")
    print("This includes activities, expenses, harvests, and revenues.")
    print("This action cannot be undone.")

    confirmation = (
        input("\nAre you sure you want to delete this farmer? (yes/no): ")
        .strip()
        .lower()
    )

    if confirmation != "yes":
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

    farmer_id = validators.get_positive_integer("Enter farmer ID: ")

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
    field_name = validators.get_text_input("Enter field name: ")

    area = validators.get_positive_number("Enter field area: ")

    area_unit = validators.get_choice("Select area unit: ", area_units)

    soil_type = validators.get_choice("Select soil type: ", soil_types)

    irrigation = validators.get_choice("Select irrigation type: ", irrigation_types)

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
            f"Field_ID: {field[0]} | "
            f"Farmer: {field[1]} | "
            f"Field: {field[2]} | "
            f"Area: {field[3]} {field[4]} | "
            f"Soil: {field[5]} | "
            f"Irrigation: {field[6]}"
        )


# Searches for a field by field name or farmer name
def search_fields():
    print("\n>>> SEARCH FIELD <<<")
    search_value = validators.get_non_empty_input("Enter Field Name or Farmer Name: ")

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
            f"Field_ID: {field[0]} | "
            f"Farmer: {field[1]} | "
            f"Field: {field[2]} | "
            f"Area: {field[3]} {field[4]} | "
            f"Soil: {field[5]} | "
            f"Irrigation: {field[6]}"
        )


#! Updates an existing field's information
def update_field():
    print("\n>>> UPDATE FIELD <<<")

    field_id = validators.get_positive_integer("Enter field ID: ")

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
    print(f"Field_ID: {field[0]}")
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
        field_name = validators.get_text_input("Enter new field name: ")

        update_query = """
            UPDATE fields
            SET field_name = ?
            WHERE field_id = ?
        """

        cursor.execute(update_query, (field_name, field_id))

        connection.commit()

        print("\nField name updated successfully!")

    elif choice == "2":
        area = validators.get_positive_number("Enter new field area: ")

        update_query = """
                UPDATE fields
                SET area = ?
                WHERE field_id = ?
            """

        cursor.execute(update_query, (area, field_id))

        connection.commit()

        print("\nField area updated successfully!")

    elif choice == "3":
        area_unit = validators.get_choice("Select new area unit: ", area_units)
        update_query = """
            UPDATE fields
            SET area_unit = ?
            WHERE field_id = ?
        """

        cursor.execute(update_query, (area_unit, field_id))

        connection.commit()

        print("\nField area unit updated successfully!")

    elif choice == "4":
        soil_type = validators.get_choice("Select new soil type: ", soil_types)

        update_query = """
            UPDATE fields
            SET soil_type = ?
            WHERE field_id = ?
        """

        cursor.execute(update_query, (soil_type, field_id))

        connection.commit()

        print("\nField soil type updated successfully!")

    elif choice == "5":
        irrigation = validators.get_choice(
            "Select new irrigation type: ", irrigation_types
        )

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

        field_name = validators.get_text_input("Enter new field name: ")
        area = validators.get_positive_number("Enter new field area: ")
        area_unit = validators.get_choice("Select new area unit: ", area_units)
        soil_type = validators.get_choice("Select new soil type: ", soil_types)
        irrigation = validators.get_choice(
            "Select new irrigation type: ", irrigation_types
        )

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

    field_id = validators.get_positive_integer("Enter field ID: ")

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
    print(f"Field_ID: {field[0]}")
    print(f"Farmer: {field[1]}")
    print(f"Field Name: {field[2]}")
    print(f"Area: {field[3]} {field[4]}")
    print(f"Soil Type: {field[5]}")
    print(f"Irrigation: {field[6]}")

    print("\nWARNING:")
    print("Deleting this field will also delete all crop plans")
    print("associated with this field.")
    print("Their activities, expenses, harvests, and revenues")
    print("will also be deleted.")
    print("This action cannot be undone.")

    confirmation = (
        input("\nAre you sure you want to delete this field? (yes/no): ")
        .strip()
        .lower()
    )

    if confirmation != "yes":
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
    field_id = validators.get_positive_integer("Enter Field ID: ")

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
    crop_name = validators.get_text_input("Enter crop name: ")
    variety = validators.get_text_input("Enter crop variety: ")
    season = validators.get_choice("Select season: ", seasons)
    planting_date = validators.get_date("Enter planting date (YYYY-MM-DD): ")
    while True:
        expected_harvest_date = validators.get_date(
            "Enter expected harvest date (YYYY-MM-DD): "
        )
        planting = datetime.strptime(planting_date, "%Y-%m-%d")
        harvest = datetime.strptime(expected_harvest_date, "%Y-%m-%d")
        if harvest >= planting:
            break
        print("\nExpected harvest date cannot be earlier than planting date.")
    status = validators.get_choice("Select crop status: ", crop_statuses)

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
    connection.close()


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
            f"Crop_ID: {crop[0]} | "
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

    search_value = validators.get_non_empty_input("Enter Crop Name or Farmer Name: ")

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
            f"Crop_ID: {crop[0]} | "
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

    crop_id = validators.get_positive_integer("Enter Crop ID: ")

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
        new_crop_name = validators.get_text_input("Enter new crop name: ")

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
        new_variety = validators.get_text_input("Enter new crop variety: ")

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
        new_season = validators.get_choice("Select new season: ", seasons)

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
        new_planting_date = validators.get_date(
            "Enter new planting date (YYYY-MM-DD): "
        )

        if crop[5]:
            planting = datetime.strptime(new_planting_date, "%Y-%m-%d")
            harvest = datetime.strptime(crop[5], "%Y-%m-%d")

            if planting > harvest:
                print("\nPlanting date cannot be later than expected harvest date.")
                connection.close()
                return
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
        new_harvest_date = validators.get_date(
            "Enter new expected harvest date (YYYY-MM-DD): "
        )

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
        new_status = validators.get_choice("Select new crop status: ", crop_statuses)

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

        new_crop_name = validators.get_text_input("Enter new crop name: ")
        new_variety = validators.get_text_input("Enter new crop variety: ")
        new_season = validators.get_choice("Select new season: ", seasons)

        new_planting_date = validators.get_date(
            "Enter new planting date (YYYY-MM-DD): "
        )

        while True:
            new_harvest_date = validators.get_date(
                "Enter new expected harvest date (YYYY-MM-DD): "
            )

            planting = datetime.strptime(new_planting_date, "%Y-%m-%d")

            harvest = datetime.strptime(new_harvest_date, "%Y-%m-%d")

            if harvest >= planting:
                break

            print("\nExpected harvest date cannot be earlier than planting date.")

        new_status = validators.get_choice("Select new crop status: ", crop_statuses)

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

    crop_id = validators.get_positive_integer("Enter Crop ID: ")

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

    print("\nWARNING:")
    print("Deleting this crop plan will also delete all")
    print("activities, expenses, harvests, and revenues")
    print("associated with this crop.")
    print("This action cannot be undone.")

    confirmation = (
        input("\nAre you sure you want to delete this crop plan? (yes/no): ")
        .strip()
        .lower()
    )

    if confirmation != "yes":
        print("\nDeletion cancelled.")
        connection.close()
        return

    delete_query = """
        DELETE FROM crop_plans
        WHERE crop_id = ?
    """

    cursor.execute(delete_query, (crop_id,))
    connection.commit()

    print("\nCrop plan deleted successfully!")
    connection.close()


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

    crop_id = validators.get_positive_integer("Enter Crop ID: ")

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

    activity_type = validators.get_choice("Select activity type: ", activity_types)

    activity_date = validators.get_date("Enter activity date (YYYY-MM-DD): ")

    description = input("Enter description (optional): ").strip()

    query = """
        INSERT INTO activities
        (crop_id, activity_type, activity_date, description)
        VALUES (?, ?, ?, ?)
    """

    cursor.execute(query, (crop_id, activity_type, activity_date, description))

    connection.commit()

    print("\nFarming activity added successfully!")
    connection.close()


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
            f"Activity_ID: {activity[0]} | "
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

    search_value = validators.get_non_empty_input(
        "Enter Crop Name, Farmer Name, or Activity Type: "
    )

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
            f"Activity_ID: {activity[0]} | "
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

    activity_id = validators.get_positive_integer("Enter Activity ID: ")

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
        new_activity_type = validators.get_choice(
            "Select new activity type: ", activity_types
        )

        update_query = """
            UPDATE activities
            SET activity_type = ?
            WHERE activity_id = ?
        """

        cursor.execute(update_query, (new_activity_type, activity_id))
        print("\nActivity type updated successfully!")
    elif choice == "2":
        new_activity_date = validators.get_date(
            "Enter new activity date (YYYY-MM-DD): "
        )

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
        new_activity_type = validators.get_choice(
            "Select new activity type: ", activity_types
        )

        new_activity_date = validators.get_date(
            "Enter new activity date (YYYY-MM-DD): "
        )

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
    connection.close()


#! Deletes an existing farming activity
def delete_activity():
    print("\n>>> DELETE FARMING ACTIVITY <<<")

    activity_id = validators.get_positive_integer("Enter Activity ID: ")

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
        print("\nDeletion cancelled.")
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


#! Expense Management
expense_types = [
    "Seeds",
    "Fertilizer",
    "Pesticides",
    "Labor",
    "Irrigation",
    "Equipment",
    "Transportation",
    "Other",
]


#!Add Expenses
def add_expense():
    connection = get_conn()
    cursor = connection.cursor()

    query = """
    SELECT cp.crop_id, cp.crop_name, f.field_name, fr.name
    FROM crop_plans AS cp
    JOIN fields AS f ON cp.field_id= f.field_id
    JOIN farmers AS fr ON f.farmer_id= fr.farmer_id
    ORDER BY cp.crop_id
    """
    cursor.execute(query)
    crops = cursor.fetchall()

    if not crops:
        print("No crop plans found. Please add a crop plan first.")
        connection.close()
        return

    print("\n>>> AVAILABLE CROP PLANS <<<")

    for crop in crops:
        print(
            f"Crop_ID: {crop[0]} | "
            f"Crop: {crop[1]} | "
            f"Field: {crop[2]} | "
            f"Farmer: {crop[3]}"
        )

    # Select crop plan
    while True:
        crop_id = validators.get_positive_integer("Enter Crop Plan ID: ")
        query = """
            SELECT crop_id
            FROM crop_plans
            WHERE crop_id = ?
        """

        cursor.execute(query, (crop_id,))
        crop = cursor.fetchone()

        if crop:
            break
        print("Crop plan not found. Please enter a valid ID.")

    expense_type = validators.get_choice("Select Expense Type: ", expense_types)
    amount = validators.get_positive_number("Enter Expense Amount: ")
    expense_date = validators.get_date("Enter Expense Date (YYYY-MM-DD): ")
    description = input("Enter Description (optional): ").strip()

    # Insert expense
    query = """
        INSERT INTO expenses (
            crop_id,
            expense_type,
            amount,
            expense_date,
            description
        )
        VALUES (?, ?, ?, ?, ?)
    """

    cursor.execute(query, (crop_id, expense_type, amount, expense_date, description))

    connection.commit()
    connection.close()

    print("Expense added successfully!")


#! View Expenses
def view_expenses():
    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT
            e.expense_id,
            fr.name,
            f.field_name,
            cp.crop_name,
            e.expense_type,
            e.amount,
            e.expense_date,
            e.description
        FROM expenses e
        JOIN crop_plans cp ON e.crop_id = cp.crop_id
        JOIN fields f ON cp.field_id = f.field_id
        JOIN farmers fr ON f.farmer_id = fr.farmer_id
        ORDER BY e.expense_id
    """

    cursor.execute(query)
    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses found.")
        connection.close()
        return

    print("\n>>> EXPENSE LIST <<<")

    for expense in expenses:
        print(
            f"Expense_ID: {expense[0]} | "
            f"Farmer: {expense[1]} | "
            f"Field: {expense[2]} | "
            f"Crop: {expense[3]} | "
            f"Type: {expense[4]} | "
            f"Amount: {expense[5]:.2f} | "
            f"Date: {expense[6]} | "
            f"Description: {expense[7] or 'N/A'}"
        )
    connection.close()


#! Search Expenses
def search_expense():
    connection = get_conn()
    cursor = connection.cursor()

    search_term = validators.get_non_empty_input(
        "Enter crop name, farmer name, or expense type to search: "
    )

    query = """
        SELECT
            e.expense_id,
            fr.name,
            f.field_name,
            cp.crop_name,
            e.expense_type,
            e.amount,
            e.expense_date,
            e.description
        FROM expenses e
        JOIN crop_plans cp ON e.crop_id = cp.crop_id
        JOIN fields f ON cp.field_id = f.field_id
        JOIN farmers fr ON f.farmer_id = fr.farmer_id
        WHERE cp.crop_name LIKE ?
           OR fr.name LIKE ?
           OR e.expense_type LIKE ?
        ORDER BY e.expense_id
    """

    search_pattern = f"%{search_term}%"

    cursor.execute(query, (search_pattern, search_pattern, search_pattern))

    expenses = cursor.fetchall()

    if not expenses:
        print("No matching expenses found.")
        connection.close()
        return

    print("\n>>> SEARCH RESULTS <<<")

    for expense in expenses:
        print(
            f"Expense_ID: {expense[0]} | "
            f"Farmer: {expense[1]} | "
            f"Field: {expense[2]} | "
            f"Crop: {expense[3]} | "
            f"Type: {expense[4]} | "
            f"Amount: {expense[5]:.2f} | "
            f"Date: {expense[6]} | "
            f"Description: {expense[7] or 'N/A'}"
        )

    connection.close()


#! Updates an existing expense
def update_expense():
    print("\n>>> UPDATE EXPENSE <<<")

    expense_id = validators.get_positive_integer("Enter Expense ID: ")

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT
            e.expense_id,
            fr.name,
            f.field_name,
            cp.crop_name,
            e.expense_type,
            e.amount,
            e.expense_date,
            e.description
        FROM expenses e
        JOIN crop_plans cp ON e.crop_id = cp.crop_id
        JOIN fields f ON cp.field_id = f.field_id
        JOIN farmers fr ON f.farmer_id = fr.farmer_id
        WHERE e.expense_id = ?
    """

    cursor.execute(query, (expense_id,))

    expense = cursor.fetchone()

    if not expense:
        print("\nExpense not found. Please enter a valid expense ID.")
        connection.close()
        return

    print("\nCurrent Expense:")
    print(f"Farmer: {expense[1]}")
    print(f"Field: {expense[2]}")
    print(f"Crop: {expense[3]}")
    print(f"Expense Type: {expense[4]}")
    print(f"Amount: {expense[5]}")
    print(f"Expense Date: {expense[6]}")
    print(f"Description: {expense[7] or 'N/A'}")

    print("\nWhat would you like to update?")
    print("1. Expense Type")
    print("2. Amount")
    print("3. Expense Date")
    print("4. Description")
    print("5. All Information")
    print("6. Cancel")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        new_expense_type = validators.get_choice(
            "Select new expense type: ", expense_types
        )

        update_query = """
            UPDATE expenses
            SET expense_type = ?
            WHERE expense_id = ?
        """

        cursor.execute(update_query, (new_expense_type, expense_id))

        connection.commit()

        print("\nExpense type updated successfully!")
        connection.close()
        return

    elif choice == "2":
        new_amount = validators.get_positive_number("Enter new expense amount: ")

        update_query = """
            UPDATE expenses
            SET amount = ?
            WHERE expense_id = ?
        """

        cursor.execute(update_query, (new_amount, expense_id))

        connection.commit()

        print("\nExpense amount updated successfully!")
        connection.close()
        return

    elif choice == "3":
        new_expense_date = validators.get_date("Enter new expense date (YYYY-MM-DD): ")

        update_query = """
            UPDATE expenses
            SET expense_date = ?
            WHERE expense_id = ?
        """

        cursor.execute(update_query, (new_expense_date, expense_id))

        connection.commit()

        print("\nExpense date updated successfully!")
        connection.close()
        return

    elif choice == "4":
        new_description = input("Enter new description (optional): ").strip()

        update_query = """
            UPDATE expenses
            SET description = ?
            WHERE expense_id = ?
        """

        cursor.execute(update_query, (new_description, expense_id))

        connection.commit()

        print("\nExpense description updated successfully!")
        connection.close()
        return

    elif choice == "5":
        print("\n>>> UPDATE ALL EXPENSE INFORMATION <<<")

        new_expense_type = validators.get_choice(
            "Select new expense type: ", expense_types
        )

        new_amount = validators.get_positive_number("Enter new expense amount: ")

        new_expense_date = validators.get_date("Enter new expense date (YYYY-MM-DD): ")

        new_description = input("Enter new description (optional): ").strip()

        update_query = """
            UPDATE expenses
            SET expense_type = ?,
                amount = ?,
                expense_date = ?,
                description = ?
            WHERE expense_id = ?
        """

        cursor.execute(
            update_query,
            (
                new_expense_type,
                new_amount,
                new_expense_date,
                new_description,
                expense_id,
            ),
        )

        connection.commit()

        print("\nExpense information updated successfully!")
        connection.close()
        return

    elif choice == "6":
        print("\nUpdate cancelled.")
        connection.close()
        return

    else:
        print("\nInvalid choice. Please select a number from 1 to 6.")
        connection.close()
        return


#!Delete Expenses
def delete_expense():
    print("\n>>> DELETE EXPENSE <<<")

    expense_id = validators.get_positive_integer("Enter Expense ID: ")

    connection = get_conn()
    cursor = connection.cursor()
    query = """
        SELECT expense_id, crop_id, expense_type, amount,
               expense_date, description
        FROM expenses
        WHERE expense_id = ?
    """

    cursor.execute(query, (expense_id,))
    expense = cursor.fetchone()
    if not expense:
        print("\nExpense not found.")
        connection.close()
        return
    print("\nExpense Details:")
    print(f"Expense ID: {expense[0]}")
    print(f"Crop ID: {expense[1]}")
    print(f"Expense Type: {expense[2]}")
    print(f"Amount: {expense[3]}")
    print(f"Expense Date: {expense[4]}")
    print(f"Description: {expense[5]}")

    confirmation = (
        input("\nAre you sure you want to delete this expense? (yes/no): ")
        .strip()
        .lower()
    )

    if confirmation != "yes":
        print("\nExpense deletion cancelled.")
        connection.close()
        return

    delete_query = """
        DELETE FROM expenses
        WHERE expense_id = ?
    """

    cursor.execute(delete_query, (expense_id,))
    connection.commit()

    print("\nExpense deleted successfully!")

    connection.close()


#!Harvest Management
harvest_units = ["Kg", "Quintal", "Ton", "Crate", "Bags", "Pieces", "Box"]


#! Add Harvests
def add_harvest():
    print("\n>>> ADD HARVEST <<<")

    crop_id = validators.get_positive_integer("Enter Crop ID: ")

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT crop_id, crop_name
        FROM crop_plans
        WHERE crop_id = ?
    """

    cursor.execute(query, (crop_id,))

    crop = cursor.fetchone()

    if not crop:
        print("\nCrop plan not found. Please enter a valid crop ID.")
        connection.close()
        return

    print(f"\nCrop: {crop[1]}")

    harvest_date = validators.get_date("Enter harvest date (YYYY-MM-DD): ")

    quantity = validators.get_positive_number("Enter harvested quantity: ")

    unit = validators.get_choice("Select harvest unit: ", harvest_units)

    insert_query = """
        INSERT INTO harvests (
            crop_id,
            harvest_date,
            quantity,
            unit
        )
        VALUES (?, ?, ?, ?)
    """

    cursor.execute(insert_query, (crop_id, harvest_date, quantity, unit))

    connection.commit()

    print("\nHarvest record added successfully!")

    connection.close()


#! View Harvests
def view_harvests():
    print("\n>>> HARVEST RECORDS <<<")

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT h.harvest_id,
               fr.name,
               f.field_name,
               c.crop_name,
               h.harvest_date,
               h.quantity,
               h.unit
        FROM harvests AS h
        INNER JOIN crop_plans AS c
            ON h.crop_id = c.crop_id
        INNER JOIN fields AS f
            ON c.field_id = f.field_id
        INNER JOIN farmers AS fr
            ON f.farmer_id = fr.farmer_id
        ORDER BY h.harvest_id
    """

    cursor.execute(query)

    harvests = cursor.fetchall()

    if not harvests:
        print("\nNo harvest records found.")
        connection.close()
        return

    for harvest in harvests:
        print("\n--------------------------------")
        print(f"Harvest ID: {harvest[0]}")
        print(f"Farmer: {harvest[1]}")
        print(f"Field: {harvest[2]}")
        print(f"Crop: {harvest[3]}")
        print(f"Harvest Date: {harvest[4]}")
        print(f"Quantity: {harvest[5]} {harvest[6]}")

    print("\n--------------------------------")

    connection.close()


#! Search Harvests
def search_harvest():
    connection = get_conn()
    cursor = connection.cursor()

    search_term = validators.get_non_empty_input(
        "Enter crop name, farmer name, or harvest unit to search: "
    )

    query = """
        SELECT
            h.harvest_id,
            fr.name,
            f.field_name,
            cp.crop_name,
            h.harvest_date,
            h.quantity,
            h.unit
        FROM harvests h
        JOIN crop_plans cp ON h.crop_id = cp.crop_id
        JOIN fields f ON cp.field_id = f.field_id
        JOIN farmers fr ON f.farmer_id = fr.farmer_id
        WHERE cp.crop_name LIKE ?
           OR fr.name LIKE ?
           OR h.unit LIKE ?
        ORDER BY h.harvest_id
    """

    search_pattern = f"%{search_term}%"

    cursor.execute(query, (search_pattern, search_pattern, search_pattern))

    harvests = cursor.fetchall()

    if not harvests:
        print("No matching harvests found.")
        connection.close()
        return

    print("\n>>> SEARCH RESULTS <<<")

    for harvest in harvests:
        print(
            f"Harvest_ID: {harvest[0]} | "
            f"Farmer: {harvest[1]} | "
            f"Field: {harvest[2]} | "
            f"Crop: {harvest[3]} | "
            f"Date: {harvest[4]} | "
            f"Quantity: {harvest[5]:.2f} {harvest[6]}"
        )

    connection.close()


#! Updates an existing harvest
def update_harvest():
    print("\n>>> UPDATE HARVEST <<<")

    harvest_id = validators.get_positive_integer("Enter Harvest ID: ")

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT
            h.harvest_id,
            fr.name,
            f.field_name,
            cp.crop_name,
            h.harvest_date,
            h.quantity,
            h.unit
        FROM harvests h
        JOIN crop_plans cp ON h.crop_id = cp.crop_id
        JOIN fields f ON cp.field_id = f.field_id
        JOIN farmers fr ON f.farmer_id = fr.farmer_id
        WHERE h.harvest_id = ?
    """

    cursor.execute(query, (harvest_id,))

    harvest = cursor.fetchone()

    if not harvest:
        print("\nHarvest not found. Please enter a valid harvest ID.")
        connection.close()
        return

    print("\nCurrent Harvest:")
    print(f"Farmer: {harvest[1]}")
    print(f"Field: {harvest[2]}")
    print(f"Crop: {harvest[3]}")
    print(f"Harvest Date: {harvest[4]}")
    print(f"Quantity: {harvest[5]}")
    print(f"Unit: {harvest[6]}")

    print("\nWhat would you like to update?")
    print("1. Harvest Date")
    print("2. Quantity")
    print("3. Unit")
    print("4. All Information")
    print("5. Cancel")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        new_harvest_date = validators.get_date("Enter new harvest date (YYYY-MM-DD): ")

        update_query = """
            UPDATE harvests
            SET harvest_date = ?
            WHERE harvest_id = ?
        """

        cursor.execute(update_query, (new_harvest_date, harvest_id))

        connection.commit()

        print("\nHarvest date updated successfully!")
        connection.close()
        return

    elif choice == "2":
        new_quantity = validators.get_positive_number("Enter new harvested quantity: ")

        update_query = """
            UPDATE harvests
            SET quantity = ?
            WHERE harvest_id = ?
        """

        cursor.execute(update_query, (new_quantity, harvest_id))

        connection.commit()

        print("\nHarvest quantity updated successfully!")
        connection.close()
        return

    elif choice == "3":
        harvest_units = ["Kg", "Quintal", "Ton", "Crate", "Bags", "Pieces", "Box"]

        new_unit = validators.get_choice("Select new harvest unit: ", harvest_units)

        update_query = """
            UPDATE harvests
            SET unit = ?
            WHERE harvest_id = ?
        """

        cursor.execute(update_query, (new_unit, harvest_id))

        connection.commit()

        print("\nHarvest unit updated successfully!")
        connection.close()
        return

    elif choice == "4":
        print("\n>>> UPDATE ALL HARVEST INFORMATION <<<")

        new_harvest_date = validators.get_date("Enter new harvest date (YYYY-MM-DD): ")

        new_quantity = validators.get_positive_number("Enter new harvested quantity: ")

        harvest_units = ["Kg", "Quintal", "Ton", "Crate", "Bags", "Pieces", "Box"]

        new_unit = validators.get_choice("Select new harvest unit: ", harvest_units)

        update_query = """
            UPDATE harvests
            SET harvest_date = ?,
                quantity = ?,
                unit = ?
            WHERE harvest_id = ?
        """

        cursor.execute(
            update_query, (new_harvest_date, new_quantity, new_unit, harvest_id)
        )

        connection.commit()

        print("\nHarvest information updated successfully!")
        connection.close()
        return

    elif choice == "5":
        print("\nUpdate cancelled.")
        connection.close()
        return

    else:
        print("\nInvalid choice. Please select a number from 1 to 5.")
        connection.close()
        return


#! Deletes an existing harvest
def delete_harvest():
    print("\n>>> DELETE HARVEST <<<")

    harvest_id = validators.get_positive_integer("Enter Harvest ID: ")

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT
            h.harvest_id,
            fr.name,
            f.field_name,
            cp.crop_name,
            h.harvest_date,
            h.quantity,
            h.unit
        FROM harvests h
        JOIN crop_plans cp ON h.crop_id = cp.crop_id
        JOIN fields f ON cp.field_id = f.field_id
        JOIN farmers fr ON f.farmer_id = fr.farmer_id
        WHERE h.harvest_id = ?
    """

    cursor.execute(query, (harvest_id,))

    harvest = cursor.fetchone()

    if not harvest:
        print("\nHarvest not found. Please enter a valid harvest ID.")
        connection.close()
        return

    print("\nHarvest to be deleted:")
    print(f"Farmer: {harvest[1]}")
    print(f"Field: {harvest[2]}")
    print(f"Crop: {harvest[3]}")
    print(f"Harvest Date: {harvest[4]}")
    print(f"Quantity: {harvest[5]}")
    print(f"Unit: {harvest[6]}")

    confirmation = (
        input("\nAre you sure you want to delete this harvest? (yes/no): ")
        .strip()
        .lower()
    )

    if confirmation == "yes":

        delete_query = """
            DELETE FROM harvests
            WHERE harvest_id = ?
        """

        cursor.execute(delete_query, (harvest_id,))

        connection.commit()

        print("\nHarvest deleted successfully!")

    else:
        print("\nDeletion cancelled.")

    connection.close()


#! Revenue management
#! Adds a new revenue record
def add_revenue():
    print("\n>>> ADD REVENUE <<<")

    crop_id = validators.get_positive_integer("Enter Crop ID: ")

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT crop_id, crop_name
        FROM crop_plans
        WHERE crop_id = ?
    """

    cursor.execute(query, (crop_id,))

    crop = cursor.fetchone()

    if not crop:
        print("\nCrop plan not found. Please enter a valid crop ID.")
        connection.close()
        return

    print(f"\nCrop: {crop[1]}")

    sale_date = validators.get_date("Enter sale date (YYYY-MM-DD): ")

    quantity = validators.get_positive_number("Enter quantity sold: ")

    price_per_unit = validators.get_positive_number("Enter price per unit: ")

    total_amount = quantity * price_per_unit

    insert_query = """
        INSERT INTO revenues (
            crop_id,
            sale_date,
            quantity,
            price_per_unit,
            total_amount
        )
        VALUES (?, ?, ?, ?, ?)
    """

    cursor.execute(
        insert_query, (crop_id, sale_date, quantity, price_per_unit, total_amount)
    )

    connection.commit()

    print("\nRevenue record added successfully!")
    print(f"Total Amount: {total_amount:.2f}")

    connection.close()


#! Views all revenue records
def view_revenues():
    print("\n>>> REVENUE RECORDS <<<")

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT
            r.revenue_id,
            fr.name,
            f.field_name,
            cp.crop_name,
            r.sale_date,
            r.quantity,
            r.price_per_unit,
            r.total_amount
        FROM revenues r
        JOIN crop_plans cp ON r.crop_id = cp.crop_id
        JOIN fields f ON cp.field_id = f.field_id
        JOIN farmers fr ON f.farmer_id = fr.farmer_id
        ORDER BY r.revenue_id ASC
    """

    cursor.execute(query)

    revenues = cursor.fetchall()

    if not revenues:
        print("\nNo revenue records found.")
        connection.close()
        return

    for revenue in revenues:
        print("\n--------------------------------")
        print(f"Revenue ID: {revenue[0]}")
        print(f"Farmer: {revenue[1]}")
        print(f"Field: {revenue[2]}")
        print(f"Crop: {revenue[3]}")
        print(f"Sale Date: {revenue[4]}")
        print(f"Quantity: {revenue[5]}")
        print(f"Price Per Unit: {revenue[6]}")
        print(f"Total Amount: {revenue[7]:.2f}")

    print("\n--------------------------------")

    connection.close()


#! Searches revenue records
def search_revenue():
    print("\n>>> SEARCH REVENUE <<<")

    connection = get_conn()
    cursor = connection.cursor()

    search_term = validators.get_non_empty_input(
        "Enter crop name, farmer name, or sale date to search: "
    )

    query = """
        SELECT
            r.revenue_id,
            fr.name,
            f.field_name,
            cp.crop_name,
            r.sale_date,
            r.quantity,
            r.price_per_unit,
            r.total_amount
        FROM revenues r
        JOIN crop_plans cp ON r.crop_id = cp.crop_id
        JOIN fields f ON cp.field_id = f.field_id
        JOIN farmers fr ON f.farmer_id = fr.farmer_id
        WHERE cp.crop_name LIKE ?
           OR fr.name LIKE ?
           OR r.sale_date LIKE ?
        ORDER BY r.revenue_id ASC
    """

    search_pattern = f"%{search_term}%"

    cursor.execute(query, (search_pattern, search_pattern, search_pattern))

    revenues = cursor.fetchall()

    if not revenues:
        print("\nNo matching revenue records found.")
        connection.close()
        return

    print("\n>>> SEARCH RESULTS <<<")

    for revenue in revenues:
        print(
            f"Revenue ID: {revenue[0]} | "
            f"Farmer: {revenue[1]} | "
            f"Field: {revenue[2]} | "
            f"Crop: {revenue[3]} | "
            f"Date: {revenue[4]} | "
            f"Quantity: {revenue[5]:.2f} | "
            f"Price/Unit: {revenue[6]:.2f} | "
            f"Total: {revenue[7]:.2f}"
        )

    connection.close()


#! Update Revenue
def update_revenue():
    print("\n>>> UPDATE REVENUE <<<")

    revenue_id = validators.get_positive_integer("Enter Revenue ID: ")

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT
            r.revenue_id,
            fr.name,
            f.field_name,
            cp.crop_name,
            r.sale_date,
            r.quantity,
            r.price_per_unit,
            r.total_amount
        FROM revenues r
        JOIN crop_plans cp ON r.crop_id = cp.crop_id
        JOIN fields f ON cp.field_id = f.field_id
        JOIN farmers fr ON f.farmer_id = fr.farmer_id
        WHERE r.revenue_id = ?
    """

    cursor.execute(query, (revenue_id,))
    revenue = cursor.fetchone()

    if not revenue:
        print("\nRevenue not found. Please enter a valid revenue ID.")
        connection.close()
        return

    print("\nCurrent Revenue:")
    print(f"Farmer: {revenue[1]}")
    print(f"Field: {revenue[2]}")
    print(f"Crop: {revenue[3]}")
    print(f"Sale Date: {revenue[4]}")
    print(f"Quantity: {revenue[5]}")
    print(f"Price Per Unit: {revenue[6]}")
    print(f"Total Amount: {revenue[7]}")

    print("\nWhat would you like to update?")
    print("1. Sale Date")
    print("2. Quantity")
    print("3. Price Per Unit")
    print("4. All Information")
    print("5. Cancel")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        new_sale_date = validators.get_date("Enter new sale date (YYYY-MM-DD): ")

        update_query = """
            UPDATE revenues
            SET sale_date = ?
            WHERE revenue_id = ?
        """

        cursor.execute(update_query, (new_sale_date, revenue_id))
        connection.commit()

        print("\nRevenue sale date updated successfully!")

    elif choice == "2":
        new_quantity = validators.get_positive_number("Enter new quantity sold: ")

        current_price = revenue[6]
        new_total_amount = new_quantity * current_price

        update_query = """
            UPDATE revenues
            SET quantity = ?,
                total_amount = ?
            WHERE revenue_id = ?
        """

        cursor.execute(update_query, (new_quantity, new_total_amount, revenue_id))
        connection.commit()

        print("\nRevenue quantity updated successfully!")
        print(f"New Total Amount: {new_total_amount:.2f}")

    elif choice == "3":
        new_price_per_unit = validators.get_positive_number(
            "Enter new price per unit: "
        )

        current_quantity = revenue[5]
        new_total_amount = current_quantity * new_price_per_unit

        update_query = """
            UPDATE revenues
            SET price_per_unit = ?,
                total_amount = ?
            WHERE revenue_id = ?
        """

        cursor.execute(update_query, (new_price_per_unit, new_total_amount, revenue_id))
        connection.commit()

        print("\nRevenue price per unit updated successfully!")
        print(f"New Total Amount: {new_total_amount:.2f}")

    elif choice == "4":
        print("\n>>> UPDATE ALL REVENUE INFORMATION <<<")

        new_sale_date = validators.get_date("Enter new sale date (YYYY-MM-DD): ")

        new_quantity = validators.get_positive_number("Enter new quantity sold: ")

        new_price_per_unit = validators.get_positive_number(
            "Enter new price per unit: "
        )

        new_total_amount = new_quantity * new_price_per_unit

        update_query = """
            UPDATE revenues
            SET sale_date = ?,
                quantity = ?,
                price_per_unit = ?,
                total_amount = ?
            WHERE revenue_id = ?
        """

        cursor.execute(
            update_query,
            (
                new_sale_date,
                new_quantity,
                new_price_per_unit,
                new_total_amount,
                revenue_id,
            ),
        )

        connection.commit()

        print("\nRevenue information updated successfully!")
        print(f"New Total Amount: {new_total_amount:.2f}")

    elif choice == "5":
        print("\nUpdate cancelled.")

    else:
        print("\nInvalid choice. Please select a number from 1 to 5.")

    connection.close()


#! Delete Revenue
def delete_revenue():
    print("\n>>> DELETE REVENUE <<<")

    revenue_id = validators.get_positive_integer("Enter Revenue ID: ")

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT
            r.revenue_id,
            fr.name,
            f.field_name,
            cp.crop_name,
            r.sale_date,
            r.quantity,
            r.price_per_unit,
            r.total_amount
        FROM revenues r
        JOIN crop_plans cp ON r.crop_id = cp.crop_id
        JOIN fields f ON cp.field_id = f.field_id
        JOIN farmers fr ON f.farmer_id = fr.farmer_id
        WHERE r.revenue_id = ?
    """

    cursor.execute(query, (revenue_id,))
    revenue = cursor.fetchone()

    if not revenue:
        print("\nRevenue not found. Please enter a valid revenue ID.")
        connection.close()
        return

    print("\nRevenue Details:")
    print(f"Farmer: {revenue[1]}")
    print(f"Field: {revenue[2]}")
    print(f"Crop: {revenue[3]}")
    print(f"Sale Date: {revenue[4]}")
    print(f"Quantity: {revenue[5]}")
    print(f"Price Per Unit: {revenue[6]}")
    print(f"Total Amount: {revenue[7]}")

    confirmation = (
        input("\nAre you sure you want to delete this revenue record? (yes/no): ")
        .strip()
        .lower()
    )

    if confirmation == "yes":

        delete_query = """
            DELETE FROM revenues
            WHERE revenue_id = ?
        """

        cursor.execute(delete_query, (revenue_id,))
        connection.commit()

        print("\nRevenue record deleted successfully!")

    else:
        print("\nDeletion cancelled.")

    connection.close()
