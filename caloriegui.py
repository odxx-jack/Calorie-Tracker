from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox
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

# Define the Food class
@dataclass
class Food:
    name: str
    calories: int
    protein: int
    fat: int
    carbs: int
    date: str

class CalorieTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calorie Tracker")
        self.root.geometry("500x600")
        self.root.configure(bg="black")

        self.data = load_data()

        # Goals variables
        self.calorie_limit = tk.IntVar()
        self.protein_goal = tk.IntVar()
        self.fat_goal = tk.IntVar()
        self.carbs_goal = tk.IntVar()

        self.setup_goals_page()

    def setup_goals_page(self):
        # Hide any previous widgets
        for widget in self.root.winfo_children():
            widget.grid_forget()

        tk.Label(self.root, text="Set Your Daily Goals", font=("Arial", 18), fg="white", bg="black").grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(self.root, text="Calorie Limit (kcal):", font=("Arial", 12), fg="white", bg="black").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.calorie_limit, font=("Arial", 12)).grid(row=1, column=1)

        tk.Label(self.root, text="Protein Goal (g):", font=("Arial", 12), fg="white", bg="black").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.protein_goal, font=("Arial", 12)).grid(row=2, column=1)

        tk.Label(self.root, text="Fat Goal (g):", font=("Arial", 12), fg="white", bg="black").grid(row=3, column=0)
        tk.Entry(self.root, textvariable=self.fat_goal, font=("Arial", 12)).grid(row=3, column=1)

        tk.Label(self.root, text="Carbs Goal (g):", font=("Arial", 12), fg="white", bg="black").grid(row=4, column=0)
        tk.Entry(self.root, textvariable=self.carbs_goal, font=("Arial", 12)).grid(row=4, column=1)

        tk.Button(self.root, text="Submit Goals", font=("Arial", 12), fg="black", bg="white", command=self.submit_goals).grid(row=5, column=0, columnspan=2, pady=20)

    def submit_goals(self):
        self.calorie_limit_value = self.calorie_limit.get()
        self.protein_goal_value = self.protein_goal.get()
        self.fat_goal_value = self.fat_goal.get()
        self.carbs_goal_value = self.carbs_goal.get()

        if not all([self.calorie_limit_value, self.protein_goal_value, self.fat_goal_value, self.carbs_goal_value]):
            messagebox.showerror("Input Error", "Please enter all goal values.")
            return

        messagebox.showinfo("Goals Set", f"Goals set successfully!\n\nCalorie Limit: {self.calorie_limit_value} kcal\nProtein Goal: {self.protein_goal_value} g\nFat Goal: {self.fat_goal_value} g\nCarbs Goal: {self.carbs_goal_value} g")

        self.show_food_page()

    def show_food_page(self):
        # Hide any previous widgets
        for widget in self.root.winfo_children():
            widget.grid_forget()

        tk.Label(self.root, text="Add Food", font=("Arial", 18), fg="white", bg="black").grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(self.root, text="Food Name:", font=("Arial", 12), fg="white", bg="black").grid(row=1, column=0)
        self.food_name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.food_name_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Calories:", font=("Arial", 12), fg="white", bg="black").grid(row=2, column=0)
        self.food_calories_entry = tk.Entry(self.root, font=("Arial", 12))
        self.food_calories_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Protein:", font=("Arial", 12), fg="white", bg="black").grid(row=3, column=0)
        self.food_protein_entry = tk.Entry(self.root, font=("Arial", 12))
        self.food_protein_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Fat:", font=("Arial", 12), fg="white", bg="black").grid(row=4, column=0)
        self.food_fat_entry = tk.Entry(self.root, font=("Arial", 12))
        self.food_fat_entry.grid(row=4, column=1)

        tk.Label(self.root, text="Carbs:", font=("Arial", 12), fg="white", bg="black").grid(row=5, column=0)
        self.food_carbs_entry = tk.Entry(self.root, font=("Arial", 12))
        self.food_carbs_entry.grid(row=5, column=1)

        tk.Button(self.root, text="Submit Food", font=("Arial", 12), fg="black", bg="white", command=self.add_food).grid(row=6, column=0, columnspan=2, pady=20)

        tk.Button(self.root, text="Visualize Data", font=("Arial", 12), fg="black", bg="white", command=self.visualize_data).grid(row=7, column=0, columnspan=2, pady=20)

        tk.Button(self.root, text="Export to PDF", font=("Arial", 12), fg="black", bg="white", command=self.export_to_pdf).grid(row=8, column=0, columnspan=2, pady=20)

    def add_food(self):
        name = self.food_name_entry.get()
        calories = self.food_calories_entry.get()
        protein = self.food_protein_entry.get()
        fat = self.food_fat_entry.get()
        carbs = self.food_carbs_entry.get()

        # Validate inputs
        if not all([name, calories, protein, fat, carbs]):
            messagebox.showerror("Input Error", "Please enter all food details.")
            return

        try:
            calories = int(calories)
            protein = int(protein)
            fat = int(fat)
            carbs = int(carbs)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for calories, protein, fat, and carbs.")
            return

        date = datetime.today().strftime('%Y-%m-%d')

        food = Food(name, calories, protein, fat, carbs, date)
        self.data.append(food.__dict__)
        save_data(self.data)

        messagebox.showinfo("Food Added", f"Food added successfully!\n\n{name} - {calories} kcal")

    def visualize_data(self):
        if not self.data:
            messagebox.showerror("No Data", "No food data to visualize.")
            return

    # Time period selection
        tk.Label(self.root, text="Select Time Period:", font=("Arial", 12), fg="white", bg="black").grid(row=9, column=0)
        self.time_period_var = tk.StringVar(value="Custom")
        time_period_options = ["Daily", "Weekly", "Monthly", "Custom"]
        self.time_period_dropdown = tk.OptionMenu(self.root, self.time_period_var, *time_period_options)
        self.time_period_dropdown.grid(row=9, column=1)

    # Custom range selection
        self.start_date_entry = tk.Entry(self.root, font=("Arial", 12))
        self.end_date_entry = tk.Entry(self.root, font=("Arial", 12))

    # Show custom date range inputs only if "Custom" is selected
        if self.time_period_var.get() == "Custom":
            tk.Label(self.root, text="Enter start date (YYYY-MM-DD):", font=("Arial", 12), fg="white", bg="black").grid(row=10, column=0)
            self.start_date_entry.grid(row=10, column=1)

            tk.Label(self.root, text="Enter end date (YYYY-MM-DD):", font=("Arial", 12), fg="white", bg="black").grid(row=11, column=0)
            self.end_date_entry.grid(row=11, column=1)
        else:
            self.start_date_entry.grid_forget()
            self.end_date_entry.grid_forget()

        tk.Button(self.root, text="Generate Graphs", font=("Arial", 12), fg="black", bg="white", command=self.plot_time_period_graphs).grid(row=12, column=0, columnspan=2, pady=20)

    def plot_time_period_graphs(self):
        time_period = self.time_period_var.get()

        # If Custom is selected, use the custom date range
        if time_period == "Custom":
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get()

            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter valid dates in the format YYYY-MM-DD.")
                return

            filtered_data = [f for f in self.data if start_date <= datetime.strptime(f['date'], "%Y-%m-%d") <= end_date]
        else:
            # Group data by the selected period (daily, weekly, monthly)
            filtered_data = self.group_data_by_period(time_period)

        if not filtered_data:
            messagebox.showerror("No Data", "No food data available for the selected period.")
            return

        # Generate the 4 graphs as per your original code
        fig, axs = plt.subplots(2, 2)

        # Total Calories vs Time
        datewise_calories = {}
        for food in filtered_data:
            datewise_calories[food['date']] = datewise_calories.get(food['date'], 0) + food['calories']

        dates = list(datewise_calories.keys())
        calories = list(datewise_calories.values())
        axs[0, 0].bar(dates, calories)
        axs[0, 0].set_title('Total Calories')

        # Protein, Fat, Carbs Distribution Pie Chart
        total_protein = sum(f['protein'] for f in filtered_data)
        total_fat = sum(f['fat'] for f in filtered_data)
        total_carbs = sum(f['carbs'] for f in filtered_data)
        axs[0, 1].pie([total_protein, total_fat, total_carbs], labels=["Protein", "Fat", "Carbs"], autopct='%1.1f%%')
        axs[0, 1].set_title('Macronutrient Distribution')

        # Total Protein vs Time
        datewise_protein = {}
        for food in filtered_data:
            datewise_protein[food['date']] = datewise_protein.get(food['date'], 0) + food['protein']

        protein_dates = list(datewise_protein.keys())
        protein_values = list(datewise_protein.values())
        axs[1, 0].bar(protein_dates, protein_values)
        axs[1, 0].set_title('Protein Intake')

        # Total Fat vs Time
        datewise_fat = {}
        for food in filtered_data:
            datewise_fat[food['date']] = datewise_fat.get(food['date'], 0) + food['fat']

        fat_dates = list(datewise_fat.keys())
        fat_values = list(datewise_fat.values())
        axs[1, 1].bar(fat_dates, fat_values)
        axs[1, 1].set_title('Fat Intake')

        plt.show()

    def group_data_by_period(self, time_period):
        """ Group data by the selected time period (daily, weekly, monthly) """
        grouped_data = {}

        for food in self.data:
            food_date = datetime.strptime(food['date'], "%Y-%m-%d")

            # Group by daily
            if time_period == "Daily":
                key = food_date.date()

            # Group by weekly
            elif time_period == "Weekly":
                start_of_week = food_date - timedelta(days=food_date.weekday())
                key = start_of_week.date()

            # Group by monthly
            elif time_period == "Monthly":
                key = food_date.replace(day=1).date()

            # Update grouped data
            if key not in grouped_data:
                grouped_data[key] = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
            
            grouped_data[key]["calories"] += food['calories']
            grouped_data[key]["protein"] += food['protein']
            grouped_data[key]["fat"] += food['fat']
            grouped_data[key]["carbs"] += food['carbs']

        # Convert grouped data to a list
        return [{"date": str(date), "calories": values["calories"], "protein": values["protein"], 
                "fat": values["fat"], "carbs": values["carbs"]} for date, values in grouped_data.items()]

    def export_to_pdf(self):
        c = canvas.Canvas("calorie_tracker.pdf", pagesize=letter)
        c.drawString(100, 750, "Calorie Tracker Report")

        for i, food in enumerate(self.data):
            c.drawString(100, 730 - i * 20, f"Food: {food['name']}, Calories: {food['calories']}, Date: {food['date']}")

        c.save()

        messagebox.showinfo("Export to PDF", "PDF generated successfully!")

# Run the app
root = tk.Tk()
app = CalorieTrackerApp(root)
root.mainloop()
