from database import get_conn


def farm_summary():
    print("\n===== FARM SUMMARY =====")

    connection = get_conn()
    cursor = connection.cursor()

    #! Total Number of Farmers
    query = "SELECT COUNT(*) FROM farmers"
    cursor.execute(query)
    total_farmers = cursor.fetchone()[0]

    #! Total Number of Fields
    query = "SELECT COUNT(*) FROM fields"
    cursor.execute(query)
    total_fields = cursor.fetchone()[0]

    #! Total Number of Crop_plans
    query = "SELECT COUNT(*) FROM crop_plans"
    cursor.execute(query)
    total_crop_plans = cursor.fetchone()[0]

    #! Total Number of Farming_activities
    query = "SELECT COUNT(*) FROM activities"
    cursor.execute(query)
    total_activities = cursor.fetchone()[0]

    #! Total Number of Expenses
    query = "SELECT COUNT(*) FROM expenses"
    cursor.execute(query)
    total_expenses = cursor.fetchone()[0]

    #! Total Number of Harvests
    query = "SELECT COUNT(*) FROM harvests"
    cursor.execute(query)
    total_harvests = cursor.fetchone()[0]

    #! Total Number of Revenues
    query = "SELECT COUNT(*) FROM revenues"
    cursor.execute(query)
    total_revenues = cursor.fetchone()[0]

    print(f"\nTotal Farmers  : {total_farmers}")
    print(f"Total Fields     : {total_fields}")
    print(f"Total Crop Plans : {total_crop_plans}")
    print(f"Total Activities : {total_activities}")
    print(f"Total Expenses   : {total_expenses}")
    print(f"Total Harvests   : {total_harvests}")
    print(f"Total Revenues   : {total_revenues}")

    connection.close()


#!Crop Report
def crop_performance():
    print("\n===== CROP PERFORMANCE =====")

    connection = get_conn()
    cursor = connection.cursor()

    #! Get Crop ID, Crop Name, Farmer Name and Field Name
    query = """
        SELECT
            cp.crop_id,
            cp.crop_name,
            fr.name,
            f.field_name,
            
    #! Calculate total expense, total harvest and total revenue for each crop
            COALESCE(
                (SELECT SUM(e.amount)
                 FROM expenses e
                 WHERE e.crop_id = cp.crop_id),
                0
            ) AS total_expense,

            COALESCE(
                (SELECT SUM(h.quantity)
                 FROM harvests h
                 WHERE h.crop_id = cp.crop_id),
                0
            ) AS total_harvest,

            COALESCE(
                (SELECT SUM(r.total_amount)
                 FROM revenues r
                 WHERE r.crop_id = cp.crop_id),
                0
            ) AS total_revenue

        FROM crop_plans cp

        INNER JOIN fields f
            ON cp.field_id = f.field_id

        INNER JOIN farmers fr
            ON f.farmer_id = fr.farmer_id

        ORDER BY cp.crop_id ASC
    """

    cursor.execute(query)

    crops = cursor.fetchall()

    if not crops:
        print("\nNo crop records found.")
        connection.close()
        return

    for crop in crops:

        crop_id = crop[0]
        crop_name = crop[1]
        farmer_name = crop[2]
        field_name = crop[3]
        total_expense = crop[4]
        total_harvest = crop[5]
        total_revenue = crop[6]

        #! Calculate profit or loss
        profit_loss = total_revenue - total_expense

        print("\n" + "-" * 40)
        print(f"Crop ID        : {crop_id}")
        print(f"Crop Name      : {crop_name}")
        print(f"Farmer         : {farmer_name}")
        print(f"Field          : {field_name}")
        print(f"Total Expense  : Rs. {total_expense:.2f}")
        print(f"Total Harvest  : {total_harvest:.2f}")
        print(f"Total Revenue  : Rs. {total_revenue:.2f}")
        print(f"Profit/Loss    : Rs. {profit_loss:.2f}")

    print("-" * 40)

    connection.close()


#! Expense Report
def expense_analysis():
    print("\n===== EXPENSE ANALYSIS =====")

    connection = get_conn()
    cursor = connection.cursor()

    #! Get farmer name, crop name, expense type and expense amount
    query = """
        SELECT
            fr.name,
            cp.crop_name,
            e.expense_type,
            e.amount
        FROM expenses e
        INNER JOIN crop_plans cp
            ON e.crop_id = cp.crop_id
        INNER JOIN fields f
            ON cp.field_id = f.field_id
        INNER JOIN farmers fr
            ON f.farmer_id = fr.farmer_id
        ORDER BY fr.name, cp.crop_name, e.expense_type
    """

    cursor.execute(query)

    #! Get all expense records
    expenses = cursor.fetchall()

    #! Check if expense records exist
    if not expenses:
        print("\nNo expense records found.")
        connection.close()
        return

    current_farmer = None
    current_crop = None
    crop_total = 0
    farmer_total = 0

    #! Display expenses farmer-wise and crop-wise
    for expense in expenses:

        farmer_name = expense[0]
        crop_name = expense[1]
        expense_type = expense[2]
        amount = expense[3]

        #! Check if farmer has changed
        if farmer_name != current_farmer:

            if current_farmer is not None:

                #! Display total for the previous crop
                if current_crop is not None:
                    print(f"Crop Total     : Rs. {crop_total:.2f}")
                    print()

                #! Display total for the previous farmer
                print(f"Farmer Total   : Rs. {farmer_total:.2f}")
                print("-" * 40)

            print(f"\nFarmer: {farmer_name}")

            current_farmer = farmer_name
            current_crop = None
            crop_total = 0
            farmer_total = 0

        #! Check if crop has changed
        if crop_name != current_crop:

            if current_crop is not None:
                print(f"Crop Total     : Rs. {crop_total:.2f}")
                print()

            print(f"\nCrop: {crop_name}")
            print("-" * 40)

            current_crop = crop_name
            crop_total = 0

        print(f"{expense_type:<18}: Rs. {amount:.2f}")

        #! Add expense amount to crop and farmer totals
        crop_total = crop_total + amount
        farmer_total = farmer_total + amount

    if current_crop is not None:
        print(f"Crop Total     : Rs. {crop_total:.2f}")

    if current_farmer is not None:
        print(f"\nFarmer Total   : Rs. {farmer_total:.2f}")

    connection.close()


#! Revenue and Profit/Loss Report
def revenue_profit_loss():
    print("\n===== REVENUE AND PROFIT/LOSS =====")

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT
            fr.name,
            cp.crop_name,

            COALESCE(
                (SELECT SUM(e.amount)
                 FROM expenses e
                 WHERE e.crop_id = cp.crop_id),
                0
            ) AS total_expense,

            COALESCE(
                (SELECT SUM(r.total_amount)
                 FROM revenues r
                 WHERE r.crop_id = cp.crop_id),
                0
            ) AS total_revenue

        FROM crop_plans cp
        INNER JOIN fields f
            ON cp.field_id = f.field_id
        INNER JOIN farmers fr
            ON f.farmer_id = fr.farmer_id

        ORDER BY fr.name, cp.crop_id
    """

    cursor.execute(query)

    records = cursor.fetchall()

    if not records:
        print("\nNo revenue records found.")
        connection.close()
        return

    current_farmer = None
    farmer_total_expense = 0
    farmer_total_revenue = 0

    farm_total_expense = 0
    farm_total_revenue = 0

    for record in records:
        farmer_name = record[0]
        crop_name = record[1]
        total_expense = record[2]
        total_revenue = record[3]

        if farmer_name != current_farmer:

            if current_farmer is not None:
                farmer_profit_loss = farmer_total_revenue - farmer_total_expense

                print(f"\nFarmer Total Expense : Rs. {farmer_total_expense:.2f}")
                print(f"Farmer Total Revenue : Rs. {farmer_total_revenue:.2f}")
                print(f"Farmer Profit/Loss   : Rs. {farmer_profit_loss:.2f}")
                print("-" * 40)

            #! Display new farmer
            print(f"\nFarmer: {farmer_name}")

            current_farmer = farmer_name

            farmer_total_expense = 0
            farmer_total_revenue = 0

        profit_loss = total_revenue - total_expense

        print(f"\nCrop: {crop_name}")
        print("-" * 40)
        print(f"Total Expense : Rs. {total_expense:.2f}")
        print(f"Total Revenue : Rs. {total_revenue:.2f}")
        print(f"Profit/Loss   : Rs. {profit_loss:.2f}")

        # Add crop totals to farmer totals
        farmer_total_expense = farmer_total_expense + total_expense
        farmer_total_revenue = farmer_total_revenue + total_revenue

        # Add crop totals to farm totals
        farm_total_expense = farm_total_expense + total_expense
        farm_total_revenue = farm_total_revenue + total_revenue

    # Display total for the last farmer
    if current_farmer is not None:
        farmer_profit_loss = farmer_total_revenue - farmer_total_expense

        print(f"\nFarmer Total Expense : Rs. {farmer_total_expense:.2f}")
        print(f"Farmer Total Revenue : Rs. {farmer_total_revenue:.2f}")
        print(f"Farmer Profit/Loss   : Rs. {farmer_profit_loss:.2f}")
        print("-" * 40)

    farm_profit_loss = farm_total_revenue - farm_total_expense

    print("\n===== FARM TOTAL =====")
    print(f"Total Expense : Rs. {farm_total_expense:.2f}")
    print(f"Total Revenue : Rs. {farm_total_revenue:.2f}")
    print(f"Profit/Loss   : Rs. {farm_profit_loss:.2f}")

    connection.close()
