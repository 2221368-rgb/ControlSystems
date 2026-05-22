import streamlit as st
import random

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Echo BudgetBites",
    page_icon="🍔",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* ---------- Hero ---------- */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    border-radius: 18px;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}
.hero h1 { font-size: 2.4rem; font-weight: 700; color: #f0c040; margin: 0 0 .3rem; letter-spacing: -0.5px; }
.hero p  { font-size: 1rem; color: #a0c4ff; margin: 0; }

/* ---------- Budget bar ---------- */
.budget-bar-wrap {
    background: #f8f9fb;
    border-radius: 10px;
    height: 10px;
    margin: .4rem 0 .6rem;
    overflow: hidden;
}
.budget-bar-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #22c55e, #f59e0b, #ef4444);
    transition: width .5s ease;
}

/* ---------- Combo card ---------- */
.combo-card {
    background: #ffffff;
    border: 1.5px solid #e8ecf1;
    border-radius: 16px;
    padding: 1.1rem 1.3rem 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,.06);
    transition: transform .15s ease, box-shadow .15s ease;
}
.combo-card:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(0,0,0,.10); }

.combo-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: .75rem;
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: .6rem;
}
.combo-title { font-size: 1rem; font-weight: 600; color: #1a1a2e; }

.badge {
    font-size: .72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: .3px;
}
.badge-savings { background: #d1fae5; color: #065f46; }
.badge-feast   { background: #dbeafe; color: #1e40af; }

/* ---------- Item row ---------- */
.item-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 0;
    border-bottom: 1px dashed #f0f0f0;
}
.item-row:last-of-type { border-bottom: none; }
.item-name { font-size: .88rem; color: #374151; }
.item-cat  { font-size: .70rem; color: #9ca3af; margin-left: 5px; }
.item-price { font-size: .88rem; font-weight: 600; color: #1a1a2e; font-family: 'DM Mono', monospace; }

/* ---------- Totals footer ---------- */
.combo-footer {
    display: flex;
    justify-content: space-between;
    margin-top: .8rem;
    padding-top: .6rem;
    border-top: 1.5px solid #f0f0f0;
    font-family: 'DM Mono', monospace;
    font-size: .85rem;
}
.total-label  { color: #6b7280; }
.total-amount { font-weight: 600; color: #1a1a2e; }
.change-positive { color: #16a34a; font-weight: 600; }
.change-zero     { color: #6b7280; }

/* ---------- Category pill ---------- */
.cat-pill {
    display: inline-block;
    font-size: .65rem;
    padding: 2px 7px;
    border-radius: 12px;
    margin: 1px 2px 4px 0;
    font-weight: 500;
}

/* ---------- Section header ---------- */
.section-header {
    font-size: .8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #9ca3af;
    margin: 1.5rem 0 .6rem;
}

/* ---------- Menu table ---------- */
.menu-price {
    font-family: 'DM Mono', monospace;
    font-size: .85rem;
    color: #f0c040;
    font-weight: 500;
}

/* ---------- Strategy radio custom ---------- */
div[data-testid="stRadio"] > label { font-weight: 500; }

/* ---------- Input field ---------- */
div[data-testid="stTextInput"] input {
    font-size: 1.4rem !important;
    font-weight: 600 !important;
    font-family: 'DM Mono', monospace !important;
    color: #1a1a2e !important;
}

/* ---------- Run button ---------- */
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #f0c040, #f59e0b) !important;
    color: #1a1a2e !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 12px !important;
    height: 3rem !important;
    letter-spacing: .3px;
    transition: opacity .2s;
}
div[data-testid="stButton"] button:hover { opacity: .88; }

/* ---------- Dark mode compat ---------- */
@media (prefers-color-scheme: dark) {
    .combo-card { background: #1e2235; border-color: #2d3250; }
    .combo-title { color: #e2e8f0; }
    .item-name   { color: #cbd5e1; }
    .total-amount { color: #e2e8f0; }
    .combo-footer { border-color: #2d3250; }
    .combo-header { border-color: #2d3250; }
    .item-row { border-color: #2d3250; }
}
</style>
""", unsafe_allow_html=True)

# ── MENU DATA ──────────────────────────────────────────────────────────────────
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
        {"name": "Hotdog (with Rice)", "price": 55},
    ],
    "🥢 Noodles": [
        {"name": "Pancit Canton (Original)", "price": 30},
        {"name": "Pancit Canton (Calamansi)", "price": 30},
        {"name": "Pancit Canton (Chili Mansi)", "price": 30},
        {"name": "Pancit Canton (Sweet and Spicy)", "price": 30},
        {"name": "Pancit Canton (Extra Hot)", "price": 30},
        {"name": "Fried Noodles", "price": 35},
    ],
    "🥟 Snacks & Dimsum": [
        {"name": "Kwek Kwek", "price": 20},
        {"name": "Empanada", "price": 35},
        {"name": "Chicken Siomai", "price": 45},
        {"name": "Pork Siomai", "price": 45},
        {"name": "Sharksfin Siomai", "price": 55},
    ],
    "🍩 Sweets & Desserts": [
        {"name": "Banana Que", "price": 30},
        {"name": "Karioka", "price": 15},
        {"name": "Donut", "price": 15},
        {"name": "Palitaw", "price": 15},
        {"name": "Brownies", "price": 35},
        {"name": "Cookies", "price": 35},
    ],
    "🍚 Rice Add-ons": [
        {"name": "1 Cup Rice", "price": 20},
        {"name": "Half Cup Rice", "price": 10},
    ],
    "🥤 Beverages": [
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
        {"name": "Kopiko Blanca", "price": 15},
    ],
}

# Category color mapping
CAT_COLORS = {
    "🍱 Main Dishes & Rice Meals": ("#fff3cd", "#856404"),
    "🥢 Noodles":                   ("#fde8d8", "#7c3100"),
    "🥟 Snacks & Dimsum":           ("#e8f4fd", "#0c4a6e"),
    "🍩 Sweets & Desserts":         ("#fce7f3", "#831843"),
    "🍚 Rice Add-ons":              ("#f0fdf4", "#14532d"),
    "🥤 Beverages":                  ("#ede9fe", "#3730a3"),
}

# ── OPTIMIZATION ENGINE ────────────────────────────────────────────────────────
def generate_exact_combinations(menu, max_budget, is_feast, total_needed=6):
    all_items = []
    for cat, items in menu.items():
        for item in items:
            all_items.append({"name": item["name"], "price": item["price"], "category": cat})

    usable_items = [i for i in all_items if i["price"] <= max_budget]
    if not usable_items:
        return []

    def is_valid_meal(combo):
        cats = [i["category"] for i in combo]
        has_rice = "🍚 Rice Add-ons" in cats
        has_ulam = (
            "🍱 Main Dishes & Rice Meals" in cats
            or "🥟 Snacks & Dimsum" in cats
            or "🥢 Noodles" in cats
        )
        if has_rice and not has_ulam:
            return False
        pure_addons = all(c in ["🍚 Rice Add-ons", "🥤 Beverages"] for c in cats)
        if pure_addons:
            return False
        return True

    valid_combos = []
    seen_sigs = set()
    iterations = 40000 if is_feast else 30000

    for _ in range(iterations):
        combo_size = None if is_feast else random.randint(2, 3)
        shuffled = usable_items.copy()
        random.shuffle(shuffled)

        current_combo, current_sum, seen_items = [], 0, set()
        for item in shuffled:
            if combo_size and len(current_combo) >= combo_size:
                break
            if (current_sum + item["price"] <= max_budget) and item["name"] not in seen_items:
                current_combo.append(item)
                current_sum += item["price"]
                seen_items.add(item["name"])

        if not current_combo:
            continue
        if combo_size and len(current_combo) < combo_size:
            continue
        if not is_valid_meal(current_combo):
            continue

        sig = frozenset(seen_items)
        if sig in seen_sigs:
            continue
        seen_sigs.add(sig)

        valid_combos.append({
            "items": current_combo,
            "total": current_sum,
            "change": max_budget - current_sum,
        })

    # Tipid = most change first; Feast = least change first (max spend)
    valid_combos.sort(key=lambda x: x["change"], reverse=not is_feast)
    return valid_combos[:total_needed]


# ── HELPERS ────────────────────────────────────────────────────────────────────
def cat_pill(cat):
    bg, fg = CAT_COLORS.get(cat, ("#f3f4f6", "#374151"))
    label = cat.split(" ", 1)[1] if " " in cat else cat
    return f'<span class="cat-pill" style="background:{bg};color:{fg}">{label}</span>'

def render_combo_card(idx, combo, budget, is_feast):
    change = combo["change"]
    pct_used = int((combo["total"] / budget) * 100)
    badge_cls = "badge-feast" if is_feast else "badge-savings"
    badge_txt = f"₱{change} change" if change > 0 else "Exact budget!"
    bar_width  = min(pct_used, 100)

    items_html = ""
    for it in combo["items"]:
        items_html += f"""
        <div class="item-row">
            <span>
                <span class="item-name">{it['name']}</span>
                {cat_pill(it['category'])}
            </span>
            <span class="item-price">₱{it['price']}</span>
        </div>"""

    change_cls  = "change-positive" if change > 0 else "change-zero"
    budget_note = f"₱{budget} budget"

    card = f"""
    <div class="combo-card">
        <div class="combo-header">
            <span class="combo-title">Option {idx}</span>
            <span class="badge {badge_cls}">{badge_txt}</span>
        </div>
        {items_html}
        <div class="budget-bar-wrap" title="{pct_used}% of budget used">
            <div class="budget-bar-fill" style="width:{bar_width}%"></div>
        </div>
        <div class="combo-footer">
            <div>
                <span class="total-label">Total &nbsp;</span>
                <span class="total-amount">₱{combo['total']}</span>
            </div>
            <div>
                <span class="total-label">Budget &nbsp;</span>
                <span class="total-amount">₱{budget}</span>
            </div>
            <div>
                <span class="total-label">Change &nbsp;</span>
                <span class="{change_cls}">₱{change}</span>
            </div>
        </div>
    </div>"""
    return card


# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🍔 Echo BudgetBites</h1>
    <p>AI Canteen Optimizer · Find your best meal for any budget · USTP Edition 🦅</p>
</div>
""", unsafe_allow_html=True)

# ── CONTROLS ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("**💵 Your budget (PHP ₱)**")
    budget_input = st.text_input(
        label="Budget",
        value="100",
        label_visibility="collapsed",
        placeholder="e.g. 150",
    )
    try:
        budget = int(budget_input.replace("₱", "").replace("PHP", "").strip())
        if budget <= 0:
            st.error("Enter a budget greater than ₱0.")
            budget = 0
    except ValueError:
        st.error("Numbers only — no letters or symbols.")
        budget = 0

    if budget > 0:
        cheapest = min(i["price"] for cat in menu_data.values() for i in cat)
        if budget < cheapest:
            st.warning(f"Minimum item price is ₱{cheapest}. Try a higher budget.")

with col2:
    st.markdown("**🍽️ Optimization strategy**")
    strategy = st.radio(
        "Strategy",
        options=[
            "💰 Tipid Mode — maximize savings",
            "🍖 Feast Mode — maximize volume",
        ],
        label_visibility="collapsed",
        help="Tipid keeps leftover change; Feast spends as much of your budget as possible.",
    )
    st.caption("Tipid = best value · Feast = most food for your money")

st.markdown("---")

# ── MENU REFERENCE (COLLAPSIBLE) ───────────────────────────────────────────────
with st.expander("📋 View full canteen menu & prices", expanded=False):
    tabs = st.tabs(list(menu_data.keys()))
    for idx, cat_name in enumerate(menu_data.keys()):
        with tabs[idx]:
            for item in menu_data[cat_name]:
                c1, c2 = st.columns([5, 1])
                c1.write(f"· {item['name']}")
                c2.markdown(f'<span class="menu-price">₱{item["price"]}</span>', unsafe_allow_html=True)

st.markdown("---")

# ── RUN BUTTON ─────────────────────────────────────────────────────────────────
run = st.button("🔥 Run Echo BudgetBites Optimizer", use_container_width=True, disabled=(budget == 0))

if run and budget > 0:
    is_feast = "Feast" in strategy

    with st.spinner("Crunching combinations…"):
        combos = generate_exact_combinations(menu_data, budget, is_feast, total_needed=6)

    if not combos:
        st.warning("No valid meal combinations found for this budget. Try raising it a little!")
    else:
        st.balloons()

        mode_label = "🍖 Feast Mode" if is_feast else "💰 Tipid Mode"
        st.markdown(
            f'<div class="section-header">{mode_label} · ₱{budget} budget · {len(combos)} options found</div>',
            unsafe_allow_html=True,
        )

        # Summary stats row
        totals   = [c["total"]  for c in combos]
        changes  = [c["change"] for c in combos]
        avg_spend = int(sum(totals) / len(totals))
        best_deal = min(changes) if is_feast else max(changes)

        s1, s2, s3 = st.columns(3)
        s1.metric("Options Generated",  len(combos))
        s2.metric("Avg Spend",         f"₱{avg_spend}")
        s3.metric("Best Change",       f"₱{best_deal}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Render combo cards
        for i, combo in enumerate(combos, start=1):
            st.markdown(render_combo_card(i, combo, budget, is_feast), unsafe_allow_html=True)

        # Footer tip
        st.markdown(
            "<div style='text-align:center;font-size:.8rem;color:#9ca3af;margin-top:1rem'>"
            "💡 Tip: Run again for different combinations — the engine randomizes each time."
            "</div>",
            unsafe_allow_html=True,
        )
