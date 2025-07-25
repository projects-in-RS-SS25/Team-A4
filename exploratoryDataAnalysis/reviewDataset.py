import os
import pandas as pd
import matplotlib
from seaborn import heatmap, kdeplot, histplot
import matplotlib.pyplot as plt


matplotlib.use('TkAgg')
os.makedirs("figures", exist_ok=True)
reviews = pd.read_csv("../data/train.csv")


# Length of Positive vs. Negative Reviews
reviews["positive_length"] = reviews["review_positive"].astype(str).apply(len)
reviews["negative_length"] = reviews["review_negative"].astype(str).apply(len)
plt.figure(figsize=(8, 5))
kdeplot(reviews["positive_length"], label="Positive", fill=True)
kdeplot(reviews["negative_length"], label="Negative", fill=True)
plt.title("Distribution of Review Lengths (Positive vs Negative)")
plt.xlabel("Review Length (characters)")
plt.legend()
plt.tight_layout()
plt.savefig("figures/review_lengths.png")
plt.close()


# Distribution of Review Scores
plt.figure(figsize=(8, 5))
histplot(reviews["review_score"], bins=20, kde=True, color="teal")
plt.title("Distribution of Review Scores")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("figures/review_scores_distribution.png")
plt.close()


# Accommodation Preferences by Guest Type
guest_pref = pd.crosstab(reviews["guest_type"], reviews["accommodation_type"])
guest_pref_percent = guest_pref.div(guest_pref.sum(axis=1), axis=0)
plt.figure(figsize=(15, 8))
heatmap(guest_pref_percent, annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Accommodation Type Preferences by Guest Type")
plt.ylabel("Guest Type")
plt.xlabel("Accommodation Type")
plt.tight_layout()
plt.savefig("figures/guest_preferences_heatmap.png")
plt.close()


# Unique Accommodations per Country
accommodation_counts = reviews.groupby("accommodation_country")["accommodation_id"].nunique().reset_index()
accommodation_counts.columns = ["Country", "Number_of_Unique_Accommodations"]
accommodation_counts = accommodation_counts.sort_values(by="Number_of_Unique_Accommodations", ascending=False)
accommodation_counts.to_csv("figures/accommodation_counts_by_country.csv", index=False)



