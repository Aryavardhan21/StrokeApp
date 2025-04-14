from preswald import text, selectbox, table, plotly, connect, get_df
import plotly.express as px
import pandas as pd

# Connect to dataset
connect()
df = get_df("stroke_data")

# Preprocess: replace unknowns and cast types
df = df[df['gender'] != 'Other']
df['bmi'] = pd.to_numeric(df['bmi'], errors='coerce')
df = df.dropna(subset=['bmi', 'avg_glucose_level'])

# Title
text("# 🧠 Stroke Risk Explorer")
text("Explore stroke risk factors and filter the data interactively.")

# --- FILTERS ---

gender = selectbox("Select Gender", options=["All"] + sorted(df["gender"].unique().tolist()))
work = selectbox("Select Work Type", options=["All"] + sorted(df["work_type"].unique().tolist()))
smoke = selectbox("Smoking Status", options=["All"] + sorted(df["smoking_status"].unique().tolist()))

# Apply filters
filtered_df = df.copy()
if gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == gender]
if work != "All":
    filtered_df = filtered_df[filtered_df["work_type"] == work]
if smoke != "All":
    filtered_df = filtered_df[filtered_df["smoking_status"] == smoke]

# --- TABLE VIEW ---
text("## 📋 Filtered Dataset View")
table(filtered_df.head(10))

# --- VISUALIZATIONS ---

# Stroke by Age Group
bins = [0, 20, 40, 60, 80, 120]
labels = ["0–20", "21–40", "41–60", "61–80", "81+"]
filtered_df["age_group"] = pd.cut(filtered_df["age"], bins=bins, labels=labels)

fig1 = px.bar(
    filtered_df.groupby("age_group")["stroke"].mean().reset_index(),
    x="age_group",
    y="stroke",
    title="🔢 Stroke Rate by Age Group",
    labels={"stroke": "Stroke Rate"}
)
plotly(fig1)

# Glucose vs BMI
fig2 = px.scatter(
    filtered_df,
    x="avg_glucose_level",
    y="bmi",
    color="stroke",
    hover_data=["age", "gender", "smoking_status"],
    title="🧬 Glucose Level vs. BMI (Colored by Stroke)"
)
plotly(fig2)
