
def Get_BGP(AS_number:str, list_routeur_as:list, router_name, type_routage)->str:
    id = router_name[-1]
    bgp_beighbor = get_bgp_neighbor(list_routeur_as, AS_number, router_name)
    bgp_family = get_bgp_family(list_routeur_as, AS_number,router_name) 
    redistribute = f"redistribute ospf {id}"
    return f"""\
router bgp {AS_number}
 bgp router-id {id}.{id}.{id}.{id}
 bgp log-neighbor-changes
 no bgp default ipv4-unicast
 {bgp_beighbor}
 !
 address-family ipv4
 exit-address-family
 !
 address-family ipv6
  {redistribute if type_routage == "ospf" else ""}
  {bgp_family}
 exit-address-family
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
"""


def get_bgp_family(as_list_routeur_name: list, as_number: str, router_name: str) -> str:
    res = ""
    first = True
    for name in as_list_routeur_name:
        if name != router_name:
            id_voisin = name[-1]
            if first:
                res += f"  neighbor 2001:100::{id_voisin} activate\n"
                first = False
            else:
                res += f"  neighbor 2001:100::{id_voisin} activate\n"
    return res





def get_bgp_neighbor(as_list_routeur_name: list, as_number: str, router_name: str) -> str:
    res = ""
    for i, name in enumerate(as_list_routeur_name):
        if name != router_name:
            id_voisin = name[-1]
            if i > 0:
                res += "\n"  # Ajoute une nouvelle ligne sauf pour le premier élément
            res += f" neighbor 2001:100::{id_voisin} remote-as {as_number}\n"
            res += f" neighbor 2001:100::{id_voisin} update-source Loopback0"
    return res



def Get_BGP_border_router(AS_number:str,list_routeur_as:list, loopback_adress:str, router_name, AS, type_routage, masque, border_routeurs, liens, passive_interface=None)->str:
    id = router_name[-1]
    bgp_beighbor = get_bgp_neighbor(list_routeur_as, AS_number, router_name)
    bgp_family = get_bgp_family(list_routeur_as, AS_number,router_name) 
    bgp_links = get_links(liens, masque)
    redistribute = f"redistribute ospf {id}"
    [adress, as_number] = get_border_routeur_link(border_routeurs, router_name)
    routage_ospf = ""
    if type_routage == "ospf":
        routage_ospf = f"""\
router ospf {id}
 router-id {id}.{id}.{id}.{id}
 redistribute connected subnets
 passive-interface {passive_interface}
!
"""
    return f"""\
{routage_ospf if type_routage == "ospf" else ""}
router bgp {AS_number}
 bgp router-id {id}.{id}.{id}.{id}
 bgp log-neighbor-changes
 no bgp default ipv4-unicast
 {bgp_beighbor}
 neighbor {adress} remote-as {as_number}
 !
 address-family ipv4
  redistribute rip
 exit-address-family
 !
 address-family ipv6
  {redistribute if type_routage == "ospf" else ""}
  network {loopback_adress}::/125    
{bgp_links}
{bgp_family}
  neighbor {adress} activate
 exit-address-family
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
"""
def get_links(liste_liens, masque)-> str:
    print("laaa\n",liste_liens, '\n')
    res = ""
    i = 0
    space = ""
    for lien in liste_liens:
        print(lien)
        if i == 0:
            space = "   "
        res += f"{space}network {lien}::/{masque}\n"
        i += 1
    return res

def get_border_routeur_link(border_routeurs:dict, router_name)->list:
    for (name, link) in border_routeurs.items():
        if name == router_name:
            return [f"{link[0]}::{link[1][-1]}",link[2]]
    
    