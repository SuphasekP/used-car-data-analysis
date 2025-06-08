# ----------------------
# 1. Import Libraries
# ----------------------
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ตั้งค่ารูปแบบกราฟ
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)

# ----------------------
# 2. Load Data
# ----------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_used_cars.csv")
    return df

df = load_data()

# ----------------------
# 3. Sidebar Filters
# ----------------------
st.sidebar.title("🔍 Filter Options")

manufacturers = st.sidebar.multiselect(
    "Select Manufacturer(s):", options=sorted(df['manufacturer'].dropna().unique()), default=None
)

years = st.sidebar.slider(
    "Select Year Range:", int(df['year'].min()), int(df['year'].max()),
    (int(df['year'].min()), int(df['year'].max()))
)

# Filter Data
filtered_df = df.copy()
if manufacturers:
    filtered_df = filtered_df[filtered_df['manufacturer'].isin(manufacturers)]
filtered_df = filtered_df[(filtered_df['year'] >= years[0]) & (filtered_df['year'] <= years[1])]

# ----------------------
# 4. Dashboard Header
# ----------------------
st.title("🚗 Used Car Data Dashboard")
st.markdown("Explore the pricing trends and distribution of used cars in the market.")

# ----------------------
# 5. KPIs Section
# ----------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Cars", f"{len(filtered_df):,}")
col2.metric("Average Price", f"${filtered_df['price'].mean():,.0f}")
col3.metric("Avg. Mileage", f"{filtered_df['odometer'].mean():,.0f} mi")

# ----------------------
# 6. Visualization Section
# ----------------------

# 6.1 Price Distribution
st.subheader("Price Distribution")
fig1, ax1 = plt.subplots()
sns.histplot(filtered_df['price'], bins=50, kde=True, ax=ax1)
ax1.set_xlim(0, 100000)
st.pyplot(fig1)

# 6.2 Average Price by Manufacturer
st.subheader("Average Price by Manufacturer")
avg_price_man = filtered_df.groupby('manufacturer')['price'].mean().sort_values(ascending=False).head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=avg_price_man.values, y=avg_price_man.index, ax=ax2)
ax2.set_xlabel("Average Price ($)")
st.pyplot(fig2)

# 6.3 Price by Year
st.subheader("Price by Year")
fig3, ax3 = plt.subplots()
sns.boxplot(data=filtered_df, x='year', y='price', ax=ax3)
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45)
ax3.set_ylim(0, 100000)
st.pyplot(fig3)

# 6.4 Odometer vs Price
st.subheader("Mileage vs Price")
fig4, ax4 = plt.subplots()
sns.scatterplot(data=filtered_df, x='odometer', y='price', alpha=0.4, ax=ax4)
ax4.set_xlim(0, filtered_df['odometer'].max())
ax4.set_ylim(0, 100000)
st.pyplot(fig4)
