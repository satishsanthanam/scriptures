import csv

def process_bhagavad_gita_with_detailed_log(input_file, output_csv, log_file):
    # 1. Read original data
    with open(input_file, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        indexed_rows = []
        for i, row in enumerate(reader):
            indexed_rows.append({'data': row, 'orig_row_num': i + 2})

    new_rows_data = []
    skip_indices = set()
    detailed_logs = []

    # 2. Rearrangement Logic
    for i in range(len(indexed_rows)):
        if i in skip_indices:
            continue
        
        current_item = indexed_rows[i]
        row = current_item['data']
        
        # Check if 8th column (index 7) starts with "Context"
        # and 6th column (index 5) is not empty (Verse data)
        is_context_start = len(row) > 7 and row[7].strip().startswith("Context")
        has_verse_data = len(row) > 5 and row[5].strip() != ""

        if is_context_start and has_verse_data:
            target_index = -1
            intermediate_indices = []
            
            # Find next row with filled Column 6
            for j in range(i + 1, len(indexed_rows)):
                if len(indexed_rows[j]['data']) > 5 and indexed_rows[j]['data'][5].strip() != "":
                    target_index = j
                    break
                else:
                    intermediate_indices.append(j)
            
            # Perform swap if intermediate rows (footnotes) exist
            if target_index != -1 and intermediate_indices:
                orig_pos = current_item['orig_row_num']
                last_skipped_row = indexed_rows[intermediate_indices[-1]]['orig_row_num']
                context_text = row[7].strip() # Capture the 8th column

                detailed_logs.append({
                    'orig_row': orig_pos,
                    'moved_after': last_skipped_row,
                    'text': context_text
                })

                # Move footnotes before the context
                for idx in intermediate_indices:
                    new_rows_data.append(indexed_rows[idx]['data'])
                    skip_indices.add(idx)
                
                new_rows_data.append(row)
            else:
                new_rows_data.append(row)
        else:
            new_rows_data.append(row)

    # 3. Save Final CSV with pkey
    final_header = ['pkey'] + header
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(final_header)
        for i, row_data in enumerate(new_rows_data, start=1):
            writer.writerow([i] + row_data)
    
    # 4. Save Detailed Log (including 8th column content)
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"--- Detailed Movement Log ({len(detailed_logs)} moves) ---\n\n")
        for entry in detailed_logs:
            f.write(f"Moved from Original Row {entry['orig_row']} to after Row {entry['moved_after']}\n")
            f.write(f"Context Text (Col 8): {entry['text']}\n")
            f.write("-" * 80 + "\n")
    
    return len(detailed_logs)

# Execute
process_bhagavad_gita_with_detailed_log('bhagavadgita_gbp-csv.csv', 'bhagavadgita_final.csv', 'rearrange_log_detailed.txt')
print("Processing complete. Check 'rearrange_log_detailed.txt' for the detailed content log.")