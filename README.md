# CPC2015 Behavioral Data Pipeline

## Project Overview
The goal of this project is to use a real behavioral dataset to learn data loading, cleaning, exploratory data analysis (EDA), and statistical testing. The dataset comes from the Choice Prediction Competition 2015 (CPC2015), which studies human decision-making under risk and ambiguity. 

This project closely mirrors the typical workflow used when analyzing experimental behavioral data, serving as preparation for a behavioral decision-making internship.

## The Experiment
Participants repeatedly choose between two gambles: Option A and Option B. Researchers investigate how people make decisions when outcomes are risky, probabilities are ambiguous, and feedback is available or unavailable.

**Key Variables:**
* **Risk:** The most important behavioral variable. `Risk = 1` indicates Option B (the riskier option) was chosen, and `Risk = 0` indicates Option A was chosen.
* **Feedback:** Indicates whether outcome information was shown (`0` = No feedback, `1` = Outcome shown).
* **Ambiguity (Amb):** Indicates whether probabilities are known (`0` = Probabilities shown, `1` = Probabilities hidden or uncertain).
## Phase 1: The Feedback Effect (Current MVP)
The initial phase of this pipeline analyzes the `ByProb` experimental condition, where problems are played sequentially. Within every problem, Trials 1–5 are played with no feedback, while Trials 6–25 have feedback available. 

**The core question:** Do people change their behavior after receiving feedback? 

Using participant-level averages and a Paired T-test, this project statistically examines the shift in risk-taking behavior once outcomes are revealed. The results mathematically prove a significant change in human decision-making when feedback is introduced.

## Future Investigations
This pipeline is designed to be iteratively expanded. Upcoming analyses include:
* **The Ambiguity Effect:** Comparing risky choice rates between `Amb = 0` and `Amb = 1` to see if humans are naturally risk-averse when odds are hidden.
* **Demographic Differences:** Investigating if certain participants are more risk-seeking based on variables like age or gender.

## Tech Stack
* **Language:** Python
* **Libraries:** Pandas, Matplotlib, SciPy 
