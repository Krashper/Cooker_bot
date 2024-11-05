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