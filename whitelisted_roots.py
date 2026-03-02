import pandas as pd
import sys

# Usage: python3 whitelisted_roots.py program.csv
df = pd.read_csv(sys.argv[1])
# Extract only where submission is True
seeds = df[df['eligible_for_submission'] == True]['identifier']

# Clean and Save
with open('whitelisted_roots.txt', 'w') as f:
    for item in seeds.unique():
        # Strip *. and https:// to get the base root
        clean = item.replace('*.', '').replace('https://', '').split('/')[0]
        if "." in clean: f.write(f"{clean}\n")
