import pandas as pd
import sys

# Usage: python3 get_blacklist.py program.csv
df = pd.read_csv(sys.argv[1])
# Extract only where submission is False
blacklist = df[df['eligible_for_submission'] == False]['identifier']

# Clean and Save
with open('blacklist.txt', 'w') as f:
    for item in blacklist.unique():
        clean = item.replace('*.', '').replace('https://', '').split('/')[0]
        if "." in clean: f.write(f"{clean}\n")
