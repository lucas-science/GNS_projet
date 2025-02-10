def Get_BGP(AS_number: str, list_routeur_as: list, router_id: int, router_name: str, type_routage: str) -> str:
    bgp_neighbor = get_bgp_neighbor(list_routeur_as, AS_number, router_name)
    bgp_family = get_bgp_family(list_routeur_as, AS_number, router_name)
    redistribute = f"  redistribute ospf {router_id}"
    return f"""\
router bgp {AS_number}
 bgp router-id {router_id}.{router_id}.{router_id}.{router_id}
 bgp log-neighbor-changes
 no bgp default ipv4-unicast
{bgp_neighbor}
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
    for name in as_list_routeur_name:
        if name != router_name:
            id_voisin = name[-1]
            res += f"  neighbor 2001:100::{id_voisin} activate\n"
    return res

def get_bgp_neighbor(as_list_routeur_name: list, as_number: str, router_name: str) -> str:
    res = ""
    for name in as_list_routeur_name:
        if name != router_name:
            id_voisin = name[-1]
            res += f" neighbor 2001:100::{id_voisin} remote-as {as_number}\n"
            res += f" neighbor 2001:100::{id_voisin} update-source Loopback0\n"
    return res



def Get_BGP_border_router(
    AS_number:str,
    list_routeur_as:list,
    loopback_adress:str,
    router_id:int,
    router_name:str, 
    AS, 
    type_routage, 
    masque, 
    border_routeurs, 
    liens, 
    passive_interface=None
)->str:
    bgp_beighbor = get_bgp_neighbor(list_routeur_as, AS_number, router_name)
    bgp_family = get_bgp_family(list_routeur_as, AS_number,router_name) 
    bgp_links = get_links(liens, masque)
    redistribute = f"  redistribute ospf {router_id}"
    [adress, as_number] = get_border_routeur_link(border_routeurs, router_name)
    routage_ospf = ""
    if type_routage == "ospf":
        routage_ospf = f"""\
router ospf {router_id}
 router-id {router_id}.{router_id}.{router_id}.{router_id}
 redistribute connected subnets
 passive-interface {passive_interface}
!
"""
    return f"""\
{routage_ospf if type_routage == "ospf" else ""}
router bgp {AS_number}
 bgp router-id {router_id}.{router_id}.{router_id}.{router_id}
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
    res = ""
    for lien in liste_liens:
        res += f"  network {lien}::/{masque}\n"
    return res

def get_border_routeur_link(border_routeurs:dict, router_name)->list:
    for (name, link) in border_routeurs.items():
        if name == router_name:
            return [f"{link[0]}::{link[1][-1]}",link[2]]
    
    