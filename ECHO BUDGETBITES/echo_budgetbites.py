import streamlit as st
import random
from openai import OpenAI

# --- 1. SETUP LOCAL LM STUDIO SERVER ---
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")

# --- 2. THE HAND-GATHERED CANTEEN DATASET ---
menu_data = {
    "🍱 Main Dishes & Rice Meals": [
        {"name": "Fried Pork (with Rice)", "price": 85}, {"name": "Bicol Express (with Rice)", "price": 75},
        {"name": "Fried Chicken (with Rice)", "price": 75}, {"name": "Humba (with Rice)", "price": 75},
        {"name": "Adobong Manok (with Rice)", "price": 75}, {"name": "Adobong Baboy (with Rice)", "price": 75},
        {"name": "Ginisang Gulay with Giniling (with Rice)", "price": 75}, {"name": "Chicken Fingers (with Rice)", "price": 65},
        {"name": "Cordon Bleu (with Rice)", "price": 65}, {"name": "Shawarma Rice", "price": 65},
        {"name": "Shawarma Rice with Iced Tea Combo", "price": 75}, {"name": "Longganisa (with Rice)", "price": 55},
        {"name": "Hotdog (with Rice)", "price": 55}
    ],
    "🥢 Noodles": [
        {"name": "Pancit Canton (Original)", "price": 30}, {"name": "Pancit Canton (Calamansi)", "price": 30},
        {"name": "Pancit Canton (Chili Mansi)", "price": 30}, {"name": "Pancit Canton (Sweet and Spicy)", "price": 30},
        {"name": "Pancit Canton (Extra Hot)", "price": 30}, {"name": "Fried Noodles", "price": 35}
    ],
    "🥟 Snacks & Dimsum": [
        {"name": "Kwek Kwek", "price": 20}, {"name": "Empanada", "price": 35},
        {"name": "Chicken Siomai", "price": 45}, {"name": "Pork Siomai", "price": 45},
        {"name": "Sharksfin Siomai", "price": 55}
    ],
    "🍩 Sweets & Desserts": [
        {"name": "Banana Que", "price": 30}, {"name": "Karioka", "price": 15},
        {"name": "Donut", "price": 15}, {"name": "Palitaw", "price": 15},
        {"name": "Brownies", "price": 35}, {"name": "Cookies", "price": 35}
    ],
    "🍚 Rice Add-ons": [
        {"name": "1 Cup Rice", "price": 20}, {"name": "Half Cup Rice", "price": 10}
    ],
    "🥤 Beverages (Cold & Hot)": [
        {"name": "Bottled Water", "price": 20}, {"name": "Coke Mismo", "price": 20},
        {"name": "Sprite", "price": 25}, {"name": "Royal", "price": 25},
        {"name": "Iced Tea", "price": 25}, {"name": "Nutriboost (Chocolate)", "price": 30},
        {"name": "Nutriboost (Strawberry)", "price": 30}, {"name": "Fruit Shake (Watermelon)", "price": 45},
        {"name": "Fruit Shake (Strawberry)", "price": 45}, {"name": "Fruit Shake (Cantaloupe)", "price": 45},
        {"name": "Fruit Shake (Mango)", "price": 45}, {"name": "Fruit Shake (Lemonade)", "price": 45},
        {"name": "Milo", "price": 15}, {"name": "Bearbrand Milk", "price": 20},
        {"name": "Nescafe Classic", "price": 15}, {"name": "Nescafe Creamy White", "price": 15},
        {"name": "Kopiko Blanca", "price": 15}
    ]
}

# --- 3. CORE DETERMINISTIC OPTIMIZATION ENGINE ---
def generate_exact_combinations(menu, max_budget, is_feast, total_needed=6):
    all_items = []
    for cat, items in menu.items():
        all_items.extend(items)
    
    usable_items = [i for i in all_items if i['price'] <= max_budget]
    if not usable_items:
        return []

    valid_combos = []
    seen_combo_signatures = [] 
    
    if is_feast:
        # FEAST MODE: Unique items only, deeply maximizing budget down to ₱0 change
        for _ in range(40000): 
            current_combo = []
            current_sum = 0
            shuffled = usable_items.copy()
            random.shuffle(shuffled)
            seen_items = set()
            
            for item in shuffled:
                if (current_sum + item['price'] <= max_budget) and (item['name'] not in seen_items):
                    current_combo.append(item)
                    current_sum += item['price']
                    seen_items.add(item['name'])
            
            if current_combo:
                combo_signature = " | ".join(sorted(list(seen_items)))
                if combo_signature not in seen_combo_signatures:
                    formatted_items = [{"name": n, "price": next(i['price'] for i in usable_items if i['name'] == n)} for n in seen_items]
                    change = max_budget - current_sum
                    
                    valid_combos.append({"items": formatted_items, "total": current_sum, "change": change})
                    seen_combo_signatures.append(combo_signature)
                    
        valid_combos.sort(key=lambda x: x['change'])
        
    else:
        # TIPID MODE: Strictly forced to 2 or 3 distinct low-cost items
        for _ in range(30000):
            combo_size = random.randint(2, 3) # Strict math lock: 2 or 3 foods ONLY
            shuffled = usable_items.copy()
            random.shuffle(shuffled)
            
            sample = []
            current_sum = 0
            seen_items = set()
            
            for item in shuffled:
                if len(sample) < combo_size and (current_sum + item['price'] <= max_budget):
                    if item['name'] not in seen_items:
                        sample.append(item)
                        current_sum += item['price']
                        seen_items.add(item['name'])
            
            if len(sample) < combo_size:
                continue
                
            pure_addons_only = all("Rice" in i['name'] or "Water" in i['name'] for i in sample)
            if pure_addons_only:
                continue
                
            combo_signature = " | ".join(sorted(list(seen_items)))
            
            if combo_signature not in seen_combo_signatures:
                formatted_items = [{"name": n, "price": next(i['price'] for i in usable_items if i['name'] == n)} for n in seen_items]
                change = max_budget - current_sum
                
                valid_combos.append({"items": formatted_items, "total": current_sum, "change": change})
                seen_combo_signatures.append(combo_signature)
                    
        valid_combos.sort(key=lambda x: x['change'], reverse=True)

    return valid_combos[:total_needed]

# --- 4. STREAMLIT INTERFACE UI ---
st.set_page_config(page_title="Echo BudgetBites", page_icon="🍔", layout="centered")
st.title("🍔 Echo BudgetBites")
st.subheader("AI Canteen Food Recommendation System for Student Budgets 🦅")
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
    strategy = st.radio("Select objective profile:", ["Tipid Mode (Maximize savings)", "Feast Mode (Maximize volume)"], label_visibility="collapsed")

st.write("### 🔍 Canteen Price Reference")
tabs = st.tabs(list(menu_data.keys()))
for idx, cat_name in enumerate(menu_data.keys()):
    with tabs[idx]:
        for item in menu_data[cat_name]:
            c1, c2 = st.columns([3, 1])
            c1.write(f"• {item['name']}")
            c2.write(f"**₱{item['price']}**")

st.write("---")

# --- 5. EXECUTE & RE-FORMATTING LOOP ---
if st.button("🔥 Run Echo BudgetBites Optimizer", use_container_width=True):
    if budget > 0:
        with st.spinner("Echo is processing combinations via Gemma-3..."):
            is_feast = "Feast" in strategy
            raw_combos = generate_exact_combinations(menu_data, budget, is_feast, total_needed=6)
            
            if not raw_combos:
                st.warning("No item combinations match your specified strategy profile.")
            else:
                try:
                    pre_formatted_output = ""
                    for i, combo in enumerate(raw_combos):
                        pre_formatted_output += f"### Option {i+1}\n"
                        for item in combo['items']:
                            pre_formatted_output += f"- {item['name']} - ₱{item['price']}\n"
                        
                        # Added newline formatting to push the totals down
                        pre_formatted_output += "\n" 
                        pre_formatted_output += f"**Total Expense:** ₱{combo['total']}\n"
                        pre_formatted_output += f"**Your Change:** ₱{combo['change']}\n\n"
                        pre_formatted_output += "---\n\n"

                    prompt = f"Here is the finalized menu. Output this EXACTLY as written:\n\n{pre_formatted_output}"
                    
                    clean_vertical_instruction = (
                        "You are Echo. Do not add conversational paragraphs, adjectives, or commentary filler words. "
                        "CRITICAL RULE: Do not recalculate the math. The math is already 100% correct. "
                        "Your ONLY job is to repeat the user's prompt text exactly, keeping the exact vertical format."
                    )
                    
                    completion = client.chat.completions.create(
                        model="google/gemma-3-4b",
                        messages=[
                            {"role": "system", "content": clean_vertical_instruction},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.0, 
                    )
                    st.balloons()
                    st.markdown(completion.choices[0].message.content)
                except Exception as e:
                    st.error("⚠️ Connection Error with LM Studio. Verify your local server configurations on port 1234.")
    else:
        st.warning("Please type a budget greater than 0 first!")
