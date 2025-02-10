INTERFACE = {
    "f0/0":"FastEthernet0/0",
    "g1/0":"GigabitEthernet1/0",
    "g2/0":"GigabitEthernet2/0",
    "g3/0": "GigabitEthernet3/0",
}


NOT_set_INTERFACE = {
    "f0/0":    """\
interface FastEthernet0/0
 no ip address
 shutdown
 duplex full
!
 """,
    "g1/0": """\
interface GigabitEthernet1/0
 no ip address
 shutdown
 negotiation auto
!
""",
    "g2/0":"""\
interface GigabitEthernet2/0
 no ip address
 shutdown
 negotiation auto
!
""",
    "g3/0": """\
interface GigabitEthernet3/0
 no ip address
 shutdown
 negotiation auto
!
""",
}



def get_interface_txt(router_id, router_name,interface_name, adresse, masque)->str:
    if interface_name != "FastEthernet0/0":
        return f"""\
interface {interface_name}
 no ip address
 ip ospf cost 5
 negotiation auto
 ipv6 address {adresse}::{router_id}/{masque}
 ipv6 enable
 ipv6 ospf 4 area 0
!
"""
    return f"""\
interface FastEthernet0/0
 no ip address
 ip ospf cost 1
 duplex full
 ipv6 address {adresse}::{router_id}/{masque}
 ipv6 enable
 ipv6 ospf 4 area 0
!
"""


def Get_loopback(loopback_adress:str,router_id, router_name:str):
    return f"""\
interface Loopback0
 no ip address
 ipv6 address {loopback_adress}::{router_id}/128
 ipv6 enable
 ipv6 ospf 4 area 0
!
"""


def Get_interface(router_id, router_name: str, liens: dict, masque) -> str:
    res = ""
    for interface in INTERFACE.keys():
        if interface not in liens.keys():
            res += NOT_set_INTERFACE.get(interface, "")
        else:
            res += get_interface_txt(router_id, router_name, INTERFACE[interface], liens[interface][0], masque)
    return res



def Get_end(isBorder: bool,router_id, name: str) -> str:
    res = f"""\
ipv6 router ospf 4
 router-id {router_id}.{router_id}.{router_id}.{router_id}
{" passive-interface FastEthernet0/0" if isBorder else ""}
!
"""
    if isBorder:
        res += """\
ipv6 router rip p1
 redistribute connected
!
"""
    return res
