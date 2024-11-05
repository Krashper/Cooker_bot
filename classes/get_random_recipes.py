from pprint import pprint
import requests
import re
import nltk

from base_function import BaseFunction
from functions_info import FunctionsInfo
from config_data.config import Config
from data_classes import RecipesNumber


class GetRandomRecipes(BaseFunction):
    def __init__(self, name: str = "Случайный рецепт", api_key: None | str = None):
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

    def __set_recipes_number(self):
        try:
            recipes_number = RecipesNumber()
            flag = True

            while flag:
                recipes_number: int = int(input("Введите кол-во рецептов: "))
                self.recipes_number = recipes_number

                pressed_key = input("Q - выйти, другие клавиши - ввести значение заново: ").lower()
                flag = False if pressed_key == "q" else True

        except Exception as e:
            raise Exception("Ошибка при задании кол-ва рецептов: ", e)

    def __get_api_key(self):
        config = Config().load_config()
        return config.api.api_key

    def __prepare_instructions(self, instructions: str):
        try:
            cleaned_instructions = re.sub('<[^>]+>', ' ', instructions)

            instruction_steps = nltk.sent_tokenize(cleaned_instructions)

            instruction_steps = [step.strip() for step in instruction_steps]

            return instruction_steps
        except Exception as e:
            raise Exception("Ошибка при обработке инструкции по приготовлению блюда: ", e)

    def __get_recipes(self):
        try:
            if self.__api_key is None:
                self.__api_key = self.__get_api_key()

            url = f"https://api.spoonacular.com/recipes/random"
            params = {
                "number": self.recipes_number,
                "apiKey": self.__api_key
            }

            response = requests.get(url, params=params)

            # Обработайте результат
            if response.status_code == 200:
                recipes_information = []
                recipes_data = response.json()

                for recipe_data in recipes_data["recipes"]:
                    recipe_information = {
                        "title": recipe_data["title"],
                        "instruction": self.__prepare_instructions(recipe_data["instructions"])
                    }
                    recipes_information.append(recipe_information)

                return recipes_information
            else:
                raise Exception(f"Ошибка при вызове GET запроса: {response.status_code}")

        except Exception as e:
            raise Exception("Ошибка при получении информации о случайных блюдах через API: ", e)

    def __show_recipes(self, recipes: list):
        try:
            for recipe in recipes:
                print()
                print("Название: ", recipe["title"])
                print()
                for i, step in enumerate(recipe["instruction"]):
                    print(f"{i + 1}. {step}")
                print("-" * 20)
        except Exception as e:
            raise Exception("Ошибка при отображении полученных рецептов через API: ", e)

    def execute_function(self):
        self.__set_recipes_number()
        recipes = self.__get_recipes()
        self.__show_recipes(recipes)
