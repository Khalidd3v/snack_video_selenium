from django.shortcuts import render
from urllib.parse import unquote
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_video_info(video_url):
    options = Options()
    options.headless = True

    # Generate a random User-Agent
    user_agent = UserAgent().random
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(video_url)
        wait = WebDriverWait(driver, 10)
        video_tag = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
        if video_tag:
            video_src = video_tag.get_attribute('src')
            driver.quit()
            return video_src
    except Exception as e:
        driver.quit()
        return None

    return None

def homepage(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        if video_url:
            video_src = get_video_info(video_url)
            if video_src:
                video_src_decoded = unquote(video_src)  # Decode the URL
                context = {'video_src': video_src_decoded}
                return render(request, 'app/video_download.html', context)

    return render(request, 'app/homepage.html')
