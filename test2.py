from dataclasses import dataclass
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Load saved data
DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# User input for daily goals
while True:
    try:
        CALORIE_LIMIT = int(input("Enter your daily calorie limit (kcal): "))
        PROTEIN_GOAL = int(input("Enter your daily protein goal (grams): "))
        FAT_GOAL = int(input("Enter your daily fat goal (grams): "))
        CARBS_GOAL = int(input("Enter your daily carbs goal (grams): "))
    except ValueError:
        print("\nInvalid input. Please enter numeric values.\n")
        continue

    print("Your goals are set as follows:")
    print(f"Calorie Limit: {CALORIE_LIMIT} kcal")
    print(f"Protein Goal: {PROTEIN_GOAL} grams")
    print(f"Fat Goal: {FAT_GOAL} grams")
    print(f"Carbs Goal: {CARBS_GOAL} grams")

    confirmation = input("\nDo you confirm these goals? (yes/no): ").strip().lower()
    if confirmation == "yes":
        print("\nGoals confirmed!")
        break
    else:
        print("\nPlease re-enter your goals\n")

done = False

@dataclass
class Food:
    name: str
    calories: int
    protein: int
    fat: int
    carbs: int
    date: str

while not done:
    print("""
    (1) Add a new food
    (2) Visualize Data
    (3) Export Data to PDF
    (q) Quit
    """)
    
    choice = input("Choose an option: ")

    if choice == "1":
        print("Adding a new food!")
        try:
            name = input("Name: ")
            calories = int(input("Calories: "))
            protein = int(input("Proteins: "))
            fats = int(input("Fats: "))
            carbs = int(input("Carbs: "))
            date = datetime.today().strftime('%Y-%m-%d')
            food = Food(name, calories, protein, fats, carbs, date)
            data.append(food.__dict__)
            save_data(data)
            print("Successfully added!")
        except ValueError:
            print("\nInvalid input. Please enter numeric values.\n")

    elif choice == "2":
        if not data:
            print("No data to visualize. Please add food items first.")
            continue

        print("Select graph time range:")
        print("(1) Daily\n(2) Weekly\n(3) Monthly\n(4) Custom Range")
        graph_choice = input("Choose an option: ")

        if graph_choice == "1":
            start_date = datetime.today().strftime('%Y-%m-%d')
        elif graph_choice == "2":
            start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        elif graph_choice == "3":
            start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
        elif graph_choice == "4":
            start_date = input("Enter start date (YYYY-MM-DD): ")
        else:
            print("Invalid choice, defaulting to daily.")
            start_date = datetime.today().strftime('%Y-%m-%d')

        filtered_data = [f for f in data if f.get('date', '') >= start_date]

        # Helper function to ensure valid numbers
        def get_valid_number(value):
            try:
                return float(value) if value not in [None, "", "NaN"] else 0
            except ValueError:
                return 0

        protein_sum = sum(get_valid_number(f.get("protein", 0)) for f in filtered_data)
        fat_sum = sum(get_valid_number(f.get("fat", 0)) for f in filtered_data)
        carb_sum = sum(get_valid_number(f.get("carbs", 0)) for f in filtered_data)

        if protein_sum == 0 and fat_sum == 0 and carb_sum == 0:
            print("No valid macronutrient data to display.")
            continue

        datewise_calories = {}
        for food in filtered_data:
            datewise_calories[food['date']] = datewise_calories.get(food['date'], 0) + get_valid_number(food.get('calories', 0))

        dates = list(datewise_calories.keys())
        calories = list(datewise_calories.values())

        fig, axs = plt.subplots(2, 2)
        axs[0, 0].pie(
            [protein_sum, fat_sum, carb_sum],
            labels=["Proteins", "Fats", "Carbs"], autopct="%1.1f%%"
        )
        axs[0, 0].set_title("Macronutrients Distribution (Macros)")

        axs[0, 1].bar(
            [0, 1, 2], 
            [protein_sum, fat_sum, carb_sum], 
            width=0.4, 
            color='blue', 
            label="Consumed"
        )
        axs[0, 1].set_xticks([0, 0.5, 1, 1.5, 2, 2.5])
        axs[0, 1].set_xticklabels(
            ["Total Protein\nConsumed", "Protein Goal", "Total Fats\nConsumed", "Fat Goal", "Total Carbs\nConsumed", "Carbs Goal"], 
            fontsize=8
        )
        axs[0, 1].bar([0.5, 1.5, 2.5], [PROTEIN_GOAL, FAT_GOAL, CARBS_GOAL], width=0.4, color='orange', label="Goal")
        axs[0, 1].set_title("Macronutrient Progress")

        axs[1, 0].pie([sum(f['calories'] for f in filtered_data), CALORIE_LIMIT - sum(f['calories'] for f in filtered_data)], labels=["Calories", "Remaining"], autopct="%1.1f%%")
        axs[1, 0].set_title("Calorie Goal Progress")

        axs[1, 1].bar(dates, calories, color='green')
        axs[1, 1].set_title("Calorie Intake Over Time")
        axs[1, 1].set_xticklabels(dates, rotation=45, ha='right')

        fig.tight_layout()
        plt.show()

    elif choice == "3":
        pdf_filename = "calorie_report.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.drawString(100, 750, "Calorie Tracker Report")
        y = 720
        for food in data:
            c.drawString(100, y, f"{food['date']} - {food['name']}: {food['calories']} kcal")
            y -= 20
            if y < 50:
                c.showPage()
                y = 750
        c.save()
        print(f"Data successfully exported to {pdf_filename}")

    elif choice == "q":
        done = True

    else:
        print("Invalid Choice")
