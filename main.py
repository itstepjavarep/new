import re
import time

import requests
import urllib.parse



def encode_url(text):
    return urllib.parse.quote(text, safe='')


def send_get_request(search_query):
    url = f"https://www.alib.ru/find3.php4?tfind={encode_url(search_query)}"
    # url = f"https://www.alib.ru/find3.php4?tfind={search_query}"
    response = requests.get(url)
    return response


def send_post_request(search_query):
    url = "https://www.alib.ru/subsfind.php4"
    payload = {
        'subsemail': 'zh.semen@yandex.ru',
        # 'subsfind': encode_url(search_query),
        # 'subsfind': encode_url(search_query),
        'subsfind': search_query,
        'Bo1': '%CF%EE%E4%EF%E8%F1%E0%F2%FC%F1%FF'
    }

    response = requests.post(url, data=payload, headers=headers)
    print(response.text)
    return response


def convert_delay_to_seconds(delay_text):
    if delay_text.endswith("секунд"):
        delay_seconds = int(re.search(r'\d+', delay_text).group())
    elif delay_text.endswith("минут"):
        delay_minutes = int(re.search(r'\d+', delay_text).group())
        delay_seconds = delay_minutes * 60
    else:
        delay_seconds = 0
    return delay_seconds


def main():
    # with open("queries.txt", "r", encoding="cp1251") as file:
    with open("../queries.txt", "r") as file:
        for line in file:
            search_query = line.strip()

            try:
                # Отправка запроса
                response = send_post_request(search_query)
                print(f"POST request status code for '{search_query}':", response.status_code)

                # Проверка наличия строки "Слишком частое обращение к сайту."
                if "Слишком частое обращение к сайту." in response.text:
                    # Извлечение текста с задержкой из ответа
                    delay_text = re.search(r'Продолжить работу можно через (.+?)\.', response.text).group(1)
                    # Конвертация задержки в секунды
                    delay_seconds = convert_delay_to_seconds(delay_text)
                    print(f"Too frequent requests. Waiting for {delay_seconds + 1} seconds.")
                    time.sleep(delay_seconds + 1)  # Подождать X + 1 секунду перед повторным запросом

                    # Повторная отправка запроса
                    response = send_post_request(search_query)
                    print(f"POST request status code after delay for '{search_query}':", response.status_code)

                # Дополнительная обработка ответа...
            except requests.exceptions.ConnectionError as e:
                print(f"Ошибка соединения: {e}")
                print("Повторная попытка через 5 минут...")
                time.sleep(300)  # Подождать 5 минут (300 секунд)
                response = send_post_request(search_query)  # Повторная отправка запроса
                print(f"RETRY after ex POST request status code for '{search_query}':", response.status_code)
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при отправке запроса: {e}")


if __name__ == "__main__":
    main()
