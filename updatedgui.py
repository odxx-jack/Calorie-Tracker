import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class CalorieTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Calorie Tracker")
        self.root.geometry("500x500")
        self.data = []

        tk.Label(root, text="Food Name:").pack()
        self.food_entry = tk.Entry(root)
        self.food_entry.pack()

        tk.Label(root, text="Calories:").pack()
        self.calories_entry = tk.Entry(root)
        self.calories_entry.pack()

        tk.Label(root, text="Protein (g):").pack()
        self.protein_entry = tk.Entry(root)
        self.protein_entry.pack()

        tk.Label(root, text="Fat (g):").pack()
        self.fat_entry = tk.Entry(root)
        self.fat_entry.pack()

        tk.Label(root, text="Carbs (g):").pack()
        self.carbs_entry = tk.Entry(root)
        self.carbs_entry.pack()

        tk.Label(root, text="Date (YYYY-MM-DD):").pack()
        self.date_entry = tk.Entry(root)
        self.date_entry.pack()

        tk.Button(root, text="Add Entry", command=self.add_entry).pack(pady=5)
        tk.Button(root, text="Visualize Data", command=self.visualize_data).pack(pady=5)

    def add_entry(self):
        try:
            food = self.food_entry.get()
            calories = int(self.calories_entry.get())
            protein = float(self.protein_entry.get())
            fat = float(self.fat_entry.get())
            carbs = float(self.carbs_entry.get())
            date = self.date_entry.get()
            datetime.strptime(date, "%Y-%m-%d")  # Ensure valid date format

            self.data.append({
                "food": food,
                "calories": calories,
                "protein": protein,
                "fat": fat,
                "carbs": carbs,
                "date": date
            })

            messagebox.showinfo("Success", "Food entry added!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Ensure all fields are filled correctly.")

    def visualize_data(self):
        if not self.data:
            messagebox.showerror("No Data", "No food data to visualize.")
            return

        self.graph_window = tk.Toplevel(self.root)
        self.graph_window.title("Data Visualization")
        self.graph_window.geometry("800x600")

        tk.Label(self.graph_window, text="Enter start date (YYYY-MM-DD):").pack()
        self.start_date_entry = tk.Entry(self.graph_window)
        self.start_date_entry.pack()

        tk.Label(self.graph_window, text="Enter end date (YYYY-MM-DD):").pack()
        self.end_date_entry = tk.Entry(self.graph_window)
        self.end_date_entry.pack()

        tk.Button(self.graph_window, text="Generate Graphs", command=self.plot_custom_range_graphs).pack()

    def plot_custom_range_graphs(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter valid dates in the format YYYY-MM-DD.")
            return

        filtered_data = [f for f in self.data if start_date <= datetime.strptime(f['date'], "%Y-%m-%d") <= end_date]

        if not filtered_data:
            messagebox.showerror("No Data", "No food data available for the selected period.")
            return

        fig, axs = plt.subplots(2, 2, figsize=(10, 8))

        datewise_calories = {}
        for food in filtered_data:
            datewise_calories[food['date']] = datewise_calories.get(food['date'], 0) + food['calories']
        axs[0, 0].bar(datewise_calories.keys(), datewise_calories.values())
        axs[0, 0].set_title('Total Calories')
        axs[0, 0].tick_params(axis='x', rotation=45)

        total_protein = sum(f['protein'] for f in filtered_data)
        total_fat = sum(f['fat'] for f in filtered_data)
        total_carbs = sum(f['carbs'] for f in filtered_data)
        axs[0, 1].pie([total_protein, total_fat, total_carbs], labels=["Protein", "Fat", "Carbs"], autopct='%1.1f%%')
        axs[0, 1].set_title('Macronutrient Distribution')

        datewise_protein = {}
        for food in filtered_data:
            datewise_protein[food['date']] = datewise_protein.get(food['date'], 0) + food['protein']
        axs[1, 0].bar(datewise_protein.keys(), datewise_protein.values())
        axs[1, 0].set_title('Protein Intake')
        axs[1, 0].tick_params(axis='x', rotation=45)

        datewise_fat = {}
        for food in filtered_data:
            datewise_fat[food['date']] = datewise_fat.get(food['date'], 0) + food['fat']
        axs[1, 1].bar(datewise_fat.keys(), datewise_fat.values())
        axs[1, 1].set_title('Fat Intake')
        axs[1, 1].tick_params(axis='x', rotation=45)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalorieTracker(root)
    root.mainloop()
