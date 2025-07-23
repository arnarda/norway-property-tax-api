# Norway Property Tax API 🇳🇴

**Complete property tax data for all 357 Norwegian municipalities** - API for the FINN Property Analyzer Chrome Extension.

[![Data Source](https://img.shields.io/badge/Data%20Source-SSB%20(Statistics%20Norway)-blue)](https://www.ssb.no/offentlig-sektor/kommunale-finanser/artikler/kommuner-med-eiendomsskatt)
[![License](https://img.shields.io/badge/License-Public%20Domain-green)](LICENSE)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-2025-brightgreen)](norwegian-municipalities-complete-2025.json)

## 🎯 Data URL

```
https://arnarda.github.io/norway-property-tax-api/norwegian-municipalities-complete-2025.json
```

## 📊 What's Included

- **357 total municipalities** (100% coverage)
- **325 municipalities** with property tax (91%)
- **249 municipalities** with residential property tax (70%)
- Official tax rates, tax-free thresholds, and exemption rules

## 🏛️ Usage Example

```javascript
// Fetch municipality property tax data
fetch('https://arnarda.github.io/norway-property-tax-api/norwegian-municipalities-complete-2025.json')
  .then(response => response.json())
  .then(data => {
    console.log(`Loaded data for ${data.municipalities.length} municipalities`);
    
    // Find a specific municipality
    const oslo = data.municipalities.find(m => m.name === 'Oslo');
    console.log('Oslo property tax rate:', oslo.skattesats_bolig + '%');
  });
```

## 📋 Data Structure

```json
{
  "version": "2025.1",
  "total_municipalities": 357,
  "municipalities": [
    {
      "name": "Oslo",
      "kommune_nummer": "0301",
      "fylke": "Oslo",
      "eiendomsskatt_bolig": true,
      "skattesats_bolig": 0.30,
      "bunnfradrag_bolig": 4000000,
      "fritak_nye_boliger": true,
      "fritak_aar": 5
    }
  ]
}
```

## 🏛️ Examples

| Municipality | Tax Rate | Threshold | Notes |
|-------------|----------|-----------|-------|
| **Oslo** | 0.30% | 4,000,000 kr | 5 years exemption for new buildings |
| **Bergen** | 0.28% | 750,000 kr | No exemption for new buildings |
| **Trondheim** | 0.32% | 550,000 kr | 3 years exemption for new buildings |
| **Steinkjer** | 0.32% | 200,000 kr | Highest rate, lowest threshold |

## 🔄 Updates

### Data Sources
- **Primary**: [SSB (Statistics Norway)](https://www.ssb.no/offentlig-sektor/kommunale-finanser/artikler/kommuner-med-eiendomsskatt)
- **Municipal websites** for detailed regulations
- **Annual municipal budgets**

### Update Schedule
- **January-March**: Check for new SSB data
- **As needed**: Municipal rate changes
- **Automatically reflected**: No Chrome extension update required

## 🛠️ Integration

This API is used by the [FINN Property Analyzer Chrome Extension](https://github.com/arnarda/finn-property-analyzer) to:

1. Detect property location from FINN.no listings
2. Match to municipality using this data
3. Calculate accurate property tax costs
4. Include in total investment analysis

## 📄 License

This data is compiled from official Norwegian government sources and is in the **public domain**. 

---

**Last Updated**: January 2025  
**Data Version**: 2025.1  
**Source**: SSB (Statistics Norway) + Municipal websites
