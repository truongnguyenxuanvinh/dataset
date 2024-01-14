# Import packages
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# Header to set the requests as a browser requests
headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

# Define Page No
len_page = 1000
#len_page = 10

### <font color="red">Functions</font>

# Extra Data as Html object from amazon Review page
def reviewsHtml(url, len_page):
    
    # Empty List define to store all pages html data
    soups = []
    
    # Loop for gather all 3000 reviews from 300 pages via range
    for page_no in range(1, len_page + 1):
        
        # parameter set as page no to the requests body
        params = {
            'ie': 'UTF8',
            'reviewerType': 'all_reviews',
            'filterByStar': 'critical',
            'pageNumber': page_no,
        }
        
        # Request make for each page
        response = requests.get(url, headers=headers)
        
        # Save Html object by using BeautifulSoup4 and lxml parser
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Add single Html page data in master soups list
        soups.append(soup)
        
    return soups

# Grab Reviews name, description, date, stars, title from HTML
def getReviews(html_data):

    # Create Empty list to Hold all data
    data_dicts = []
    
    # Select all Reviews BOX html using css selector
    boxes = html_data.select('div[data-hook="review"]')
    
    # Iterate all Reviews BOX 
    for box in boxes:
        
        # Select Name using css selector and cleaning text using strip()
        # If Value is empty define value with 'N/A' for all.
        try:
            name = box.select_one('[class="a-profile-name"]').text.strip()
        except Exception as e:
            name = 'N/A'

        try:
            stars = box.select_one('[data-hook="review-star-rating"]').text.strip().split(' out')[0]
        except Exception as e:
            stars = 'N/A'  

        try:
            title = box.select_one('[data-hook="review-title"]').text.strip()
        except Exception as e:
            title = 'N/A'

        try:
#            country = box.select_one('[data-hook="review-date"]').text.strip().split('Reviewed in ')[-1].text.strip().split(' on ')[0]
            country = box.select_one('[data-hook="review-date"]').text.strip().split(' on ')[0].split('Reviewed in ')[-1]
            # Convert date str to dd/mm/yyy format
            datetime_str = box.select_one('[data-hook="review-date"]').text.strip().split(' on ')[-1]
            date = datetime.strptime(datetime_str, '%B %d, %Y').strftime("%d/%m/%Y")
        except Exception as e:
            country = 'N/A'
#            datetime_str = 'N/A'
            date = 'N/A'

        try:
            description = box.select_one('[data-hook="review-body"]').text.strip()
        except Exception as e:
            description = 'N/A'

        # create Dictionary with al review data 
        data_dict = {
            'Name' : name,
            'Stars' : stars,
            'Title' : title,
            'Country' : country,
#            'Datetime_str': datetime_str,
            'Date' : date,
            'Description' : description
        }

        # Add Dictionary in master empty List
        data_dicts.append(data_dict)
    
    return data_dicts

### <font color="red">Data Process</font>

#for reviews_url in reviews_urls:
# URL of The amazon Review page
#reviews_url = 'https://www.amazon.com/Legendary-Whitetails-Journeyman-Jacket-Tarmac/product-reviews/B013KW38RQ/'
#reviews_url = "https://www.amazon.com/Apple-iPhone-12-Pro-Max/product-reviews/B09JFFG8D7/"
#reviews_url = "https://www.amazon.com/OPPO-Dual-Sim-Factory-Unlocked-Smartphone/product-reviews/B0B6JCK4RR"
#reviews_url = "https://www.amazon.com/Xiaomi-Version-Factory-Unlocked-Charger/product-reviews/B0BCHBMZRV"
'''reviews_urls = [
    "https://www.amazon.com/SAMSUNG-Factory-Unlocked-Android-Smartphone/product-reviews/B0BLP45GY8",
    "https://www.amazon.com/SAMSUNG-Factory-Unlocked-Android-Smartphone/product-reviews/B0BLP45GY8",
    "https://www.amazon.com/SAMSUNG-Factory-Unlocked-Android-Smartphone/product-reviews/B0BLP45GY8"    
]

reviews_urls = [
    #"https://www.amazon.com/SAMSUNG-Factory-Unlocked-Android-Smartphone/product-reviews/B0BSLR2L5R",
#"https://www.amazon.com/Google-Pixel-7a-Unlocked-Smartphone/product-reviews/B0BZ9XNBRB",
#"https://www.amazon.com/Tracfone-Samsung-Galaxy-A03s-Black/product-reviews/B09T2JFWKR",
#"https://www.amazon.com/Motorola-Stylus-Battery-Unlocked-Emerald/product-reviews/B0BFYRV4CD",
#"https://www.amazon.com/SAMSUNG-Factory-Unlocked-Android-Smartphone/product-reviews/B0BLP57HTN",
#"https://www.amazon.com/SAMSUNG-Factory-Unlocked-Android-Smartphone/product-reviews/B09R6FJWWS",
#"https://www.amazon.com/TCL-Unlocked-Display-Smartphone-Android/product-reviews/B0BTP6PJ9J",
#"https://www.amazon.com/Apple-iPhone-11-64GB-Black/product-reviews/B07ZPKN6YR",
#"https://www.amazon.com/Samsung-Galaxy-S21-5G-Version/product-reviews/B08VLMQ3KS",
#"https://www.amazon.com/Apple-iPhone-GSM-Unlocked-64GB/product-reviews/B0775MV9K2",
#"https://www.amazon.com/SAMSUNG-A14-Unlocked-Worldwide-T-Mobile/product-reviews/B0BXVKVR98",
#"https://www.amazon.com/Apple-iPhone-SE-64GB-Black/product-reviews/B088NQXD8T",
#"https://www.amazon.com/Tracfone-Motorola-moto-Pure-32GB/product-reviews/B09NWDJQ78",
#"https://www.amazon.com/Samsung-Galaxy-128GB-Prism-Black/product-reviews/B082T4F34B",
#"https://www.amazon.com/Samsung-Galaxy-S20-FE-128GB/product-reviews/B08L34JQ9C",
#"https://www.amazon.com/Apple-iPhone-12-64GB-Black/product-reviews/B08PP5MSVB",
#"https://www.amazon.com/Apple-iPhone-12-Mini-Black/product-reviews/B08PPDJWC8",
#"https://www.amazon.com/SAMSUNG-Factory-Unlocked-Android-Smartphone/product-reviews/B0BLP45GY8",
#"https://www.amazon.com/Google-Pixel-6a-Smartphone-Megapixel/product-reviews/B0B3PSRHHN",
#"https://www.amazon.com/Samsung-Factory-Unlocked-Warranty-Renewed/product-reviews/B07PFL39NH",
#"https://www.amazon.com/Apple-iPhone-Plus-64GB-Space/product-reviews/B07YYM3HFW",
#"https://www.amazon.com/Galaxy-S21-Ultra-5G-Smartphone/product-reviews/B096T6Y623",
"https://www.amazon.com/OnePlus-Dual-SIM-Smartphone-Hasselblad-Processor/product-reviews/B0BNWPSCGB",
"https://www.amazon.com/Samsung-Galaxy-A12-Unlocked-T-Mobile/product-reviews/B0991J62ZY",
"https://www.amazon.com/Samsung-Galaxy-A03-Core-International/product-reviews/B09Q98BRRN",
"https://www.amazon.com/Galaxy-S21-Ultra-5G-SM-G998UZKAXAA/product-reviews/B0939K5M9Q",
"https://www.amazon.com/Cat-S22-Flip-Touchscreen-Resistant/product-reviews/B0BTTQGVVW",
"https://www.amazon.com/Stylus-battery-Unlocked-Motorola-Twilight/product-reviews/B09PFC2DVD",
"https://www.amazon.com/Total-Verizon-TCL-32GB-Black/product-reviews/B0BBXBXCFC",
"https://www.amazon.com/Unlocked-Google-Pixel-GA01316-US-Renewed/product-reviews/B08MV7HWFK",
"https://www.amazon.com/Jitterbug-Smart3-Smartphone-for-Seniors/product-reviews/B098KF1G4Q",
"https://www.amazon.com/Nokia-2780-Unlocked-Verizon-T-Mobile/product-reviews/B0BLD393H7",
"https://www.amazon.com/GreatCall-Lively-Flip-Makers-Jitterbug/product-reviews/B08HVVCBHL",
"https://www.amazon.com/TCL-Unlocked-Smartphone-Atlantic-Compatible/product-reviews/B09XV8SCMP",
"https://www.amazon.com/SAMSUNG-Galaxy-Unlocked-Smartphone-Intuitive/product-reviews/B09FRBJZSY",
"https://www.amazon.com/TracFone-Flip-Prepaid-Phone-Locked/product-reviews/B09KZDG9Z2",
"https://www.amazon.com/REDMAGIC-Smartphone-Snapdragon-Dual-Sim-Unlocked/product-reviews/B0C9ZYTJZ3",
"https://www.amazon.com/Sony-Unlocked-Smartphone-Official-Warranty/product-reviews/B0C3WN5JZM",

"https://www.amazon.com/Motorola-battery-Unlocked-Camera-Nebula/product-reviews/B098TXKW8K",
"https://www.amazon.com/Alcatel-Android-Worldwide-Unlocked-Volcano/product-reviews/B07YX9VG5V",
"https://www.amazon.com/Nokia-Unlocked-Hotspot-Assistant-Charcoal/product-reviews/B08SV2Y7J6",
"https://www.amazon.com/Battery-Unlocked-AMOLED-Display-Camera/product-reviews/B0B3B8VY4D",
"https://www.amazon.com/Battery-Unlocked-Display-Capable-Warranty/product-reviews/B0CGY2KM7S"]'''

'''reviews_urls = ["https://www.amazon.com/Apple-iPhone-12-256GB-Blue/product-reviews/B09JFGGR33",
                "https://www.amazon.com/SAMSUNG-Factory-Unlocked-Android-Smartphone/product-reviews/B0BLP57HTN",
                "https://www.amazon.com/Xperia-III-Smartphone-display-lengths/product-reviews/B091YC2SJZ",
                "https://www.amazon.co.jp/-/en/Apple-iPhone-White-SIM-Free-Refurbished/product-reviews/B0928LZ4HD",
                "https://www.amazon.co.jp/-/en/Samsung-Galaxy-Updated-Black-SM-N960U/product-reviews/B07KQFRLDV",
                "https://www.amazon.co.jp/-/en/SEF8332BLKEU/product-reviews/B01LXF0W5L"]'''

#reviews_urls = ["https://www.amazon.co.jp/-/en/SEF8332BLKEU/product-reviews/B01LXF0W5L"]
reviews_urls = ["https://www.amazon.co.jp/-/en/docomo-Galaxy-A20-SC-02M-White/dp/B08185JY75"]

for reviews_url in reviews_urls:

    # Grab all HTML
    html_datas = reviewsHtml(reviews_url, len_page)

    # Empty List to Hold all reviews data
    reviews = []

    # Iterate all Html page 
    for html_data in html_datas:
        
        # Grab review data
        review = getReviews(html_data)
        
        # add review data in reviews empty list
        reviews += review

    # Create a dataframe with reviews Data
    df_reviews = pd.DataFrame(reviews)

    print(df_reviews)

    # Save data
    df_reviews.to_csv('reviews.csv', index=False)

    from transformers import pipeline
    classifier = pipeline("text-classification",model='arpanghoshal/EmoRoBERTa', return_all_scores=True)

#    from transformers import pipeline
#    classifier2 = pipeline("text-classification",model='bhadresh-savani/roberta-base-emotion', return_all_scores=True)

    import pandas as pd
    df = pd.read_csv('reviews.csv')
#    sentiment_list = []
#    df['sentiment'] =""
    emotion_list = []
    df['emotion'] =""

    for i in range(len(df)):
        print(i)
        prediction = classifier(df.iloc[i][4][:1000])
#        prediction = classifier(df.iloc[i][4],)
#        prediction2 = classifier2(df.iloc[i][4], )
#        sentiment_list.append(prediction2)
        emotion_list.append(prediction)

#    series_neg2 = pd.Series(sentiment_list)
#    df['sentiment'] = series_neg2.values

    series_neg = pd.Series(emotion_list)
    df['emotion'] = series_neg.values

    filename = reviews_url[-10:]+".xlsx"
    print(filename)

    #df.to_excel('SAMSUNG-Factory-Unlocked-Android-Smartphone2.xlsx')
    #df.to_excel(reviews_url+".xlsx")

    df.to_excel(filename)