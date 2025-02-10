import yaml
import json
import os
from constante import *
from utils import clean_cfg_file, add_newline_after_third_line
import rip 
import ospf
from bgp import Get_BGP_border_router, Get_BGP

PATH = './router_config_files'

with open('index.yml', 'r') as file:
    prime_service = yaml.safe_load(file) 

pretty_json = json.dumps(prime_service, indent=4)
print(pretty_json)

loopback_adress = prime_service["loopback"]["ip"]
masque = prime_service["adresses"]["masque"]
liens = prime_service["liens"]

contenu = ""

data = {}

for (as_name, as_data) in prime_service["AS"].items():
    data[as_name] = []
    as_number, as_type = as_name.split('-')
    for (routeurName, routeurId) in as_data["list_routeur"].items():
        data[as_name].append([(routeurName, routeurId),0])
    for border_routeur in as_data["border_routeur"]:
        for index in range(len(data[as_name])):
            if data[as_name][index][0] == border_routeur:
                data[as_name][index][1] = 1

print(data)
list_neighbor_by_as = prime_service["AS"]

for (as_name, list_routeur) in data.items():
    as_number, as_type = as_name.split('-')
    for routeur_data in list_routeur:
        contenu = ""
        routeur_name, router_id = routeur_data[0][0], routeur_data[0][1]
        isBorder = routeur_data[1]
        liens_in_as = prime_service["AS"][as_name]["liens"]
        border_routeurs = prime_service["AS"][as_name]["border_routeur"]
        neighbors = list_neighbor_by_as[as_name]["list_routeur"]
        passive_interface = prime_service["passive_interface"]
        if as_type == "rip":
            if isBorder:
                contenu += get_debut_text(routeur_name)
                contenu += rip.Get_loopback(loopback_adress, router_id,routeur_name)
                contenu += rip.Get_interface(router_id, routeur_name, liens[routeur_name])
                contenu += Get_BGP_border_router(as_number, 
                                                 neighbors, 
                                                 loopback_adress, 
                                                 router_id,
                                                 routeur_name, 
                                                 prime_service, 
                                                 as_type, masque, 
                                                 border_routeurs, 
                                                 liens_in_as)
                contenu += rip.Get_end()
                contenu += get_fin_text()
            else:
                contenu += get_debut_text(routeur_name)
                contenu += rip.Get_loopback(loopback_adress, router_id, routeur_name)
                contenu += rip.Get_interface(router_id, routeur_name, liens[routeur_name])
                contenu += Get_BGP(as_number, neighbors, router_id, routeur_name, as_type)
                contenu += rip.Get_end()
                contenu += get_fin_text()
        if as_type == "ospf":
            if isBorder:
                contenu += get_debut_text(routeur_name)
                contenu += ospf.Get_loopback(loopback_adress, router_id, routeur_name)
                contenu += ospf.Get_interface(router_id, routeur_name, liens[routeur_name], masque)
                contenu += Get_BGP_border_router(as_number, 
                                                 neighbors, 
                                                 loopback_adress, 
                                                 router_id,
                                                 routeur_name,
                                                 prime_service,
                                                 as_type, 
                                                 masque, 
                                                 border_routeurs, 
                                                 liens_in_as, 
                                                 passive_interface)
                contenu += ospf.Get_end(isBorder, router_id, routeur_name)
                contenu += get_fin_text()
            else:
                contenu += get_debut_text(routeur_name)
                contenu += ospf.Get_loopback(loopback_adress,router_id, routeur_name)
                contenu += ospf.Get_interface(router_id, routeur_name, liens[routeur_name], masque)
                contenu += Get_BGP(as_number, neighbors, router_id, routeur_name, as_type)
                contenu += ospf.Get_end(isBorder, router_id, routeur_name)
                contenu += get_fin_text()
        filename = PATH + f"/i{router_id}_startup-config.cfg"  
        if os.path.exists(filename):
            os.remove(filename)

        with open(filename, "w") as file:
            file.write(contenu)
        
        clean_cfg_file(filename)
        add_newline_after_third_line(filename)
        

