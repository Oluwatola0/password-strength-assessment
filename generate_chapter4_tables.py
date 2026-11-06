import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# ============================================================
# LOAD FINAL VALIDATION DATASET
# ============================================================

FILE = r"C:\Users\STARGIRL\Documents\Password strength_Project\FINAL_3000_VALIDATION_NEW_FALSE_CONFIDENCE.csv"

df = pd.read_csv(FILE)

print("=" * 70)
print("FINAL CHAPTER FOUR RESULTS TABLE GENERATION")
print("=" * 70)

print(f"\nTotal passwords: {len(df):,}")

# ============================================================
# 1. DATASET COMPOSITION
# ============================================================

dataset_table = pd.DataFrame({
    "Dataset Component": [
        "RockYou Passwords",
        "Researcher-Generated Passwords",
        "Total"
    ],
    "Number of Passwords": [
        2500,
        500,
        len(df)
    ]
})

dataset_table["Percentage (%)"] = (
    dataset_table["Number of Passwords"] / len(df) * 100
).round(2)

print("\nTABLE 4.1 — DATASET COMPOSITION")
print(dataset_table.to_string(index=False))


# ============================================================
# 2. TRADITIONAL PASSWORD STRENGTH
# ============================================================

traditional_order = ["Weak", "Medium", "Strong"]

traditional_counts = (
    df["traditional_strength"]
    .value_counts()
    .reindex(traditional_order, fill_value=0)
)

traditional_table = pd.DataFrame({
    "Traditional Strength": traditional_counts.index,
    "Number of Passwords": traditional_counts.values,
    "Percentage (%)": (
        traditional_counts.values / len(df) * 100
    ).round(2)
})

print("\nTABLE 4.2 — TRADITIONAL PASSWORD STRENGTH")
print(traditional_table.to_string(index=False))


# ============================================================
# 3. CDR CLASSIFICATION
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

cdr_table = pd.DataFrame({
    "CDR Risk Class": cdr_counts.index,
    "Number of Passwords": cdr_counts.values,
    "Percentage (%)": (
        cdr_counts.values / len(df) * 100
    ).round(2)
})

print("\nTABLE 4.3 — CDR PREDICTABILITY RISK CLASSIFICATION")
print(cdr_table.to_string(index=False))


# ============================================================
# 4. CRACK-DIFFICULTY CLASSIFICATION
# ============================================================

crack_order = ["Easy", "Moderate", "Difficult"]

crack_counts = (
    df["crack_class"]
    .value_counts()
    .reindex(crack_order, fill_value=0)
)

crack_table = pd.DataFrame({
    "Crack-Difficulty Class": crack_counts.index,
    "Number of Passwords": crack_counts.values,
    "Percentage (%)": (
        crack_counts.values / len(df) * 100
    ).round(2)
})

print("\nTABLE 4.4 — CRACK-DIFFICULTY CLASSIFICATION")
print(crack_table.to_string(index=False))


# ============================================================
# 5. FALSE-CONFIDENCE RESULTS
# ============================================================

fc_count = df["false_confidence_new"].sum()
non_fc_count = len(df) - fc_count
fcr = fc_count / len(df) * 100

false_confidence_table = pd.DataFrame({
    "Group": [
        "False-Confidence Passwords",
        "Remaining Passwords",
        "Total"
    ],
    "Number of Passwords": [
        fc_count,
        non_fc_count,
        len(df)
    ],
    "Percentage (%)": [
        round(fc_count / len(df) * 100, 2),
        round(non_fc_count / len(df) * 100, 2),
        100.00
    ]
})

print("\nTABLE 4.5 — FALSE-CONFIDENCE RESULTS")
print(false_confidence_table.to_string(index=False))

print(f"\nFalse-Confidence Rate (FCR): {fcr:.2f}%")


# ============================================================
# 6. CDR DESCRIPTIVE STATISTICS
# ============================================================

cdr_stats = df["cdr_score"].describe()

cdr_stats_table = pd.DataFrame({
    "Statistic": [
        "Count",
        "Mean",
        "Standard Deviation",
        "Minimum",
        "25th Percentile",
        "Median",
        "75th Percentile",
        "Maximum"
    ],
    "CDR Score": [
        cdr_stats["count"],
        cdr_stats["mean"],
        df["cdr_score"].std(),
        cdr_stats["min"],
        cdr_stats["25%"],
        cdr_stats["50%"],
        cdr_stats["75%"],
        cdr_stats["max"]
    ]
})

cdr_stats_table["CDR Score"] = cdr_stats_table["CDR Score"].round(6)

print("\nTABLE 4.6 — DESCRIPTIVE STATISTICS OF CDR SCORE")
print(cdr_stats_table.to_string(index=False))


# ============================================================
# 7. CRACK-DIFFICULTY SCORE DESCRIPTIVE STATISTICS
# ============================================================

crack_stats = df["crack_score"].describe()

crack_stats_table = pd.DataFrame({
    "Statistic": [
        "Count",
        "Mean",
        "Standard Deviation",
        "Minimum",
        "25th Percentile",
        "Median",
        "75th Percentile",
        "Maximum"
    ],
    "Crack-Difficulty Score": [
        crack_stats["count"],
        crack_stats["mean"],
        df["crack_score"].std(),
        crack_stats["min"],
        crack_stats["25%"],
        crack_stats["50%"],
        crack_stats["75%"],
        crack_stats["max"]
    ]
})

crack_stats_table["Crack-Difficulty Score"] = (
    crack_stats_table["Crack-Difficulty Score"].round(6)
)

print("\nTABLE 4.7 — DESCRIPTIVE STATISTICS OF CRACK-DIFFICULTY SCORE")
print(crack_stats_table.to_string(index=False))


# ============================================================
# 8. FALSE-CONFIDENCE VS REMAINING PASSWORDS
# ============================================================

fc = df[df["false_confidence_new"] == True]
remaining = df[df["false_confidence_new"] == False]

comparison_table = pd.DataFrame({
    "Group": [
        "False-Confidence",
        "Remaining Passwords"
    ],
    "N": [
        len(fc),
        len(remaining)
    ],
    "Mean CDR Score": [
        fc["cdr_score"].mean(),
        remaining["cdr_score"].mean()
    ],
    "SD CDR Score": [
        fc["cdr_score"].std(),
        remaining["cdr_score"].std()
    ],
    "Mean Crack-Difficulty Score": [
        fc["crack_score"].mean(),
        remaining["crack_score"].mean()
    ],
    "SD Crack-Difficulty Score": [
        fc["crack_score"].std(),
        remaining["crack_score"].std()
    ]
})

numeric_columns = comparison_table.columns[2:]
comparison_table[numeric_columns] = comparison_table[numeric_columns].round(6)

print("\nTABLE 4.8 — FALSE-CONFIDENCE VS REMAINING PASSWORDS")
print(comparison_table.to_string(index=False))


# ============================================================
# 9. WELCH'S T-TEST
# ============================================================

cdr_test = ttest_ind(
    fc["cdr_score"],
    remaining["cdr_score"],
    equal_var=False
)

crack_test = ttest_ind(
    fc["crack_score"],
    remaining["crack_score"],
    equal_var=False
)

statistical_table = pd.DataFrame({
    "Measure": [
        "CDR Risk Score",
        "Crack-Difficulty Score"
    ],
    "False-Confidence Mean": [
        fc["cdr_score"].mean(),
        fc["crack_score"].mean()
    ],
    "Remaining Mean": [
        remaining["cdr_score"].mean(),
        remaining["crack_score"].mean()
    ],
    "t-statistic": [
        cdr_test.statistic,
        crack_test.statistic
    ],
    "p-value": [
        cdr_test.pvalue,
        crack_test.pvalue
    ],
    "Significance": [
        "Significant" if cdr_test.pvalue < 0.05 else "Not Significant",
        "Significant" if crack_test.pvalue < 0.05 else "Not Significant"
    ]
})

statistical_table.iloc[:, 1:5] = statistical_table.iloc[:, 1:5].round(6)

print("\nTABLE 4.9 — WELCH'S INDEPENDENT TWO-SAMPLE T-TEST")
print(statistical_table.to_string(index=False))


# ============================================================
# 10. PREDICTABILITY INDICATORS
# ============================================================

indicator_columns = {
    "dictionary_word": "Dictionary Word",
    "common_year": "Common Year",
    "sequential_pattern": "Sequential Pattern",
    "repeated_character": "Repeated Character",
    "predictable_structure": "Predictable Structure"
}

indicator_results = []

for column, label in indicator_columns.items():
    count = df[column].sum()
    percentage = count / len(df) * 100

    indicator_results.append({
        "Predictability Indicator": label,
        "Number of Passwords": int(count),
        "Percentage (%)": round(percentage, 2)
    })

indicator_table = pd.DataFrame(indicator_results)

print("\nTABLE 4.10 — PREDICTABILITY INDICATOR DISTRIBUTION")
print(indicator_table.to_string(index=False))


# ============================================================
# SAVE TABLES TO EXCEL
# ============================================================

output_file = "CHAPTER_4_OFFICIAL_RESULTS_TABLES.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    dataset_table.to_excel(writer, sheet_name="Table 4.1", index=False)
    traditional_table.to_excel(writer, sheet_name="Table 4.2", index=False)
    cdr_table.to_excel(writer, sheet_name="Table 4.3", index=False)
    crack_table.to_excel(writer, sheet_name="Table 4.4", index=False)
    false_confidence_table.to_excel(writer, sheet_name="Table 4.5", index=False)
    cdr_stats_table.to_excel(writer, sheet_name="Table 4.6", index=False)
    crack_stats_table.to_excel(writer, sheet_name="Table 4.7", index=False)
    comparison_table.to_excel(writer, sheet_name="Table 4.8", index=False)
    statistical_table.to_excel(writer, sheet_name="Table 4.9", index=False)
    indicator_table.to_excel(writer, sheet_name="Table 4.10", index=False)

print("\n" + "=" * 70)
print(f"ALL TABLES SAVED TO: {output_file}")
print("=" * 70)
