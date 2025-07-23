#!/usr/bin/env python3
import csv
import json
from datetime import datetime

def convert_csv_to_json():
    municipalities = []
    
    # Read the CSV data
    with open('ssb-property-tax-data-2025.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            municipality = {
                "name": row['Kommune'],
                "fylke": "Unknown",  # We'll need to add this separately
                "eiendomsskatt_bolig": row['Har_eiendomsskatt_bolig'] == 'Ja',
                "eiendomsskatt_naering": row['Har_eiendomsskatt_naering'] == 'Ja',
                "skattesats_bolig_promille": float(row['Skattesats_bolig_promille']) if row['Skattesats_bolig_promille'] != '-' else 0,
                "skattesats_bolig_prosent": float(row['Skattesats_bolig_promille']) / 10 if row['Skattesats_bolig_promille'] != '-' else 0,
                "skattesats_naering_promille": float(row['Skattesats_naering_promille']) if row['Skattesats_naering_promille'] != '-' else 0,
                "skattesats_naering_prosent": float(row['Skattesats_naering_promille']) / 10 if row['Skattesats_naering_promille'] != '-' else 0,
                "bunnfradrag": int(row['Bunnfradrag_kr']) if row['Bunnfradrag_kr'].isdigit() else 0,
                "fritak_nye_boliger": row['Fritak_nye_boliger_aar'] != 'Har ikke',
                "fritak_aar": int(row['Fritak_nye_boliger_aar']) if row['Fritak_nye_boliger_aar'].isdigit() else 0,
                "eiendomsskattefritak_historiske": row['Eiendomsskattefritak_historiske'] == 'Ja',
                "formuesgrunnlag": row['Formuesgrunnlag'] == 'Ja',
                "gjennomsnittlig_skatt_2024": int(row['Gjennomsnittlig_skatt_2024_kr']) if row['Gjennomsnittlig_skatt_2024_kr'].isdigit() else 0
            }
            municipalities.append(municipality)
    
    # Create the final JSON structure
    data = {
        "version": "2025.2-ssb-official",
        "lastUpdated": datetime.now().isoformat() + "Z",
        "source": "SSB (Statistics Norway) - https://www.ssb.no/offentlig-sektor/kommunale-finanser/artikler/kommuner-med-eiendomsskatt",
        "description": "OFFICIAL SSB property tax data for all 357 Norwegian municipalities. Tax rates are in PROMILLE (‰) as per SSB standard.",
        "total_municipalities": len(municipalities),
        "municipalities_with_property_tax": sum(1 for m in municipalities if m['eiendomsskatt_bolig'] or m['eiendomsskatt_naering']),
        "municipalities_with_residential_tax": sum(1 for m in municipalities if m['eiendomsskatt_bolig']),
        "data_explanation": {
            "eiendomsskatt_bolig": "Property tax on residential properties (true/false)",
            "eiendomsskatt_naering": "Property tax on commercial properties (true/false)",
            "skattesats_bolig_promille": "Tax rate for residential properties in PROMILLE (‰) - official SSB format",
            "skattesats_bolig_prosent": "Tax rate for residential properties in PERCENT (%) - converted for calculations",
            "skattesats_naering_promille": "Tax rate for commercial properties in PROMILLE (‰) - official SSB format",
            "skattesats_naering_prosent": "Tax rate for commercial properties in PERCENT (%) - converted for calculations",
            "bunnfradrag": "Tax-free threshold for properties (NOK)",
            "fritak_nye_boliger": "Exemption for new residential buildings (true/false)",
            "fritak_aar": "Years of exemption for new buildings",
            "eiendomsskattefritak_historiske": "Tax exemption for historical buildings (true/false)",
            "formuesgrunnlag": "Uses wealth basis for property valuation (true/false)",
            "gjennomsnittlig_skatt_2024": "Average property tax paid in 2024 (NOK)"
        },
        "important_notes": [
            "Tax rates are provided in both PROMILLE (‰) and PERCENT (%) formats",
            "Use PERCENT values for calculations: skattesats_bolig_prosent",
            "Data is directly from SSB official table published 2025",
            "325 out of 357 municipalities have some form of property tax",
            "249 municipalities have property tax on residential properties"
        ],
        "municipalities": municipalities
    }
    
    # Write to JSON file
    with open('norwegian-municipalities-ssb-official-2025.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"✅ Created norwegian-municipalities-ssb-official-2025.json with {len(municipalities)} municipalities")
    
    # Print some examples for verification
    print("\n📊 Sample municipalities for verification:")
    examples = ['Oslo', 'Bergen', 'Trondheim', 'Stavanger']
    for municipality in municipalities:
        if municipality['name'] in examples:
            print(f"• {municipality['name']}: {municipality['skattesats_bolig_promille']}‰ = {municipality['skattesats_bolig_prosent']:.2f}%")

if __name__ == "__main__":
    convert_csv_to_json() 