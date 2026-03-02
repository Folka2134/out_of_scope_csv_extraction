import pandas as pd
import re

# Load the file
df = pd.read_csv('scopes_for_superbet_at_2026-02-25_00_42_37_UTC.csv')

# Filter for rows where submission is NOT allowed
oos_raw = df[df['eligible_for_submission'] == False]['identifier']

def clean_identifier(text):
    # 1. Remove http/https
    text = re.sub(r'^https?://', '', text)
    # 2. Remove leading wildcard *.
    text = re.sub(r'^\*\.', '', text)
    # 3. Remove trailing paths/slashes
    text = text.split('/')[0]
    return text.strip()

# Apply cleaning and remove duplicates
blacklist = sorted(list(set(oos_raw.apply(clean_identifier))))

# Save to a text file for your tools
with open('out_of_scope.txt', 'w') as f:
    for domain in blacklist:
        f.write(f"{domain}\n")

print(f"Created out_of_scope.txt with {len(blacklist)} entries.")
