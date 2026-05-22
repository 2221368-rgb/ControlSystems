import streamlit as st
import json
import random
from openai import OpenAI

# --- 1. SETUP LOCAL LM STUDIO SERVER ---
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")

# --- 2. UBLC CANTEEN MENU DATA ---
menu_data = {
    "🍱 Main Dishes & Rice Meals": [
        {"name": "Fried Pork (with Rice)", "price": 85},
        {"name": "Bicol Express (with Rice)", "price": 75},
        {"name": "Fried Chicken (with Rice)", "price": 75},
        {"name": "Humba (with Rice)", "price": 75},
        {"name": "Adobong Manok (with Rice)", "price": 75},
        {"name": "Adobong Baboy (with Rice)", "price": 75},
        {"name": "Ginisang Gulay with Giniling (with Rice)", "price": 75},
        {"name": "Chicken Fingers (with Rice)", "price": 65},
        {"name": "Cordon Bleu (with Rice)", "price": 65},
        {"name": "Shawarma Rice", "price": 65},
        {"name": "Shawarma Rice with Iced Tea Combo", "price": 75},
        {"name": "Longganisa (with Rice)", "price": 55},
        {"name": "Hotdog (with Rice)", "price": 55}
    ],
    "🥢 Noodles": [
        {"name": "Pancit Canton (Original)", "price": 30},
        {"name": "Pancit Canton (Calamansi)", "price": 30},
        {"name": "Pancit Canton (Chili Mansi)", "price": 30},
        {"name": "Pancit Canton (Sweet and Spicy)", "price": 30},
        {"name": "Pancit Canton (Extra Hot)", "price": 30},
        {"name": "Fried Noodles", "price": 35}
    ],
    "🥟 Snacks & Dimsum": [
        {"name": "Kwek Kwek", "price": 20},
        {"name": "Empanada", "price": 35},
        {"name": "Chicken Siomai", "price": 45},
        {"name": "Pork Siomai", "price": 45},
        {"name": "Sharksfin Siomai", "price": 55}
    ],
    "🍩 Sweets & Desserts": [
        {"name": "Banana Que", "price": 30},
        {"name": "Karioka", "price": 15},
        {"name": "Donut", "price": 15},
        {"name": "Palitaw", "price": 15},
        {"name": "Brownies", "price": 35},
        {"name": "Cookies", "price": 35}
    ],
    "🍚 Rice Add-ons": [
        {"name": "1 Cup Rice", "price": 20},
        {"name": "Half Cup Rice", "price": 10}
    ],
    "🥤 Beverages (Cold & Hot)": [
        {"name": "Bottled Water", "price": 20},
        {"name": "Coke Mismo", "price": 20},
        {"name": "Sprite", "price": 25},
        {"name": "Royal", "price": 25},
        {"name": "Iced Tea", "price": 25},
        {"name": "Nutriboost (Chocolate)", "price": 30},
        {"name": "Nutriboost (Strawberry)", "price": 30},
        {"name": "Fruit Shake (Watermelon)", "price": 45},
        {"name": "Fruit Shake (Strawberry)", "price": 45},
        {"name": "Fruit Shake (Cantaloupe)", "price": 45},
        {"name": "Fruit Shake (Mango)", "price": 45},
        {"name": "Fruit Shake (Lemonade)", "price": 45},
        {"name": "Milo", "price": 15},
        {"name": "Bearbrand Milk", "price": 20},
        {"name": "Nescafe Classic", "price": 15},
        {"name": "Nescafe Creamy White", "price": 15},
        {"name": "Kopiko Blanca", "price": 15}
    ]
}

# --- 3. EXACT PYTHON CALCULATOR ENGINE ---
# Set default total to 6 combinations
def generate_exact_combinations(menu, max_budget, is_feast, total_needed=6):
    all_items = []
    for cat, items in menu.items():
        all_items.extend(items)
        
    valid_combos = []
    attempts = 0
    
    while len(valid_combos) < total_needed * 4 and attempts < 5000:
        attempts += 1
        combo_size = random.randint(1, 4)
        sample = random.choices(all_items, k=combo_size)
        
        unique_sample = []
        for s in sample:
            if s not in unique_sample:
                unique_sample.append(s)
                
        total_cost = sum(item['price'] for item in unique_sample)
        change = max_budget - total_cost
        
        if total_cost <= max_budget:
            combo_data = {
                "items": unique_sample,
                "total": total_cost,
                "change": change
            }
            if combo_data not in valid_combos:
                valid_combos.append(combo_data)

    if is_feast:
        # Feast Mode: Sorts closest to the budget limit (lowest change first)
        valid_combos.sort(key=lambda x: x['change'])
    else:
        # Tipid Mode: Sorts cheapest combinations first (highest change first)
        valid_combos.sort(key=lambda x: x['change'], reverse=True)
        
    return valid_combos[:total_needed]

# --- 4. UI SETUP ---
st.set_page_config(page_title="Echo BudgetBites", page_icon="🍔", layout="centered")

st.title("🍔 Echo BudgetBites")
st.subheader("AI Canteen Food Recommendation System for UBLC 🦅")
st.write("Welcome, fellow Brahman! Enter your allowance below to calculate your food choices.")
st.write("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.write("**💵 Enter your budget:**")
    pay_col1, pay_col2 = st.columns([1, 3])
    with pay_col1:
        st.code("PHP ₱")
    with pay_col2:
        budget_input = st.text_input(label="Budget Field", value="100", label_visibility="collapsed")
    
    try:
        clean_input = budget_input.replace("₱", "").replace("PHP", "").strip()
        budget = int(clean_input) if clean_input else 0
    except ValueError:
        budget = 0
        st.error("Please enter a valid whole number!")

with col2:
    st.write("**🍽️ Choose Strategy:**")
    strategy = st.radio(
        "Select objective profile:",
        ["Tipid Mode (Maximize your change/savings)", "Feast Mode (Use up all your money to get full)"],
        label_visibility="collapsed"
    )

st.write("")

st.write("### 🔍 UBLC Canteen Menu Reference")
categories_list = list(menu_data.keys())
tabs = st.tabs(categories_list)

for idx, cat_name in enumerate(categories_list):
    with tabs[idx]:
        for item in menu_data[cat_name]:
            c1, c2 = st.columns([3, 1])
            c1.write(f"• {item['name']}")
            c2.write(f"**₱{item['price']}**")

st.write("---")

# --- 5. EXECUTE ---
if st.button("🔥 Run Echo BudgetBites Optimizer", use_container_width=True):
    if budget > 0:
        with st.spinner("Echo is processing mathematical matrices via Gemma-3..."):
            
            is_feast = "Feast" in strategy
            # Request exactly 6 options from our pre-sorter
            raw_combos = generate_exact_combinations(menu_data, budget, is_feast, total_needed=6)
            
            if not raw_combos:
                st.warning("No combinations match your budget limit. Try increasing the amount!")
            else:
                try:
                    prompt = f"""
                    You are Echo, the AI system behind 'Echo BudgetBites' for the UBLC Canteen.
                    The student has a maximum budget of exactly ₱{budget}.
                    The chosen mode is: {'FEAST MODE (Minimize change)' if is_feast else 'TIPID MODE (Maximize change)'}.
                    
                    Here are 6 mathematical calculations already processed for you:
                    {json.dumps(raw_combos, indent=2)}
                    
                    Your task:
                    Display these 6 combinations beautifully to the user.
                    
                    CRITICAL FORMATTING LAWS:
                    1. List them clearly from Option 1 to Option 6.
                    2. For each option, list out the items and their individual prices.
                    3. Display the exact total cost provided in the data.
                    4. You must end every single option block with this exact line: "Your change is ₱[amount]." 
                       If change is 0, write "Your change is ₱0." Use the exact change data provided above. Do not guess or do your own math.
                    5. Format with beautiful headers, bold text, and food emojis.
                    """
                    
                    completion = client.chat.completions.create(
                        model="google/gemma-3-4b",
                        messages=[
                            {"role": "system", "content": "You are Echo, an elite layout assistant that outputs exactly 6 structured options using verified datasets."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.1, 
                    )
                    
                    output_text = completion.choices[0].message.content
                    
                    st.balloons()
                    st.success(f"✨ Echo BudgetBites generated 6 verified options within your ₱{budget} limit:")
                    st.markdown(output_text)
                    
                except Exception as e:
                    st.error("⚠️ Connection Error with LM Studio. Re-verify server configuration settings.")
                    with st.expander("🛠️ View Local Connection Error Logs"):
                        st.code(str(e))
    else:
        st.warning("Please type a budget greater than 0 first!")