import json
from time import sleep
import requests
import os

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

'''Небольшой скрипт для парсинга данных со станиц озона.
 Собирает заголовок, описание, все фотографии в максимальном качестве.
 Далее создает папки согласно заголовкам и кладет туда фото и отдельно json и текст описание
 Для работы скрипта нужно папка pic в корневом, или поправить пути для записи'''


chrome_options = Options()
# chrome_options.add_argument("--headless")

serv = Service(executable_path=ChromeDriverManager().install())


#тут список ссылок что нужно обойти :

urls_box = ["https://www.ozon.ru/product/shkatulka-dlya-taro-sila-dlya-hraneniya-4-kolod-i-aksessuarov-chtetsa-20h15h10sm-424910625/?_bctx=CAMQ4JzgLw&asb=xyBp9bZ1nCKq7Mx%252FCm67IuoFFgLWvAtUb0nQ%252Bu04QcU%253D&asb2=9EASpRVnb7wrHUJltsQWRKJFNkICPVQ9dnmGMJ57LU4nXxdc4wLJ0d-GcMz7_xh8&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/shkatulka-dlya-run-kart-taro-i-aksessuarov-gadatelya-runicheskiy-krug-20h15h6-5sm-694264914/?_bctx=CAMQ4JzgLw&asb=PJxijLfjrqS%252FO0NjVTdkN67Xqp%252FQP6PhN%252FqJ3dd%252BGYw%253D&asb2=nyr382obu7BkW8Y7NNLE6SdhETnsHNMp8933TFt9o09Yl2vYhS7LhnTtU1v6TGbE&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/shkatulka-dlya-taro-mir-532054305/?_bctx=CAMQ4JzgLw&asb=Mg6p7Yh8TVl0MgRjPlWPXhQkPv2nNAPrfgOUS5OdceU%253D&asb2=6ECKzwwMLqTwl3_HlpQZdD6I1mFxmZWZqxf_zXfoo03UhbrL-v3EyV1Zi0OueHoJ&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/shkatulka-dlya-taro-koleso-fortuny-590416599/?_bctx=CAMQ4JzgLw&asb=eFzzhhyMK9Vyv%252F7HBrgyw1fXfSdabcu18NFlyJFTGFI%253D&asb2=2VYNtVcwiEatC3KocdPKoM2QnYjSjX-F9auJD2etAXQfXCeb5rTIuBIOojl9TzFr&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/shkatulka-dlya-taro-umerennost-dlya-hraneniya-4-kolod-i-aksessuarov-chtetsa-19-5h14-5h9sm-505119464/?_bctx=CAMQ4JzgLw&asb=9m%252B7bpGGe%252BGxbIinTWWMcRWAkm7atSmAYJIXTJROgaA%253D&asb2=5ULCWJT-Hp8doZnNWH26fgL6DAXp7JiPvOFgoirsWRIBQcXWHZxM1xBnX3Fdi1NH&avtc=1&avte=2&avts=1683745856",
            "https://www.ozon.ru/product/shkatulka-dlya-taro-dyavol-dlya-hraneniya-4-5-kolod-i-aksessuarov-chtetsa-20h15h10sm-811403581/?_bctx=CAMQ4JzgLw&asb=LJ6iJUpJx17VzVCssbj20Dwi%252BTb64AWxg%252BzuPXgNGlg%253D&asb2=WK8ayIsR_MHjExG0yYqz7O67_yGo3QytEnP4Se8hUCN8pfYu8qJrbqtsRS0GJbN3&avtc=1&avte=2&avts=1683745856",
            "https://www.ozon.ru/product/shkatulka-dlya-taro-otshelnik-dlya-hraneniya-4-5-kolod-i-aksessuarov-chtetsa-19-5h14-5h9sm-753726513/?_bctx=CAMQ4JzgLw&asb=rIUHHMicfTWL7gUF0ipDDY6Mmee1aSoIUp3gmrvHA4U%253D&asb2=5iSeF9dLgGabM1MihqAcBvMGzp8Y-7uoW5TsFE55xcjxTisfLnWSNMI_SQk2ADrJ&avtc=1&avte=2&avts=1683745856",

            "https://www.ozon.ru/product/ruchka-mebelnaya-derevyannaya-mini-skoba-anitis-7sm-2sht-539159097/?_bctx=CAMQ4JzgLw&asb=AkwGLydyApSem5HyFjaP7OVGF3PEnZeDZYtSujpTvIM%253D&asb2=U429YTgJOX7UNaAllYhaUtdoXih_qWv1ntZX-je-XBvFq0rsM605eBXZoTqr6KKS&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/ruchka-mebelnaya-derevyannaya-reyling-anitis-20sm-6sht-921512570/?_bctx=CAMQ4JzgLw&asb=sHLs8Bxemy8G1s5isZLmZH%252BvpJJmcYTLFP2CavGWceU%253D&asb2=KSgZmjSQJkATSUynQ65Z-hJkD9aeHhY-ir_dU_e4vXsawUrad6FMTl3uX38zYS_T&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/ruchka-mebelnaya-derevyannaya-reyling-kira-34sm-komplekt-2sht-406291094/?_bctx=CAMQ4JzgLw&asb=VxZ11xOjmP9xcjFuKPdlLGbwOwSq9hPEuW%252FRo2XaCGQ%253D&asb2=Q751ZjxV0ORNJjVu22nQvIEaYQJ_cifirzuan2Mag_4sgxeWWFOssAYz4MeVs8Ic&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/ruchka-mebelnaya-derevyannaya-reyling-anitis-20sm-2sht-532204801/?_bctx=CAMQ4JzgLw&asb=LDpAuDVBGxBa8ru0YC8jpJSF%252BWSMc4LaRmlyyi725W8%253D&asb2=2oSl-ccOAmALOyRMVT3E3zNsRRm5TMVNjHgyv48zolYur2AFvIqagalxqfTd0lvO&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/ruchka-mebelnaya-derevyannaya-skoba-kira-17sm-komplekt-4sht-406032252/?_bctx=CAMQ4JzgLw&asb=2o2lKuoya5GSxVo8TRPLNFo6lhEd%252Bo5MhHeXmEQT9FE%253D&asb2=rhQh6WZ6D5_TRd9s864p2h8OfBrnPgzYhlqVP9PGq_Ezspvusy9ggk3-3yuwz0NS&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/ruchka-mebelnaya-derevyannaya-knopka-kira-s-metallicheskimi-futorkami-2-5h2-5sm-komplekt-4sht-872762636/?_bctx=CAMQ4JzgLw&asb=cnQmR7%252FiXCIfexs1l2vCzYkv7Gl9M9cq45snVhOcRs4%253D&asb2=DVdXyXLSQBP9dj9974a19tCo060uK87YzAH81A5aKVqx5ODcHLhvWX98z_qnMQvB&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/ruchka-mebelnaya-derevyannaya-usilennyy-reyling-kira-34sm-komplekt-2sht-406300507/?_bctx=CAMQ4JzgLw&asb=0JilDyZStzMcoRXy4YCuV7R2%252FUDDwrZFyhkbe9%252Bg6gs%253D&asb2=jTwZDb6U5P2E6aPWJP_VFCRr0i8iq7EwOTlGiQVvnT_F-wpmFp6jrTQNojpPvHsQ&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/ruchka-mebelnaya-derevyannaya-skoba-kira-17sm-komplekt-8sht-615328431/?_bctx=CAMQ4JzgLw&asb=sK2Gm84JF870mRKL1Gce1GdN1cYgB%252BnCfwcn5bIJOAc%253D&asb2=Qn8i9L5otzWPWfGqQLdbMh7oNobGwS17ulQ8OiVvNbui-n3JlQ4HggfxgwiMNLZq&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/ruchka-mebelnaya-derevyannaya-skoba-kira-17sm-komplekt-2sht-807891316/?_bctx=CAMQ4JzgLw&asb=tn5ew6Z%252Ft39KXukzs%252FyWexP4IrBXjCyQ%252BJi39NTCyIk%253D&asb2=YUMpzhDDBdEksE7pD4OIm98M4bUMkyWZ7bpypolb4iVlP2Oc0_r7f6i4pN0qKe88&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/ruchka-mebelnaya-derevyannaya-reyling-anitis-20sm-3sht-615359893/?_bctx=CAMQ4JzgLw&asb=ERMNtQ1CDTfO0qWY8%252FKieEBoR4D0ydGQ3YUuzqFNB8Y%253D&asb2=oCdja7_24oIL1lGtPAtkbhofoi29wfdRbL3jJqZj20UzCkB9btfVdwMo5YktiNcq&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/ruchka-mebelnaya-derevyannaya-skoba-kira-17sm-komplekt-6sht-434480877/?_bctx=CAMQ4JzgLw&asb=sf%252FGVWYVH%252B5VQ4NlB4mYgNGAb6x5SKXtHGPaSPJPpgk%253D&asb2=EeJ1Uf9NRKMalCDso44LSTBDITKBN5sJOrouacY5YG9iU52hDQB61pGZs1XH2nU8&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/ruchka-mebelnaya-derevyannaya-mini-skoba-anitis-7sm-4sht-615327894/?_bctx=CAMQ4JzgLw&asb=6UIbCH5n2G83jm6Ylcj9cCqYRGmbxipHDyTbDpq57zQ%253D&asb2=z4tC1SFbpu3f0Hi8ACU3xHgw13_z25bNFfudTwd_q611Hgil4jDJJo4YhVvCfrto&avtc=1&avte=2&avts=1683734400",
            "https://www.ozon.ru/product/ruchka-mebelnaya-derevyannaya-mini-skoba-kira-11sm-komplekt-2sht-699735812/?_bctx=CAMQ4JzgLw&asb=o1aURBzUVm1ymj8EDdGq17zLkL%252FkHtXnbHIIU29YJFg%253D&asb2=yS78qgWNxS1yHn5Xo1DC0At2P3_4caHUMSe4EMlNdwxu4LLL-XAcnvMkxIuwgKzv&avtc=1&avte=2&avts=1683734400"
            ]



for url in urls_box:

    with webdriver.Chrome(service=serv, options=chrome_options) as driver:
        driver.get(url)
        sleep(5)

        head = driver.find_element(By.CLASS_NAME, "mp3").text.replace('"', '')
        price = driver.find_element(By.CLASS_NAME, "m9m").text.replace("\u2009","").replace("₽","")
        elements_img = driver.find_element(By.CLASS_NAME, "l9r").find_elements(By.CLASS_NAME, "km9")
        for num, el in enumerate(tqdm(elements_img, colour="green")):

            el.click()
            sleep(3)
            pic = driver.find_element(By.XPATH,
                                      '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[1]/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/div/img')
            pi = pic.get_attribute("src")
            if not os.path.exists(f"./pic/{head}"):
                os.mkdir(f"./pic/{head}")

            photo = requests.get(pi).content
            filename = pi.split('/')[-1]

        #  запись фото
            with open(f'pic/{head}/{filename}', "wb" ) as file:
                file.write(photo)

        driver.find_element(By.CLASS_NAME, "s9k").click()
        disc = driver.find_element(By.ID, "section-description").text
        text = [x for x in disc.split("\n") if x][1:]
        data = {"Заголовок": head,
                "Цена": price,
                "Описание": ' '.join(text)}
        text_from_data = [x for x in data.values()]

        # запись файлов

        with open(f"pic/{head}/text.json", 'w', encoding="utf-8") as filej:
            json.dump(data, filej, ensure_ascii=False, indent=4)
        with open(f"pic/{head}/text.txt", 'w', encoding="utf-8") as filet:
            filet.write("\n".join(text_from_data))
        print(data)




