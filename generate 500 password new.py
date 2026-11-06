import csv
from pathlib import Path

# Locate the project folder
PROJECT_FOLDER = Path(
    r"C:\Users\STARGIRL\Documents\Password strength_Project"
)

# Locate the existing 500-password dataset
INPUT_FILE = PROJECT_FOLDER / "generated_500_passwords_fixed.csv"

# Output file
OUTPUT_FILE = PROJECT_FOLDER / "generated_500_passwords_reconstructed.csv"


def main():

    print("=" * 60)
    print("PASSWORD DATASET RECONSTRUCTION")
    print("=" * 60)

    if not INPUT_FILE.is_file():
        raise FileNotFoundError(
            f"Cannot find the dataset:\n{INPUT_FILE}"
        )

    with INPUT_FILE.open(
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as source:

        reader = csv.DictReader(source)

        if not reader.fieldnames:
            raise ValueError("The CSV file has no column headings.")

        records = list(reader)
        columns = reader.fieldnames

    print("Dataset found:", INPUT_FILE.name)
    print("Total records:", len(records))

    if len(records) != 500:
        raise ValueError(
            f"Expected 500 records but found {len(records)}."
        )

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as destination:

        writer = csv.DictWriter(
            destination,
            fieldnames=columns
        )

        writer.writeheader()
        writer.writerows(records)

    print("\nSUCCESS")
    print("The 500 existing records have been exported.")
    print("Output file:", OUTPUT_FILE)
    print("=" * 60)


if __name__ == "__main__":
    main()
