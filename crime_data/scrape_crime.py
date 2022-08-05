from splinter import Browser
from bs4 import BeautifulSoup as soup, Tag
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://nixle.us/DRWAB?_ga=2.243516741.11491368.1659568246-285813041.1659568246'
browser.visit(url)
browser.is_element_present_by_css('div.alert-body', wait_time=1)

alertsHTML = browser.find_by_id('alert-body').html

alertsRaw = soup(alertsHTML, 'html.parser')

browser.quit()

# Build list of from childs
alertsList = []
for i in alertsRaw.childGenerator():
    alertsList.append(i)

# We want to break out of the loop when we reach this point in the HTML
gateClause = "CRIME PREVENTION TIPS"

# Obligatory empty df
crimeDf = pd.DataFrame(columns=['Date', 'Alert', 'Location', 'Description'])

for i in range(len(alertsList)):

    # Find date (there are two variations we need to check for)
    if isinstance(alertsList[i].find('u'), Tag):
        date = alertsList[i].find('u').get_text(strip=True)
    elif alertsList[i].name == 'u':
        date = alertsList[i].get_text(strip=True)

    # Find alert
    elif isinstance(alertsList[i].find('strong'), Tag):
        alert = alertsList[i].get_text(strip=True)

    # Find location
    elif alertsList[i].name == 'strong':
        location = alertsList[i].get_text(strip=True)

    # Find description
    else:
        if alertsList[i].get_text(strip=True) == '':
            pass
        else:
            description = alertsList[i].get_text(strip=True)

            # When a description is collected it means we have a full set of results and we can then output them to our dataframe.
            crimeDf = crimeDf.append({'Date':date,
                                    'Alert':alert,
                                    'Location':location,
                                    'Description':description}, ignore_index=True)

    # Don't need all the following data after "gateClause"
    try:
        if alertsList[i].find('strong').get_text(strip=True) == gateClause:
            print('BREAKING', gateClause)
            break
    except:
        pass

print(crimeDf)