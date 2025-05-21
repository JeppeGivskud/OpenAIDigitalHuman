import os

# Define the folder names
folders = ["Day02", "Day08", "Day09", "Day13"]

# Get the current script directory
base_path = os.path.dirname(os.path.abspath(__file__))

# Initialize a list to store the combined lines
combined_lines = []

# Iterate through each folder
for folder in folders:
    folder_path = os.path.join(base_path, folder)
    if os.path.exists(folder_path):
        # Iterate through all text files in the folder
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".txt"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r", encoding="utf-8") as file:
                    # Read the first five lines
                    lines = [file.readline().strip() for _ in range(5)]
                    combined_lines.extend(lines)

# Write the combined lines to a new file
output_file = os.path.join(base_path, "combined_output.txt")
with open(output_file, "w", encoding="utf-8") as output:
    output.write("\n".join(combined_lines))
