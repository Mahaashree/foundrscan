from pytrends.request import TrendReq
from requests.exceptions import RequestException

def get_trend_insights(keywords):
    pytrends = TrendReq(hl='en-US', tz=330)

    try:
        pytrends.build_payload(keywords, cat=0, timeframe='today 5-y', geo='IN', gprop='')
        related_queries = pytrends.related_queries()
        trending_keywords = []

        for k in keywords:
            kw_data = related_queries.get(k)
            if kw_data and 'top' in kw_data and kw_data['top'] is not None:
                trending_keywords += list(kw_data['top']['query'].values[:3])  # top 3
            else:
                print(f"No top queries for {k}")

        geo_trend = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True)
        regional_hotspots = geo_trend.sort_values(by=keywords[0], ascending=False).head(5).index.tolist()

        return {
            "trending_keywords": trending_keywords,
            "regional_hotspots": regional_hotspots
        }

    except (RequestException, IndexError, KeyError) as e:
        print(f"⚠️ Trend error: {e}")
        return {
            "trending_keywords": [],
            "regional_hotspots": []
        }
