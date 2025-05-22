import os
import csv
from datetime import datetime

# Define the folder names
folders = ["Day02", "Day08", "Day09", "Day13"]

# Get the current script directory
base_path = os.path.dirname(os.path.abspath(__file__))

# Initialize a list to store the combined lines
combined_data = []

# Iterate through each folder
for folder in folders:
    folder_path = os.path.join(base_path, folder)
    if os.path.exists(folder_path):
        # Iterate through all text files in the folder
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".txt"):
                file_path = os.path.join(folder_path, file_name)
                # Determine if the file name number is even or odd
                file_number = int(file_name.split("_")[0])
                ai_initiated = "True" if file_number % 2 == 0 else "False"
                oldest_date = None
                newest_date = None
                with open(file_path, "r", encoding="utf-8") as file:
                    # Read the first five lines
                    for i in range(4):
                        line = file.readline().strip()
                        if ": " in line:
                            variable, value = line.split(": ", 1)
                            if variable == "Oldest Date":
                                oldest_date = value
                            elif variable == "Newest Date":
                                newest_date = value
                        else:
                            variable, value = line, ""
                        combined_data.append(
                            {
                                "Folder": folder,
                                "File": file_name,
                                "Variable": variable,
                                "Value": value,
                            }
                        )
                    # Recalculate Difference in Seconds
                    if oldest_date and newest_date:
                        fmt = "%Y-%m-%d_%H-%M-%S"
                        diff_seconds = int(
                            (
                                datetime.strptime(newest_date, fmt)
                                - datetime.strptime(oldest_date, fmt)
                            ).total_seconds()
                        )
                        combined_data.append(
                            {
                                "Folder": folder,
                                "File": file_name,
                                "Variable": "Difference in Seconds",
                                "Value": str(diff_seconds),
                            }
                        )
                    # Add AI Initiated as a variable-value pair
                    combined_data.append(
                        {
                            "Folder": folder,
                            "File": file_name,
                            "Variable": "AI Initiated",
                            "Value": ai_initiated,
                        }
                    )

# Write the combined data to a CSV file
output_file = os.path.join(base_path, "combined_output.csv")
with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
    fieldnames = ["Folder", "File", "Variable", "Value"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(combined_data)
