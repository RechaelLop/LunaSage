import csv
import os

def generate_synthetic_crop_calendar(output_file='data/agriculture/synthetic_crop_calendar.csv'):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Synthetic crop calendar data (7 countries, various crops and stages)
    data = [
        # Asia
        {'country': 'India', 'crop': 'Rice', 'stage': 'Planting', 'start_month': 'June', 'end_month': 'July'},
        {'country': 'India', 'crop': 'Rice', 'stage': 'Harvesting', 'start_month': 'October', 'end_month': 'November'},
        {'country': 'Japan', 'crop': 'Barley', 'stage': 'Planting', 'start_month': 'March', 'end_month': 'April'},
        {'country': 'Japan', 'crop': 'Barley', 'stage': 'Harvesting', 'start_month': 'July', 'end_month': 'August'},

        # Oceania
        {'country': 'Australia', 'crop': 'Wheat', 'stage': 'Planting', 'start_month': 'May', 'end_month': 'June'},
        {'country': 'Australia', 'crop': 'Wheat', 'stage': 'Harvesting', 'start_month': 'November', 'end_month': 'December'},

        # South America
        {'country': 'Brazil', 'crop': 'Soybean', 'stage': 'Planting', 'start_month': 'October', 'end_month': 'November'},
        {'country': 'Brazil', 'crop': 'Soybean', 'stage': 'Harvesting', 'start_month': 'January', 'end_month': 'February'},

        # North America
        {'country': 'USA', 'crop': 'Corn', 'stage': 'Planting', 'start_month': 'April', 'end_month': 'May'},
        {'country': 'USA', 'crop': 'Corn', 'stage': 'Harvesting', 'start_month': 'September', 'end_month': 'October'},

        # Africa
        {'country': 'Kenya', 'crop': 'Maize', 'stage': 'Planting', 'start_month': 'March', 'end_month': 'April'},
        {'country': 'Kenya', 'crop': 'Maize', 'stage': 'Harvesting', 'start_month': 'August', 'end_month': 'September'},

        # Europe
        {'country': 'France', 'crop': 'Barley', 'stage': 'Planting', 'start_month': 'September', 'end_month': 'October'},
        {'country': 'France', 'crop': 'Barley', 'stage': 'Harvesting', 'start_month': 'June', 'end_month': 'July'},
    ]

    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['country', 'crop', 'stage', 'start_month', 'end_month']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"Synthetic crop calendar data written to: {output_file}")

if __name__ == "__main__":
    generate_synthetic_crop_calendar()
