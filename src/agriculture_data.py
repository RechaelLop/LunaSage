import csv
from datetime import datetime

import csv

file_path = "data/agriculture/fao_crop_calendar.csv"

with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    print("CSV Columns:", reader.fieldnames)
    countries_set = set()
    for i, row in enumerate(reader):
        country = row.get("countryName") or row.get("Country")
        if country:
            countries_set.add(country)
        if i > 100:  # limit to first 100 rows for speed
            break

print("Sample countries in CSV:", sorted(countries_set))


def format_period(row):
    all_year = row.get("allYear", "").lower() == "yes"
    start_date_str = row.get("start_date", "")
    end_date_str = row.get("end_date", "")
    
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
    
    if all_year:
        return "All Year"
    if start_date and end_date:
        return f"{start_date.strftime('%b %d')} to {end_date.strftime('%b %d')}"
    return "Unknown"

def load_crop_calendar(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    return data

def filter_crop_data(data, countries, crop_process=None, crop_id=None):
    filtered = []
    for row in data:
        country = row.get("countryName") or row.get("Country")  # try both keys if any
        if country not in countries:
            continue
        if crop_process and row.get("cropProcess") != crop_process:
            continue
        if crop_id and row.get("cropId") != crop_id:
            continue
        filtered.append(row)
    return filtered

def print_crop_calendar(data, countries):
    for country in countries:
        print(f"\nCrop Calendar for {country}:\n" + "-"*30)
        country_rows = [row for row in data if (row.get("countryName") or row.get("Country")) == country]
        if not country_rows:
            print(f"No crop calendar data available for '{country}'.")
            continue
        
        for row in country_rows:
            crop = row.get("cropName", "Unknown Crop")
            period = format_period(row)
            print(f"{crop}: {period}")

if __name__ == "__main__":
    # Path to your downloaded CSV
    file_path = "data/agriculture/fao_crop_calendar.csv"
    
    # Countries you want to show data for
    countries = ["India", "United States", "Brazil", "France", "Kenya"]
    
    # Optional: specify crop process & crop id if you want to filter those too
    crop_process = None  # e.g. "Harvesting"
    crop_id = None  # e.g. "123"
    
    crop_data = load_crop_calendar(file_path)
    filtered_data = filter_crop_data(crop_data, countries, crop_process, crop_id)
    print_crop_calendar(filtered_data, countries)
