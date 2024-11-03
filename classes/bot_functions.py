import requests
from pprint import pprint
import re
import nltk

from base_function import BaseFunction
from functions_info import FunctionsInfo
from config_data.config import Config


class Ingredient:
    def __init__(self, value: None | str = None):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if isinstance(value, str) and value.isalpha():
            self.value = value.lower()
        else:
            raise Exception("Ошибка при задании ингредиента: Значение должно быть строчным и содержать только буквы английского алфавита")


class RecipesNumber:
    def __init__(self, value: None | int = None):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if isinstance(value, int) and value <= 10 and value > 0:
            self.value = value
        else:
            raise Exception(
                "Ошибка при задании количества рецептов: Значение должно быть числовым в диапозоне 1-10")



class SearchByIngredients(BaseFunction):
    def __init__(self, name: str = "Рецепт по ингредиентам", api_key: None | str = None):
        self.name = name
        self.__api_key = api_key
        self.ingredients = []
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


    def __set_ingredients(self):
        try:
            ingredient = Ingredient()
            flag = True

            while flag:
                ingredient: str = input("Введите ингредиент (на английском): ")
                self.ingredients.append(ingredient)

                pressed_key = input("Q - выйти, другие клавиши - продолжить: ").lower()
                flag = False if pressed_key == "q" else True
        except Exception as e:
            raise Exception("Ошибка при задании ингредиентов: ", e)

    def __set_recipes_number(self):
        try:
            recipes_number = RecipesNumber()
            flag = True

            while flag:
                recipes_number: int = input("Введите кол-во рецептов: ")
                self.recipes_number = recipes_number

                pressed_key = input("Q - выйти, другие клавиши - продолжить: ").lower()
                flag = False if pressed_key == "q" else True
        except Exception as e:
            raise Exception("Ошибка при задании кол-ва рецептов: ", e)

    def __get_api_key(self):
        config = Config().load_config()
        return config.api.api_key

    def __convert_ingredients_to_param(self):
        if len(self.ingredients) > 0:
            return ",".join(self.ingredients)
        else:
            raise Exception("Ошибка при конвертации ингредиентов в параметр: Не заданы ингредиенты")

    def __get_dish_ids(self):
        try:
            if self.__api_key == None:
                self.__api_key = self.__get_api_key()

            url = "https://api.spoonacular.com/recipes/findByIngredients"
            params = {
                "ingredients": self.__convert_ingredients_to_param(),
                "number": self.recipes_number,
                "apiKey": self.__api_key
            }

            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                dish_ids = [dish["id"] for dish in data]
                return dish_ids
            else:
                raise Exception(f"Ошибка при вызове GET запроса: {response.status_code}")

        except Exception as e:
            raise Exception("Ошибка при получении Id блюд через API: ", e)

    def __prepare_instructions(self, instructions: str):
        try:
            cleaned_instructions = re.sub('<[^>]+>', ' ', instructions)

            instruction_steps = nltk.sent_tokenize(cleaned_instructions)

            instruction_steps = [step.strip() for step in instruction_steps]

            return instruction_steps
        except Exception as e:
            raise Exception("Ошибка при обработке инструкции по приготовлению блюда: ", e)

    def __get_recipe_information(self, dish_id: int):
        try:
            url = f"https://api.spoonacular.com/recipes/{dish_id}/information"
            params = {
                "apiKey": self.__api_key
            }

            response = requests.get(url, params=params)

            # Обработайте результат
            if response.status_code == 200:
                data = response.json()
                recipe_information = {
                    "title": data["title"],
                    "instruction": self.__prepare_instructions(data["instructions"])
                }
                return recipe_information
            else:
                raise Exception(f"Ошибка при вызове GET запроса: {response.status_code}")

        except Exception as e:
            raise Exception("Ошибка при получении информации о блюде через API: ", e)

    def __get_recipes(self):
        try:
            dish_ids = self.__get_dish_ids()
            recipes = []
            for dish_id in dish_ids:
                recipe_information = self.__get_recipe_information(dish_id)
                recipes.append(recipe_information)

            return recipes

        except Exception as e:
            raise Exception("Ошибка при получении рецептов через информацию о блюде через API: ", e)

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
        self.__set_ingredients()
        self.__set_recipes_number()
        recipes = self.__get_recipes()
        self.__show_recipes(recipes)

