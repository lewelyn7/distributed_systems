from flask import Flask, render_template
import requests
from flask import request
app = Flask(__name__)
import aiohttp
import traceback
import asyncio

API_URL = "https://www.thecocktaildb.com/api/json/v1/1/"
SEARCH_SUFFIX = "search.php"

FOOD_API_URL = "https://api.edamam.com/api/food-database/v2/parser"
FOOD_API_KEY = "9933bbafe0d12f7c300eecfb5bfceb66"
FOOD_API_APP_ID = "a0dbc8f7"

def standarize_measure(measure):
    def str_to_num(fraction):
        if "/" in num_str:
            nums = num_str.split('/')
            num = int(nums[0])/int(nums[1])
        else:
            num = float(num_str)        
        return num

    try:
        if "cl" in measure:
            num = float(measure.split()[0])
            num *= 10
            return "{:.2f} ml".format(num)
        if "dl" in measure:
            num = float(measure.split()[0])
            num *= 100
            return "{:.2f} ml".format(num)
        if "oz" in measure:
            num_str =  measure.split()[0]
            num = str_to_num(num_str)
            num /= 0.035274
            return "{:.2f} g".format(num)

        if 'cup' in measure:
            num_str =  measure.split()[0]
            num = str_to_num(num_str)
            num *= 236.588237
            return "{:.2f} ml".format(num)
        return measure
    except (TypeError, ValueError):
        return measure

calories_map = {}
units_map = {}
async def get_calorie_info(item, session):
    global calories_map
    global units_map
    if item in calories_map:
        return (item, calories_map[item], units_map[item])
    else:
        params = {
            'app_id': FOOD_API_APP_ID, 
            'app_key': FOOD_API_KEY,
            'ingr': item}

        async with session.get(FOOD_API_URL, params=params) as response:
            data = await response.json()
            if len(data['parsed']) > 0:
                kcal = data['parsed'][0]['food']['nutrients']['ENERC_KCAL']
                val = float(kcal)
                calories_map[item] = val
                units = data['hints'][0]['measures']
                units_map[item] = units
                return (item, val, units)
    return (item, None, None)
    
def calc_portion_calories(ingredient):
    calories100g = ingredient['calories100g']
    quantity = ingredient['measure']
    units_dict = ingredient['units']
    try:
        weight_in_g = 0
        if not quantity:
            return None
        if not calories100g:
            return None
        if 'ml' in quantity:
            val = float(quantity.split()[0])
            val_ounce = val * 0.0338140227
            ounce_weight = list(filter(lambda a: a.get('label', '#')== 'Ounce', units_dict))[0]['weight']
            weight_in_g = val_ounce * ounce_weight
        if 'g' in quantity:
            weight_in_g = float(quantity.split()[0])
        
        calories = weight_in_g * calories100g/100
        return "{:.2f}".format(calories)

    except (TypeError, KeyError, ValueError):
        print(ingredient['name'])
        print(quantity)
        print(units_dict)
        traceback.print_exc()

        return 0

async def calc_calories(ingredients):
    async with aiohttp.ClientSession() as session:
        promises = []
        for ingredient in ingredients:
            promises.append(get_calorie_info(ingredient['name'], session))
        result = await asyncio.gather(*promises)
        calories_dict = {i[0]:i[1] for i in result}
        units_dict = {i[0]:i[2] for i in result}
        print(calories_dict)
        for ingredient in ingredients:
            ingredient['calories100g'] = calories_dict[ingredient['name']]
            ingredient['units'] = units_dict[ingredient['name']]
            ingredient['calories'] = calc_portion_calories(ingredient)


@app.route("/index.html", methods=['GET', 'POST'])                   # at the end point /
def hello():
    form_data = request.form
    drinks = []
    drink_name = form_data.get('drinkName')
    if drink_name:
        response = requests.get(API_URL + SEARCH_SUFFIX, params={'s': drink_name})
        data = response.json()
        if data['drinks']: 
            drinks = data['drinks']
            for drink in drinks:
                ingredients = []
                for i in range(1, 16):
                    if drink[f'strIngredient{i}']:
                        name = drink[f'strIngredient{i}']
                        measure = standarize_measure(drink[f'strMeasure{i}'])

                        ingredients.append({'name': name , 'measure': measure})
                drink['ingredients'] = ingredients
                asyncio.run(calc_calories(ingredients))
                drink['caloriesSum'] = "{:.2f}".format(sum([float(ing['calories']) for ing in ingredients if ing['calories'] != None]))

    print(request.form)

    return render_template('index.html', drinks=drinks)




if __name__ == "__main__":
    app.run(debug=True)