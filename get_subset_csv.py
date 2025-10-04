import pandas as pd
import os

# Define the base directory as the directory of this file
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, 'fungi')

# Iterate over each subfolder in the fungi directory
for folder_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder_name)
    
    # Check if it's a directory
    if os.path.isdir(folder_path):
        # Find the CSV file (assuming one per folder starting with 'observations-')
        for file_name in os.listdir(folder_path):
            if file_name.startswith('observations-') and file_name.endswith('.csv'):
                csv_path = os.path.join(folder_path, file_name)
                
                # Read the CSV
                df = pd.read_csv(csv_path)
                
                # Sample 100 rows (or all if less than 100)
                subset = df.sample(n=min(100, len(df)), random_state=42)
                
                # Overwrite the original CSV with the subset
                subset.to_csv(csv_path, index=False)
                print(f"Processed {csv_path}: {len(subset)} rows")
                break  # Assuming only one CSV per folder