from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

data_folder = Path.home() / "Desktop" / "Faculdade" / "Mestrado" / "3ºSemestre-Erasmus" / "KDD" / "HW2" / "UCIdata"

ecg_original = pd.read_csv(data_folder / "ecg.csv")
bp_original = pd.read_csv(data_folder / "bp.csv")
temp_original = pd.read_csv(data_folder / "temp.csv")

ecg_test = ecg_original.copy()
bp_test = bp_original.copy()
temp_test = temp_original.copy()


ecg_test["timestamp"] = pd.to_datetime(ecg_test['timestamp'], format = "ISO8601", errors = 'coerce', utc = True)
bp_test["timestamp"] = pd.to_datetime(bp_test['timestamp'], format = "ISO8601", errors = 'coerce', utc = True)
temp_test["timestamp"] = pd.to_datetime(temp_test['timestamp'], format = "ISO8601", errors = 'coerce', utc = True)


print(f"Number of missing values on ecg: \n{ecg_test.isna().sum()}")
print(f"Number of missing values on bp: \n{bp_test.isna().sum()}")
print(f"Number of missing values on temp: \n{temp_test.isna().sum()}")


def clean_timestamp(df):
    return (
        df.dropna(subset=["timestamp"])
        .sort_values("timestamp")
        .reset_index(drop=True)
    )


ecg_test = clean_timestamp(ecg_test)
bp_test = clean_timestamp(bp_test)
temp_test = clean_timestamp(temp_test)

def identify_and_clean_duplicates(df):
    duplicates = df.duplicated(subset=["timestamp"], keep=False)
    if duplicates.any():
        print(f"Found {duplicates.sum()} duplicate timestamps. Cleaning...")
        df = df.drop_duplicates(subset=["timestamp"], keep="first")
    return df


ecg_test = identify_and_clean_duplicates(ecg_test)
bp_test = identify_and_clean_duplicates(bp_test)
temp_test = identify_and_clean_duplicates(temp_test)


print (ecg_test.head())
print (bp_test.head())
print (temp_test.head())


#After cleaning the missing and invalid timestamp values
print(f"Number of missing values on ecg: \n{ecg_test.isna().sum()}")
print(f"Number of missing values on bp: \n{bp_test.isna().sum()}")
print(f"Number of missing values on temp: \n{temp_test.isna().sum()}")


fig, axes = plt.subplots(3, 1, figsize=(12, 9))

# Frequência cardíaca
axes[0].plot(
    ecg_test["timestamp"],
    ecg_test["heart_rate_bpm"],
    marker=".",
    linewidth=0.8
)
axes[0].set_title("Frequência cardíaca")
axes[0].set_ylabel("bpm")

# Pressão arterial
axes[1].plot(
    bp_test["timestamp"],
    bp_test["systolic_bp_mmhg"],
    marker=".",
    linewidth=0.8
)
axes[1].set_title("Pressão arterial sistólica")
axes[1].set_ylabel("mmHg")

# Temperatura
axes[2].plot(
    temp_test["timestamp"],
    temp_test["temperature_c"],
    marker=".",
    linewidth=0.8
)
axes[2].set_title("Temperatura")
axes[2].set_ylabel("°C")

for ax in axes:
    ax.set_xlabel("Hora (UTC)")
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.show()
