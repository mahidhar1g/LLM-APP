from googleapiclient.discovery import build
from src.config import GOOGLE_API_KEY
from src.config import GOOGLE_CSE_ID

my_api_key = GOOGLE_API_KEY #The API_KEY you acquired
my_cse_id = GOOGLE_CSE_ID #The search-engine-ID you created


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


results = google_search('Elon Musk', my_api_key, my_cse_id, num=1)
for result in results:
    print(result)