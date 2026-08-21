import re
import math
import string
import wordninja
from wordfreq import zipf_frequency


# ============================================================
# PASSWORD STRENGTH ASSESSMENT MODEL
# Crack Difficulty-Based Password Strength Assessment Model
# ============================================================


# ------------------------------------------------------------
# 1. COMMON DICTIONARY WORDS
# ------------------------------------------------------------
# These words are used to identify common dictionary/password
# words embedded in passwords.

COMMON_WORDS = {
    "password",
    "admin",
    "administrator",
    "welcome",
    "letmein",
    "qwerty",
    "login",
    "user",
    "love",
    "hello",
    "dream",
    "cloud",
    "football",
    "monkey",
    "dragon",
    "master",
    "superman",
    "iloveyou",
    "princess",
    "computer",
    "secret",
    "summer",
    "winter",
    "freedom",
    "access",
    "manager"
}


# ------------------------------------------------------------
# 2. COMMON YEARS
# ------------------------------------------------------------

COMMON_YEARS = {
    str(year) for year in range(1950, 2027)
}


# ------------------------------------------------------------
# 3. CHARACTER DIVERSITY
# ------------------------------------------------------------

def character_diversity(password):
    """
    Returns the number of character classes present.

    1 = lowercase
    2 = uppercase
    3 = digits
    4 = special characters
    """

    diversity = 0

    if re.search(r"[a-z]", password):
        diversity += 1

    if re.search(r"[A-Z]", password):
        diversity += 1

    if re.search(r"\d", password):
        diversity += 1

    if re.search(r"[^A-Za-z0-9]", password):
        diversity += 1

    return diversity


# ------------------------------------------------------------
# 4. CHARACTER POOL SIZE
# ------------------------------------------------------------

def character_pool_size(password):
    """
    Calculates the theoretical character pool size based on
    the character classes present in the password.
    """

    pool = 0

    if re.search(r"[a-z]", password):
        pool += 26

    if re.search(r"[A-Z]", password):
        pool += 26

    if re.search(r"\d", password):
        pool += 10

    if re.search(r"[^A-Za-z0-9]", password):
        pool += 32

    return pool


# ------------------------------------------------------------
# 5. ENTROPY
# ------------------------------------------------------------

def calculate_entropy(password):
    """
    Calculates Shannon-style password entropy using:

        H = L * log2(N)

    where:
        L = password length
        N = character pool size
    """

    length = len(password)
    pool = character_pool_size(password)

    if length == 0 or pool == 0:
        return 0.0

    return length * math.log2(pool)


# ------------------------------------------------------------
# 6. DICTIONARY WORD DETECTION
# ------------------------------------------------------------

def dictionary_word_detected(password):
    """
    Detects common dictionary words occurring inside a password.

    Detection uses three layers:

    1. Existing COMMON_WORDS
    2. wordninja for splitting joined words
    3. wordfreq for common-English-word detection

    Short fragments of 1-2 characters are ignored.
    Three-letter words require a stronger frequency score.
    """

    password_lower = password.lower()

    # --------------------------------------------------------
    # 1. EXISTING MODEL DICTIONARY
    # --------------------------------------------------------

    for word in COMMON_WORDS:

        if word in password_lower:
            return True

    # --------------------------------------------------------
    # 2. EXTRACT ALPHABETIC SEQUENCES
    # --------------------------------------------------------

    alphabetic_sequences = re.findall(
        r"[A-Za-z]+",
        password
    )

    # --------------------------------------------------------
    # 3. SPLIT JOINED WORDS WITH WORDNINJA
    # --------------------------------------------------------

    for sequence in alphabetic_sequences:

        parts = wordninja.split(sequence)

        for word in parts:

            word = word.lower().strip()

            # Ignore fragments shorter than 3 characters
            if len(word) < 3:
                continue

            score = zipf_frequency(
                word,
                "en"
            )

            # Four or more characters
            if len(word) >= 4 and score >= 3.0:
                return True

            # Three-letter words require stronger evidence
            if len(word) == 3 and score >= 4.0:
                return True

    return False


# ------------------------------------------------------------
# 7. COMMON YEAR DETECTION
# ------------------------------------------------------------

def common_year_detected(password):
    """
    Detects four-digit years commonly used in passwords.
    """

    years = re.findall(r"(19\d{2}|20\d{2})", password)

    for year in years:
        if year in COMMON_YEARS:
            return True

    return False


# ------------------------------------------------------------
# 8. SEQUENTIAL PATTERN DETECTION
# ------------------------------------------------------------

def sequential_pattern_detected(password):
    """
    Detects simple sequential patterns such as:

        123
        234
        345
        abc
        bcd
        xyz

    Also checks common keyboard sequences.
    """

    password_lower = password.lower()

    # Numeric sequences
    for i in range(len(password) - 2):
        part = password[i:i + 3]

        if part.isdigit():
            a, b, c = map(int, part)

            if b == a + 1 and c == b + 1:
                return True

            if b == a - 1 and c == b - 1:
                return True

    # Alphabetic sequences
    for i in range(len(password_lower) - 2):
        part = password_lower[i:i + 3]

        if part.isalpha():
            a = ord(part[0])
            b = ord(part[1])
            c = ord(part[2])

            if b == a + 1 and c == b + 1:
                return True

            if b == a - 1 and c == b - 1:
                return True

    # Common keyboard sequences
    keyboard_patterns = [
        "qwerty",
        "asdf",
        "zxcv",
        "123456",
        "654321",
        "abcdef",
        "fedcba"
    ]

    for pattern in keyboard_patterns:
        if pattern in password_lower:
            return True

    return False


# ------------------------------------------------------------
# 9. REPEATED CHARACTER DETECTION
# ------------------------------------------------------------

def repeated_character_detected(password):
    """
    Detects repeated consecutive characters.

    Examples:
        aaa
        111
        !!!
        xx
    """

    return bool(re.search(r"(.)\1", password))


# ------------------------------------------------------------
# 10. PREDICTABLE STRUCTURE DETECTION
# ------------------------------------------------------------

def predictable_structure_detected(password):
    """
    Detects meaningful predictable password structures.

    Examples detected:
        Password123
        Welcome123
        Admin2024
        Tola2026
        Password2026!
        Welcome@123

    Does NOT automatically flag random mixed-character
    passwords simply because letters and numbers are adjacent.
    """

    password_lower = password.lower()

    # --------------------------------------------------------
    # 1. Dictionary word + numeric suffix
    # --------------------------------------------------------

    if dictionary_word_detected(password):

        # Word followed by 2 or more digits
        if re.search(r"[A-Za-z]{3,}\d{2,}", password):
            return True

        # Digits followed by a dictionary word
        if re.search(r"\d{2,}[A-Za-z]{3,}", password):
            return True

    # --------------------------------------------------------
    # 2. Dictionary word + common year
    # --------------------------------------------------------

    if dictionary_word_detected(password) and common_year_detected(password):
        return True

    # --------------------------------------------------------
    # 3. Common predictable suffixes
    # --------------------------------------------------------

    predictable_suffixes = [
        "123",
        "1234",
        "12345",
        "123456",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025",
        "2026",
        "2027",
        "2028",
         "!!",
        "!!!",
        "@123",
        "@1234",
        "@2024",
        "@2025",
        "@2026",
        "#123",
        "#1234",
        "#2024",
        "#2025",
        "#2026",
    ]

    for suffix in predictable_suffixes:
        if password_lower.endswith(suffix):
            return True

    # --------------------------------------------------------
    # 4. Sequential patterns
    # --------------------------------------------------------

    if sequential_pattern_detected(password):
        return True

    # --------------------------------------------------------
    # 5. Repeated-character structure
    # --------------------------------------------------------

    if repeated_character_detected(password):
        return True

    # --------------------------------------------------------
    # 6. Common predictable words
    # --------------------------------------------------------

    predictable_words = [
        "password",
        "welcome",
        "admin",
        "qwerty",
        "letmein",
        "login",
        "user",
        "guest",
        "football",
        "iloveyou",
    ]

    for word in predictable_words:
        if word in password_lower:
            return True

    return False

# ------------------------------------------------------------
# 11. NORMALIZED LENGTH STRENGTH
# ------------------------------------------------------------

def normalized_length_strength(password):
    """
    Length reference = 20 characters.

    Values above the reference are capped at 1.
    """

    return min(len(password) / 20, 1.0)


# ------------------------------------------------------------
# 12. NORMALIZED DIVERSITY STRENGTH
# ------------------------------------------------------------

def normalized_diversity_strength(password):
    """
    Four character classes represent maximum diversity.
    """

    return min(character_diversity(password) / 4, 1.0)


# ------------------------------------------------------------
# 13. NORMALIZED ENTROPY STRENGTH
# ------------------------------------------------------------

def normalized_entropy_strength(password):
    """
    Entropy reference = 80 bits.
    """

    entropy = calculate_entropy(password)

    return min(entropy / 80, 1.0)


# ------------------------------------------------------------
# 14. CDR RISK MODEL
# ------------------------------------------------------------

def calculate_cdr(password):
    """
    Calculates the weighted CDR risk score.

    Weights:

        Length Risk             = 0.10
        Diversity Risk          = 0.10
        Entropy Risk            = 0.15
        Dictionary Risk         = 0.20
        Common Year Risk        = 0.10
        Sequential Risk         = 0.10
        Repeated Character Risk = 0.05
        Predictable Structure   = 0.20

    Total weight = 1.00
    """

    length_strength = normalized_length_strength(password)
    diversity_strength = normalized_diversity_strength(password)
    entropy_strength = normalized_entropy_strength(password)

    length_risk = 1 - length_strength
    diversity_risk = 1 - diversity_strength
    entropy_risk = 1 - entropy_strength

    dictionary_risk = 1 if dictionary_word_detected(password) else 0
    year_risk = 1 if common_year_detected(password) else 0
    sequential_risk = 1 if sequential_pattern_detected(password) else 0
    repeated_risk = 1 if repeated_character_detected(password) else 0
    predictable_risk = 1 if predictable_structure_detected(password) else 0

    weighted_length = 0.10 * length_risk
    weighted_diversity = 0.10 * diversity_risk
    weighted_entropy = 0.15 * entropy_risk
    weighted_dictionary = 0.20 * dictionary_risk
    weighted_year = 0.10 * year_risk
    weighted_sequential = 0.10 * sequential_risk
    weighted_repeated = 0.05 * repeated_risk
    weighted_predictable = 0.20 * predictable_risk

    cdr_score = (
        weighted_length
        + weighted_diversity
        + weighted_entropy
        + weighted_dictionary
        + weighted_year
        + weighted_sequential
        + weighted_repeated
        + weighted_predictable
    )

    return cdr_score


# ------------------------------------------------------------
# 15. CDR CLASSIFICATION
# ------------------------------------------------------------

def classify_cdr(cdr_score):
    """
    CDR classification thresholds from Chapter Three.
    """

    if cdr_score < 0.35:
        return "Low Predictability Risk"

    elif cdr_score < 0.50:
        return "Moderate Predictability Risk"

    elif cdr_score < 0.70:
        return "High Predictability Risk"

    else:
        return "Very High Predictability Risk"


# ------------------------------------------------------------
# 16. TRADITIONAL PASSWORD STRENGTH
# ------------------------------------------------------------

def traditional_strength(password):
    """
    Traditional password-strength classification based on:

        Length
        Lowercase
        Uppercase
        Digit
        Special character
    """

    length = len(password)

    lowercase = bool(re.search(r"[a-z]", password))
    uppercase = bool(re.search(r"[A-Z]", password))
    digit = bool(re.search(r"\d", password))
    special = bool(re.search(r"[^A-Za-z0-9]", password))

    conditions = sum([
        lowercase,
        uppercase,
        digit,
        special
    ])

    if length >= 12 and conditions == 4:
        return "Strong"

    elif length >= 8 and conditions >= 3:
        return "Medium"

    else:
        return "Weak"


# ------------------------------------------------------------
# 17. CRACK-DIFFICULTY SCORE
# ------------------------------------------------------------

def calculate_crack_difficulty(password):
    """
    Calculates the Crack-Difficulty Score defined in Chapter Three.

    Positive indicators:

        Length >= 12          +2
        Diversity = 4         +2
        Entropy >= 60         +2

    Negative indicators:

        Dictionary word       -2
        Common year           -2
        Predictable pattern   -2
        Repeated characters   -1
    """

    length_indicator = 1 if len(password) >= 12 else 0

    diversity_indicator = (
        1 if character_diversity(password) == 4 else 0
    )

    entropy_indicator = (
        1 if calculate_entropy(password) >= 60 else 0
    )

    dictionary_indicator = (
        1 if dictionary_word_detected(password) else 0
    )

    year_indicator = (
        1 if common_year_detected(password) else 0
    )

    predictable_indicator = (
        1 if predictable_structure_detected(password) else 0
    )

    repeated_indicator = (
        1 if repeated_character_detected(password) else 0
    )

    crack_score = (
        2 * length_indicator
        + 2 * diversity_indicator
        + 2 * entropy_indicator
        - 2 * dictionary_indicator
        - 2 * year_indicator
        - 2 * predictable_indicator
        - repeated_indicator
    )

    return crack_score


# ------------------------------------------------------------
# 18. CRACK-DIFFICULTY CLASSIFICATION
# ------------------------------------------------------------

def classify_crack_difficulty(score):
    """
    Chapter Three classification:

        Score <= 2       = Easy
        2 < Score <= 5   = Moderate
        Score > 5        = Difficult
    """

    if score <= 2:
        return "Easy"

    elif score <= 5:
        return "Moderate"

    else:
        return "Difficult"


# ------------------------------------------------------------
# 19. COMPLETE PASSWORD ASSESSMENT
# ------------------------------------------------------------

def assess_password(password):
    """
    Runs the complete proposed password assessment model.
    """

    length = len(password)
    diversity = character_diversity(password)
    pool_size = character_pool_size(password)
    entropy = calculate_entropy(password)

    dictionary = dictionary_word_detected(password)
    year = common_year_detected(password)
    sequential = sequential_pattern_detected(password)
    repeated = repeated_character_detected(password)
    predictable = predictable_structure_detected(password)

    cdr_score = calculate_cdr(password)
    cdr_class = classify_cdr(cdr_score)

    crack_score = calculate_crack_difficulty(password)
    crack_class = classify_crack_difficulty(crack_score)

    traditional = traditional_strength(password)

    return {
        "password": password,
        "length": length,
        "character_diversity": diversity,
        "character_pool_size": pool_size,
        "entropy": entropy,
        "dictionary_word": dictionary,
        "common_year": year,
        "sequential_pattern": sequential,
        "repeated_character": repeated,
        "predictable_structure": predictable,
        "cdr_score": cdr_score,
        "cdr_class": cdr_class,
        "crack_score": crack_score,
        "crack_class": crack_class,
        "traditional_strength": traditional
    }


# ------------------------------------------------------------
# 20. FALSE-CONFIDENCE IDENTIFICATION
# ------------------------------------------------------------

def is_false_confidence_case(result):
    """
    Operational definition from Chapter Three:

        Traditionally Strong
        +
        High Predictability Risk
        +
        Easy Crack Difficulty
    """

    return (
        result["traditional_strength"] == "Strong"
        and result["cdr_class"] == "High Predictability Risk"
        and result["crack_class"] == "Easy"
    )


# ------------------------------------------------------------
# 21. DISPLAY FUNCTION
# ------------------------------------------------------------

def display_result(result):

    print("Password:", result["password"])
    print("Length:", result["length"])
    print("Character Diversity:", result["character_diversity"])
    print("Character Pool Size:", result["character_pool_size"])
    print("Entropy:", round(result["entropy"], 4), "bits")

    print("\n## Predictability Indicators")
    print("Dictionary Word:", result["dictionary_word"])
    print("Common Year:", result["common_year"])
    print("Sequential Pattern:", result["sequential_pattern"])
    print("Repeated Character:", result["repeated_character"])
    print("Predictable Structure:", result["predictable_structure"])

    print("\n## Traditional Password Strength")
    print("Traditional Class:", result["traditional_strength"])

    print("\n## CDR Assessment")
    print("CDR Score:", round(result["cdr_score"], 6))
    print("CDR Class:", result["cdr_class"])

    print("\n## Crack-Difficulty Assessment")
    print("Crack-Difficulty Class:", result["crack_class"])
    print("Crack-Difficulty Score:", result["crack_score"])

    print("\n## False-Confidence Assessment")

    if is_false_confidence_case(result):
        print("False-Confidence Case: TRUE")
    else:
        print("False-Confidence Case: FALSE")


# ------------------------------------------------------------
# 22. TEST PASSWORD
# ------------------------------------------------------------

if __name__ == "__main__":

    password = "Password@2024!"

    result = assess_password(password)

    display_result(result)
