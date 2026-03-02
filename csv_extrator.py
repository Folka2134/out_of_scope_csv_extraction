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
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 extract_scope.py -roots <csv_file>  # Creates in_scope_roots.txt")
        print("  python3 extract_scope.py -subs  <csv_file>  # Creates out_of_scope.txt")
        sys.exit(1)

    flag = sys.argv[1]
    csv_file = sys.argv[2]

    try:
        df = pd.read_csv(csv_file)
        
        if flag == "-roots":
            # Logic: Submission is Allowed (True)
            mask = (df['eligible_for_submission'] == True) | (df['eligible_for_submission'].astype(str).str.lower() == 'true')
            output_file = 'in_scope_roots.txt'
            msg = "In-Scope Roots (Seeds)"
        elif flag == "-subs":
            # Logic: Submission is Forbidden (False)
            mask = (df['eligible_for_submission'] == False) | (df['eligible_for_submission'].astype(str).str.lower() == 'false')
            output_file = 'out_of_scope.txt'
            msg = "Out-of-Scope (Blacklist)"
        else:
            print(f"Error: Invalid flag '{flag}'. Use -roots or -subs.")
            sys.exit(1)

        raw_list = df[mask]['identifier']
        # Clean domains and filter out things that aren't actually domains (like "WGP Slot Games")
        cleaned_list = sorted(list(set(raw_list.apply(clean_identifier))))
        final_list = [d for d in cleaned_list if d and "." in d] 

        with open(output_file, 'w') as f:
            for domain in final_list:
                f.write(f"{domain}\n")

        print(f"[*] Successfully generated {output_file} ({len(final_list)} {msg})")

    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
