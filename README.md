# FarmTrack

## Farm Record & Crop Planning System

FarmTrack is a command-line based farm record and crop planning system developed using Python and SQLite.

The system helps agricultural staff, technicians, cooperatives, NGOs, or local agricultural offices maintain organized records of farmers, fields, crops, farming activities, expenses, harvests, and revenue.

It also provides reports, CSV export, and charts to help users analyze farm performance and financial results.

---

## 1. Problem Statement

Farm-related information is often maintained using notebooks, spreadsheets, or separate records. This can make it difficult to track farming activities, calculate expenses and revenue, and evaluate the performance of individual crops.

FarmTrack provides a centralized system where farmer and farm-related information can be stored, managed, analyzed, and reported using a structured SQLite database.

---

## 2. Objectives

The main objectives of FarmTrack are:

- To maintain organized farmer records.
- To manage field information associated with farmers.
- To plan and track crops.
- To record farming activities.
- To record and manage farming expenses.
- To record harvested quantities.
- To record crop sales and revenue.
- To calculate crop-wise profit or loss.
- To generate useful reports and charts.
- To export reports into CSV files.
- To provide data validation and error handling through a command-line interface.

---

## 3. Key Features

### Farmer Management

- Add farmer
- View farmers
- Search farmers
- Update farmer information
- Delete farmer records

### Field Management

- Add field
- View fields
- Search fields
- Update field information
- Delete field records

### Crop Planning

- Add crop plan
- View crop plans
- Search crop plans
- Update crop information
- Delete crop plans
- Track crop status and important dates

### Farming Activity Tracking

- Add farming activities
- View activities
- Search activities
- Update activities
- Delete activities

Examples of activities include:

- Land preparation
- Planting
- Irrigation
- Fertilization
- Weeding
- Pest control
- Spraying
- Harvest preparation

### Expense Management

- Add expenses
- View expenses
- Search expenses
- Update expenses
- Delete expenses
- Categorize expenses

### Harvest Management

- Add harvest records
- View harvest records
- Search harvest records
- Update harvest records
- Delete harvest records
- Record harvest quantity and unit

### Revenue Management

- Add revenue records
- View revenue records
- Search revenue records
- Update revenue records
- Delete revenue records
- Automatically calculate total revenue

### Reports and Analysis

FarmTrack provides:

- Farm Summary
- Crop Performance Report
- Expense Analysis
- Revenue and Profit/Loss Report

### CSV Export

Reports can be exported into CSV files for further analysis or record keeping.

### Charts

FarmTrack generates visual charts including:

- Expense by Crop
- Revenue by Crop
- Profit/Loss by Crop
- Expense Distribution by Farmer

---

## 4. Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Application development |
| SQLite | Database management |
| SQL | Data retrieval and analysis |
| Matplotlib | Chart generation |
| CSV | Report export |
| Git | Version control |
| GitHub | Source code hosting |
| VS Code | Development environment |
| DBeaver | Database inspection and management |

---

## 5. Project Structure

```text
FarmTrack/
│
├── main.py
├── database.py
├── services.py
├── validators.py
├── reports.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── farm.db
│
├── exports/
│   └── generated CSV reports
│
└── charts/
    └── generated chart images
```

### File Responsibilities

**main.py**

Handles the command-line interface, menus, and navigation between different modules.

**database.py**

Creates the SQLite database connection and initializes the database tables.

**services.py**

Contains CRUD operations and business logic for farmers, fields, crop plans, activities, expenses, harvests, and revenues.

**validators.py**

Contains reusable input validation functions for names, phone numbers, numbers, dates, choices, IDs, and text values.

**reports.py**

Generates reports, performs data analysis, exports reports to CSV, and generates charts.

**requirements.txt**

Contains the external Python packages required by the project.

**data/farm.db**

SQLite database file created when the application initializes the database.

**exports/**

Stores generated CSV reports.

**charts/**

Stores generated chart images.

---

## 6. Database Design

FarmTrack uses SQLite as its relational database.

The system contains the following tables:

### farmers

Stores information about farmers.

Main fields:

- farmer_id
- name
- phone
- location
- created_at

### fields

Stores field information associated with farmers.

Main fields:

- field_id
- farmer_id
- field_name
- area
- area_unit
- soil_type
- irrigation

### crop_plans

Stores crop planning information for each field.

Main fields:

- crop_id
- field_id
- crop_name
- variety
- season
- planting_date
- expected_harvest_date
- status

### activities

Stores farming activities performed for each crop.

Main fields:

- activity_id
- crop_id
- activity_type
- activity_date
- description

### expenses

Stores expenses associated with crops.

Main fields:

- expense_id
- crop_id
- expense_type
- amount
- expense_date
- description

### harvests

Stores harvested quantities.

Main fields:

- harvest_id
- crop_id
- harvest_date
- quantity
- unit

### revenues

Stores crop sales and revenue information.

Main fields:

- revenue_id
- crop_id
- sale_date
- quantity
- price_per_unit
- total_amount

---

## 7. Database Relationships

The main relationship flow of FarmTrack is:

```text
Farmer
   │
   └── Field
         │
         └── Crop Plan
                │
                ├── Farming Activities
                ├── Expenses
                ├── Harvests
                └── Revenues
```

Relationships:

- One farmer can have multiple fields.
- One field can have multiple crop plans.
- One crop plan can have multiple farming activities.
- One crop plan can have multiple expenses.
- One crop plan can have multiple harvest records.
- One crop plan can have multiple revenue records.

Foreign keys and cascading deletes are used to maintain relationships between related records.

---

## 8. Application Workflow

The general workflow of FarmTrack is:

```text
Farmer
   ↓
Field
   ↓
Crop Planning
   ↓
Farming Activities
   ↓
Expenses
   ↓
Harvest
   ↓
Revenue
   ↓
Reports & Analysis
```

This allows the user to track a crop from planning and farming activities through harvest and financial analysis.

---

## 9. Reports and Analysis

### Farm Summary

Provides an overall count of:

- Farmers
- Fields
- Crop Plans
- Farming Activities
- Expenses
- Harvests
- Revenues

### Crop Performance

Provides crop-wise information including:

- Total expenses
- Total harvest
- Total revenue
- Profit/Loss

Profit/Loss is calculated as:

```text
Profit/Loss = Total Revenue - Total Expense
```

### Expense Analysis

Analyzes expenses by farmer and crop.

This helps identify where farming costs are being spent.

### Revenue and Profit/Loss

Provides revenue and financial performance information for crop plans.

---

## 10. Charts

FarmTrack uses Matplotlib to generate visual representations of farm data.

The available charts are:

### Expense by Crop

Displays total expenses for each crop.

### Revenue by Crop

Displays total revenue generated by each crop.

### Profit/Loss by Crop Plan

Displays the profit or loss generated by individual crop plans.

### Expense Distribution by Farmer

Shows how the total farming expenses are distributed among farmers.

Generated charts are saved inside the `charts/` directory.

---

## 11. Data Validation

FarmTrack uses reusable validation functions to reduce invalid data entry.

Examples include:

- Required field validation
- Farmer name validation
- Phone number validation
- Positive number validation
- Positive integer validation
- Date validation
- Controlled choice validation
- Text validation

For example, phone numbers are validated to ensure that a valid 10-digit number is entered.

Dates are validated using the:

```text
YYYY-MM-DD
```

format.

---

## 12. CRUD Operations

FarmTrack implements CRUD operations where appropriate.

CRUD stands for:

```text
Create
Read
Update
Delete
```

The system supports these operations for major management modules such as:

- Farmers
- Fields
- Crop Plans
- Farming Activities
- Expenses
- Harvests
- Revenues

---

## 13. CSV Export

FarmTrack allows reports to be exported as CSV files.

Available exported reports include:

- Farm Summary
- Crop Performance
- Expense Analysis
- Revenue and Profit/Loss

The generated CSV files are stored in:

```text
exports/
```

---

## 14. How to Run the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/snehaaa939/FarmTrack.git
```

### Step 2: Open the project directory

```bash
cd FarmTrack
```

### Step 3: Create a virtual environment

Windows:

```bash
python -m venv venv
```

### Step 4: Activate the virtual environment

Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the application

```bash
python main.py
```

The application will automatically create the required SQLite database and tables.

---

## 15. Command-Line Interface

FarmTrack provides a menu-driven command-line interface.

The main menu includes:

```text
1. Farmer Management
2. Field Management
3. Crop Planning
4. Farming Activities
5. Expense Management
6. Harvest and Revenue
7. Reports and Analysis
8. Exit
```

Users can navigate through the menus to manage records and generate reports.

---

## 16. Version Control

Git and GitHub are used for version control.

The project follows meaningful commits for major development milestones instead of using vague commit messages.

Examples include:

```text
Initialize FarmTrack Project
Add harvest and revenue management
Add reports and analysis
Add project dependencies
```

The source code is hosted on GitHub:

```text
https://github.com/snehaaa939/FarmTrack
```

---

## AI Usage

AI was used as a learning and development support tool during the project.

- Used AI to understand programming concepts and database relationships.
- Used AI for guidance while designing the SQLite database and project structure.
- Used AI to help troubleshoot errors and improve code when problems occurred.
- Used AI suggestions as references for implementing features and reports.
- The project logic, database design, implementation, testing, modifications, and final integration were reviewed and understood by the developer.

## 18. Future Improvements

Possible future improvements include:

- User authentication and role-based access
- Graphical user interface
- Web-based interface
- Weather data integration
- Mobile application
- Advanced farm performance analytics
- Automated backup and restore
- Additional agricultural reports

---

## 19. Author

**Sneha Kumari Yadav**
BIT graduate.

### Training / Learning Context
Developed as an individual project during Data Science training
