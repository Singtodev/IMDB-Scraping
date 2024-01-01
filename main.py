import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class Imdb:
    scraped_data = []
    base = "https://www.google.com/"
    fileName = "most-popular-movies-imdb"

    def __init__(self):
        self.driver = webdriver.Chrome()

    def request(self):
        self.driver.get('https://www.imdb.com/chart/moviemeter/?ref_=watch_tpks_chtmvm')
        try:
            movies_container = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul'))
            )
            movies_html = movies_container.get_attribute('outerHTML')
            html = BeautifulSoup(movies_html, 'html.parser')
            movies = html.select('li.ipc-metadata-list-summary-item')
            i = 1;
            for item in movies:
                try:
                    movieName = item.find('h3', class_="ipc-title__text").text
                except:
                    movieName = 'None'
                try:
                    image = item.find('img', class_="ipc-image")['src']
                except:
                    image = 'None'
                try:
                    imdbRate = item.find('span', class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb sc-9ab53865-1 iXEijC ratingGroup--imdb-rating").text.strip()
                except:
                    imdbRate = 'None',
                try:
                    rate = item.find('div', class_="sc-43986a27-7 dBkaPT cli-title-metadata").text
                except AttributeError:
                    rate = 'None'
                    
                self.scraped_data.append({
                    "idx": i,
                    "name": movieName,
                    "image": image,
                    "imdbRate": imdbRate,
                    "rate": rate  # Corrected variable name
                })
                i += 1
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.driver.quit()

    def dump(self):
        try:
            folder_name = "data"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name);
            path = folder_name + "/" + self.fileName + '.json'
            with open(path, 'w' ) as file:
                ## convert array to string and write this to data.json
                result_string = json.dumps(self.scraped_data , indent=2)
                file.write(result_string);
        except:
            print("write file json failed.")
    

obj = Imdb()
obj.request()
obj.dump()