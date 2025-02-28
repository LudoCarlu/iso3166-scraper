from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession
import asyncio
import re
import pandas as pd
from datetime import date, datetime
import time
import logging

RENDER_SLEEP = 5
BASE_URL = "https://www.iso.org/obp/ui/"
COUNTRY_CODES_COLLECTION_PAGE_ID = "#iso:pub:PUB500001:en"

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s",
    style="%",
    datefmt="%Y-%m-%d %H:%M:%S", 
    level = logging.INFO
)

logger = logging.getLogger(__name__)

def none_if(expression_1: str, expression_2: str) -> (None | str):
    """
    The none_if() function returns None if two expressions are equal, otherwise it returns the first expression.
    """
    return None if expression_1 == expression_2 else expression_1

def async_measure_execution_time(async_func) :
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        await async_func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"{async_func.__name__} - elapsed time: {elapsed_time:.3f}s")

    return wrapper

def measure_execution_time(func) :
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"{func.__name__} - elapsed time: {elapsed_time:.3f}s")

    return wrapper

semaphore = asyncio.Semaphore(8)
async def fetch(session, url: str):

    async with semaphore:
        response = await session.get(url)
        await response.html.arender(sleep = RENDER_SLEEP)

        logger.info(f"{url} : {response}")

        return response

async def parse_code_elements_statuses(html :str) -> list[dict[str, str]]:

    code_elements_statuses = []

    soup = BeautifulSoup(html, "html.parser")
    grs_grid_legend_table_rows = soup.find('table', class_ = 'grs-grid-legend').find_all('tr')

    """
    Exemple in HTML
    <tr>
        <td class="grs-status2" width="5%"></td>
        <td align="left" width="95%">User-assigned code elements</td>
    </tr>
    <tr>
        <td class="grs-status2" width="5%"></td>
        <td align="left" width="95%">Exceptionally reserved code elements</td>
    </tr>
    """
    
    for table_row in grs_grid_legend_table_rows:
        table_data = table_row.find_all('td')

        if len(table_data) == 2:
            status_code = table_data[0].get('class')[0]
            status_text = table_data[1].get_text()
            status = status_text.lower().strip().replace(' ', '-').replace('-code-elements', '')
            
            code_elements_statuses.append(
                {
                    'status_code' : status_code,
                    'status_text' : status_text,
                    'status' : status
                }
            )
    #logger.info(f"parsed_code_elements_statuses : {code_elements_statuses}")

    return code_elements_statuses

async def parse_country_codes_collection(html :str) -> list[dict[str, str]]:

    countries = []
    soup = BeautifulSoup(html, "html.parser")

    grs_grid_table_data = soup.find('table', class_ = 'grs-grid').find_all('td', class_ = re.compile("grs-status[0-9]"))

    for td in grs_grid_table_data:
        """
        <td class="grs-status1" title="United States of America (the)">
            <a href="#iso:code:3166:US" target="_blank">US</a>
        </td>
        """
        td_class = td.get('class')[0] # status
        td_title = td.get('title') # short_name_lower_case
        td_anchor = td.find('a')
        td_anchor_href = None # page_id
        td_anchor_text = None # alpha_2_code
        td_text = td.get_text() # alpha_2_code

        if td_anchor is not None:
            td_anchor_href = td_anchor.get('href')
            td_anchor_text = td_anchor.get_text()

        #print(f"""class: {td_class}, title: {td_title}, td_anchor: {td_anchor}, anchor_href: {td_anchor_href}, anchor_text: {td_anchor_text}, td_text: {td_text}""")
        
        countries.append(
            {
                'alpha_2_code' : none_if(td_text,''),
                'short_name_lower_case': none_if(td_title.strip(),''),
                'status_code' : none_if(td_class,''),
                'page_id' : none_if(td_anchor_href,''),
            }
        )

    return countries

async def parse_summary(html :str) -> dict[str,str]:

    soup = BeautifulSoup(html, "html.parser")

    summary = {}

    core_view_lines = soup.find('div', 'core-view-summary').find_all('div', 'core-view-line')

    for line in core_view_lines:
        #print(line)
        core_view_field_name_div = line.find('div', 'core-view-field-name')
        core_view_field_value_div = line.find('div', 'core-view-field-value') 
        field_name = None if core_view_field_name_div is None else core_view_field_name_div.get_text()
        field_value = None if core_view_field_value_div is None else core_view_field_value_div.get_text()

        if field_name is not None:
            summary[field_name] = none_if(field_value,'')

    return summary

def to_snake_case(s: str) -> str:
  return '_'.join(
    re.sub('([A-Z][a-z]+)', r' \1',
    re.sub('([A-Z]+)', r' \1',
    s.replace('-', ' '))).split()).lower()


def to_csv(input:list[dict[str, str]], filename:str) -> None:

    today = date.today()
    df = pd.DataFrame.from_dict(input)
    df.rename(columns=lambda x: to_snake_case(x), inplace=True)

    if filename == 'country-codes':
        country_codes_columns = [
            "alpha_2_code",
            "alpha_3_code",
            "alpha_4_code",
            "numeric_code",
            "short_name",
            "short_name_lower_case",
            "full_name",
            "independent",
            "territory_name",
            "status",
            "status_remark",
            "remarks",
            "remark_part_1",
            "remark_part_2",
            "remark_part_3"
        ]

        df = df[country_codes_columns]

    df.to_csv(f'./output/{today.strftime("%Y%m%d")}_{filename}.csv', sep='|', index=False)

@async_measure_execution_time
async def main() -> None:

    try:
        session = AsyncHTMLSession()

        response = await fetch(session, f"{BASE_URL}{COUNTRY_CODES_COLLECTION_PAGE_ID}")
        html = response.html.html
        #logger.info(f"html : {html}")
        
        code_elements_statuses = await parse_code_elements_statuses(html)
        logger.info(f"code_elements_statuses : {code_elements_statuses}")

        country_codes_collection = await parse_country_codes_collection(html)
        logger.info(f"country_codes_collection[:5] : {country_codes_collection[:5]}")

        tasks = []
        
        for country in country_codes_collection:
            page_id = country.get("page_id")
            
            if page_id is not None:
                tasks.append(fetch(session, f"{BASE_URL}{page_id}"))

        logger.info(f"{len(tasks)} countries to parse")

        responses = await asyncio.gather(*tasks)

        summaries :list = []
        for response in responses:
            summaries.append(await parse_summary(response.html.html))

        logger.info(f"summaries[:5] : {summaries[:5]}")

        to_csv(code_elements_statuses, 'code-elements-statuses')
        to_csv(country_codes_collection, 'country-codes-collection')
        to_csv(summaries, 'country-codes')

    except Exception as e:
        logger.error(e)

    finally:
        await session.close()

if __name__ == '__main__':

    asyncio.run(main())


    
    # Additional information
    # Excepted fields : Administrative language(s) alpha-2 | Administrative language(s) alpha-3 | Local short name


    # Subdivisions
    # Excepted fields : Subdivision category | 3166-2 code | Subdivision name | Local variant | Language code | Romanization system | Parent subdivision
    # Change history of country code
    # Excepted fields : Effective date of change | Short description of change (en) | Short description of change (fr)
