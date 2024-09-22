import os
import csv
from datetime import datetime, timedelta

def collect_data_for_last_days(input_dir, end_date, days_count):
    all_data = []
    for i in range(days_count):
        current_date = end_date - timedelta(days=i)
        file_path = os.path.join(input_dir, f"{current_date.strftime('%Y-%m-%d')}.csv")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                all_data.extend([row for row in reader])
    return all_data

def aggregate_user_actions(data):
    aggregated_data = {}
    for row in data:
        email = row['email'].strip()
        if email not in aggregated_data:
            aggregated_data[email] = {
                'create_count': 0,
                'read_count': 0,
                'update_count': 0,
                'delete_count': 0
            }
        aggregated_data[email]['create_count'] += int(row['create_count'].strip())
        aggregated_data[email]['read_count'] += int(row['read_count'].strip())
        aggregated_data[email]['update_count'] += int(row['update_count'].strip())
        aggregated_data[email]['delete_count'] += int(row['delete_count'].strip())
    return aggregated_data

def write_aggregated_data_to_csv(output_filepath, aggregated_data):
    with open(output_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['email', 'create_count', 'read_count', 'update_count', 'delete_count'])
        for email, actions in aggregated_data.items():
            writer.writerow([
                email, 
                actions['create_count'], 
                actions['read_count'], 
                actions['update_count'], 
                actions['delete_count']
            ])

if __name__ == "__main__":
    input_dir = 'input'
    output_dir = 'output'
    end_date = datetime.strptime('2024-09-22', '%Y-%m-%d')
    days_count = 7  

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = collect_data_for_last_days(input_dir, end_date, days_count)
    aggregated_data = aggregate_user_actions(data)
    output_filepath = os.path.join(output_dir, f"{end_date.strftime('%Y-%m-%d')}.csv")
    write_aggregated_data_to_csv(output_filepath, aggregated_data)
