
from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import user


class Recipes:
    db = 'user_and_recipes'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.when_made = data['when_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creater = None

    @classmethod
    def show_all_recipes(cls):
        query = 'SELECT * FROM recipes'
        results = connectToMySQL('user_and_recipes').query_db(query)
        return results



    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM recipes JOIN users on recipes.user_id = users.id'
                
        results = connectToMySQL('user_and_recipes').query_db(query)
        recipes = []
        for row in results:
            this_recipe = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            this_recipe.creater = user.User(user_data)
            recipes.append(this_recipe)
        return recipes

    @classmethod
    def one_recipe_with_user(cls,data):
        
        query = 'SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s'
        results = connectToMySQL('user_and_recipes').query_db(query,data)
        print(results)

        result = results[0]
        this_recipe = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['created_at'],
                "updated_at": result['updated_at']
        }
        this_recipe.creater = user.User(user_data)
        return this_recipe

    @classmethod
    def save_recipe(cls,data):
        query = 'INSERT INTO recipes(name, description, instructions, under_30, when_made, user_id) VALUES( %(name)s, %(description)s, %(instructions)s, %(under_30)s, %(when_made)s, %(user_id)s)'        
        result = connectToMySQL('user_and_recipes').query_db(query, data)
        return result

    @classmethod
    def delete(cls,data):
        query = 'DELETE FROM recipes WHERE id = %(id)s'
        result  = connectToMySQL('user_and_recipes').query_db(query,data)
        return result


