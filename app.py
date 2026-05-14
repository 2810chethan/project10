import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_oauth import OAuth2Component

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- GOOGLE LOGIN ----------------
CLIENT_ID = st.secrets["google"]["client_id"]
CLIENT_SECRET = st.secrets["google"]["client_secret"]

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REFRESH_TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_TOKEN_URL = "https://oauth2.googleapis.com/revoke"

oauth2 = OAuth2Component(
    CLIENT_ID,
    CLIENT_SECRET,
    AUTHORIZE_URL,
    TOKEN_URL,
    REFRESH_TOKEN_URL,
    REVOKE_TOKEN_URL,
)

# Redirect URI
REDIRECT_URI = st.secrets["google"]["redirect_uri"]

# Login Button
result = oauth2.authorize_button(
    name="Login with Google",
    redirect_uri=REDIRECT_URI,
    scope="openid email profile",
    key="google",
)

# ---------------- LOGIN SUCCESS ----------------
if result and "token" in result:

    st.success("Login Successful ✅")

    st.title("📊 Analytics Dashboard")

    # ---------------- RANDOM DATASET ----------------
    np.random.seed(42)

    data = pd.DataFrame({
        "Category": np.random.choice(
            ["Electronics", "Fashion", "Food", "Sports"],
            200
        ),
        "Sales": np.random.randint(1000, 10000, 200),
        "Profit": np.random.randint(100, 3000, 200),
        "Region": np.random.choice(
            ["North", "South", "East", "West"],
            200
        )
    })

    # ---------------- SIDEBAR FILTER ----------------
    st.sidebar.header("Filters")

    selected_region = st.sidebar.multiselect(
        "Select Region",
        options=data["Region"].unique(),
        default=data["Region"].unique()
    )

    filtered_data = data[data["Region"].isin(selected_region)]

    # ---------------- KPI CARDS ----------------
    total_sales = filtered_data["Sales"].sum()
    total_profit = filtered_data["Profit"].sum()
    avg_sales = filtered_data["Sales"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", f"₹{total_sales:,.0f}")
    col2.metric("Total Profit", f"₹{total_profit:,.0f}")
    col3.metric("Average Sales", f"₹{avg_sales:,.0f}")

    st.divider()

    # ---------------- CHARTS ----------------
    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Sales by Category")

        category_sales = (
            filtered_data.groupby("Category")["Sales"]
            .sum()
            .reset_index()
        )

        fig1 = px.bar(
            category_sales,
            x="Category",
            y="Sales",
            title="Category Sales"
        )

        st.plotly_chart(fig1, use_container_width=True)

    with col5:
        st.subheader("Profit Distribution")

        fig2 = px.pie(
            filtered_data,
            names="Region",
            values="Profit",
            title="Region Wise Profit"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # ---------------- DATA TABLE ----------------
    st.subheader("Dataset Preview")

    st.dataframe(filtered_data, use_container_width=True)

else:
    st.title("🔐 Google Login Required")
    st.info("Please login using Google to access dashboard.")