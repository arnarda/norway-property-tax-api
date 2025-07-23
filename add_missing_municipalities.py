#!/usr/bin/env python3
import json

# List of municipalities without property tax in 2025
municipalities_without_tax = [
    "Asker", "Austevoll", "Bjørnafjorden", "Bærum", "Drammen", "Dyrøy", 
    "Enebakk", "Færder", "Gjerdrum", "Hasvik", "Hole", "Hægebostad", 
    "Hå", "Kárášjohka - Karasjok", "Klepp", "Larvik", "Lier", "Nannestad", 
    "Nordre Follo", "Rælingen", "Sande", "Sandefjord", "Sola", "Stjørdal", 
    "Sveio", "Søndre Land", "Sørreisa", "Træna", "Tønsberg", "Vanylven", 
    "Øksnes", "Øvre Eiker"
]

def add_missing_municipalities():
    # Read existing JSON
    with open('norwegian-municipalities-ssb-official-2025.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    existing_names = {municipality['name'] for municipality in data['municipalities']}
    
    print(f"📊 Current municipalities in JSON: {len(existing_names)}")
    print(f"📊 Municipalities without property tax: {len(municipalities_without_tax)}")
    
    # Check which municipalities are missing
    missing = []
    already_included = []
    
    for muni in municipalities_without_tax:
        # Handle special case for Karasjok
        name_variants = [muni, "Karasjok"] if "Karasjok" in muni else [muni]
        
        found = any(variant in existing_names for variant in name_variants)
        
        if found:
            already_included.append(muni)
        else:
            missing.append(muni)
    
    print(f"\n✅ Already included: {len(already_included)}")
    for name in already_included:
        print(f"  - {name}")
    
    print(f"\n❌ Missing municipalities: {len(missing)}")
    for name in missing:
        print(f"  - {name}")
    
    # Add missing municipalities
    for name in missing:
        municipality = {
            "name": name,
            "fylke": "Unknown",
            "eiendomsskatt_bolig": False,
            "eiendomsskatt_naering": False,
            "skattesats_bolig_promille": 0,
            "skattesats_bolig_prosent": 0.0,
            "skattesats_naering_promille": 0,
            "skattesats_naering_prosent": 0.0,
            "bunnfradrag": 0,
            "fritak_nye_boliger": False,
            "fritak_aar": 0,
            "eiendomsskattefritak_historiske": False,
            "formuesgrunnlag": False,
            "gjennomsnittlig_skatt_2024": 0
        }
        data['municipalities'].append(municipality)
    
    # Update metadata
    data['total_municipalities'] = len(data['municipalities'])
    data['municipalities_with_property_tax'] = sum(1 for m in data['municipalities'] if m['eiendomsskatt_bolig'] or m['eiendomsskatt_naering'])
    data['municipalities_with_residential_tax'] = sum(1 for m in data['municipalities'] if m['eiendomsskatt_bolig'])
    data['municipalities_without_property_tax'] = len(missing) + len(already_included)
    data['version'] = "2025.3-complete-ssb"
    
    # Add explanation about municipalities without tax
    data['important_notes'].append(f"Includes {len(municipalities_without_tax)} municipalities without property tax (eiendomsskatt_bolig: false)")
    
    # Sort municipalities alphabetically for easier lookup
    data['municipalities'].sort(key=lambda x: x['name'])
    
    # Write updated JSON
    with open('norwegian-municipalities-complete-ssb-2025.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Created norwegian-municipalities-complete-ssb-2025.json")
    print(f"📊 Total municipalities: {data['total_municipalities']}")
    print(f"📊 With property tax: {data['municipalities_with_property_tax']}")
    print(f"📊 With residential tax: {data['municipalities_with_residential_tax']}")
    print(f"📊 Without property tax: {data['municipalities_without_property_tax']}")

if __name__ == "__main__":
    add_missing_municipalities() 