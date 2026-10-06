import streamlit as st
import ollama
import sqlite3
import re

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Colorful Shopping Store",
    page_icon="🛍️",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #fff0f6, #eef7ff, #f3e8ff);
}

/* Main title */
.title-box {
    background: linear-gradient(
        90deg,
        #ff0080,
        #7928ca,
        #2afadf,
        #00c6ff
    );
    padding: 30px;
    border-radius: 25px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0px 8px 25px rgba(121, 40, 202, 0.30);
}

.title-box h1 {
    color: white;
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 8px;
}

.title-box p {
    color: white;
    font-size: 19px;
}

/* Section headings */
.section-title {
    background: linear-gradient(90deg, #ff0080, #7928ca);
    color: white;
    padding: 12px 20px;
    border-radius: 15px;
    font-size: 25px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 18px;
}

/* Product cards */
.product-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.12);
    margin-bottom: 20px;
    border: 3px solid transparent;
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 10px 30px rgba(121,40,202,0.25);
}

/* Male cards */
.male-card {
    border-color: #2196f3;
    background: linear-gradient(180deg, #e3f2fd, #ffffff);
}

/* Female cards */
.female-card {
    border-color: #ff4081;
    background: linear-gradient(180deg, #fce4ec, #ffffff);
}

/* Dashboard */
.dashboard-card {
    padding: 20px;
    border-radius: 18px;
    color: white;
    text-align: center;
    font-weight: bold;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.15);
}

.blue-card {
    background: linear-gradient(135deg, #2196f3, #21cbf3);
}

.pink-card {
    background: linear-gradient(135deg, #ff4081, #ff80ab);
}

.purple-card {
    background: linear-gradient(135deg, #7b1fa2, #ba68c8);
}

.green-card {
    background: linear-gradient(135deg, #00b09b, #96c93d);
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    font-weight: bold;
    border: none;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff0f6, #e3f2fd);
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# TITLE
# =====================================================

st.markdown("""
<div class="title-box">
    <h1>🛍️ AI Colorful Shopping Store</h1>
    <p>👨 Male • 👩 Female • 👕 Fashion • 👟 Footwear • 👜 Accessories • 💄 Beauty</p>
    <p>Ask your shopping question in English and get SQL results using AI 🤖</p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = sqlite3.connect("shopping.db")
cursor = conn.cursor()


# =====================================================
# CREATE TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS shopping (
    id INTEGER PRIMARY KEY,
    product_name TEXT,
    gender TEXT,
    category TEXT,
    price INTEGER,
    quantity INTEGER
)
""")


# =====================================================
# SAMPLE PRODUCTS
# =====================================================

products = [

    # ---------------- MALE PRODUCTS ----------------

    (1, "Men's T-Shirt", "Male", "Clothing", 799, 30),
    (2, "Men's Shirt", "Male", "Clothing", 1299, 25),
    (3, "Men's Jeans", "Male", "Clothing", 1799, 20),
    (4, "Men's Jacket", "Male", "Clothing", 2499, 15),

    (5, "Men's Sneakers", "Male", "Footwear", 1999, 20),
    (6, "Men's Formal Shoes", "Male", "Footwear", 2299, 18),
    (7, "Men's Sports Shoes", "Male", "Footwear", 2499, 15),

    (8, "Men's Watch", "Male", "Accessories", 2999, 12),
    (9, "Men's Wallet", "Male", "Accessories", 999, 25),
    (10, "Men's Sunglasses", "Male", "Accessories", 1499, 18),

    # ---------------- FEMALE PRODUCTS ----------------

    (11, "Women's Top", "Female", "Clothing", 899, 30),
    (12, "Women's Kurti", "Female", "Clothing", 1499, 25),
    (13, "Women's Jeans", "Female", "Clothing", 1699, 20),
    (14, "Women's Dress", "Female", "Clothing", 2199, 15),

    (15, "Women's Sneakers", "Female", "Footwear", 1899, 20),
    (16, "Women's Heels", "Female", "Footwear", 2299, 18),
    (17, "Women's Sandals", "Female", "Footwear", 999, 25),

    (18, "Women's Handbag", "Female", "Accessories", 2499, 15),
    (19, "Women's Watch", "Female", "Accessories", 2799, 12),
    (20, "Women's Sunglasses", "Female", "Accessories", 1299, 20),

    (21, "Lipstick", "Female", "Beauty", 599, 30),
    (22, "Face Cream", "Female", "Beauty", 799, 25),
    (23, "Perfume", "Female", "Beauty", 1499, 20),

    # ---------------- COMMON PRODUCTS ----------------

    (24, "Laptop", "Unisex", "Electronics", 50000, 10),
    (25, "Mobile Phone", "Unisex", "Electronics", 20000, 15),
    (26, "Headphones", "Unisex", "Electronics", 2000, 25)
]


# =====================================================
# INSERT PRODUCTS
# =====================================================

for product in products:

    cursor.execute("""
    INSERT OR IGNORE INTO shopping
    (id, product_name, gender, category, price, quantity)
    VALUES (?, ?, ?, ?, ?, ?)
    """, product)

conn.commit()


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("🛍️ Shopping Menu")

    st.markdown("""
    ### 👨 Male
    👕 Clothing  
    👟 Footwear  
    ⌚ Accessories  

    ### 👩 Female
    👗 Clothing  
    👠 Footwear  
    👜 Accessories  
    💄 Beauty  

    ### 🌈 Common
    💻 Electronics
    """)

    st.divider()

    st.subheader("💡 Example Questions")

    example = st.selectbox(
        "Choose a question",
        [
            "Show all products",
            "Show all male products",
            "Show all female products",
            "Show male clothing products",
            "Show female clothing products",
            "Show male footwear products",
            "Show female footwear products",
            "Show female beauty products",
            "Show products below 2000",
            "Show products above 1000",
            "Show the most expensive product",
            "Show the cheapest product",
            "Show products with quantity greater than 20",
            "Show product names and prices"
        ]
    )


# =====================================================
# DATABASE STATISTICS
# =====================================================

cursor.execute("SELECT COUNT(*) FROM shopping")
total_products = cursor.fetchone()[0]

cursor.execute("SELECT SUM(quantity) FROM shopping")
total_quantity = cursor.fetchone()[0]

cursor.execute("SELECT MAX(price) FROM shopping")
highest_price = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM shopping WHERE gender='Male'"
)
male_products = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM shopping WHERE gender='Female'"
)
female_products = cursor.fetchone()[0]


# =====================================================
# DASHBOARD
# =====================================================

st.markdown(
    '<div class="section-title">📊 Shopping Dashboard</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(
        f"""
        <div class="dashboard-card blue-card">
            🛍️<br>
            Total Products<br>
            <h2>{total_products}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class="dashboard-card blue-card">
            👨<br>
            Male Products<br>
            <h2>{male_products}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""
        <div class="dashboard-card pink-card">
            👩<br>
            Female Products<br>
            <h2>{female_products}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:

    st.markdown(
        f"""
        <div class="dashboard-card purple-card">
            💰<br>
            Highest Price<br>
            <h2>₹{highest_price:,}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# PRODUCT DISPLAY
# =====================================================

st.markdown(
    '<div class="section-title">👨 Male Products</div>',
    unsafe_allow_html=True
)

cursor.execute("""
SELECT product_name, category, price, quantity
FROM shopping
WHERE gender='Male'
""")

male_data = cursor.fetchall()

cols = st.columns(4)

for i, product in enumerate(male_data):

    name, category, price, quantity = product

    with cols[i % 4]:

        st.markdown(
            f"""
            <div class="product-card male-card">

                <h2>👨</h2>

                <h3>{name}</h3>

                <p>📂 {category}</p>

                <h2>₹{price:,}</h2>

                <p>📦 Stock: {quantity}</p>

            </div>
            """,
            unsafe_allow_html=True
        )


# =====================================================
# FEMALE PRODUCTS
# =====================================================

st.markdown(
    '<div class="section-title">👩 Female Products</div>',
    unsafe_allow_html=True
)

cursor.execute("""
SELECT product_name, category, price, quantity
FROM shopping
WHERE gender='Female'
""")

female_data = cursor.fetchall()

cols = st.columns(4)

for i, product in enumerate(female_data):

    name, category, price, quantity = product

    with cols[i % 4]:

        st.markdown(
            f"""
            <div class="product-card female-card">

                <h2>👩</h2>

                <h3>{name}</h3>

                <p>📂 {category}</p>

                <h2>₹{price:,}</h2>

                <p>📦 Stock: {quantity}</p>

            </div>
            """,
            unsafe_allow_html=True
        )


# =====================================================
# COMMON PRODUCTS
# =====================================================

st.markdown(
    '<div class="section-title">🌈 Common Products</div>',
    unsafe_allow_html=True
)

cursor.execute("""
SELECT product_name, category, price, quantity
FROM shopping
WHERE gender='Unisex'
""")

common_data = cursor.fetchall()

cols = st.columns(3)

for i, product in enumerate(common_data):

    name, category, price, quantity = product

    with cols[i % 3]:

        st.markdown(
            f"""
            <div class="product-card">

                <h2>🛍️</h2>

                <h3>{name}</h3>

                <p>📂 {category}</p>

                <h2>₹{price:,}</h2>

                <p>📦 Stock: {quantity}</p>

            </div>
            """,
            unsafe_allow_html=True
        )


# =====================================================
# QUESTION INPUT
# =====================================================

st.markdown(
    '<div class="section-title">🔎 Ask Your Shopping Question</div>',
    unsafe_allow_html=True
)

question = st.text_input(
    "Enter your question:",
    value=example,
    placeholder="Example: Show female products below 2000"
)


# =====================================================
# BUTTONS
# =====================================================

col1, col2 = st.columns(2)

with col1:

    generate = st.button(
        "🚀 Generate SQL",
        use_container_width=True
    )

with col2:

    clear = st.button(
        "🧹 Clear",
        use_container_width=True
    )


if clear:
    st.rerun()


# =====================================================
# GENERATE SQL
# =====================================================

if generate:

    if not question.strip():

        st.warning("⚠️ Please enter a question.")

    else:

        try:

            # =================================================
            # OLLAMA
            # =================================================

            with st.spinner("🤖 AI is generating SQL..."):

                response = ollama.chat(

                    model="llama3.2:3b",

                    messages=[

                        {
                            "role": "system",

                            "content": """
You are an SQL generator.

Database table:
shopping

Columns:
id,
product_name,
gender,
category,
price,
quantity

Gender values:
Male,
Female,
Unisex

Categories:
Clothing,
Footwear,
Accessories,
Beauty,
Electronics

Convert the user's question into SQLite SQL.

Rules:
1. Return ONLY one SELECT query.
2. Do not give explanations.
3. Do not use markdown.
4. Do not use ```sql.
5. Do not write any text before or after the SQL.
6. Use only the shopping table.
7. You can filter using gender.
8. You can filter using category.
"""
                        },

                        {
                            "role": "user",
                            "content": question
                        }

                    ]
                )


            # =================================================
            # GET SQL
            # =================================================

            sql_query = response["message"]["content"].strip()


            # Remove markdown

            sql_query = re.sub(
                r"```sql\s*",
                "",
                sql_query,
                flags=re.IGNORECASE
            )

            sql_query = re.sub(
                r"```",
                "",
                sql_query
            )

            sql_query = sql_query.strip()


            # =================================================
            # EXTRACT SELECT QUERY
            # =================================================

            match = re.search(
                r"SELECT\s+.*?(?:;|$)",
                sql_query,
                flags=re.IGNORECASE | re.DOTALL
            )


            if not match:

                st.error(
                    "❌ Ollama did not generate a valid SQL query."
                )

            else:

                sql_query = match.group(0).strip()


                # =================================================
                # SECURITY CHECK
                # =================================================

                if not sql_query.upper().startswith("SELECT"):

                    st.error(
                        "❌ Only SELECT queries are allowed."
                    )

                else:

                    # =================================================
                    # GENERATED SQL
                    # =================================================

                    st.markdown(
                        '<div class="section-title">💻 Generated SQL</div>',
                        unsafe_allow_html=True
                    )

                    st.code(
                        sql_query,
                        language="sql"
                    )


                    # =================================================
                    # EXECUTE SQL
                    # =================================================

                    cursor.execute(sql_query)

                    result = cursor.fetchall()


                    # =================================================
                    # RESULT
                    # =================================================

                    st.markdown(
                        '<div class="section-title">🛒 Shopping Result</div>',
                        unsafe_allow_html=True
                    )


                    if result:

                        st.success(
                            f"✅ {len(result)} record(s) found!"
                        )

                        st.dataframe(
                            result,
                            use_container_width=True
                        )

                    else:

                        st.info(
                            "ℹ️ No products found."
                        )


        except ollama.ResponseError as e:

            st.error(
                f"🤖 Ollama Error: {e}"
            )

        except sqlite3.Error as e:

            st.error(
                f"🗄️ SQLite Error: {e}"
            )

        except Exception as e:

            st.error(
                f"❌ Error: {e}"
            )


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; padding:20px;">

    <h3>🛍️ AI Colorful Shopping Store</h3>

    <p>
    👨 Male Products |
    👩 Female Products |
    👕 Fashion |
    👟 Footwear |
    👜 Accessories |
    💄 Beauty |
    🤖 AI SQL
    </p>

    <p>✨ Smart Shopping with Natural Language ✨</p>

    </div>
    """,
    unsafe_allow_html=True
)