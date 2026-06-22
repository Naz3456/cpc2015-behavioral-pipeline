import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# ==========================================
# STEP 1: DATA INGESTION & FILTERING
# ==========================================
print("Loading raw data...")
df = pd.read_csv('data/raw/RawDataExperiment1sorted.csv')

# Filter the dataset for the ByProb condition
# ByProb -> First 5 trials without feedback, remaining 20 with feedback
Probdf = df[df["Condition"] == "ByProb"].copy()

print(f"Total ByProb trials isolated: {len(Probdf)}")

# ==========================================
# STEP 2: VISUALIZATION (EDA)
# ==========================================
print("\nGenerating graph...")

# Calculate the mean of risky choices for each trial
mean_risk_per_trial = Probdf.groupby("Trial")["Risk"].mean()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(mean_risk_per_trial.index, mean_risk_per_trial.values, marker="o", color="#2ca02c")

# Pro-Tip: Add a vertical line to show exactly where feedback begins
plt.axvline(x=5.5, color='red', linestyle='--', label='Feedback Starts')

plt.xlabel("Trials")
plt.ylabel("Risky option chosen ratio")
plt.title("Risk-Taking Behavior: Before vs. After Feedback")
plt.legend()

# The code will pause here to show the graph. Close the graph window to let the code finish!
plt.show() 

# ==========================================
# STEP 3: STATISTICAL ANALYSIS (T-TEST)
# ==========================================
print("\nCalculating statistics...")

# Split into No Feedback (Trials 1-5) and Feedback (Trials 6-25)
first5 = Probdf.query('Trial <= 5')
last20 = Probdf.query('Trial > 5')

# Calculate the mean risk taking for each Subject ID
noFB = first5.groupby("SubjID")["Risk"].mean().to_frame()
noFB.rename(columns={"Risk": "Risk_noFB"}, inplace=True)

wFB = last20.groupby("SubjID")["Risk"].mean().to_frame()
wFB.rename(columns={"Risk": "Risk_FB"}, inplace=True)

# Merge the two averages together side-by-side
merged = pd.merge(noFB, wFB, on="SubjID", how="outer")

# Run the Paired T-Test
t_stat, p_value = stats.ttest_rel(merged["Risk_noFB"], merged["Risk_FB"])

print("\n--- FINAL RESULTS ---")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value:     {p_value:.5f}")

if p_value < 0.05:
    print("\nConclusion: The difference in risk-taking is statistically significant!")
    print("Participants genuinely changed their behavior after receiving feedback.")
else:
    print("\nConclusion: The difference is NOT statistically significant.")