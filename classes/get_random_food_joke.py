from pprint import pprint
import requests
import re
import nltk
from deep_translator import GoogleTranslator

from base_function import BaseFunction
from functions_info import FunctionsInfo
from config_data.config import Config
from data_classes import RecipesNumber


class GetRandomFoodJoke(BaseFunction):
    def __init__(self, name: str = "Случайная шутка о еде", api_key: None | str = None):
        self.name = name
        self.__api_key = api_key
        self.recipes_number = 1

    def get_function_info(self):
        try:
            functions_info = FunctionsInfo.functions
        except Exception as e:
            raise Exception("Ошибка при извлечении информации о функции: ", e)

        if self.name in functions_info.keys():
            return functions_info[self.name]
        else:
            raise Exception(f"Ошибка при извлечении информации о функции: функция {self.name} не найдена в справочнике")

    def __get_api_key(self):
        config = Config().load_config()
        return config.api.api_key

    def __get_joke(self):
        try:
            if self.__api_key is None:
                self.__api_key = self.__get_api_key()

            url = f"https://api.spoonacular.com/food/jokes/random"
            params = {
                "apiKey": self.__api_key
            }

            response = requests.get(url, params=params)

            # Обработайте результат
            if response.status_code == 200:
                data = response.json()
                joke = data["text"]

                return joke
            else:
                raise Exception(f"Ошибка при вызове GET запроса: {response.status_code}")

        except Exception as e:
            raise Exception("Ошибка при получении шутки о еде через API: ", e)

    def __translate_joke(self, joke, from_lang: str = "en", to_lang: str = "ru"):
        try:
            translated_joke = GoogleTranslator(source=from_lang, target=to_lang).translate(joke)

            return translated_joke

        except Exception as e:
            return None

    def __show_joke(self, joke):
        try:
            print("\nШутка на английском:")
            print(joke)

            translated_joke = self.__translate_joke(joke)

            if translated_joke is not None:
                print("\nШутка на русском:")
                print(translated_joke)

            print("-" * 20)

        except Exception as e:
            raise Exception("Ошибка при отображении шутки о еде через API: ", e)

    def execute_function(self):
        joke = self.__get_joke()
        self.__show_joke(joke)