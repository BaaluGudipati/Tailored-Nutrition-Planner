import streamlit as st
import random

# Set page configuration
st.set_page_config(
    page_title="Meal Planner with Weight Goals",
    page_icon="🍴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants for conversions
UNITS_IN_TO_CM = 2.54
UNITS_LB_TO_KG = 0.453592
CALORIES_PER_KG = 7700  # Approximate calories needed to lose/gain 1 kg

# Meal data with calorie counts
vegetarian_items = {
    "Breakfast": [
        ("Oatmeal with Berries", 250),
        ("Avocado Toast", 300),
        ("Smoothie Bowl", 350),
        ("Greek Yogurt with Granola", 200),
        ("Veggie Omelette", 180),
        ("Chia Pudding", 230),
        ("Banana Pancakes", 320)
    ],
    "Lunch": [
        ("Grilled Veggie Wrap", 400),
        ("Quinoa Salad", 350),
        ("Lentil Soup", 300),
        ("Stuffed Bell Peppers", 280),
        ("Vegetable Stir-fry", 250),
        ("Tofu Buddha Bowl", 450),
        ("Spinach and Feta Pie", 320)
    ],
    "Dinner": [
        ("Vegetable Pasta", 400),
        ("Paneer Tikka", 350),
        ("Mushroom Risotto", 380),
        ("Eggplant Parmesan", 420),
        ("Tofu Stir-fry", 350),
        ("Vegetarian Chili", 360),
        ("Sweet Potato Curry", 400)
    ]
}

non_vegetarian_items = {
    "Breakfast": [
        ("Scrambled Eggs", 250),
        ("Turkey Bacon Toast", 280),
        ("Chicken Sausage Omelette", 300),
        ("Protein Pancakes", 350),
        ("Egg Muffins", 200),
        ("Smoked Salmon Bagel", 400),
        ("Breakfast Burrito", 450)
    ],
    "Lunch": [
        ("Grilled Chicken Salad", 400),
        ("Turkey Sandwich", 350),
        ("Beef Chili", 450),
        ("Chicken Burrito Bowl", 500),
        ("Shrimp Pasta", 450),
        ("Grilled Tuna Steak", 400),
        ("Pulled Pork Wrap", 450)
    ],
    "Dinner": [
        ("Grilled Salmon", 400),
        ("Chicken Alfredo", 500),
        ("Beef Steak", 600),
        ("Baked Cod with Veggies", 350),
        ("Lamb Curry", 550),
        ("Chicken Stir-fry", 400),
        ("Seafood Paella", 450)
    ]
}

# BMR Calculation
def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        return int(9.99 * weight + 6.25 * height - 4.92 * age + 5)
    else:
        return int(9.99 * weight + 6.25 * height - 4.92 * age - 161)

# Generate meal plan based on target calories and preference
def generate_meal_plan(target_calories, preference):
    food_items = vegetarian_items if preference == "Vegetarian" else non_vegetarian_items
    meal_plan = {}
    total_calories = 0
    calories_per_meal = target_calories // 3  # Divide target equally across meals

    for meal_type, items in food_items.items():
        random.shuffle(items)
        selected_items = []
        meal_calories = 0

        for item, calories in items:
            if meal_calories + calories <= calories_per_meal or len(selected_items) == 0:
                selected_items.append((item, calories))
                meal_calories += calories
            if meal_calories >= calories_per_meal:
                break

        meal_plan[meal_type] = selected_items
        total_calories += meal_calories

    return meal_plan, total_calories


# UI Styling
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #ffffff;
        
        padding: 15px;
        border-radius: 8px;
    }
    .meal-section {
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 8px;
        
        margin-bottom: 10px;
    }
    .meal-section strong {
        font-size: 18px;
        color: #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="main-title">Tailored Nutrition Planner</h1>', unsafe_allow_html=True)

# Sidebar Inputs
st.sidebar.header("User Details")
name = st.sidebar.text_input("Enter your name")
age = st.sidebar.number_input("Enter your age", min_value=0, step=1, value=0)
unit_preference = st.sidebar.radio("Preferred units:", ["Metric (kg, cm)", "Imperial (lb, ft + in)"])

# Weight and height inputs
if unit_preference == "Metric (kg, cm)":
    # weight = st.sidebar.number_input("Enter your weight (kg)", min_value=0, value=0)
    height = st.sidebar.number_input("Enter your height (cm)", min_value=0, value=0)
else:
    weight_lb = st.sidebar.number_input("Enter your weight (lb)", min_value=0, value=0)
    height_ft = st.sidebar.number_input("Enter your height (ft)", min_value=0, value=0)
    height_in = st.sidebar.number_input("Enter your height (in)", min_value=0, value=0)

    # weight = weight_lb * UNITS_LB_TO_KG
    height = (height_ft * 12 + height_in) * UNITS_IN_TO_CM

gender = st.sidebar.radio("Choose your gender:", ["Male", "Female"])
preference = st.sidebar.radio("Meal Preference:", ["Vegetarian", "Non-Vegetarian"])

# Weight goal inputs
current_weight = st.sidebar.number_input("Enter your current weight (kg)", min_value=0.0, value=0.0)
goal_weight = st.sidebar.number_input("Enter your goal weight (kg)", min_value=0.0, value=0.0)

# Validation
if current_weight > 0 and height > 0 and age > 0:
    if goal_weight > 0:  # User has specified a goal weight
        weight_change = goal_weight - current_weight
        if weight_change > 0:
            goal_type = "Gain Weight"
            daily_calorie_adjustment = (weight_change * CALORIES_PER_KG) / 30  # Assuming 30 days for simplicity
            target_calories = calculate_bmr(current_weight, height, age, gender) + daily_calorie_adjustment
        else:
            goal_type = "Lose Weight"
            daily_calorie_adjustment = (abs(weight_change) * CALORIES_PER_KG) / 30  # Assuming 30 days for simplicity
            target_calories = calculate_bmr(current_weight, height, age, gender) - daily_calorie_adjustment
    else:  # No goal weight, suggest maintenance
        goal_type = "Maintenance"
        target_calories = calculate_bmr(current_weight, height, age, gender)

    # Protein Goal: Bodyweight * 1.5 (for all goals)
    protein_goal = current_weight * 1.5

    # Display Results
    st.sidebar.subheader(f"Target Calories: {int(target_calories)} kcal")
    st.sidebar.subheader(f"Protein Goal: {protein_goal} grams/day")

    # Generate Meal Plan Button
    if st.sidebar.button("Generate Meal Plan"):
        meal_plan, total_calories = generate_meal_plan(target_calories, preference)

        st.markdown(f"<h2 style='text-align: center;'>Meal Plan for {name}</h2>", unsafe_allow_html=True)
        st.write(f"**Target Calories:** {int(target_calories)} kcal")
        st.write(f"**Protein Goal:** {protein_goal} grams/day")
        st.write(f"**Goal:** {goal_type} ({weight_change:.2f} kg)")

        # Display meals
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="meal-section"><strong>Breakfast</strong></div>', unsafe_allow_html=True)
            for item, calories in meal_plan["Breakfast"]:
                st.markdown(f'<div class="meal-section">{item} - {calories} kcal</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="meal-section"><strong>Lunch</strong></div>', unsafe_allow_html=True)
            for item, calories in meal_plan["Lunch"]:
                st.markdown(f'<div class="meal-section">{item} - {calories} kcal</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="meal-section"><strong>Dinner</strong></div>', unsafe_allow_html=True)
            for item, calories in meal_plan["Dinner"]:
                st.markdown(f'<div class="meal-section">{item} - {calories} kcal</div>', unsafe_allow_html=True)

        st.write(f"**Total Estimated Calories:** {int(total_calories)} kcal")
else:
    st.sidebar.error("Please fill all fields to generate a meal plan!")
