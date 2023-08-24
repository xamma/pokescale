import requests

"""
Class for handling the request logic.
Takes a name as argument and returns
the response data as dictionary.
"""

class PokeCaller():
    def __init__(self, poke_name:str):
        self.base_url = "https://pokeapi.co/api/v2/pokemon/"
        self.poke_name = poke_name.lower()
        self.res_data = []
        self.query_url = None
        self.poke_data = {}

        self.build_url()
        self.make_request()
        self.return_dict()
        self.get_types()

    def build_url(self):
        self.query_url = self.base_url + self.poke_name

    def make_request(self):
        res_obj = requests.get(self.query_url)
        self.res_data = res_obj.json()
        # print(self.res_data)

    def return_dict(self):
        weight = self.res_data["weight"]
        image = self.res_data["sprites"]["front_shiny"]

        self.poke_data["weight"] = weight
        self.poke_data["image"] = image

        types = self.get_types()
        self.poke_data["types"] = types

    def get_types(self):
        types_list = []
        for ele in self.res_data["types"]:
            if "type" in ele and "name" in ele["type"]:
                types_list.append(ele["type"]["name"])
                types_string = "/".join(types_list)
        return types_string
