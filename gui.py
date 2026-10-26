import re
import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from database import create_tables, get_conn
import services
import validators

TITLE = "FarmTrack — Farm Record & Crop Planning System"

window = tk.Tk()
window.title("FarmTrack")
window.geometry("1000x680")
window.minsize(860, 560)

main_frame = tk.Frame(window, padx=25, pady=25)
main_frame.pack(fill="both", expand=True)

area_units = ["Ropani", "Aana", "Bigha", "Kattha", "Dhur", "Hectare", "Square Meter"]
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
seasons = ["Spring", "Summer", "Autumn", "Winter"]
crop_statuses = ["Planned", "Growing", "Harvested"]
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


def clear_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()


def show_message(title, message, kind="info"):
    if kind == "error":
        messagebox.showerror(title, message)
    elif kind == "warning":
        messagebox.showwarning(title, message)
    else:
        messagebox.showinfo(title, message)


def normalize_phone(value):
    value = (value or "").strip()
    digits = re.sub(r"[^0-9]", "", value)
    if digits.startswith("977"):
        digits = digits[3:]
    if digits.startswith("0"):
        digits = digits[1:]
    return digits


def validate_farmer_name(name):
    cleaned = (name or "").strip()
    if not cleaned:
        return False, "Farmer name is required."
    if not cleaned.replace(" ", "").isalpha():
        return False, "Use letters and spaces only for the farmer name."
    return True, cleaned


def validate_phone_number(value):
    normalized = normalize_phone(value)
    if not normalized:
        return False, "Phone number is required."
    if re.fullmatch(r"9[678]\d{8}", normalized):
        return True, normalized
    return False, "Enter a valid Nepali mobile number like 98XXXXXXXX."


def validate_positive_number(value, field_name):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False, f"{field_name} must be a valid number."
    if number <= 0:
        return False, f"{field_name} must be greater than zero."
    return True, number


def validate_date_string(value, field_name):
    if not validators.is_valid_date(value):
        return False, f"{field_name} must be a valid date in YYYY-MM-DD format."
    return True, value


def get_all_farmers():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT farmer_id, name, phone, location FROM farmers ORDER BY farmer_id"
        )
        return cursor.fetchall()


def get_all_fields():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.field_id, fr.name, f.field_name, f.area, f.area_unit, f.soil_type, f.irrigation
            FROM fields f
            INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
            ORDER BY f.field_id
            """)
        return cursor.fetchall()


def get_all_crop_plans():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cp.crop_id, fr.name, f.field_name, cp.crop_name, cp.variety, cp.season,
                   cp.planting_date, cp.expected_harvest_date, cp.status
            FROM crop_plans cp
            INNER JOIN fields f ON cp.field_id = f.field_id
            INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
            ORDER BY cp.crop_id
            """)
        return cursor.fetchall()


def get_all_activities():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.activity_id, fr.name, f.field_name, cp.crop_name, a.activity_type,
                   a.activity_date, a.description
            FROM activities a
            INNER JOIN crop_plans cp ON a.crop_id = cp.crop_id
            INNER JOIN fields f ON cp.field_id = f.field_id
            INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
            ORDER BY a.activity_id
            """)
        return cursor.fetchall()


def get_all_expenses():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.expense_id, fr.name, f.field_name, cp.crop_name, e.expense_type,
                   e.amount, e.expense_date, e.description
            FROM expenses e
            INNER JOIN crop_plans cp ON e.crop_id = cp.crop_id
            INNER JOIN fields f ON cp.field_id = f.field_id
            INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
            ORDER BY e.expense_id
            """)
        return cursor.fetchall()


def get_all_harvests():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT h.harvest_id, fr.name, f.field_name, cp.crop_name, h.harvest_date,
                   h.quantity, h.unit
            FROM harvests h
            INNER JOIN crop_plans cp ON h.crop_id = cp.crop_id
            INNER JOIN fields f ON cp.field_id = f.field_id
            INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
            ORDER BY h.harvest_id
            """)
        return cursor.fetchall()


def get_all_revenues():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.revenue_id, fr.name, f.field_name, cp.crop_name, r.sale_date,
                   r.quantity, r.price_per_unit, r.total_amount
            FROM revenues r
            INNER JOIN crop_plans cp ON r.crop_id = cp.crop_id
            INNER JOIN fields f ON cp.field_id = f.field_id
            INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
            ORDER BY r.revenue_id
            """)
        return cursor.fetchall()


def get_farmer_dropdown_values():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT farmer_id, name FROM farmers ORDER BY farmer_id")
        return cursor.fetchall()


def get_field_dropdown_values(farmer_id=None):
    with get_conn() as conn:
        cursor = conn.cursor()
        if farmer_id is None:
            cursor.execute("""
                SELECT f.field_id, fr.name, f.field_name
                FROM fields f
                INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
                ORDER BY f.field_id
                """)
        else:
            cursor.execute(
                """
                SELECT f.field_id, fr.name, f.field_name
                FROM fields f
                INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
                WHERE f.farmer_id = ?
                ORDER BY f.field_id
                """,
                (farmer_id,),
            )
        # IDs keep the labels distinct when farmers or fields share names.
        return [
            (
                field_id,
                f"Field #{field_id} - {farmer_name} / {field_name}",
            )
            for field_id, farmer_name, field_name in cursor.fetchall()
        ]


def get_crop_dropdown_values():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cp.crop_id, fr.name, f.field_name, cp.crop_name
            FROM crop_plans cp
            INNER JOIN fields f ON cp.field_id = f.field_id
            INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
            ORDER BY cp.crop_id
            """)
        # Crop IDs prevent duplicate crop and field names from making edits ambiguous.
        return [
            (
                crop_id,
                f"Crop #{crop_id} - {farmer_name} / {field_name} / {crop_name}",
            )
            for crop_id, farmer_name, field_name, crop_name in cursor.fetchall()
        ]


def show_dashboard():
    clear_screen()
    title_label = tk.Label(main_frame, text="FarmTrack", font=("Arial", 28, "bold"))
    title_label.pack(pady=(10, 5))

    subtitle_label = tk.Label(
        main_frame, text="Farm Record & Crop Planning System", font=("Arial", 13)
    )
    subtitle_label.pack(pady=(0, 20))

    dashboard_buttons = [
        ("Farmer Management", show_farmer_management),
        ("Field Management", show_field_management),
        ("Crop Planning", show_crop_management),
        ("Farming Activities", show_activity_management),
        ("Expense Management", show_expense_management),
        ("Harvest & Revenue", show_harvest_revenue_management),
        ("Reports", show_reports),
        ("Exit", lambda: window.destroy()),
    ]

    for text, command in dashboard_buttons:
        tk.Button(
            main_frame,
            text=text,
            width=30,
            height=2,
            command=command,
            font=("Arial", 10, "bold"),
        ).pack(pady=6)


def show_reports():
    clear_screen()
    tk.Label(main_frame, text="Reports & Summary", font=("Arial", 22, "bold")).pack(
        pady=20
    )

    table = ttk.Treeview(
        main_frame, columns=("category", "count"), show="headings", height=10
    )
    table.heading("category", text="Category")
    table.heading("count", text="Record Count")
    table.column("category", width=220, anchor="center")
    table.column("count", width=140, anchor="center")
    table.pack(fill="x", pady=10)

    queries = [
        ("Farmers", "SELECT COUNT(*) FROM farmers"),
        ("Fields", "SELECT COUNT(*) FROM fields"),
        ("Crop Plans", "SELECT COUNT(*) FROM crop_plans"),
        ("Activities", "SELECT COUNT(*) FROM activities"),
        ("Expenses", "SELECT COUNT(*) FROM expenses"),
        ("Harvests", "SELECT COUNT(*) FROM harvests"),
        ("Revenues", "SELECT COUNT(*) FROM revenues"),
    ]

    with get_conn() as conn:
        for title, query in queries:
            result = conn.execute(query).fetchone()[0]
            table.insert("", tk.END, values=(title, result))

    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=20)
    tk.Button(button_frame, text="Back to Dashboard", command=show_dashboard).pack(
        side="left", padx=10
    )


def build_table(frame, columns, headings):
    table = ttk.Treeview(frame, columns=columns, show="headings")
    for column, heading in zip(columns, headings):
        table.heading(column, text=heading)
        table.column(column, width=120, anchor="center")
    table.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
    scrollbar.pack(side="right", fill="y")
    table.configure(yscrollcommand=scrollbar.set)
    return table


def show_farmer_management():
    clear_screen()
    tk.Label(main_frame, text="Farmer Management", font=("Arial", 22, "bold")).pack(
        pady=(10, 15)
    )

    form_frame = tk.LabelFrame(main_frame, text="Farmer Details", padx=12, pady=12)
    form_frame.pack(fill="x", pady=(0, 15))

    fields = {}
    labels = [("Name", "name"), ("Phone", "phone"), ("Location", "location")]
    for index, (label_text, key) in enumerate(labels):
        tk.Label(form_frame, text=f"{label_text}:", width=14, anchor="e").grid(
            row=index, column=0, padx=8, pady=6, sticky="e"
        )
        entry = tk.Entry(form_frame, width=35)
        entry.grid(row=index, column=1, padx=8, pady=6, sticky="w")
        fields[key] = entry

    form_buttons = tk.Frame(form_frame)
    form_buttons.grid(row=3, column=0, columnspan=2, pady=10)

    current_farmer_id = tk.IntVar(value=-1)
    status_var = tk.StringVar(value="")

    def clear_form():
        for key in fields:
            fields[key].delete(0, tk.END)
        current_farmer_id.set(-1)
        status_var.set("Form cleared.")

    def fill_form_from_selection():
        selection = table.selection()
        if not selection:
            show_message(
                "No Farmer Selected",
                "Select a farmer from the table to edit.",
                "warning",
            )
            return
        values = table.item(selection[0], "values")
        current_farmer_id.set(int(values[0]))
        fields["name"].delete(0, tk.END)
        fields["name"].insert(0, values[1])
        fields["phone"].delete(0, tk.END)
        fields["phone"].insert(0, values[2])
        fields["location"].delete(0, tk.END)
        fields["location"].insert(0, values[3])
        status_var.set(f"Editing farmer #{values[0]}.")

    def save_farmer():
        name = fields["name"].get().strip()
        phone = fields["phone"].get().strip()
        location = fields["location"].get().strip()

        valid_name, name_msg = validate_farmer_name(name)
        if not valid_name:
            status_var.set(name_msg)
            return

        valid_phone, phone_msg = validate_phone_number(phone)
        if not valid_phone:
            status_var.set(phone_msg)
            return

        if not location:
            status_var.set("Location is required.")
            return

        with get_conn() as conn:
            cursor = conn.cursor()
            farmer_id = current_farmer_id.get()
            if farmer_id != -1:
                cursor.execute(
                    "SELECT farmer_id FROM farmers WHERE phone = ? AND farmer_id != ?",
                    (phone_msg, farmer_id),
                )
                if cursor.fetchone():
                    status_var.set("This phone number is already registered.")
                    return
                cursor.execute(
                    "UPDATE farmers SET name = ?, phone = ?, location = ? WHERE farmer_id = ?",
                    (name_msg, phone_msg, location, farmer_id),
                )
                status_var.set("Farmer updated successfully.")
            else:
                cursor.execute(
                    "SELECT farmer_id FROM farmers WHERE phone = ?",
                    (phone_msg,),
                )
                if cursor.fetchone():
                    status_var.set("This phone number is already registered.")
                    return
                cursor.execute(
                    "INSERT INTO farmers (name, phone, location) VALUES (?, ?, ?)",
                    (name_msg, phone_msg, location),
                )
                status_var.set("Farmer added successfully.")
        load_farmers_table()
        clear_form()

    def delete_selected_farmer():
        selection = table.selection()
        if not selection:
            show_message(
                "No Farmer Selected",
                "Select a farmer from the table before deleting.",
                "warning",
            )
            return
        farmer_id = int(table.item(selection[0], "values")[0])
        farmer_name = table.item(selection[0], "values")[1]
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete {farmer_name} ({farmer_id}) and all associated fields, crop plans, activities, expenses, harvests, and revenues?",
        )
        if not confirm:
            return
        try:
            success, message = services.delete_farmer_gui(farmer_id)
        except sqlite3.Error as error:
            show_message("Database Error", f"Could not delete farmer: {error}", "error")
            return
        if not success:
            show_message("Cannot Delete Farmer", message, "error")
            return
        status_var.set(message)
        show_message("Farmer Deleted", message)
        load_farmers_table()
        clear_form()

    def load_farmers_table(search_text=""):
        table.delete(*table.get_children())
        with get_conn() as conn:
            cursor = conn.cursor()
            if search_text:
                cursor.execute(
                    "SELECT farmer_id, name, phone, location FROM farmers WHERE name LIKE ? OR phone LIKE ? ORDER BY farmer_id",
                    (f"%{search_text}%", f"%{search_text}%"),
                )
            else:
                cursor.execute(
                    "SELECT farmer_id, name, phone, location FROM farmers ORDER BY farmer_id"
                )
            rows = cursor.fetchall()
        if not rows:
            status_var.set("No farmers found.")
        for row in rows:
            table.insert("", tk.END, values=row)

    table_frame = tk.Frame(main_frame)
    table_frame.pack(fill="both", expand=True)
    table = build_table(
        table_frame,
        ("farmer_id", "name", "phone", "location"),
        ["Farmer ID", "Name", "Phone", "Location"],
    )
    table.column("farmer_id", width=90)
    table.column("name", width=200)
    table.column("phone", width=140)
    table.column("location", width=200)

    search_frame = tk.Frame(main_frame)
    search_frame.pack(fill="x", pady=(8, 0))
    tk.Label(search_frame, text="Search by name or phone:").pack(
        side="left", padx=(0, 8)
    )
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var, width=28)
    search_entry.pack(side="left")
    tk.Button(
        search_frame,
        text="Search",
        command=lambda: load_farmers_table(search_var.get().strip()),
    ).pack(side="left", padx=6)
    tk.Button(
        search_frame,
        text="Clear",
        command=lambda: (search_var.set(""), load_farmers_table()),
    ).pack(side="left", padx=6)

    tk.Button(form_buttons, text="Save Farmer", command=save_farmer).pack(
        side="left", padx=5
    )
    tk.Button(
        form_buttons, text="Edit Selected", command=fill_form_from_selection
    ).pack(side="left", padx=5)
    tk.Button(
        form_buttons, text="Delete Selected", command=delete_selected_farmer
    ).pack(side="left", padx=5)
    tk.Button(form_buttons, text="Clear Form", command=clear_form).pack(
        side="left", padx=5
    )
    tk.Button(form_buttons, text="Back to Dashboard", command=show_dashboard).pack(
        side="left", padx=5
    )

    status_label = tk.Label(main_frame, textvariable=status_var, fg="darkgreen")
    status_label.pack(pady=(8, 0))

    load_farmers_table()


def show_field_management():
    clear_screen()
    tk.Label(main_frame, text="Field Management", font=("Arial", 22, "bold")).pack(
        pady=(10, 15)
    )

    form_frame = tk.LabelFrame(main_frame, text="Field Details", padx=12, pady=12)
    form_frame.pack(fill="x", pady=(0, 15))

    farmer_options = get_farmer_dropdown_values()
    farmer_map = {f"{farmer[0]} - {farmer[1]}": farmer[0] for farmer in farmer_options}
    farmer_label_by_id = {
        farmer_id: f"{farmer_id} - {farmer_name}"
        for farmer_id, farmer_name in farmer_options
    }
    farmer_combo = ttk.Combobox(
        form_frame,
        values=[f"{farmer[0]} - {farmer[1]}" for farmer in farmer_options],
        state="readonly",
        width=35,
    )
    farmer_combo.grid(row=0, column=1, padx=8, pady=6, sticky="w")
    tk.Label(form_frame, text="Farmer:", width=14, anchor="e").grid(
        row=0, column=0, padx=8, pady=6, sticky="e"
    )

    field_name_var = tk.StringVar()
    area_var = tk.StringVar()
    area_unit_var = tk.StringVar(value=area_units[0])
    soil_var = tk.StringVar(value=soil_types[0])
    irrigation_var = tk.StringVar(value=irrigation_types[0])

    tk.Label(form_frame, text="Field Name:", width=14, anchor="e").grid(
        row=1, column=0, padx=8, pady=6, sticky="e"
    )
    tk.Entry(form_frame, textvariable=field_name_var, width=35).grid(
        row=1, column=1, padx=8, pady=6, sticky="w"
    )

    tk.Label(form_frame, text="Area:", width=14, anchor="e").grid(
        row=2, column=0, padx=8, pady=6, sticky="e"
    )
    tk.Entry(form_frame, textvariable=area_var, width=35).grid(
        row=2, column=1, padx=8, pady=6, sticky="w"
    )

    tk.Label(form_frame, text="Area Unit:", width=14, anchor="e").grid(
        row=3, column=0, padx=8, pady=6, sticky="e"
    )
    ttk.Combobox(
        form_frame,
        textvariable=area_unit_var,
        values=area_units,
        state="readonly",
        width=32,
    ).grid(row=3, column=1, padx=8, pady=6, sticky="w")

    tk.Label(form_frame, text="Soil Type:", width=14, anchor="e").grid(
        row=4, column=0, padx=8, pady=6, sticky="e"
    )
    ttk.Combobox(
        form_frame, textvariable=soil_var, values=soil_types, state="readonly", width=32
    ).grid(row=4, column=1, padx=8, pady=6, sticky="w")

    tk.Label(form_frame, text="Irrigation:", width=14, anchor="e").grid(
        row=5, column=0, padx=8, pady=6, sticky="e"
    )
    ttk.Combobox(
        form_frame,
        textvariable=irrigation_var,
        values=irrigation_types,
        state="readonly",
        width=32,
    ).grid(row=5, column=1, padx=8, pady=6, sticky="w")

    current_field_id = tk.IntVar(value=-1)
    status_var = tk.StringVar(value="")

    table_frame = tk.Frame(main_frame)
    table_frame.pack(fill="both", expand=True)
    table = build_table(
        table_frame,
        (
            "field_id",
            "farmer",
            "field_name",
            "area",
            "area_unit",
            "soil_type",
            "irrigation",
        ),
        ["Field ID", "Farmer", "Field Name", "Area", "Unit", "Soil", "Irrigation"],
    )
    table.column("field_id", width=80)
    table.column("farmer", width=150)
    table.column("field_name", width=160)
    table.column("area", width=90)
    table.column("area_unit", width=90)
    table.column("soil_type", width=110)
    table.column("irrigation", width=110)

    def load_fields_table(search_text=""):
        table.delete(*table.get_children())
        with get_conn() as conn:
            cursor = conn.cursor()
            if search_text:
                cursor.execute(
                    """
                    SELECT f.field_id, fr.name, f.field_name, f.area, f.area_unit, f.soil_type, f.irrigation
                    FROM fields f
                    INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
                    WHERE fr.name LIKE ? OR f.field_name LIKE ?
                    ORDER BY f.field_id
                    """,
                    (f"%{search_text}%", f"%{search_text}%"),
                )
            else:
                cursor.execute("""
                    SELECT f.field_id, fr.name, f.field_name, f.area, f.area_unit, f.soil_type, f.irrigation
                    FROM fields f
                    INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
                    ORDER BY f.field_id
                    """)
            rows = cursor.fetchall()
        for row in rows:
            table.insert("", tk.END, values=row)
        if not rows:
            status_var.set("No fields found.")

    def save_field():
        selected_farmer = farmer_combo.get().strip()
        if not selected_farmer:
            status_var.set("Select a valid farmer first.")
            return
        farmer_id = farmer_map.get(selected_farmer)
        if farmer_id is None:
            status_var.set("The selected farmer is invalid.")
            return
        name = field_name_var.get().strip()
        if not name:
            status_var.set("Field name is required.")
            return
        area = area_var.get().strip()
        valid_area, area_value = validate_positive_number(area, "Field area")
        if not valid_area:
            status_var.set(area_value)
            return
        selected_area_unit = area_unit_var.get()
        selected_soil = soil_var.get()
        selected_irrigation = irrigation_var.get()
        with get_conn() as conn:
            cursor = conn.cursor()
            if current_field_id.get() != -1:
                cursor.execute(
                    "UPDATE fields SET farmer_id = ?, field_name = ?, area = ?, area_unit = ?, soil_type = ?, irrigation = ? WHERE field_id = ?",
                    (
                        farmer_id,
                        name,
                        area_value,
                        selected_area_unit,
                        selected_soil,
                        selected_irrigation,
                        current_field_id.get(),
                    ),
                )
                status_var.set("Field updated successfully.")
            else:
                cursor.execute(
                    "INSERT INTO fields (farmer_id, field_name, area, area_unit, soil_type, irrigation) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        farmer_id,
                        name,
                        area_value,
                        selected_area_unit,
                        selected_soil,
                        selected_irrigation,
                    ),
                )
                status_var.set("Field added successfully.")
        load_fields_table()
        clear_field_form()

    def clear_field_form():
        current_field_id.set(-1)
        field_name_var.set("")
        area_var.set("")
        farmer_combo.set("")
        area_unit_var.set(area_units[0])
        soil_var.set(soil_types[0])
        irrigation_var.set(irrigation_types[0])

    def fill_field_for_edit():
        selection = table.selection()
        if not selection:
            show_message(
                "No Field Selected", "Select a field from the table to edit.", "warning"
            )
            return
        values = table.item(selection[0], "values")
        field_id = int(values[0])
        with get_conn() as conn:
            row = conn.execute(
                "SELECT farmer_id FROM fields WHERE field_id = ?", (field_id,)
            ).fetchone()
        if row is None:
            status_var.set("The selected field no longer exists.")
            return
        current_field_id.set(field_id)
        farmer_combo.set(farmer_label_by_id.get(row[0], ""))
        field_name_var.set(values[2])
        area_var.set(values[3])
        area_unit_var.set(values[4])
        soil_var.set(values[5])
        irrigation_var.set(values[6])
        status_var.set(f"Editing field #{values[0]}.")

    def delete_selected_field():
        selection = table.selection()
        if not selection:
            show_message(
                "No Field Selected",
                "Select a field from the table before deleting.",
                "warning",
            )
            return
        field_id = int(table.item(selection[0], "values")[0])
        field_name = table.item(selection[0], "values")[2]
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM crop_plans WHERE field_id = ? LIMIT 1", (field_id,)
            )
            if cursor.fetchone():
                show_message(
                    "Cannot Delete",
                    f"Field '{field_name}' has crop plans linked to it and cannot be deleted safely.",
                    "error",
                )
                return
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete field '{field_name}'? This will not delete related crop data automatically.",
        )
        if confirm:
            with get_conn() as conn:
                conn.execute("DELETE FROM fields WHERE field_id = ?", (field_id,))
            status_var.set(f"Field '{field_name}' deleted successfully.")
            load_fields_table()
            clear_field_form()

    search_frame = tk.Frame(main_frame)
    search_frame.pack(fill="x", pady=(10, 0))
    tk.Label(search_frame, text="Search by farmer or field name:").pack(
        side="left", padx=(0, 8)
    )
    search_var = tk.StringVar()
    tk.Entry(search_frame, textvariable=search_var, width=30).pack(side="left")
    tk.Button(
        search_frame,
        text="Search",
        command=lambda: load_fields_table(search_var.get().strip()),
    ).pack(side="left", padx=6)
    tk.Button(
        search_frame,
        text="Clear",
        command=lambda: (search_var.set(""), load_fields_table()),
    ).pack(side="left", padx=6)

    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=12)
    tk.Button(button_frame, text="Save Field", command=save_field).pack(
        side="left", padx=5
    )
    tk.Button(button_frame, text="Edit Selected", command=fill_field_for_edit).pack(
        side="left", padx=5
    )
    tk.Button(button_frame, text="Delete Selected", command=delete_selected_field).pack(
        side="left", padx=5
    )
    tk.Button(button_frame, text="Clear Form", command=clear_field_form).pack(
        side="left", padx=5
    )
    tk.Button(button_frame, text="Back to Dashboard", command=show_dashboard).pack(
        side="left", padx=5
    )

    status_label = tk.Label(main_frame, textvariable=status_var, fg="darkgreen")
    status_label.pack(pady=(8, 0))

    load_fields_table()


def show_crop_management():
    clear_screen()
    tk.Label(main_frame, text="Crop Planning", font=("Arial", 22, "bold")).pack(
        pady=(10, 15)
    )

    form_frame = tk.LabelFrame(main_frame, text="Crop Plan Details", padx=12, pady=12)
    form_frame.pack(fill="x", pady=(0, 15))

    field_options = get_field_dropdown_values()
    field_map = {label: field_id for field_id, label in field_options}
    field_label_by_id = {field_id: label for field_id, label in field_options}
    field_combo = ttk.Combobox(
        form_frame,
        values=[label for _, label in field_options],
        state="readonly",
        width=50,
    )
    field_combo.grid(row=0, column=1, padx=8, pady=6, sticky="w")
    tk.Label(form_frame, text="Field:", width=16, anchor="e").grid(
        row=0, column=0, padx=8, pady=6, sticky="e"
    )

    crop_name_var = tk.StringVar()
    variety_var = tk.StringVar()
    season_var = tk.StringVar(value=seasons[0])
    planting_date_var = tk.StringVar()
    harvest_date_var = tk.StringVar()
    status_var = tk.StringVar(value=crop_statuses[0])
    current_crop_id = tk.IntVar(value=-1)
    info_var = tk.StringVar(value="")

    for row, label_text, variable, widget_type, values in [
        (1, "Crop Name", crop_name_var, "entry", None),
        (2, "Variety", variety_var, "entry", None),
        (3, "Season", season_var, "combo", seasons),
        (4, "Planting Date (YYYY-MM-DD)", planting_date_var, "entry", None),
        (5, "Expected Harvest Date (YYYY-MM-DD)", harvest_date_var, "entry", None),
        (6, "Status", status_var, "combo", crop_statuses),
    ]:
        tk.Label(
            form_frame,
            text=f"{label_text}:",
            width=max(16, len(label_text) + 1),
            anchor="e",
        ).grid(
            row=row, column=0, padx=8, pady=6, sticky="e"
        )
        if widget_type == "combo":
            ttk.Combobox(
                form_frame,
                textvariable=variable,
                values=values,
                state="readonly",
                width=38,
            ).grid(row=row, column=1, padx=8, pady=6, sticky="w")
        else:
            tk.Entry(form_frame, textvariable=variable, width=38).grid(
                row=row, column=1, padx=8, pady=6, sticky="w"
            )

    table_frame = tk.Frame(main_frame)
    table_frame.pack(fill="both", expand=True)
    table = build_table(
        table_frame,
        (
            "crop_id",
            "farmer",
            "field_name",
            "crop_name",
            "variety",
            "season",
            "planting_date",
            "expected_harvest_date",
            "status",
        ),
        [
            "Crop ID",
            "Farmer",
            "Field",
            "Crop Name",
            "Variety",
            "Season",
            "Planting Date",
            "Expected Harvest",
            "Status",
        ],
    )
    for column in [
        "crop_id",
        "farmer",
        "field_name",
        "crop_name",
        "variety",
        "season",
        "planting_date",
        "expected_harvest_date",
        "status",
    ]:
        table.column(column, width=110)

    def load_crop_table(search_text=""):
        table.delete(*table.get_children())
        with get_conn() as conn:
            cursor = conn.cursor()
            if search_text:
                cursor.execute(
                    """
                    SELECT cp.crop_id, fr.name, f.field_name, cp.crop_name, cp.variety, cp.season,
                           cp.planting_date, cp.expected_harvest_date, cp.status
                    FROM crop_plans cp
                    INNER JOIN fields f ON cp.field_id = f.field_id
                    INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
                    WHERE cp.crop_name LIKE ? OR fr.name LIKE ?
                    ORDER BY cp.crop_id
                    """,
                    (f"%{search_text}%", f"%{search_text}%"),
                )
            else:
                cursor.execute("""
                    SELECT cp.crop_id, fr.name, f.field_name, cp.crop_name, cp.variety, cp.season,
                           cp.planting_date, cp.expected_harvest_date, cp.status
                    FROM crop_plans cp
                    INNER JOIN fields f ON cp.field_id = f.field_id
                    INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
                    ORDER BY cp.crop_id
                    """)
            rows = cursor.fetchall()
        for row in rows:
            table.insert("", tk.END, values=row)
        if not rows:
            info_var.set("No crop plans found.")

    def clear_crop_form():
        current_crop_id.set(-1)
        crop_name_var.set("")
        variety_var.set("")
        season_var.set(seasons[0])
        planting_date_var.set("")
        harvest_date_var.set("")
        status_var.set(crop_statuses[0])
        field_combo.set("")

    def save_crop_plan():
        selected_field = field_combo.get().strip()
        if not selected_field:
            info_var.set("Select a field to add the crop plan.")
            return
        field_id = field_map.get(selected_field)
        if field_id is None:
            info_var.set("The selected field is invalid.")
            return
        crop_name = crop_name_var.get().strip()
        variety = variety_var.get().strip()
        if not crop_name:
            info_var.set("Crop name is required.")
            return
        if not variety:
            info_var.set("Crop variety is required.")
            return
        valid_planting, planting_error = validate_date_string(
            planting_date_var.get().strip(), "Planting date"
        )
        if not valid_planting:
            info_var.set(planting_error)
            return
        valid_harvest, harvest_error = validate_date_string(
            harvest_date_var.get().strip(), "Expected harvest date"
        )
        if not valid_harvest:
            info_var.set(harvest_error)
            return
        planting_dt = datetime.strptime(planting_date_var.get().strip(), "%Y-%m-%d")
        harvest_dt = datetime.strptime(harvest_date_var.get().strip(), "%Y-%m-%d")
        if harvest_dt < planting_dt:
            info_var.set("Expected harvest date cannot be earlier than planting date.")
            return
        with get_conn() as conn:
            cursor = conn.cursor()
            if current_crop_id.get() != -1:
                cursor.execute(
                    "UPDATE crop_plans SET field_id = ?, crop_name = ?, variety = ?, season = ?, planting_date = ?, expected_harvest_date = ?, status = ? WHERE crop_id = ?",
                    (
                        field_id,
                        crop_name,
                        variety,
                        season_var.get(),
                        planting_date_var.get().strip(),
                        harvest_date_var.get().strip(),
                        status_var.get(),
                        current_crop_id.get(),
                    ),
                )
                info_var.set("Crop plan updated successfully.")
            else:
                cursor.execute(
                    "INSERT INTO crop_plans (field_id, crop_name, variety, season, planting_date, expected_harvest_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        field_id,
                        crop_name,
                        variety,
                        season_var.get(),
                        planting_date_var.get().strip(),
                        harvest_date_var.get().strip(),
                        status_var.get(),
                    ),
                )
                info_var.set("Crop plan added successfully.")
        load_crop_table()
        clear_crop_form()

    def fill_crop_for_edit():
        selection = table.selection()
        if not selection:
            show_message(
                "No Crop Plan Selected", "Select a crop plan to edit.", "warning"
            )
            return
        values = table.item(selection[0], "values")
        crop_id = int(values[0])
        with get_conn() as conn:
            row = conn.execute(
                "SELECT field_id FROM crop_plans WHERE crop_id = ?", (crop_id,)
            ).fetchone()
        if row is None:
            info_var.set("The selected crop plan no longer exists.")
            return
        current_crop_id.set(crop_id)
        field_combo.set(field_label_by_id.get(row[0], ""))
        crop_name_var.set(values[3])
        variety_var.set(values[4])
        season_var.set(values[5])
        planting_date_var.set(values[6])
        harvest_date_var.set(values[7])
        status_var.set(values[8])
        info_var.set(f"Editing crop #{values[0]}.")

    def delete_selected_crop():
        selection = table.selection()
        if not selection:
            show_message(
                "No Crop Plan Selected",
                "Select a crop plan from the table before deleting.",
                "warning",
            )
            return
        crop_id = int(table.item(selection[0], "values")[0])
        crop_name = table.item(selection[0], "values")[3]
        with get_conn() as conn:
            cursor = conn.cursor()
            for table_name, column_name in [
                ("activities", "crop_id"),
                ("expenses", "crop_id"),
                ("harvests", "crop_id"),
                ("revenues", "crop_id"),
            ]:
                cursor.execute(
                    f"SELECT 1 FROM {table_name} WHERE {column_name} = ? LIMIT 1",
                    (crop_id,),
                )
                if cursor.fetchone():
                    show_message(
                        "Cannot Delete",
                        f"Crop '{crop_name}' has related records and cannot be deleted safely.",
                        "error",
                    )
                    return
        confirm = messagebox.askyesno(
            "Confirm Delete", f"Delete crop plan '{crop_name}'?"
        )
        if confirm:
            with get_conn() as conn:
                conn.execute("DELETE FROM crop_plans WHERE crop_id = ?", (crop_id,))
            info_var.set(f"Crop plan '{crop_name}' deleted successfully.")
            load_crop_table()
            clear_crop_form()

    search_frame = tk.Frame(main_frame)
    search_frame.pack(fill="x", pady=(10, 0))
    tk.Label(search_frame, text="Search by crop name or farmer:").pack(
        side="left", padx=(0, 8)
    )
    search_var = tk.StringVar()
    tk.Entry(search_frame, textvariable=search_var, width=30).pack(side="left")
    tk.Button(
        search_frame,
        text="Search",
        command=lambda: load_crop_table(search_var.get().strip()),
    ).pack(side="left", padx=6)
    tk.Button(
        search_frame,
        text="Clear",
        command=lambda: (search_var.set(""), load_crop_table()),
    ).pack(side="left", padx=6)

    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=12)
    tk.Button(button_frame, text="Save Crop Plan", command=save_crop_plan).pack(
        side="left", padx=5
    )
    tk.Button(button_frame, text="Edit Selected", command=fill_crop_for_edit).pack(
        side="left", padx=5
    )
    tk.Button(button_frame, text="Delete Selected", command=delete_selected_crop).pack(
        side="left", padx=5
    )
    tk.Button(button_frame, text="Clear Form", command=clear_crop_form).pack(
        side="left", padx=5
    )
    tk.Button(button_frame, text="Back to Dashboard", command=show_dashboard).pack(
        side="left", padx=5
    )

    status_label = tk.Label(main_frame, textvariable=info_var, fg="darkgreen")
    status_label.pack(pady=(8, 0))

    load_crop_table()


def show_activity_management():
    clear_screen()
    tk.Label(main_frame, text="Farming Activities", font=("Arial", 22, "bold")).pack(
        pady=(10, 15)
    )

    form_frame = tk.LabelFrame(main_frame, text="Activity Details", padx=12, pady=12)
    form_frame.pack(fill="x", pady=(0, 15))

    crop_options = get_crop_dropdown_values()
    crop_map = {label: crop_id for crop_id, label in crop_options}
    crop_label_by_id = {crop_id: label for crop_id, label in crop_options}
    crop_var = tk.StringVar()
    crop_combo = ttk.Combobox(
        form_frame,
        values=[label for _, label in crop_options],
        state="readonly",
        width=50,
    )
    crop_combo.grid(row=0, column=1, padx=8, pady=6, sticky="w")
    tk.Label(form_frame, text="Crop Plan:", width=16, anchor="e").grid(
        row=0, column=0, padx=8, pady=6, sticky="e"
    )

    activity_type_var = tk.StringVar(value=activity_types[0])
    activity_date_var = tk.StringVar()
    description_var = tk.StringVar()
    current_activity_id = tk.IntVar(value=-1)
    info_var = tk.StringVar(value="")

    tk.Label(form_frame, text="Activity Type:", width=16, anchor="e").grid(
        row=1, column=0, padx=8, pady=6, sticky="e"
    )
    ttk.Combobox(
        form_frame,
        textvariable=activity_type_var,
        values=activity_types,
        state="readonly",
        width=38,
    ).grid(row=1, column=1, padx=8, pady=6, sticky="w")
    tk.Label(form_frame, text="Activity Date:", width=16, anchor="e").grid(
        row=2, column=0, padx=8, pady=6, sticky="e"
    )
    tk.Entry(form_frame, textvariable=activity_date_var, width=38).grid(
        row=2, column=1, padx=8, pady=6, sticky="w"
    )
    tk.Label(form_frame, text="Description:", width=16, anchor="e").grid(
        row=3, column=0, padx=8, pady=6, sticky="e"
    )
    tk.Entry(form_frame, textvariable=description_var, width=38).grid(
        row=3, column=1, padx=8, pady=6, sticky="w"
    )

    table_frame = tk.Frame(main_frame)
    table_frame.pack(fill="both", expand=True)
    table = build_table(
        table_frame,
        (
            "activity_id",
            "farmer",
            "field_name",
            "crop_name",
            "activity_type",
            "activity_date",
            "description",
        ),
        ["Activity ID", "Farmer", "Field", "Crop", "Type", "Date", "Description"],
    )
    for column in [
        "activity_id",
        "farmer",
        "field_name",
        "crop_name",
        "activity_type",
        "activity_date",
        "description",
    ]:
        table.column(column, width=120)

    def load_activity_table(search_text=""):
        table.delete(*table.get_children())
        with get_conn() as conn:
            cursor = conn.cursor()
            if search_text:
                cursor.execute(
                    """
                    SELECT a.activity_id, fr.name, f.field_name, cp.crop_name, a.activity_type, a.activity_date, a.description
                    FROM activities a
                    INNER JOIN crop_plans cp ON a.crop_id = cp.crop_id
                    INNER JOIN fields f ON cp.field_id = f.field_id
                    INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
                    WHERE fr.name LIKE ? OR cp.crop_name LIKE ? OR a.activity_type LIKE ?
                    ORDER BY a.activity_id
                    """,
                    (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"),
                )
            else:
                cursor.execute("""
                    SELECT a.activity_id, fr.name, f.field_name, cp.crop_name, a.activity_type, a.activity_date, a.description
                    FROM activities a
                    INNER JOIN crop_plans cp ON a.crop_id = cp.crop_id
                    INNER JOIN fields f ON cp.field_id = f.field_id
                    INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
                    ORDER BY a.activity_id
                    """)
            rows = cursor.fetchall()
        for row in rows:
            table.insert("", tk.END, values=row)
        if not rows:
            info_var.set("No activities found.")

    def save_activity():
        selected_crop = crop_combo.get().strip()
        if not selected_crop:
            info_var.set("Select a crop plan first.")
            return
        crop_id = crop_map.get(selected_crop)
        if crop_id is None:
            info_var.set("The selected crop plan is invalid.")
            return
        valid_date, date_error = validate_date_string(
            activity_date_var.get().strip(), "Activity date"
        )
        if not valid_date:
            info_var.set(date_error)
            return
        description = description_var.get().strip()
        with get_conn() as conn:
            cursor = conn.cursor()
            if current_activity_id.get() != -1:
                cursor.execute(
                    "UPDATE activities SET crop_id = ?, activity_type = ?, activity_date = ?, description = ? WHERE activity_id = ?",
                    (
                        crop_id,
                        activity_type_var.get(),
                        activity_date_var.get().strip(),
                        description,
                        current_activity_id.get(),
                    ),
                )
                info_var.set("Activity updated successfully.")
            else:
                cursor.execute(
                    "INSERT INTO activities (crop_id, activity_type, activity_date, description) VALUES (?, ?, ?, ?)",
                    (
                        crop_id,
                        activity_type_var.get(),
                        activity_date_var.get().strip(),
                        description,
                    ),
                )
                info_var.set("Activity added successfully.")
        load_activity_table()
        clear_activity_form()

    def clear_activity_form():
        current_activity_id.set(-1)
        activity_type_var.set(activity_types[0])
        activity_date_var.set("")
        description_var.set("")
        crop_combo.set("")

    def fill_activity_for_edit():
        selection = table.selection()
        if not selection:
            show_message(
                "No Activity Selected",
                "Select an activity from the table to edit.",
                "warning",
            )
            return
        values = table.item(selection[0], "values")
        activity_id = int(values[0])
        with get_conn() as conn:
            row = conn.execute(
                "SELECT crop_id FROM activities WHERE activity_id = ?",
                (activity_id,),
            ).fetchone()
        if row is None:
            info_var.set("The selected activity no longer exists.")
            return
        current_activity_id.set(activity_id)
        crop_combo.set(crop_label_by_id.get(row[0], ""))
        activity_type_var.set(values[4])
        activity_date_var.set(values[5])
        description_var.set(values[6])
        info_var.set(f"Editing activity #{values[0]}.")

    def delete_selected_activity():
        selection = table.selection()
        if not selection:
            show_message(
                "No Activity Selected", "Select an activity to delete.", "warning"
            )
            return
        activity_id = int(table.item(selection[0], "values")[0])
        confirm = messagebox.askyesno(
            "Confirm Delete", f"Delete activity #{activity_id}?"
        )
        if confirm:
            with get_conn() as conn:
                conn.execute(
                    "DELETE FROM activities WHERE activity_id = ?", (activity_id,)
                )
            info_var.set(f"Activity #{activity_id} deleted successfully.")
            load_activity_table()
            clear_activity_form()

    search_frame = tk.Frame(main_frame)
    search_frame.pack(fill="x", pady=(10, 0))
    tk.Label(search_frame, text="Search by crop, farmer, or type:").pack(
        side="left", padx=(0, 8)
    )
    search_var = tk.StringVar()
    tk.Entry(search_frame, textvariable=search_var, width=30).pack(side="left")
    tk.Button(
        search_frame,
        text="Search",
        command=lambda: load_activity_table(search_var.get().strip()),
    ).pack(side="left", padx=6)
    tk.Button(
        search_frame,
        text="Clear",
        command=lambda: (search_var.set(""), load_activity_table()),
    ).pack(side="left", padx=6)

    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=12)
    tk.Button(button_frame, text="Save Activity", command=save_activity).pack(
        side="left", padx=5
    )
    tk.Button(button_frame, text="Edit Selected", command=fill_activity_for_edit).pack(
        side="left", padx=5
    )
    tk.Button(
        button_frame, text="Delete Selected", command=delete_selected_activity
    ).pack(side="left", padx=5)
    tk.Button(button_frame, text="Clear Form", command=clear_activity_form).pack(
        side="left", padx=5
    )
    tk.Button(button_frame, text="Back to Dashboard", command=show_dashboard).pack(
        side="left", padx=5
    )

    status_label = tk.Label(main_frame, textvariable=info_var, fg="darkgreen")
    status_label.pack(pady=(8, 0))

    load_activity_table()


def show_expense_management():
    clear_screen()
    tk.Label(main_frame, text="Expense Management", font=("Arial", 22, "bold")).pack(
        pady=(10, 15)
    )

    form_frame = tk.LabelFrame(main_frame, text="Expense Details", padx=12, pady=12)
    form_frame.pack(fill="x", pady=(0, 15))

    crop_options = get_crop_dropdown_values()
    crop_map = {label: crop_id for crop_id, label in crop_options}
    crop_label_by_id = {crop_id: label for crop_id, label in crop_options}
    crop_var = tk.StringVar()
    expense_type_options = tuple(services.expense_types)
    crop_combo = ttk.Combobox(
        form_frame,
        values=[label for _, label in crop_options],
        state="readonly",
        width=50,
    )
    crop_combo.grid(row=0, column=1, padx=8, pady=6, sticky="w")
    tk.Label(form_frame, text="Crop Plan:", width=16, anchor="e").grid(
        row=0, column=0, padx=8, pady=6, sticky="e"
    )

    expense_type_var = tk.StringVar()
    amount_var = tk.StringVar()
    expense_date_var = tk.StringVar()
    description_var = tk.StringVar()
    current_expense_id = tk.IntVar(value=-1)
    info_var = tk.StringVar(value="")

    tk.Label(form_frame, text="Expense Type:", width=16, anchor="e").grid(
        row=1, column=0, padx=8, pady=6, sticky="e"
    )
    expense_type_combo = ttk.Combobox(
        form_frame,
        textvariable=expense_type_var,
        values=expense_type_options,
        state="readonly",
        width=35,
    )
    expense_type_combo.grid(row=1, column=1, padx=8, pady=6, sticky="w")
    tk.Label(form_frame, text="Amount:", width=16, anchor="e").grid(
        row=2, column=0, padx=8, pady=6, sticky="e"
    )
    tk.Entry(form_frame, textvariable=amount_var, width=38).grid(
        row=2, column=1, padx=8, pady=6, sticky="w"
    )
    tk.Label(form_frame, text="Expense Date:", width=16, anchor="e").grid(
        row=3, column=0, padx=8, pady=6, sticky="e"
    )
    tk.Entry(form_frame, textvariable=expense_date_var, width=38).grid(
        row=3, column=1, padx=8, pady=6, sticky="w"
    )
    tk.Label(form_frame, text="Description:", width=16, anchor="e").grid(
        row=4, column=0, padx=8, pady=6, sticky="e"
    )
    tk.Entry(form_frame, textvariable=description_var, width=38).grid(
        row=4, column=1, padx=8, pady=6, sticky="w"
    )

    table_frame = tk.Frame(main_frame)
    table_frame.pack(fill="both", expand=True)
    table = build_table(
        table_frame,
        (
            "expense_id",
            "farmer",
            "field_name",
            "crop_name",
            "expense_type",
            "amount",
            "expense_date",
            "description",
        ),
        [
            "Expense ID",
            "Farmer",
            "Field",
            "Crop",
            "Type",
            "Amount",
            "Date",
            "Description",
        ],
    )
    for column in [
        "expense_id",
        "farmer",
        "field_name",
        "crop_name",
        "expense_type",
        "amount",
        "expense_date",
        "description",
    ]:
        table.column(column, width=115)

    def load_expense_table(search_text=""):
        table.delete(*table.get_children())
        with get_conn() as conn:
            cursor = conn.cursor()
            if search_text:
                cursor.execute(
                    """
                    SELECT e.expense_id, fr.name, f.field_name, cp.crop_name, e.expense_type, e.amount, e.expense_date, e.description
                    FROM expenses e
                    INNER JOIN crop_plans cp ON e.crop_id = cp.crop_id
                    INNER JOIN fields f ON cp.field_id = f.field_id
                    INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
                    WHERE fr.name LIKE ? OR cp.crop_name LIKE ? OR e.expense_type LIKE ?
                    ORDER BY e.expense_id
                    """,
                    (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"),
                )
            else:
                cursor.execute("""
                    SELECT e.expense_id, fr.name, f.field_name, cp.crop_name, e.expense_type, e.amount, e.expense_date, e.description
                    FROM expenses e
                    INNER JOIN crop_plans cp ON e.crop_id = cp.crop_id
                    INNER JOIN fields f ON cp.field_id = f.field_id
                    INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
                    ORDER BY e.expense_id
                    """)
            rows = cursor.fetchall()
        for row in rows:
            table.insert("", tk.END, values=row)
        if not rows:
            info_var.set("No expenses found.")

    def save_expense():
        selected_crop = crop_combo.get().strip()
        if not selected_crop:
            info_var.set("Select a crop plan first.")
            return
        crop_id = crop_map.get(selected_crop)
        if crop_id is None:
            info_var.set("The selected crop is invalid.")
            return
        expense_type = expense_type_var.get().strip()
        if not expense_type:
            info_var.set("Select an expense type.")
            return
        if expense_type not in expense_type_combo["values"]:
            info_var.set("Select an expense type from the dropdown.")
            return
        valid_amount, amount_value = validate_positive_number(
            amount_var.get().strip(), "Expense amount"
        )
        if not valid_amount:
            info_var.set(amount_value)
            return
        valid_date, date_error = validate_date_string(
            expense_date_var.get().strip(), "Expense date"
        )
        if not valid_date:
            info_var.set(date_error)
            return
        with get_conn() as conn:
            cursor = conn.cursor()
            if current_expense_id.get() != -1:
                cursor.execute(
                    "UPDATE expenses SET crop_id = ?, expense_type = ?, amount = ?, expense_date = ?, description = ? WHERE expense_id = ?",
                    (
                        crop_id,
                        expense_type,
                        amount_value,
                        expense_date_var.get().strip(),
                        description_var.get().strip(),
                        current_expense_id.get(),
                    ),
                )
                info_var.set("Expense updated successfully.")
            else:
                cursor.execute(
                    "INSERT INTO expenses (crop_id, expense_type, amount, expense_date, description) VALUES (?, ?, ?, ?, ?)",
                    (
                        crop_id,
                        expense_type,
                        amount_value,
                        expense_date_var.get().strip(),
                        description_var.get().strip(),
                    ),
                )
                info_var.set("Expense added successfully.")
        load_expense_table()
        clear_expense_form()

    def clear_expense_form():
        current_expense_id.set(-1)
        expense_type_combo.configure(values=expense_type_options)
        expense_type_var.set("")
        amount_var.set("")
        expense_date_var.set("")
        description_var.set("")
        crop_combo.set("")

    def fill_expense_for_edit():
        selection = table.selection()
        if not selection:
            show_message(
                "No Expense Selected",
                "Select an expense from the table to edit.",
                "warning",
            )
            return
        values = table.item(selection[0], "values")
        expense_id = int(values[0])
        with get_conn() as conn:
            row = conn.execute(
                "SELECT crop_id FROM expenses WHERE expense_id = ?", (expense_id,)
            ).fetchone()
        if row is None:
            info_var.set("The selected expense no longer exists.")
            return
        current_expense_id.set(expense_id)
        crop_combo.set(crop_label_by_id.get(row[0], ""))
        expense_type = values[4]
        if expense_type not in expense_type_options:
            # Keep older or custom saved categories selectable while editing.
            expense_type_combo.configure(
                values=expense_type_options + (expense_type,)
            )
        expense_type_var.set(values[4])
        amount_var.set(values[5])
        expense_date_var.set(values[6])
        description_var.set(values[7])
        info_var.set(f"Editing expense #{values[0]}.")

    def delete_selected_expense():
        selection = table.selection()
        if not selection:
            show_message(
                "No Expense Selected", "Select an expense before deleting.", "warning"
            )
            return
        expense_id = int(table.item(selection[0], "values")[0])
        confirm = messagebox.askyesno(
            "Confirm Delete", f"Delete expense #{expense_id}?"
        )
        if confirm:
            with get_conn() as conn:
                conn.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
            info_var.set(f"Expense #{expense_id} deleted successfully.")
            load_expense_table()
            clear_expense_form()

    search_frame = tk.Frame(main_frame)
    search_frame.pack(fill="x", pady=(10, 0))
    tk.Label(search_frame, text="Search by crop, farmer, or type:").pack(
        side="left", padx=(0, 8)
    )
    search_var = tk.StringVar()
    tk.Entry(search_frame, textvariable=search_var, width=30).pack(side="left")
    tk.Button(
        search_frame,
        text="Search",
        command=lambda: load_expense_table(search_var.get().strip()),
    ).pack(side="left", padx=6)
    tk.Button(
        search_frame,
        text="Clear",
        command=lambda: (search_var.set(""), load_expense_table()),
    ).pack(side="left", padx=6)

    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=12)
    tk.Button(button_frame, text="Save Expense", command=save_expense).pack(
        side="left", padx=5
    )
    tk.Button(button_frame, text="Edit Selected", command=fill_expense_for_edit).pack(
        side="left", padx=5
    )
    tk.Button(
        button_frame, text="Delete Selected", command=delete_selected_expense
    ).pack(side="left", padx=5)
    tk.Button(button_frame, text="Clear Form", command=clear_expense_form).pack(
        side="left", padx=5
    )
    tk.Button(button_frame, text="Back to Dashboard", command=show_dashboard).pack(
        side="left", padx=5
    )

    status_label = tk.Label(main_frame, textvariable=info_var, fg="darkgreen")
    status_label.pack(pady=(8, 0))

    load_expense_table()


def show_harvest_revenue_management():
    clear_screen()
    tk.Label(main_frame, text="Harvest & Revenue", font=("Arial", 22, "bold")).pack(
        pady=(10, 15)
    )

    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill="both", expand=True)

    harvest_frame = tk.Frame(notebook)
    revenue_frame = tk.Frame(notebook)
    notebook.add(harvest_frame, text="Harvest")
    notebook.add(revenue_frame, text="Revenue")

    def build_harvest_tab(frame):
        crop_options = get_crop_dropdown_values()
        crop_map = {label: crop_id for crop_id, label in crop_options}
        crop_label_by_id = {crop_id: label for crop_id, label in crop_options}
        crop_combo = ttk.Combobox(
            frame,
            values=[label for _, label in crop_options],
            state="readonly",
            width=50,
        )
        crop_combo.grid(row=0, column=1, padx=8, pady=6, sticky="w")
        tk.Label(frame, text="Crop Plan:", width=16, anchor="e").grid(
            row=0, column=0, padx=8, pady=6, sticky="e"
        )

        harvest_date_var = tk.StringVar()
        quantity_var = tk.StringVar()
        unit_var = tk.StringVar(value="kg")
        current_harvest_id = tk.IntVar(value=-1)
        info_var = tk.StringVar(value="")

        tk.Label(frame, text="Harvest Date:", width=16, anchor="e").grid(
            row=1, column=0, padx=8, pady=6, sticky="e"
        )
        tk.Entry(frame, textvariable=harvest_date_var, width=38).grid(
            row=1, column=1, padx=8, pady=6, sticky="w"
        )
        tk.Label(frame, text="Quantity:", width=16, anchor="e").grid(
            row=2, column=0, padx=8, pady=6, sticky="e"
        )
        tk.Entry(frame, textvariable=quantity_var, width=38).grid(
            row=2, column=1, padx=8, pady=6, sticky="w"
        )
        tk.Label(frame, text="Unit:", width=16, anchor="e").grid(
            row=3, column=0, padx=8, pady=6, sticky="e"
        )
        tk.Entry(frame, textvariable=unit_var, width=38).grid(
            row=3, column=1, padx=8, pady=6, sticky="w"
        )

        table_frame = tk.Frame(frame)
        table_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(12, 0))
        frame.grid_rowconfigure(4, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        table = build_table(
            table_frame,
            (
                "harvest_id",
                "farmer",
                "field_name",
                "crop_name",
                "harvest_date",
                "quantity",
                "unit",
            ),
            ["Harvest ID", "Farmer", "Field", "Crop", "Date", "Quantity", "Unit"],
        )

        def load_harvest_table(search_text=""):
            table.delete(*table.get_children())
            with get_conn() as conn:
                cursor = conn.cursor()
                if search_text:
                    cursor.execute(
                        """
                        SELECT h.harvest_id, fr.name, f.field_name, cp.crop_name, h.harvest_date, h.quantity, h.unit
                        FROM harvests h
                        INNER JOIN crop_plans cp ON h.crop_id = cp.crop_id
                        INNER JOIN fields f ON cp.field_id = f.field_id
                        INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
                        WHERE fr.name LIKE ? OR cp.crop_name LIKE ?
                        ORDER BY h.harvest_id
                        """,
                        (f"%{search_text}%", f"%{search_text}%"),
                    )
                else:
                    cursor.execute("""
                        SELECT h.harvest_id, fr.name, f.field_name, cp.crop_name, h.harvest_date, h.quantity, h.unit
                        FROM harvests h
                        INNER JOIN crop_plans cp ON h.crop_id = cp.crop_id
                        INNER JOIN fields f ON cp.field_id = f.field_id
                        INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
                        ORDER BY h.harvest_id
                        """)
                rows = cursor.fetchall()
            for row in rows:
                table.insert("", tk.END, values=row)
            if not rows:
                info_var.set("No harvest records found.")

        def save_harvest():
            selected_crop = crop_combo.get().strip()
            if not selected_crop:
                info_var.set("Select a crop plan first.")
                return
            crop_id = crop_map.get(selected_crop)
            valid_date, date_error = validate_date_string(
                harvest_date_var.get().strip(), "Harvest date"
            )
            if not valid_date:
                info_var.set(date_error)
                return
            valid_quantity, quantity_value = validate_positive_number(
                quantity_var.get().strip(), "Harvest quantity"
            )
            if not valid_quantity:
                info_var.set(quantity_value)
                return
            if not unit_var.get().strip():
                info_var.set("Harvest unit is required.")
                return
            with get_conn() as conn:
                cursor = conn.cursor()
                if current_harvest_id.get() != -1:
                    cursor.execute(
                        "UPDATE harvests SET crop_id = ?, harvest_date = ?, quantity = ?, unit = ? WHERE harvest_id = ?",
                        (
                            crop_id,
                            harvest_date_var.get().strip(),
                            quantity_value,
                            unit_var.get().strip(),
                            current_harvest_id.get(),
                        ),
                    )
                    info_var.set("Harvest record updated successfully.")
                else:
                    cursor.execute(
                        "INSERT INTO harvests (crop_id, harvest_date, quantity, unit) VALUES (?, ?, ?, ?)",
                        (
                            crop_id,
                            harvest_date_var.get().strip(),
                            quantity_value,
                            unit_var.get().strip(),
                        ),
                    )
                    info_var.set("Harvest record added successfully.")
            load_harvest_table()
            clear_harvest_form()

        def clear_harvest_form():
            current_harvest_id.set(-1)
            harvest_date_var.set("")
            quantity_var.set("")
            unit_var.set("kg")
            crop_combo.set("")

        def fill_harvest_for_edit():
            selection = table.selection()
            if not selection:
                show_message(
                    "No Harvest Selected", "Select a harvest record to edit.", "warning"
                )
                return
            values = table.item(selection[0], "values")
            harvest_id = int(values[0])
            with get_conn() as conn:
                row = conn.execute(
                    "SELECT crop_id FROM harvests WHERE harvest_id = ?",
                    (harvest_id,),
                ).fetchone()
            if row is None:
                info_var.set("The selected harvest record no longer exists.")
                return
            current_harvest_id.set(harvest_id)
            crop_combo.set(crop_label_by_id.get(row[0], ""))
            harvest_date_var.set(values[4])
            quantity_var.set(values[5])
            unit_var.set(values[6])
            info_var.set(f"Editing harvest #{values[0]}.")

        def delete_selected_harvest():
            selection = table.selection()
            if not selection:
                show_message(
                    "No Harvest Selected",
                    "Select a harvest record to delete.",
                    "warning",
                )
                return
            harvest_id = int(table.item(selection[0], "values")[0])
            confirm = messagebox.askyesno(
                "Confirm Delete", f"Delete harvest #{harvest_id}?"
            )
            if confirm:
                with get_conn() as conn:
                    conn.execute(
                        "DELETE FROM harvests WHERE harvest_id = ?", (harvest_id,)
                    )
                info_var.set(f"Harvest #{harvest_id} deleted successfully.")
                load_harvest_table()
                clear_harvest_form()

        search_frame = tk.Frame(frame)
        search_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        tk.Label(search_frame, text="Search by crop or farmer:").pack(
            side="left", padx=(0, 8)
        )
        search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=search_var, width=30).pack(side="left")
        tk.Button(
            search_frame,
            text="Search",
            command=lambda: load_harvest_table(search_var.get().strip()),
        ).pack(side="left", padx=6)
        tk.Button(
            search_frame,
            text="Clear",
            command=lambda: (search_var.set(""), load_harvest_table()),
        ).pack(side="left", padx=6)
        button_frame = tk.Frame(frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(button_frame, text="Save Harvest", command=save_harvest).pack(
            side="left", padx=5
        )
        tk.Button(
            button_frame, text="Edit Selected", command=fill_harvest_for_edit
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame, text="Delete Selected", command=delete_selected_harvest
        ).pack(side="left", padx=5)
        tk.Button(button_frame, text="Back to Dashboard", command=show_dashboard).pack(
            side="left", padx=5
        )
        tk.Label(frame, textvariable=info_var, fg="darkgreen").grid(
            row=7, column=0, columnspan=2, pady=(0, 10)
        )
        load_harvest_table()

    def build_revenue_tab(frame):
        crop_options = get_crop_dropdown_values()
        crop_map = {label: crop_id for crop_id, label in crop_options}
        crop_label_by_id = {crop_id: label for crop_id, label in crop_options}
        crop_combo = ttk.Combobox(
            frame,
            values=[label for _, label in crop_options],
            state="readonly",
            width=50,
        )
        crop_combo.grid(row=0, column=1, padx=8, pady=6, sticky="w")
        tk.Label(frame, text="Crop Plan:", width=16, anchor="e").grid(
            row=0, column=0, padx=8, pady=6, sticky="e"
        )

        sale_date_var = tk.StringVar()
        quantity_var = tk.StringVar()
        price_var = tk.StringVar()
        current_revenue_id = tk.IntVar(value=-1)
        info_var = tk.StringVar(value="")

        tk.Label(frame, text="Sale Date:", width=16, anchor="e").grid(
            row=1, column=0, padx=8, pady=6, sticky="e"
        )
        tk.Entry(frame, textvariable=sale_date_var, width=38).grid(
            row=1, column=1, padx=8, pady=6, sticky="w"
        )
        tk.Label(frame, text="Quantity:", width=16, anchor="e").grid(
            row=2, column=0, padx=8, pady=6, sticky="e"
        )
        tk.Entry(frame, textvariable=quantity_var, width=38).grid(
            row=2, column=1, padx=8, pady=6, sticky="w"
        )
        tk.Label(frame, text="Price per Unit:", width=16, anchor="e").grid(
            row=3, column=0, padx=8, pady=6, sticky="e"
        )
        tk.Entry(frame, textvariable=price_var, width=38).grid(
            row=3, column=1, padx=8, pady=6, sticky="w"
        )

        table_frame = tk.Frame(frame)
        table_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(12, 0))
        frame.grid_rowconfigure(4, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        table = build_table(
            table_frame,
            (
                "revenue_id",
                "farmer",
                "field_name",
                "crop_name",
                "sale_date",
                "quantity",
                "price_per_unit",
                "total_amount",
            ),
            [
                "Revenue ID",
                "Farmer",
                "Field",
                "Crop",
                "Sale Date",
                "Quantity",
                "Price/Unit",
                "Total",
            ],
        )

        def load_revenue_table(search_text=""):
            table.delete(*table.get_children())
            with get_conn() as conn:
                cursor = conn.cursor()
                if search_text:
                    cursor.execute(
                        """
                        SELECT r.revenue_id, fr.name, f.field_name, cp.crop_name, r.sale_date, r.quantity, r.price_per_unit, r.total_amount
                        FROM revenues r
                        INNER JOIN crop_plans cp ON r.crop_id = cp.crop_id
                        INNER JOIN fields f ON cp.field_id = f.field_id
                        INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
                        WHERE fr.name LIKE ? OR cp.crop_name LIKE ?
                        ORDER BY r.revenue_id
                        """,
                        (f"%{search_text}%", f"%{search_text}%"),
                    )
                else:
                    cursor.execute("""
                        SELECT r.revenue_id, fr.name, f.field_name, cp.crop_name, r.sale_date, r.quantity, r.price_per_unit, r.total_amount
                        FROM revenues r
                        INNER JOIN crop_plans cp ON r.crop_id = cp.crop_id
                        INNER JOIN fields f ON cp.field_id = f.field_id
                        INNER JOIN farmers fr ON f.farmer_id = fr.farmer_id
                        ORDER BY r.revenue_id
                        """)
                rows = cursor.fetchall()
            for row in rows:
                table.insert("", tk.END, values=row)
            if not rows:
                info_var.set("No revenue records found.")

        def save_revenue():
            selected_crop = crop_combo.get().strip()
            if not selected_crop:
                info_var.set("Select a crop plan first.")
                return
            crop_id = crop_map.get(selected_crop)
            valid_date, date_error = validate_date_string(
                sale_date_var.get().strip(), "Sale date"
            )
            if not valid_date:
                info_var.set(date_error)
                return
            valid_quantity, quantity_value = validate_positive_number(
                quantity_var.get().strip(), "Quantity"
            )
            if not valid_quantity:
                info_var.set(quantity_value)
                return
            valid_price, price_value = validate_positive_number(
                price_var.get().strip(), "Price per unit"
            )
            if not valid_price:
                info_var.set(price_value)
                return
            total_amount = quantity_value * price_value
            with get_conn() as conn:
                cursor = conn.cursor()
                if current_revenue_id.get() != -1:
                    cursor.execute(
                        "UPDATE revenues SET crop_id = ?, sale_date = ?, quantity = ?, price_per_unit = ?, total_amount = ? WHERE revenue_id = ?",
                        (
                            crop_id,
                            sale_date_var.get().strip(),
                            quantity_value,
                            price_value,
                            total_amount,
                            current_revenue_id.get(),
                        ),
                    )
                    info_var.set("Revenue record updated successfully.")
                else:
                    cursor.execute(
                        "INSERT INTO revenues (crop_id, sale_date, quantity, price_per_unit, total_amount) VALUES (?, ?, ?, ?, ?)",
                        (
                            crop_id,
                            sale_date_var.get().strip(),
                            quantity_value,
                            price_value,
                            total_amount,
                        ),
                    )
                    info_var.set("Revenue record added successfully.")
            load_revenue_table()
            clear_revenue_form()

        def clear_revenue_form():
            current_revenue_id.set(-1)
            sale_date_var.set("")
            quantity_var.set("")
            price_var.set("")
            crop_combo.set("")

        def fill_revenue_for_edit():
            selection = table.selection()
            if not selection:
                show_message(
                    "No Revenue Selected", "Select a revenue record to edit.", "warning"
                )
                return
            values = table.item(selection[0], "values")
            revenue_id = int(values[0])
            with get_conn() as conn:
                row = conn.execute(
                    "SELECT crop_id FROM revenues WHERE revenue_id = ?",
                    (revenue_id,),
                ).fetchone()
            if row is None:
                info_var.set("The selected revenue record no longer exists.")
                return
            current_revenue_id.set(revenue_id)
            crop_combo.set(crop_label_by_id.get(row[0], ""))
            sale_date_var.set(values[4])
            quantity_var.set(values[5])
            price_var.set(values[6])
            info_var.set(f"Editing revenue #{values[0]}.")

        def delete_selected_revenue():
            selection = table.selection()
            if not selection:
                show_message(
                    "No Revenue Selected",
                    "Select a revenue record to delete.",
                    "warning",
                )
                return
            revenue_id = int(table.item(selection[0], "values")[0])
            confirm = messagebox.askyesno(
                "Confirm Delete", f"Delete revenue #{revenue_id}?"
            )
            if confirm:
                with get_conn() as conn:
                    conn.execute(
                        "DELETE FROM revenues WHERE revenue_id = ?", (revenue_id,)
                    )
                info_var.set(f"Revenue #{revenue_id} deleted successfully.")
                load_revenue_table()
                clear_revenue_form()

        search_frame = tk.Frame(frame)
        search_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        tk.Label(search_frame, text="Search by crop or farmer:").pack(
            side="left", padx=(0, 8)
        )
        search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=search_var, width=30).pack(side="left")
        tk.Button(
            search_frame,
            text="Search",
            command=lambda: load_revenue_table(search_var.get().strip()),
        ).pack(side="left", padx=6)
        tk.Button(
            search_frame,
            text="Clear",
            command=lambda: (search_var.set(""), load_revenue_table()),
        ).pack(side="left", padx=6)
        button_frame = tk.Frame(frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(button_frame, text="Save Revenue", command=save_revenue).pack(
            side="left", padx=5
        )
        tk.Button(
            button_frame, text="Edit Selected", command=fill_revenue_for_edit
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame, text="Delete Selected", command=delete_selected_revenue
        ).pack(side="left", padx=5)
        tk.Button(button_frame, text="Back to Dashboard", command=show_dashboard).pack(
            side="left", padx=5
        )
        tk.Label(frame, textvariable=info_var, fg="darkgreen").grid(
            row=7, column=0, columnspan=2, pady=(0, 10)
        )
        load_revenue_table()

    build_harvest_tab(harvest_frame)
    build_revenue_tab(revenue_frame)


def on_close():
    if messagebox.askyesno("Exit FarmTrack", "Do you want to close the application?"):
        window.destroy()


create_tables()
window.protocol("WM_DELETE_WINDOW", on_close)
show_dashboard()
window.mainloop()
