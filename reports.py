import csv
import matplotlib.pyplot as plt
from pathlib import Path
from database import get_conn


#! Farm Summary
def farm_summary():
    print("\n===== FARM SUMMARY =====")

    connection = get_conn()
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM farmers"
    cursor.execute(query)
    total_farmers = cursor.fetchone()[0]

    query = "SELECT COUNT(*) FROM fields"
    cursor.execute(query)
    total_fields = cursor.fetchone()[0]

    query = "SELECT COUNT(*) FROM crop_plans"
    cursor.execute(query)
    total_crop_plans = cursor.fetchone()[0]

    query = "SELECT COUNT(*) FROM activities"
    cursor.execute(query)
    total_activities = cursor.fetchone()[0]

    query = "SELECT COUNT(*) FROM expenses"
    cursor.execute(query)
    total_expenses = cursor.fetchone()[0]

    query = "SELECT COUNT(*) FROM harvests"
    cursor.execute(query)
    total_harvests = cursor.fetchone()[0]

    query = "SELECT COUNT(*) FROM revenues"
    cursor.execute(query)
    total_revenues = cursor.fetchone()[0]

    summary = [
        ["Farmers", total_farmers],
        ["Fields", total_fields],
        ["Crop Plans", total_crop_plans],
        ["Activities", total_activities],
        ["Expenses", total_expenses],
        ["Harvests", total_harvests],
        ["Revenues", total_revenues],
    ]

    print(f"\nTotal Farmers  : {total_farmers}")
    print(f"Total Fields     : {total_fields}")
    print(f"Total Crop Plans : {total_crop_plans}")
    print(f"Total Activities : {total_activities}")
    print(f"Total Expenses   : {total_expenses}")
    print(f"Total Harvests   : {total_harvests}")
    print(f"Total Revenues   : {total_revenues}")

    connection.close()

    return summary

#! Crop Performance
def crop_performance():
    print("\n===== CROP PERFORMANCE =====")

    performance = []

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT
            cp.crop_id,
            cp.crop_name,
            fr.name,
            f.field_name,

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
        return []

    for crop in crops:
        crop_id = crop[0]
        crop_name = crop[1]
        farmer_name = crop[2]
        field_name = crop[3]
        total_expense = crop[4]
        total_harvest = crop[5]
        total_revenue = crop[6]

        profit_loss = total_revenue - total_expense

        performance.append(
            [
                crop_id,
                crop_name,
                farmer_name,
                field_name,
                total_expense,
                total_harvest,
                total_revenue,
                profit_loss,
            ]
        )

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

    return performance


#! Expense Analysis
def expense_analysis():
    print("\n===== EXPENSE ANALYSIS =====")

    expenses = []

    connection = get_conn()
    cursor = connection.cursor()

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
    expense_records = cursor.fetchall()

    if not expense_records:
        print("\nNo expense records found.")
        connection.close()
        return []

    current_farmer = None
    current_crop = None

    crop_total = 0
    farmer_total = 0

    for expense in expense_records:

        farmer_name = expense[0]
        crop_name = expense[1]
        expense_type = expense[2]
        amount = expense[3]

        expenses.append([farmer_name, crop_name, expense_type, amount])

        if farmer_name != current_farmer:

            if current_farmer is not None:

                if current_crop is not None:
                    print(f"Crop Total     : Rs. {crop_total:.2f}")
                    print()

                print(f"Farmer Total   : Rs. {farmer_total:.2f}")
                print("-" * 40)

            print(f"\nFarmer: {farmer_name}")

            current_farmer = farmer_name
            current_crop = None
            crop_total = 0
            farmer_total = 0

        if crop_name != current_crop:

            if current_crop is not None:
                print(f"Crop Total     : Rs. {crop_total:.2f}")
                print()

            print(f"\nCrop: {crop_name}")
            print("-" * 40)

            current_crop = crop_name
            crop_total = 0

        print(f"{expense_type:<18}: Rs. {amount:.2f}")

        crop_total = crop_total + amount
        farmer_total = farmer_total + amount

    if current_crop is not None:
        print(f"Crop Total     : Rs. {crop_total:.2f}")

    if current_farmer is not None:
        print(f"\nFarmer Total   : Rs. {farmer_total:.2f}")

    connection.close()

    return expenses


#! Revenue and Profit/Loss
def revenue_profit_loss():
    print("\n===== REVENUE AND PROFIT/LOSS =====")

    revenue_data = []

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
        return []

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

                print(f"\nFarmer Total Expense : " f"Rs. {farmer_total_expense:.2f}")

                print(f"Farmer Total Revenue : " f"Rs. {farmer_total_revenue:.2f}")

                print(f"Farmer Profit/Loss   : " f"Rs. {farmer_profit_loss:.2f}")

                print("-" * 40)

            print(f"\nFarmer: {farmer_name}")

            current_farmer = farmer_name

            farmer_total_expense = 0
            farmer_total_revenue = 0

        profit_loss = total_revenue - total_expense

        revenue_data.append(
            [farmer_name, crop_name, total_expense, total_revenue, profit_loss]
        )

        print(f"\nCrop: {crop_name}")
        print("-" * 40)
        print(f"Total Expense : Rs. {total_expense:.2f}")
        print(f"Total Revenue : Rs. {total_revenue:.2f}")
        print(f"Profit/Loss   : Rs. {profit_loss:.2f}")

        farmer_total_expense = farmer_total_expense + total_expense

        farmer_total_revenue = farmer_total_revenue + total_revenue

        farm_total_expense = farm_total_expense + total_expense

        farm_total_revenue = farm_total_revenue + total_revenue

    if current_farmer is not None:

        farmer_profit_loss = farmer_total_revenue - farmer_total_expense

        print(f"\nFarmer Total Expense : " f"Rs. {farmer_total_expense:.2f}")

        print(f"Farmer Total Revenue : " f"Rs. {farmer_total_revenue:.2f}")

        print(f"Farmer Profit/Loss   : " f"Rs. {farmer_profit_loss:.2f}")

        print("-" * 40)

    farm_profit_loss = farm_total_revenue - farm_total_expense

    print("\n===== FARM TOTAL =====")
    print(f"Total Expense : Rs. {farm_total_expense:.2f}")
    print(f"Total Revenue : Rs. {farm_total_revenue:.2f}")
    print(f"Profit/Loss   : Rs. {farm_profit_loss:.2f}")

    connection.close()

    return revenue_data


#! Export Farm Summary
def export_farm_summary(summary):
    print("\n===== EXPORT FARM SUMMARY =====")

    Path("exports").mkdir(exist_ok=True)

    with open("exports/farm_summary.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Report", "Total"])

        for item in summary:
            writer.writerow(item)

    print("\nFarm summary exported successfully.")
    print("File saved at: exports/farm_summary.csv")


#! Export Crop Performance
def export_crop_performance(performance):
    print("\n===== EXPORT CROP PERFORMANCE =====")

    Path("exports").mkdir(exist_ok=True)

    with open("exports/crop_performance.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Crop ID",
                "Crop Name",
                "Farmer",
                "Field",
                "Total Expense",
                "Total Harvest",
                "Total Revenue",
                "Profit/Loss",
            ]
        )

        for crop in performance:
            writer.writerow(crop)

    print("\nCrop performance exported successfully.")
    print("File saved at: exports/crop_performance.csv")


#! Export Expense Analysis
def export_expense_analysis(expenses):
    print("\n===== EXPORT EXPENSE ANALYSIS =====")

    Path("exports").mkdir(exist_ok=True)

    with open("exports/expense_analysis.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Farmer", "Crop", "Expense Type", "Total Expense"])

        for expense in expenses:
            writer.writerow(expense)

    print("\nExpense analysis exported successfully.")
    print("File saved at: exports/expense_analysis.csv")


#! Export Revenue and Profit/Loss
def export_revenue_profit_loss(revenue_data):
    print("\n===== EXPORT REVENUE AND PROFIT/LOSS =====")

    Path("exports").mkdir(exist_ok=True)

    with open("exports/revenue_profit_loss.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(
            ["Farmer", "Crop", "Total Expense", "Total Revenue", "Profit/Loss"]
        )

        for record in revenue_data:
            writer.writerow(record)

    print("\nRevenue and profit/loss report exported successfully.")
    print("File saved at: exports/revenue_profit_loss.csv")


#! Export Reports Menu
def export_reports():

    while True:

        print("\n===== EXPORT REPORTS =====")
        print("1. Export Farm Summary")
        print("2. Export Crop Performance")
        print("3. Export Expense Analysis")
        print("4. Export Revenue and Profit/Loss")
        print("5. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            summary = farm_summary()
            export_farm_summary(summary)

        elif choice == "2":

            performance = crop_performance()
            export_crop_performance(performance)

        elif choice == "3":

            expenses = expense_analysis()
            export_expense_analysis(expenses)

        elif choice == "4":

            revenue_data = revenue_profit_loss()
            export_revenue_profit_loss(revenue_data)

        elif choice == "5":
            break

        else:
            print("\nInvalid choice. Please select 1 to 5.")


#! Expense by Crop Chart
def expense_by_crop_chart():

    print("\n===== EXPENSE BY CROP CHART =====")

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT
            cp.crop_name,
            SUM(e.amount) AS total_expense

        FROM expenses e

        INNER JOIN crop_plans cp
            ON e.crop_id = cp.crop_id

        GROUP BY cp.crop_name

        ORDER BY total_expense DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    connection.close()

    if not results:
        print("\nNo expense data found.")
        return

    crop_names = []
    total_expenses = []

    for result in results:
        crop_names.append(result[0])
        total_expenses.append(result[1])

    plt.figure(figsize=(10, 6))

    plt.bar(crop_names, total_expenses, color="#356B2F")

    plt.title("Expense by Crop")
    plt.xlabel("Crop")
    plt.ylabel("Total Expense (Rs.)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    Path("charts").mkdir(exist_ok=True)

    plt.savefig("charts/expense_by_crop.png")
    plt.close()

    print("\nExpense by crop chart generated successfully.")
    print("File saved at: charts/expense_by_crop.png")


#! Revenue by Crop Chart
def revenue_by_crop_chart():

    print("\n===== REVENUE BY CROP CHART =====")

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT
            cp.crop_name,
            SUM(r.total_amount) AS total_revenue

        FROM revenues r

        INNER JOIN crop_plans cp
            ON r.crop_id = cp.crop_id

        GROUP BY cp.crop_name

        ORDER BY total_revenue DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    connection.close()

    if not results:
        print("\nNo revenue data found.")
        return

    crop_names = []
    total_revenues = []

    for row in results:
        crop_names.append(row[0])
        total_revenues.append(row[1])

    plt.figure(figsize=(10, 6))

    plt.bar(crop_names, total_revenues, color="#4F8A3D")

    plt.title("Revenue by Crop")
    plt.xlabel("Crop")
    plt.ylabel("Total Revenue (Rs.)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    Path("charts").mkdir(exist_ok=True)

    plt.savefig("charts/revenue_by_crop.png")
    plt.close()

    print("\nRevenue by crop chart generated successfully.")
    print("File saved at: charts/revenue_by_crop.png")


#! Profit/Loss by Crop Chart
def profit_loss_by_crop_chart():

    print("\n===== PROFIT/LOSS BY CROP CHART =====")

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT
            cp.crop_name,
            fr.name,

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

        ORDER BY cp.crop_id ASC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    connection.close()

    if not results:
        print("\nNo crop data found.")
        return

    crop_names = []
    profit_losses = []

    for row in results:

        crop_name = row[0]
        farmer_name = row[1]
        total_expense = row[2]
        total_revenue = row[3]

        profit_loss = total_revenue - total_expense

        crop_label = f"{crop_name} - {farmer_name}"

        crop_names.append(crop_label)
        profit_losses.append(profit_loss)

    plt.figure(figsize=(10, 6))

    bars = plt.barh(crop_names, profit_losses, color="#6A994E")

    plt.bar_label(bars, fmt="Rs. %.0f", padding=5)

    plt.xlim(0, max(profit_losses) * 1.15)

    plt.title("Profit/Loss by Crop Plan")
    plt.xlabel("Profit/Loss (Rs.)")
    plt.ylabel("Crop Plan")

    plt.gca().invert_yaxis()

    plt.tight_layout()

    Path("charts").mkdir(exist_ok=True)

    plt.savefig("charts/profit_loss_by_crop.png")
    plt.close()

    print("\nProfit/Loss by crop chart generated successfully.")
    print("File saved at: charts/profit_loss_by_crop.png")


#! Expense Distribution by Farmer Chart
def expense_distribution_by_farmer_chart():

    print("\n===== EXPENSE DISTRIBUTION BY FARMER CHART =====")

    connection = get_conn()
    cursor = connection.cursor()

    query = """
        SELECT
            fr.name,
            SUM(e.amount) AS total_expense

        FROM expenses e

        INNER JOIN crop_plans cp
            ON e.crop_id = cp.crop_id

        INNER JOIN fields f
            ON cp.field_id = f.field_id

        INNER JOIN farmers fr
            ON f.farmer_id = fr.farmer_id

        GROUP BY fr.farmer_id, fr.name

        ORDER BY total_expense DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    connection.close()

    if not results:
        print("\nNo expense data found.")
        return

    farmer_names = []
    total_expenses = []

    for result in results:
        farmer_names.append(result[0])
        total_expenses.append(result[1])

    plt.figure(figsize=(8, 8))

    plt.pie(
        total_expenses,
        labels=farmer_names,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#4F8A3D", "#6A994E", "#C9A227"],
    )

    plt.title("Expense Distribution by Farmer")

    plt.axis("equal")
    plt.tight_layout()

    Path("charts").mkdir(exist_ok=True)

    plt.savefig("charts/expense_distribution_by_farmer.png")

    plt.close()

    print("\nExpense distribution by farmer " "chart generated successfully.")

    print("File saved at: " "charts/expense_distribution_by_farmer.png")
