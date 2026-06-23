import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

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
# STEP 2: STATISTICAL ANALYSIS (T-TEST)
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


# ==========================================
# STEP 3: THE COOL-DOWN EFFECT (Shock vs. Reality)
# ==========================================
print("\n--- MEASURING THE COOL-DOWN EFFECT ---")

# 1. Isolate the "Shock Phase" (Trials 6-10)
shock_trials = Probdf.query('Trial >= 6 and Trial <= 10')
shock_mean = shock_trials.groupby("SubjID")["Risk"].mean().to_frame()
shock_mean.rename(columns={"Risk": "Risk_Shock"}, inplace=True)

# 2. Isolate the "Cool-down Phase" (Trials 21-25)
cooldown_trials = Probdf.query('Trial >= 21 and Trial <= 25')
cooldown_mean = cooldown_trials.groupby("SubjID")["Risk"].mean().to_frame()
cooldown_mean.rename(columns={"Risk": "Risk_Cooldown"}, inplace=True)

# 3. Merge the datasets
cooldown_merged = pd.merge(shock_mean, cooldown_mean, on="SubjID", how="outer")

# Drop any blank rows just in case a participant skipped a trial
cooldown_merged.dropna(inplace=True)

# 4. Run the Paired T-Test
t_stat_cool, p_value_cool = stats.ttest_rel(cooldown_merged["Risk_Shock"], cooldown_merged["Risk_Cooldown"])

print(f"Cool-down T-statistic: {t_stat_cool:.4f}")
print(f"Cool-down P-value:     {p_value_cool:.5f}")

if p_value_cool < 0.05:
    print("\nConclusion: The cool-down decrease is statistically significant!")
    print("Participants naturally became less risky as they learned the true odds over time.")
else:
    print("\nConclusion: The cool-down decrease is NOT statistically significant.")

# ==========================================
# STEP 4: VISUALIZATION (EDA)
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

# Add asterisks to indicate statistical significance (p < 0.001) and non-significance
x_coordinates = [3, 3, 14, 14]
y_coordinates = [0.565, 0.568, 0.568, 0.565]
x2_coordinates= [7,7,23,23]
y2_coordinates= [0.560, 0.563, 0.563, 0.560]

# Draw the line connecting them
plt.plot(x_coordinates, y_coordinates, color='black')
plt.text(8.2,0.5683,"***")
plt.plot(x2_coordinates, y2_coordinates, color='black')
plt.text(15.05,0.564,"ns")

# Show trend line for the last 20 trials (Trials 6-25)
x_data = mean_risk_per_trial.index[5:]
y_data = mean_risk_per_trial.values[5:]

slope, intercept = np.polyfit(x_data, y_data, 1)
trendline_y = (slope * x_data) + intercept

plt.plot(x_data, trendline_y, color='darkred', linestyle='-', label='Cool-down Trend')
plt.legend()

# The code will pause here to show the graph.
plt.show() 
