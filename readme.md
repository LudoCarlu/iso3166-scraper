# ISO 3166 scraper

This script scrapes the main page, retrieving all country codes and statuses, and then fetches detailed information for each country.

The aim is to obtain the equivalent of the “country-codes.csv” file

At the moment, I only parse the english links

```
pip install requirements.txt
python scraper.py
```

Produce 3 files in an output/ directory

- YYYYMMDD_country-codes.csv
- YYYYMMDD_country-codes-collection.csv
- YYYYMMDD_code-elements-statuses.csv

### Decoding table of ISO 3166-1 alpha-2 codes

This decoding table provides the user with a quick overview of the entire set of alpha-2 codes, some of which are reserved for the exclusive use in the ISO 3166-1 country code standard.

[Decoding table page (english)](https://www.iso.org/obp/ui/#iso:pub:PUB500001:en)

[Decoding table page (french)](https://www.iso.org/obp/ui/fr/)

[Description of a country](https://www.iso.org/obp/ui/#iso:code:3166:AE)

#### Code elements statuses
|Status code|Status|
|:-|:-|
|grs-status0|Unassigned code elements
|grs-status1|Officially assigned code elements
|grs-status2|User-assigned code elements
|grs-status3|Exceptionally reserved code elements
|grs-status4|Transitionally reserved code elements
|grs-status5|Indeterminately reserved code elements
|grs-status6|Formerly assigned code elements


### ISO 3166 — Codes for the representation of names of countries and their subdivisions

|Field name|Field value|
|:-|:-:|
|Alpha-2 code|AE|
|Short name|       |
|Full name|       |
|Alpha-3 code|ARE
|Numeric code|784
|Remarks|
|Independent|Yes
|Territory name|
|Status|Officially assigned

### Files provided by the iso site 
| Sheet / filename | Description |
|:-|:-|
| country-codes | List of all countries with their codes, status and English name|
| country-names | Names of countries, English and French for all countries, otherwise the names in the country’s official languages|
| languages | List of country languages|
| territories | List of country territories|
| subdivision-categories | List of subdivision categories and their names |
| subdivisions | Subdivision codes and their hierarchy|
| subdivision-names | Subdivision names |

- country-codes.csv

|column name|
|:-|
|alpha_2_code|
|alpha_3_code|
|numeric_code|
|independent|
|status|
|short_name_en|
|short_name_uppercase_en|
|full_name_en|

**country-names.csv**

|column name|
|:-|
|alpha_2_code|
|alpha_3_code|
|numeric_code|
|language|
|language_alpha_3_code|
|short_name|
|short_name_uppercase|
|full_name|

**languages.csv**

|column name|
|:-|
|alpha_2_code|
|alpha_3_code|
|numeric_code|
|language_alpha_2_code|
|language_alpha_3_code|
|is_administrative|
|sorting_order|

**territories.csv**

|column name|
|:-|
|alpha_2_code|
|alpha_3_code|
|numeric_code|
|territory_id|
|language|
|language_alpha_3_code|
|territory_name|

**subdivision-categories.csv**

|column name|
|:-|
|alpha_2_code|
|alpha_3_code|
|numeric_code|
|category_id|
|language|
|language_alpha_3_code|
|category_name|
|category_name_plural|

**subdivisions**

|column name|
|:-|
|alpha_2_code|
|alpha_3_code|
|numeric_code|
|subdivision_category_id|
|subdivision_code|
|subdivision_footnote|
|subdivision_parent|

**subdivision-names.csv**

|column name|
|:-|
|alpha_2_code|
|alpha_3_code| 
|numeric_code| 
|subdivision_category_id| 
|subdivision_code| 
|language| 
|language_alpha_3_code| 
|subdivision_name|
|subdivision_name_local_variation|
|romanization_system|


### Descriptions of the fields

| Fieldname | Description |
|:-|:-|
|alpha_2_code |two-letter (alpha-2) code element of the country name (e.g. DE)|
|alpha_3_code| three-letter (alpha-3) code element of the country name (e.g. DEU)|
|numeric_code| three-digit numeric (numeric-3) code element of the country name (e.g. 276)|
|independent|
|status|
|short_name_en| official short form of the country name in English (e.g. Germany)|
|short_name_uppercase_en| official short form of the country name in upper case English (e.g. GERMANY)|
|full_name_en| official long form of the country name in English (e.g. the Federal Republic of Germany)|
|language| Alpha 2 language code to identify the language of names|
|short_name| official short form of the country name
|short_name_uppercase| official short form of the country name in upper case|
|full_name| official long form of the country name|
|language_alpha_2_code Alpha 2 language code|
|language_alpha_3_code Alpha 3 language code|
|is_administrative| YES=language is an administrative language in the country|
|sorting_order| Remarks on the sorting rules for languages|
|territory_id| Territory identifier|
|territory_name| Territory name|
|category_id| Subdivision category identifier|
|category_name| Category name|
|category_name_plural| Category name in plural|
|subdivision_code| Subdivision code|
|subdivision_footnote| Subdivision footnote|
|subdivision_parent| Code of the parent subdivision|
|subdivision_name| Subdivision name|
|romanization_system| Romanization system used to transcript the name|