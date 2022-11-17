# IMPORT SECTION #
import bs4, requests, datetime, urllib
from functions.getLinks import getLinks
from functions.writeHistory import writeHistory

# ------------------------------------------------------------------------------------------------------------------------- #

# VARIABLE SECTION #
DATETIME = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# ------------------------------------------------------------------------------------------------------------------------- #

# TAGS SECTION #

# Tags for https://www.lego.com/
LEGO_SPAN_PRICE_CLASS = "Text__BaseText-sc-13i1y3k-0 zkrlj ProductPricestyles__StyledText-sc-vmt0i4-0 tMWye" # Class of the <span> tag containing the price of the item
LEGO_H1_TITLE_CLASS = "Text__BaseText-sc-13i1y3k-0 dKHUnY ProductOverviewstyles__NameText-sc-1a1az6h-7 eGjRAr" # Class of the <h1> tag containing the <span> containing the title
LEGO_SPAN_TITLE_CLASS = "Markup__StyledMarkup-sc-nc8x20-0 dbPAWk" # Class of the <span> tag (contained in H1) containing the title of the item

#Tags for https://www.amazon.it/
AMAZON_SPAN_CLASS = ["a-price aok-align-center", "a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]
AMAZON_SPAN_PRICE_CLASS = "a-offscreen"

# ------------------------------------------------------------------------------------------------------------------------- #

LINKS = getLinks("files/links.txt")

prices = dict()
for link in LINKS:
	item_prices = []
	for website in link:

		# Checking if the webserver answered our HTTP request; if not, make a request again
		while True:
			response = requests.get(website)
			if response.status_code != 503:
					break
		
		# Getting the requested HTML page 
		response = response.text
		soup = bs4.BeautifulSoup(response, "html.parser") # Navigable through HTML tags
		domain_name = '{uri.scheme}://{uri.netloc}/'.format(uri=urllib.request.urlparse(website)) # Getting the domain name of the website in analysis

		# Choosing how and which tag classes it should use, based on the website in analysis
		match domain_name:

			case "https://www.lego.com/":
					item_name = soup.find('h1', LEGO_H1_TITLE_CLASS).find('span', class_ = LEGO_SPAN_TITLE_CLASS).text # We get the title name (only) from the Lego website, since the one on Amazon in not readable
					item_price = ''.join(str(soup.find('span', class_ = LEGO_SPAN_PRICE_CLASS).text[5:].replace("€", "").replace(",", ".")).split())

			case "https://www.amazon.it/":
				counter = 0
				while (counter < len(AMAZON_SPAN_CLASS)):
					counter += 1
					try:
						item_price = ''.join(soup.find("span", AMAZON_SPAN_CLASS).find("span", AMAZON_SPAN_PRICE_CLASS).text.replace("€", "").replace(",", ".").split())
						break
					except:
						if (counter == len(AMAZON_SPAN_CLASS)) - 1:
							item_price = '*'
							print("No price for " + item_name + "on " + domain_name + "was found (possible missing tags?)")
					
		print("Visited " + domain_name + " for " + item_name)

		item_prices.append([item_price, domain_name, DATETIME])
				
	prices[item_name] = item_prices

writeHistory('files/history.txt', prices)
