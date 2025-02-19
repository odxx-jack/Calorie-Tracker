from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt

while True:
    CALORIE_LIMIT = int(input("Enter your daily calorie limit (kcal): "))
    PROTEIN_GOAL = int(input("Enter your daily protein goal (grams): "))
    FAT_GOAL = int(input("Enter your daily fat goal (grams): "))
    CARBS_GOAL = int(input("Enter your daily carbs goal (grams): "))

    print(f"Your goals are set as follows:")
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
    
today = []


@dataclass
class Food:
    name: str
    calories: int
    protein: int
    fat: int
    carbs: int 


done = False

while not done:
    print("""
    (1) Add a new food
    (2) Visualize Data
    (q) Quit
     """)
    
    choice = input("Choose an option: ")

    if choice == "1":
        print("Adding a new food!")
        name = input("Name: ")
        calories = int(input("Calories: "))
        protein = int(input("Proteins: "))
        fats = int(input("Fats: "))
        carbs = int(input("Carbs: "))
        food = Food(name, calories, protein, fats, carbs)
        today.append(food)
        print("Successfully added!")
    elif choice == "2":
        if not today:
            print("No data to visualize. Please add food items first.")
            continue

        calorie_sum = sum(food.calories for food in today)
        protein_sum = sum(food.protein for food in today)
        fats_sum = sum(food.fat for food in today)
        carbs_sum = sum(food.carbs for food in today)

        fig, axs = plt.subplots(2, 2) 
        axs[0, 0].pie(
            [protein_sum, fats_sum, carbs_sum],
            labels=["Proteins", "Fats", "Carbs"],
            autopct="%1.1f%%"
    )
        axs[0, 0].set_title("Macronutrients Distribution (Macros)")
        axs[0, 1].bar([0, 1, 2], [protein_sum, fats_sum, carbs_sum], width=0.4, color='blue', label="Consumed")
        axs[0, 1].set_xticks([0, 0.5, 1, 1.5, 2, 2.5])
        axs[0, 1].set_xticklabels(
            ["Total Protein\nConsumed", "Protein Goal", "Total Fats\nConsumed", "Fat Goal", "Total Carbs\nConsumed", "Carbs Goal"],
            fontsize=8)
        axs[0, 1].bar([0.5, 1.5, 2.5], [PROTEIN_GOAL, FAT_GOAL, CARBS_GOAL], width=0.4, color='orange', label="Goal")
        axs[0, 1].set_title("Macronutrient Progress")
        axs[1, 0].pie([calorie_sum, CALORIE_LIMIT - calorie_sum], labels=["Calories", "Remaining"], autopct="%1.1f%%")
        axs[1, 0].set_title("Calorie Goal Progress")
        axs[1, 1].plot(list(range(len(today))), np.cumsum([food.calories for food in today]), label="Calories Eaten")
        axs[1, 1].plot(list(range(len(today))), [CALORIE_LIMIT] * len(today), label="Calorie Goal")
        axs[1, 1].legend()
        axs[1, 1].set_title("Calorie Consumption Over Time")
        fig.tight_layout()
        plt.show()
    elif choice == "q":
        done = True
    else:
        print("Invalid Choice")