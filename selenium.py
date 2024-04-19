from Scrap_Functions import *

## Selenium Part
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


def make_storyline_table(url, movie_id):

    firefox_options = Options()
    firefox_options.add_argument('--headless')

    driver = webdriver.Firefox(options=firefox_options)

    wait = WebDriverWait(driver, 5)

    driver.get(url)
    driver.execute_script("arguments[0].scrollIntoView(true);", 
                        driver.find_element(By.XPATH, 
                                            '/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[7]'))
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, 
                                      '/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[6]/div[2]/div[1]/div/div'))).text
    except:
        element = wait.until(EC.presence_of_element_located((By.XPATH, 
                                                            '/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[7]/div[2]/div[1]/div/div/div'))).text
    driver.quit()
    
    storyline = {}
    storyline['movie_id'] = movie_id
    storyline['content'] = element.strip()

    return [storyline]


url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
headers = {'User-Agent': 'Chrome/120.0.0.0', 'Accept-Language': 'en-GB'}

movie_links = ['https://www.imdb.com/title/tt0035446/?ref_=chttp_t_236']
print('Links Saved.')
num_total_movies = len(movie_links)

try:
    directory = sys.argv[1]
except:
    directory = 'Output'

counter = 1

if counter == 1:
    pd.DataFrame([], columns=['movie_id', 'content']).to_csv(os.path.join(directory, 'storyline_table.csv'), index=False)

while counter != num_total_movies + 1:
    url = movie_links[counter - 1]
    movie_id = url.split('/')[4][2:]
    try:
        storyline_temp = make_storyline_table(url, movie_id)
        print(storyline_temp)
        save_to_csv(storyline_temp, os.path.join(directory, 'storyline_table.csv'))
        counter += 1
    except Exception as e:
        error_message = f"Error extracting data for Movie_{counter}: {e}"
        print(error_message)