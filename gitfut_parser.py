from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


class Get_My_Stat:
    def __init__(self, username:str, country:str = 'by') -> None:
        self.username = username
        self.country = country
        
        # Указываем папку для скачивания (абсолютный путь!)
        self.download_dir = os.path.abspath(r"D:\Programming\GitFut Widget")
        os.makedirs(self.download_dir, exist_ok=True)
    
        # Настройки профиля для автоматического скачивания
        self.profile = FirefoxProfile()
        self.profile.set_preference("browser.download.dir", self.download_dir)
        self.profile.set_preference("browser.download.folderList", 2)  # 2 = использовать custom dir
        self.profile.set_preference("browser.download.useDownloadDir", True)
        self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 
            "image/png,image/jpeg,image/jpg,image/gif,application/octet-stream")
        self.profile.set_preference("browser.helperApps.neverAsk.openFile",
            "image/png,image/jpeg,image/jpg,image/gif")
        self.profile.set_preference("pdfjs.disabled", True)  # Отключаем встроенный PDF-просмотрщик

        self.options = Options()
        self.options.add_argument("-headless") 
        # Важно: в headless режиме нужно задать размер окна, иначе кнопка может быть "свернута" и не кликабельна
        self.options.add_argument("--window-size=1920,1080") 
        self.options.profile = self.profile
        self.driver = webdriver.Firefox(options=self.options)

    def get_stat(self):
        if os.path.exists(f'{self.username}-gitfut.png'):
            os.remove(f'{self.username}-gitfut.png')
        # https://gitfut.com/Kordebalet67?country=by
        self.driver.get(f'https://gitfut.com/{self.username}?country={self.country}')
        download_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/main/div[4]/div[2]/div[3]/div[1]/div/div/button[1]'))
    )
        download_button.click()
        time.sleep(2)
        self.driver.quit()


if __name__ == '__main__':
    my_stat = Get_My_Stat('Kordebalet67')
    my_stat.get_stat()
    