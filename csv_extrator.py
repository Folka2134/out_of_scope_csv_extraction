import sys
import pandas as pd
import re

def clean_identifier(text):
    if pd.isna(text):
        return ""
    # 1. Remove http/https
    text = re.sub(r'^https?://', '', str(text))
    # 2. Remove leading wildcard *.
    text = re.sub(r'^\*\.', '', text)
    # 3. Remove trailing paths/slashes
    text = text.split('/')[0]
    return text.strip()

def main():
    # Check if the user provided the filename
    if len(sys.argv) < 2:
        print("Usage: python extract_scope.py <path_to_csv>")
        sys.exit(1)

    csv_file = sys.argv[1]

    try:
        df = pd.read_csv(csv_file)

        # Filter for rows where submission is NOT allowed
        # Handles both boolean False and the string "false"
        oos_mask = (df['eligible_for_submission'] == False) | \
                   (df['eligible_for_submission'].astype(str).str.lower() == 'false')
        
        oos_raw = df[oos_mask]['identifier']

        # Apply cleaning, remove duplicates, and remove empty strings
        blacklist = sorted(list(set(oos_raw.apply(clean_identifier))))
        blacklist = [d for d in blacklist if d]

        # Save to out_of_scope.txt
        output_file = 'out_of_scope.txt'
        with open(output_file, 'w') as f:
            for domain in blacklist:
                f.write(f"{domain}\n")

        print(f"[*] Successfully processed: {csv_file}")
        print(f"[*] Extracted {len(blacklist)} unique base domains to {output_file}")
        
    except FileNotFoundError:
        print(f"[!] Error: The file '{csv_file}' was not found.")
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
