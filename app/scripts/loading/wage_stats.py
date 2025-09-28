# Web scraping
import requests
from bs4 import BeautifulSoup as bs

from datetime import datetime

def main():
    current_year = datetime.now().year

    # TODO: check the accessability of the URL
    url = "https://www.kurzy.cz/mzda/minimalni-mzda-" + str(current_year)

    page = requests.get(url, timeout=10)
    soup = bs(page.content, "html.parser")

    # Get minimum gross wage (mgw) for current year in Kč
    # TODO: throw error in case of invalid element/attribute
    mgw_elem_id = "cC3"
    mgw_elem = soup.find(id=mgw_elem_id)
    mgw_value = mgw_elem.get("value")

    return mgw_value

if __name__=="__main__":
    main()