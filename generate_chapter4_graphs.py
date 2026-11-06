import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# CHAPTER FOUR — OFFICIAL RESULTS GRAPH GENERATION
# ============================================================

FILE = "FINAL_3000_VALIDATION_NEW_FALSE_CONFIDENCE.csv"
OUTPUT_DIR = Path("CHAPTER4_GRAPHS")

OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(FILE)

print("=" * 70)
print("CHAPTER FOUR OFFICIAL GRAPH GENERATION")
print("=" * 70)
print(f"Total passwords: {len(df):,}")
print()

# ============================================================
# FIGURE 4.1 — TRADITIONAL PASSWORD STRENGTH
# ============================================================

traditional_order = ["Weak", "Medium", "Strong"]

traditional_counts = (
    df["traditional_strength"]
    .value_counts()
    .reindex(traditional_order, fill_value=0)
)

plt.figure(figsize=(8, 6))
plt.bar(traditional_counts.index, traditional_counts.values)

plt.title("Traditional Password Strength Distribution")
plt.xlabel("Traditional Password Strength")
plt.ylabel("Number of Passwords")

for i, value in enumerate(traditional_counts.values):
    plt.text(i, value + 30, f"{value:,}", ha="center")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "Figure_4_1_Traditional_Password_Strength.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("Figure 4.1 saved.")


# ============================================================
# FIGURE 4.2 — CDR PREDICTABILITY RISK
# ============================================================

cdr_order = [
    "Low Predictability Risk",
    "Moderate Predictability Risk",
    "High Predictability Risk",
    "Very High Predictability Risk"
]

cdr_counts = (
    df["cdr_class"]
    .value_counts()
    .reindex(cdr_order, fill_value=0)
)

plt.figure(figsize=(9, 6))
plt.bar(
    ["Low", "Moderate", "High", "Very High"],
    cdr_counts.values
)

plt.title("CDR Predictability Risk Classification")
plt.xlabel("Predictability Risk Class")
plt.ylabel("Number of Passwords")

for i, value in enumerate(cdr_counts.values):
    plt.text(i, value + 25, f"{value:,}", ha="center")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "Figure_4_2_CDR_Predictability_Risk.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("Figure 4.2 saved.")


# ============================================================
# FIGURE 4.3 — CRACK-DIFFICULTY CLASSIFICATION
# ============================================================

crack_order = ["Easy", "Moderate", "Difficult"]

crack_counts = (
    df["crack_class"]
    .value_counts()
    .reindex(crack_order, fill_value=0)
)

plt.figure(figsize=(8, 6))
plt.bar(crack_counts.index, crack_counts.values)

plt.title("Crack-Difficulty Classification")
plt.xlabel("Crack-Difficulty Class")
plt.ylabel("Number of Passwords")

for i, value in enumerate(crack_counts.values):
    plt.text(i, value + 30, f"{value:,}", ha="center")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "Figure_4_3_Crack_Difficulty_Classification.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("Figure 4.3 saved.")


# ============================================================
# FIGURE 4.4 — FALSE-CONFIDENCE VS REMAINING
# ============================================================

false_confidence_count = int(df["false_confidence_new"].sum())
remaining_count = len(df) - false_confidence_count

fc_labels = ["False-Confidence", "Remaining"]
fc_values = [false_confidence_count, remaining_count]

plt.figure(figsize=(8, 6))
plt.bar(fc_labels, fc_values)

plt.title("False-Confidence and Remaining Passwords")
plt.xlabel("Password Group")
plt.ylabel("Number of Passwords")

for i, value in enumerate(fc_values):
    plt.text(i, value + 30, f"{value:,}", ha="center")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "Figure_4_4_False_Confidence_Distribution.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("Figure 4.4 saved.")


# ============================================================
# FIGURE 4.5 — MEAN CDR SCORE COMPARISON
# ============================================================

fc_cdr_mean = df.loc[
    df["false_confidence_new"] == True,
    "cdr_score"
].mean()

remaining_cdr_mean = df.loc[
    df["false_confidence_new"] == False,
    "cdr_score"
].mean()

cdr_group_labels = ["False-Confidence", "Remaining"]
cdr_group_values = [fc_cdr_mean, remaining_cdr_mean]

plt.figure(figsize=(8, 6))
plt.bar(cdr_group_labels, cdr_group_values)

plt.title("Mean CDR Score by Password Group")
plt.xlabel("Password Group")
plt.ylabel("Mean CDR Score")

for i, value in enumerate(cdr_group_values):
    plt.text(i, value + 0.01, f"{value:.4f}", ha="center")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "Figure_4_5_Mean_CDR_Score.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("Figure 4.5 saved.")


# ============================================================
# FIGURE 4.6 — MEAN CRACK-DIFFICULTY SCORE COMPARISON
# ============================================================

fc_crack_mean = df.loc[
    df["false_confidence_new"] == True,
    "crack_score"
].mean()

remaining_crack_mean = df.loc[
    df["false_confidence_new"] == False,
    "crack_score"
].mean()

crack_group_labels = ["False-Confidence", "Remaining"]
crack_group_values = [fc_crack_mean, remaining_crack_mean]

plt.figure(figsize=(8, 6))
plt.bar(crack_group_labels, crack_group_values)

plt.title("Mean Crack-Difficulty Score by Password Group")
plt.xlabel("Password Group")
plt.ylabel("Mean Crack-Difficulty Score")

for i, value in enumerate(crack_group_values):
    plt.text(
        i,
        value + (0.15 if value >= 0 else -0.25),
        f"{value:.4f}",
        ha="center"
    )

plt.axhline(0, linewidth=0.8)

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "Figure_4_6_Mean_Crack_Difficulty_Score.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("Figure 4.6 saved.")


# ============================================================
# FINAL VERIFICATION
# ============================================================

print()
print("=" * 70)
print("GRAPH GENERATION COMPLETED")
print("=" * 70)

print(f"False-Confidence cases: {false_confidence_count}")
print(f"Remaining passwords: {remaining_count}")

print(f"Mean CDR — False-Confidence: {fc_cdr_mean:.6f}")
print(f"Mean CDR — Remaining: {remaining_cdr_mean:.6f}")

print(f"Mean Crack Score — False-Confidence: {fc_crack_mean:.6f}")
print(f"Mean Crack Score — Remaining: {remaining_crack_mean:.6f}")

print()
print(f"Graphs saved in: {OUTPUT_DIR.resolve()}")
print("=" * 70)
