# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json

import pytest

from ansible.module_utils.common.text.converters import to_text
from ansible_collections.community.general.plugins.modules import nmcli
from ansible.module_utils.basic import AnsibleModule

pytestmark = pytest.mark.usefixtures('patch_ansible_module')

TESTCASE_CONNECTION = [
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'generic',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'team',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'bond',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'bond-slave',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'bridge',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'vlan',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'vxlan',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'gre',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'ipip',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'sit',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'dummy',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'gsm',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'wireguard',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'vpn',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'infiniband',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'macvlan',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
    {
        'type': 'loopback',
        'conn_name': 'non_existent_nw_device',
        'state': 'absent',
        '_ansible_check_mode': True,
    },
]

TESTCASE_GENERIC = [
    {
        'type': 'generic',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'generic_non_existant',
        'ip4': '10.10.10.10/24',
        'gw4': '10.10.10.1',
        'state': 'present',
        '_ansible_check_mode': False,
    },
]

TESTCASE_GENERIC_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              generic_non_existant
connection.autoconnect:                 yes
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.gateway:                           10.10.10.1
ipv4.route-metric:                      -1
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
"""

TESTCASE_GENERIC_DIFF_CHECK = [
    {
        'type': 'generic',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'generic_non_existant',
        'ip4': '10.10.10.10/24',
        'gw4': '10.10.10.2',
        'route_metric4': -1,
        'state': 'present',
        '_ansible_check_mode': False,
    },
]

TESTCASE_GENERIC_MODIFY_ROUTING_RULES = [
    {
        'type': 'generic',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'generic_non_existant',
        'ip4': '10.10.10.10/24',
        'gw4': '10.10.10.1',
        'routing_rules4': ['priority 5 from 10.0.0.0/24 table 5000', 'priority 10 from 10.0.1.0/24 table 5001'],
        'state': 'present',
        '_ansible_check_mode': False,
    },
]

TESTCASE_GENERIC_MODIFY_ROUTING_RULES_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              generic_non_existant
connection.autoconnect:                 yes
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.gateway:                           10.10.10.1
ipv4.routing-rules:                     priority 5 from 10.0.0.0/24 table 5000, priority 10 from 10.0.1.0/24 table 5001
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
"""

TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_ROUTE = [
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'ip6': '2001:beef:cafe:10::1/64',
        'routes6': ['fd2e:446f:d85d:5::/64 2001:beef:cafe:10::2'],
        'method6': 'manual',
        'state': 'present',
        '_ansible_check_mode': False,
    },
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'ip6': '2001:beef:cafe:10::1/64',
        'routes6_extended': [{'ip': 'fd2e:446f:d85d:5::/64',
                              'next_hop': '2001:beef:cafe:10::2'}],
        'method6': 'manual',
        'state': 'present',
        '_ansible_check_mode': False,
    },
]

TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_ROUTE_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              ethernet_non_existant
connection.autoconnect:                 yes
ipv4.method:                            auto
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            manual
ipv6.addresses:                         2001:beef:cafe:10::1/64
ipv6.routes:                            { ip = fd2e:446f:d85d:5::/64, nh = 2001:beef:cafe:10::2 }
ipv6.route-metric:                      -1
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
"""

TESTCASE_ETHERNET_MOD_IPV4_INT_WITH_ROUTE_AND_METRIC = [
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'routes4': ['192.168.200.0/24 192.168.1.1'],
        'route_metric4': 10,
        'state': 'present',
        '_ansible_check_mode': False,
    },
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'routes4_extended': [{'ip': '192.168.200.0/24', 'next_hop': '192.168.1.1'}],
        'route_metric4': 10,
        'state': 'present',
        '_ansible_check_mode': False,
    },
]

TESTCASE_ETHERNET_MOD_IPV4_INT_WITH_ROUTE_AND_METRIC_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              ethernet_non_existant
connection.autoconnect:                 yes
ipv4.method:                            manual
ipv4.addresses:                         192.168.1.10
ipv4.routes:                            { ip = 192.168.200.0/24, nh = 192.168.1.1 }
ipv4.route-metric:                      10
"""

TESTCASE_ETHERNET_MOD_IPV4_INT_WITH_ROUTE_AND_METRIC_CLEAR = [
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'routes4': [],
        'state': 'present',
        '_ansible_check_mode': False,
        '_ansible_diff': True,
    },
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'routes4_extended': [],
        'state': 'present',
        '_ansible_check_mode': False,
        '_ansible_diff': True,
    },
]

TESTCASE_ETHERNET_MOD_IPV6_INT_WITH_ROUTE_AND_METRIC = [
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'routes6': ['fd2e:446f:d85d:5::/64 2001:beef:cafe:10::2'],
        'route_metric6': 10,
        'state': 'present',
        '_ansible_check_mode': False,
    },
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'routes6_extended': [{'ip': 'fd2e:446f:d85d:5::/64', 'next_hop': '2001:beef:cafe:10::2'}],
        'route_metric6': 10,
        'state': 'present',
        '_ansible_check_mode': False,
    },
]

TESTCASE_ETHERNET_MOD_IPV6_INT_WITH_ROUTE_AND_METRIC_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              ethernet_non_existant
connection.autoconnect:                 yes
ipv6.method:                            manual
ipv6.addresses:                         2001:beef:cafe:10::1/64
ipv6.routes:                            { ip = fd2e:446f:d85d:5::/64, nh = 2001:beef:cafe:10::2 }
ipv6.route-metric                       10
"""

TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_MULTIPLE_ROUTES = [
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'ip6': '2001:beef:cafe:10::1/64',
        'routes6': ['fd2e:446f:d85d:5::/64 2001:beef:cafe:10::2', 'fd2e:8890:abcd:25::/64 2001:beef:cafe:10::5'],
        'method6': 'manual',
        'state': 'present',
        '_ansible_check_mode': False,
    },
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'ip6': '2001:beef:cafe:10::1/64',
        'routes6_extended': [{'ip': 'fd2e:446f:d85d:5::/64', 'next_hop': '2001:beef:cafe:10::2'},
                             {'ip': 'fd2e:8890:abcd:25::/64', 'next_hop': '2001:beef:cafe:10::5'}],
        'method6': 'manual',
        'state': 'present',
        '_ansible_check_mode': False,
    },
]

TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_MULTIPLE_ROUTES_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              ethernet_non_existant
connection.autoconnect:                 yes
ipv4.method:                            auto
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            manual
ipv6.addresses:                         2001:beef:cafe:10::1/64
ipv6.routes:                            { ip = fd2e:446f:d85d:5::/64, nh = 2001:beef:cafe:10::2 }; { ip = fd2e:8890:abcd:25::/64, nh = 2001:beef:cafe:10::5 }
ipv6.route-metric:                      -1
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
"""

TESTCASE_ETHERNET_ADD_SRIOV_VFS = [
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'sriov': {
            'total-vfs': 16,
            'vfs': '0 spoof-check=true vlans=100',
        },
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_ETHERNET_ADD_SRIOV_VFS_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              ethernet_non_existant
connection.autoconnect:                 yes
sriov.total-vfs:                        16
sriov.vfs:                              0 spoof-check=true vlans=100
"""

TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_ROUTE_AND_METRIC = [
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'method4': 'disabled',
        'ip6': '2001:beef:cafe:10::1/64',
        'routes6': ['fd2e:446f:d85d:5::/64 2001:beef:cafe:10::2'],
        'route_metric6': 5,
        'method6': 'manual',
        'state': 'present',
        '_ansible_check_mode': False,
    },
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'method4': 'disabled',
        'ip6': '2001:beef:cafe:10::1/64',
        'routes6_extended': [{'ip': 'fd2e:446f:d85d:5::/64', 'next_hop': '2001:beef:cafe:10::2'}],
        'route_metric6': 5,
        'method6': 'manual',
        'state': 'present',
        '_ansible_check_mode': False,
    },
]

TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_ROUTE_AND_METRIC_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              ethernet_non_existant
connection.autoconnect:                 yes
ipv4.method:                            auto
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            manual
ipv6.addresses:                         2001:beef:cafe:10::1/64
ipv6.routes:                            { ip = fd2e:446f:d85d:5::/64, nh = 2001:beef:cafe:10::2 }
ipv6.route-metric:                      5
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
"""

TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_MULTIPLE_ROUTES_AND_METRIC = [
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'method4': 'disabled',
        'ip6': '2001:beef:cafe:10::1/64',
        'routes6': ['fd2e:446f:d85d:5::/64 2001:beef:cafe:10::2', 'fd2e:8890:abcd:25::/64 2001:beef:cafe:10::5'],
        'route_metric6': 5,
        'method6': 'manual',
        'state': 'present',
        '_ansible_check_mode': False,
    },
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'method4': 'disabled',
        'ip6': '2001:beef:cafe:10::1/64',
        'routes6_extended': [{'ip': 'fd2e:446f:d85d:5::/64', 'next_hop': '2001:beef:cafe:10::2'},
                             {'ip': 'fd2e:8890:abcd:25::/64', 'next_hop': '2001:beef:cafe:10::5'}],
        'route_metric6': 5,
        'method6': 'manual',
        'state': 'present',
        '_ansible_check_mode': False,
    },
]

TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_MULTIPLE_ROUTES_AND_METRIC_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              ethernet_non_existant
connection.autoconnect:                 yes
ipv4.method:                            auto
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            manual
ipv6.addresses:                         2001:beef:cafe:10::1/64
ipv6.routes:                            { ip = fd2e:446f:d85d:5::/64, nh = 2001:beef:cafe:10::2 }; { ip = fd2e:8890:abcd:25::/64, nh = 2001:beef:cafe:10::5 }
ipv6.route-metric:                      5
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
"""

TESTCASE_GENERIC_DNS4_SEARCH = [
    {
        'type': 'generic',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'generic_non_existant',
        'ip4': '10.10.10.10/24',
        'gw4': '10.10.10.1',
        'state': 'present',
        'dns4_search': 'search.redhat.com',
        'dns6_search': 'search6.redhat.com',
        '_ansible_check_mode': False,
    }
]

TESTCASE_GENERIC_DNS4_SEARCH_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              generic_non_existant
connection.autoconnect:                 yes
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.gateway:                           10.10.10.1
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.dns-search:                        search.redhat.com
ipv4.may-fail:                          yes
ipv6.dns-search:                        search6.redhat.com
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
"""

TESTCASE_GENERIC_DNS4_OPTIONS = [
    {
        'type': 'generic',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'generic_non_existant',
        'ip4': '10.10.10.10/24',
        'gw4': '10.10.10.1',
        'state': 'present',
        'dns4_options': [],
        'dns6_options': [],
        '_ansible_check_mode': False,
    }
]

TESTCASE_GENERIC_DNS4_OPTIONS_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              generic_non_existant
connection.autoconnect:                 yes
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.gateway:                           10.10.10.1
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.dns-options:                       --
ipv4.may-fail:                          yes
ipv6.dns-options:                       --
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
"""

TESTCASE_GENERIC_ZONE = [
    {
        'type': 'generic',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'generic_non_existant',
        'ip4': '10.10.10.10/24',
        'gw4': '10.10.10.1',
        'state': 'present',
        'zone': 'external',
        '_ansible_check_mode': False,
    }
]

TESTCASE_GENERIC_ZONE_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              generic_non_existant
connection.autoconnect:                 yes
connection.zone:                        external
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.gateway:                           10.10.10.1
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
"""

TESTCASE_GENERIC_ZONE_ONLY = [
    {
        'type': 'generic',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'generic_non_existant',
        'state': 'present',
        'zone': 'public',
        '_ansible_check_mode': False,
    }
]

TESTCASE_BOND = [
    {
        'type': 'bond',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'bond_non_existant',
        'mode': 'active-backup',
        'xmit_hash_policy': 'layer3+4',
        'ip4': '10.10.10.10/24',
        'gw4': '10.10.10.1',
        'state': 'present',
        'primary': 'non_existent_primary',
        '_ansible_check_mode': False,
    }
]

TESTCASE_BOND_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              bond_non_existant
connection.autoconnect:                 yes
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.gateway:                           10.10.10.1
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
bond.options:                           mode=active-backup,primary=non_existent_primary,xmit_hash_policy=layer3+4
"""

TESTCASE_BRIDGE = [
    {
        'type': 'bridge',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'br0_non_existant',
        'ip4': '10.10.10.10/24',
        'gw4': '10.10.10.1',
        'mac': '52:54:00:ab:cd:ef',
        'maxage': 100,
        'stp': True,
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_BRIDGE_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              br0_non_existant
connection.autoconnect:                 yes
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.gateway:                           10.10.10.1
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
bridge.mac-address:                     52:54:00:AB:CD:EF
bridge.stp:                             yes
bridge.max-age:                         100
bridge.ageing-time:                     300
bridge.hello-time:                      2
bridge.priority:                        128
bridge.forward-delay:                   15
"""

TESTCASE_BRIDGE_SLAVE = [
    {
        'type': 'bridge-slave',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'br0_non_existant',
        'hairpin': True,
        'path_cost': 100,
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_BRIDGE_SLAVE_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              br0_non_existant
connection.autoconnect:                 yes
connection.slave-type:                  bridge
ipv4.never-default:                     no
bridge-port.path-cost:                  100
bridge-port.hairpin-mode:               yes
bridge-port.priority:                   32
"""

TESTCASE_TEAM = [
    {
        'type': 'team',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'team0_non_existant',
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_TEAM_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              team0_non_existant
connection.autoconnect:                 yes
connection.type:                        team
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
team.runner:                            roundrobin
team.runner-fast-rate:                  no
"""

TESTCASE_TEAM_HWADDR_POLICY_FAILS = [
    {
        'type': 'team',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'team0_non_existant',
        'runner_hwaddr_policy': 'by_active',
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_TEAM_RUNNER_FAST_RATE = [
    {
        'type': 'team',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'team0_non_existant',
        'runner': 'lacp',
        'runner_fast_rate': True,
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_TEAM_RUNNER_FAST_RATE_FAILS = [
    {
        'type': 'team',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'team0_non_existant',
        'runner_fast_rate': True,
        'state': 'present',
        '_ansible_check_mode': False,
    },
    {
        'type': 'team',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'team0_non_existant',
        'state': 'present',
        'runner_fast_rate': False,
        '_ansible_check_mode': False,
    },
    {
        'type': 'team',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'team0_non_existant',
        'state': 'present',
        'runner': 'activebackup',
        'runner_fast_rate': False,
        '_ansible_check_mode': False,
    },
    {
        'type': 'team',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'team0_non_existant',
        'state': 'present',
        'runner': 'activebackup',
        'runner_fast_rate': True,
        '_ansible_check_mode': False,
    }
]

TESTCASE_TEAM_RUNNER_FAST_RATE_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              team0_non_existant
connection.autoconnect:                 yes
connection.type:                        team
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
team.runner:                            lacp
team.runner-fast-rate:                  yes
"""

TESTCASE_TEAM_SLAVE = [
    {
        'type': 'team-slave',
        'conn_name': 'non_existent_nw_slaved_device',
        'ifname': 'generic_slaved_non_existant',
        'master': 'team0_non_existant',
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_TEAM_SLAVE_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_slaved_device
connection.interface-name:              generic_slaved_non_existant
connection.autoconnect:                 yes
connection.master:                      team0_non_existant
connection.slave-type:                  team
802-3-ethernet.mtu:                     auto
"""

TESTCASE_VLAN = [
    {
        'type': 'vlan',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'vlan_not_exists',
        'ip4': '10.10.10.10/24',
        'gw4': '10.10.10.1',
        'vlanid': 10,
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_VLAN_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              vlan_not_exists
connection.autoconnect:                 yes
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.gateway:                           10.10.10.1
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
vlan.id:                                10
802-3-ethernet.mtu:                     auto
"""

TESTCASE_VXLAN = [
    {
        'type': 'vxlan',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'vxlan-existent_nw_device',
        'vxlan_id': 11,
        'vxlan_local': '192.168.225.5',
        'vxlan_remote': '192.168.225.6',
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_VXLAN_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              vxlan-existent_nw_device
connection.autoconnect:                 yes
vxlan.id:                               11
vxlan.local:                            192.168.225.5
vxlan.remote:                           192.168.225.6
"""

TESTCASE_GRE = [
    {
        'type': 'gre',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'gre-existent_nw_device',
        'ip_tunnel_dev': 'non_existent_gre_device',
        'ip_tunnel_local': '192.168.225.5',
        'ip_tunnel_remote': '192.168.225.6',
        'ip_tunnel_input_key': '1',
        'ip_tunnel_output_key': '2',
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_GRE_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              gre-existent_nw_device
connection.autoconnect:                 yes
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
ip-tunnel.mode:                         gre
ip-tunnel.parent:                       non_existent_gre_device
ip-tunnel.local:                        192.168.225.5
ip-tunnel.remote:                       192.168.225.6
ip-tunnel.input-key:                    1
ip-tunnel.output-key:                   2
"""

TESTCASE_IPIP = [
    {
        'type': 'ipip',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ipip-existent_nw_device',
        'ip_tunnel_dev': 'non_existent_ipip_device',
        'ip_tunnel_local': '192.168.225.5',
        'ip_tunnel_remote': '192.168.225.6',
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_IPIP_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              ipip-existent_nw_device
connection.autoconnect:                 yes
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
ip-tunnel.mode:                         ipip
ip-tunnel.parent:                       non_existent_ipip_device
ip-tunnel.local:                        192.168.225.5
ip-tunnel.remote:                       192.168.225.6
"""

TESTCASE_SIT = [
    {
        'type': 'sit',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'sit-existent_nw_device',
        'ip_tunnel_dev': 'non_existent_sit_device',
        'ip_tunnel_local': '192.168.225.5',
        'ip_tunnel_remote': '192.168.225.6',
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_SIT_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              sit-existent_nw_device
connection.autoconnect:                 yes
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
ip-tunnel.mode:                         sit
ip-tunnel.parent:                       non_existent_sit_device
ip-tunnel.local:                        192.168.225.5
ip-tunnel.remote:                       192.168.225.6
"""

TESTCASE_ETHERNET_DHCP = [
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'dhcp_client_id': '00:11:22:AA:BB:CC:DD',
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_ETHERNET_DHCP_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              ethernet_non_existant
connection.autoconnect:                 yes
802-3-ethernet.mtu:                     auto
ipv4.method:                            auto
ipv4.dhcp-client-id:                    00:11:22:AA:BB:CC:DD
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
"""

TESTCASE_ETHERNET_STATIC = [
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'ip4': '10.10.10.10/24',
        'gw4': '10.10.10.1',
        'dns4': ['1.1.1.1', '8.8.8.8'],
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_LOOPBACK = [
    {
        'type': 'loopback',
        'conn_name': 'lo',
        'ifname': 'lo',
        'ip4': '127.0.0.1/8',
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_LOOPBACK_MODIFY = [
    {
        'type': 'loopback',
        'conn_name': 'lo',
        'ifname': 'lo',
        'ip4': ['127.0.0.1/8', '127.0.0.2/8'],
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_ETHERNET_STATIC_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              ethernet_non_existant
connection.autoconnect:                 yes
802-3-ethernet.mtu:                     auto
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.gateway:                           10.10.10.1
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv4.dns:                               1.1.1.1,8.8.8.8
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
"""

TESTCASE_LOOPBACK_SHOW_OUTPUT = """\
connection.id:                          lo
connection.interface-name:              lo
connection.autoconnect:                 yes
ipv4.method:                            manual
ipv4.addresses:                         127.0.0.1/8
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            manual
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
"""

TESTCASE_ETHERNET_STATIC_MULTIPLE_IP4_ADDRESSES = [
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'ip4': ['10.10.10.10/32', '10.10.20.10/32'],
        'gw4': '10.10.10.1',
        'dns4': ['1.1.1.1', '8.8.8.8'],
        'state': 'present',
        '_ansible_check_mode': False,
    },
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'ip4': ['10.10.10.10', '10.10.20.10'],
        'gw4': '10.10.10.1',
        'dns4': ['1.1.1.1', '8.8.8.8'],
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_ETHERNET_STATIC_IP6_PRIVACY_AND_ADDR_GEN_MODE = [
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'ip6': '2001:db8::cafe/128',
        'gw6': '2001:db8::cafa',
        'dns6': ['2001:4860:4860::8888'],
        'state': 'present',
        'ip_privacy6': 'prefer-public-addr',
        'addr_gen_mode6': 'eui64',
        '_ansible_check_mode': False,
    }
]

TESTCASE_ETHERNET_STATIC_MULTIPLE_IP6_ADDRESSES = [
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'ip6': ['2001:db8::cafe/128', '2002:db8::cafe/128'],
        'gw6': '2001:db8::cafa',
        'dns6': ['2001:4860:4860::8888', '2001:4860:4860::8844'],
        'state': 'present',
        '_ansible_check_mode': False,
    },
    {
        'type': 'ethernet',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'ethernet_non_existant',
        'ip6': ['2001:db8::cafe', '2002:db8::cafe'],
        'gw6': '2001:db8::cafa',
        'dns6': ['2001:4860:4860::8888', '2001:4860:4860::8844'],
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_ETHERNET_STATIC_MULTIPLE_IP4_ADDRESSES_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              ethernet_non_existant
connection.autoconnect:                 yes
802-3-ethernet.mtu:                     auto
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/32, 10.10.20.10/32
ipv4.gateway:                           10.10.10.1
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv4.dns:                               1.1.1.1,8.8.8.8
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
"""

TESTCASE_ETHERNET_STATIC_IP6_ADDRESS_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              ethernet_non_existant
connection.autoconnect:                 yes
802-3-ethernet.mtu:                     auto
ipv6.method:                            manual
ipv6.addresses:                         2001:db8::cafe/128
ipv6.gateway:                           2001:db8::cafa
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
ipv6.never-default:                     no
ipv6.may-fail:                          yes
ipv6.dns:                               2001:4860:4860::8888,2001:4860:4860::8844
ipv4.method:                            disabled
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
"""


TESTCASE_ETHERNET_STATIC_MULTIPLE_IP6_ADDRESSES_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              ethernet_non_existant
connection.autoconnect:                 yes
802-3-ethernet.mtu:                     auto
ipv6.method:                            manual
ipv6.addresses:                         2001:db8::cafe/128, 2002:db8::cafe/128
ipv6.gateway:                           2001:db8::cafa
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
ipv6.never-default:                     no
ipv6.may-fail:                          yes
ipv6.dns:                               2001:4860:4860::8888,2001:4860:4860::8844
ipv4.method:                            disabled
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
"""

TESTCASE_WIRELESS = [
    {
        'type': 'wifi',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'wireless_non_existant',
        'ip4': '10.10.10.10/24',
        'ssid': 'Brittany',
        'wifi': {
            'hidden': True,
            'mode': 'ap',
        },
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_SECURE_WIRELESS = [
    {
        'type': 'wifi',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'wireless_non_existant',
        'ip4': '10.10.10.10/24',
        'ssid': 'Brittany',
        'wifi_sec': {
            'key-mgmt': 'wpa-psk',
            'psk': 'VERY_SECURE_PASSWORD',
        },
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_DEFAULT_WIRELESS_SHOW_OUTPUT = """\
802-11-wireless.ssid:                   --
802-11-wireless.mode:                   infrastructure
802-11-wireless.band:                   --
802-11-wireless.channel:                0
802-11-wireless.bssid:                  --
802-11-wireless.rate:                   0
802-11-wireless.tx-power:               0
802-11-wireless.mac-address:            --
802-11-wireless.cloned-mac-address:     --
802-11-wireless.generate-mac-address-mask:--
802-11-wireless.mac-address-blacklist:  --
802-11-wireless.mac-address-randomization:default
802-11-wireless.mtu:                    auto
802-11-wireless.seen-bssids:            --
802-11-wireless.hidden:                 no
802-11-wireless.powersave:              0 (default)
802-11-wireless.wake-on-wlan:           0x1 (default)
802-11-wireless.ap-isolation:           -1 (default)
"""

TESTCASE_DEFAULT_SECURE_WIRELESS_SHOW_OUTPUT = \
    TESTCASE_DEFAULT_WIRELESS_SHOW_OUTPUT + """\
802-11-wireless-security.key-mgmt:      --
802-11-wireless-security.wep-tx-keyidx: 0
802-11-wireless-security.auth-alg:      --
802-11-wireless-security.proto:         --
802-11-wireless-security.pairwise:      --
802-11-wireless-security.group:         --
802-11-wireless-security.pmf:           0 (default)
802-11-wireless-security.leap-username: --
802-11-wireless-security.wep-key0:      --
802-11-wireless-security.wep-key1:      --
802-11-wireless-security.wep-key2:      --
802-11-wireless-security.wep-key3:      --
802-11-wireless-security.wep-key-flags: 0 (none)
802-11-wireless-security.wep-key-type:  unknown
802-11-wireless-security.psk:           testingtestingtesting
802-11-wireless-security.psk-flags:     0 (none)
802-11-wireless-security.leap-password: --
802-11-wireless-security.leap-password-flags:0 (none)
802-11-wireless-security.wps-method:    0x0 (default)
802-11-wireless-security.fils:          0 (default)
"""


TESTCASE_DUMMY_STATIC = [
    {
        'type': 'dummy',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'dummy_non_existant',
        'ip4': '10.10.10.10/24',
        'gw4': '10.10.10.1',
        'dns4': ['1.1.1.1', '8.8.8.8'],
        'ip6': '2001:db8::1/128',
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_DUMMY_STATIC_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              dummy_non_existant
connection.autoconnect:                 yes
802-3-ethernet.mtu:                     auto
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.gateway:                           10.10.10.1
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv4.dns:                               1.1.1.1,8.8.8.8
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
ipv6.method:                            manual
ipv6.addresses:                         2001:db8::1/128
"""

TESTCASE_DUMMY_STATIC_WITHOUT_MTU_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              dummy_non_existant
connection.autoconnect:                 yes
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.gateway:                           10.10.10.1
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv4.dns:                               1.1.1.1,8.8.8.8
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
ipv6.method:                            manual
ipv6.addresses:                         2001:db8::1/128
"""

TESTCASE_DUMMY_STATIC_WITH_CUSTOM_MTU_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              dummy_non_existant
connection.autoconnect:                 yes
802-3-ethernet.mtu:                     1500
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.gateway:                           10.10.10.1
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv4.dns:                               1.1.1.1,8.8.8.8
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
ipv6.method:                            manual
ipv6.addresses:                         2001:db8::1/128
"""

TESTCASE_ETHERNET_STATIC_IP6_PRIVACY_AND_ADDR_GEN_MODE_UNCHANGED_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              ethernet_non_existant
connection.autoconnect:                 yes
802-3-ethernet.mtu:                     auto
ipv6.method:                            manual
ipv6.addresses:                         2001:db8::cafe/128
ipv6.gateway:                           2001:db8::cafa
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
ipv6.never-default:                     no
ipv6.may-fail:                          yes
ipv6.ip6-privacy:                       1 (enabled, prefer public IP)
ipv6.addr-gen-mode:                     eui64
ipv6.dns:                               2001:4860:4860::8888
ipv4.method:                            disabled
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
"""

TESTCASE_GSM = [
    {
        'type': 'gsm',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'gsm_non_existant',
        'gsm': {
            'apn': 'internet.telekom',
            'username': 't-mobile',
            'password': 'tm',
            'pin': '1234',
        },
        'method4': 'auto',
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_GSM_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.type:                        gsm
connection.interface-name:              gsm_non_existant
connection.autoconnect:                 yes
ipv4.method:                            auto
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
gsm.auto-config:                        no
gsm.number:                             --
gsm.username:                           t-mobile
gsm.password:                           tm
gsm.password-flags:                     0 (none)
gsm.apn:                                "internet.telekom"
gsm.network-id:                         --
gsm.pin:                                1234
gsm.pin-flags:                          0 (none)
gsm.home-only:                          no
gsm.device-id:                          --
gsm.sim-id:                             --
gsm.sim-operator-id:                    --
gsm.mtu:                                auto
"""

TESTCASE_WIREGUARD = [
    {
        'type': 'wireguard',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'wg_non_existant',
        'wireguard': {
            'listen-port': '51820',
            'private-key': '<hidden>',
        },
        'method4': 'manual',
        'ip4': '10.10.10.10/24',
        'method6': 'manual',
        'ip6': '2001:db8::1/128',
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_WIREGUARD_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.type:                        wireguard
connection.interface-name:              wg_non_existant
connection.autoconnect:                 yes
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv6.method:                            manual
ipv6.addresses:                         2001:db8::1/128
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
wireguard.private-key:                  <hidden>
wireguard.private-key-flags:            0 (none)
wireguard.listen-port:                  51820
wireguard.fwmark:                       0x0
wireguard.peer-routes:                  yes
wireguard.mtu:                          0
wireguard.ip4-auto-default-route:       -1 (default)
wireguard.ip6-auto-default-route:       -1 (default)
"""

TESTCASE_VPN_L2TP = [
    {
        'type': 'vpn',
        'conn_name': 'vpn_l2tp',
        'vpn': {
            'permissions': 'brittany',
            'service-type': 'org.freedesktop.NetworkManager.l2tp',
            'gateway': 'vpn.example.com',
            'password-flags': '2',
            'user': 'brittany',
            'ipsec-enabled': 'true',
            'ipsec-psk': 'QnJpdHRhbnkxMjM=',
        },
        'gw4_ignore_auto': True,
        'routes4': ['192.168.200.0/24'],
        'autoconnect': 'false',
        'state': 'present',
        '_ansible_check_mode': False,
    },
]

TESTCASE_VPN_L2TP_SHOW_OUTPUT = """\
connection.id:                          vpn_l2tp
connection.type:                        vpn
connection.autoconnect:                 no
connection.permissions:                 brittany
ipv4.method:                            auto
ipv4.routes:                            { ip = 192.168.200.0/24 }
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                yes
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
vpn.service-type:                       org.freedesktop.NetworkManager.l2tp
vpn.data:                               gateway = vpn.example.com, ipsec-enabled = true, ipsec-psk = QnJpdHRhbnkxMjM=, password-flags = 2, user = brittany
vpn.secrets:                            ipsec-psk = QnJpdHRhbnkxMjM=
vpn.persistent:                         no
vpn.timeout:                            0
"""

TESTCASE_VPN_PPTP = [
    {
        'type': 'vpn',
        'conn_name': 'vpn_pptp',
        'vpn': {
            'permissions': 'brittany',
            'service-type': 'org.freedesktop.NetworkManager.pptp',
            'gateway': 'vpn.example.com',
            'password-flags': '2',
            'user': 'brittany',
        },
        'autoconnect': 'false',
        'state': 'present',
        '_ansible_check_mode': False,
    },
]

TESTCASE_VPN_PPTP_SHOW_OUTPUT = """\
connection.id:                          vpn_pptp
connection.type:                        vpn
connection.autoconnect:                 no
connection.permissions:                 brittany
ipv4.method:                            auto
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
vpn.service-type:                       org.freedesktop.NetworkManager.pptp
vpn.data:                               gateway=vpn.example.com, password-flags=2, user=brittany
"""

TESTCASE_INFINIBAND_STATIC = [
    {
        'type': 'infiniband',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'infiniband_non_existant',
        'ip4': '10.10.10.10/24',
        'gw4': '10.10.10.1',
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_INFINIBAND_STATIC_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.type:                        infiniband
connection.interface-name:              infiniband_non_existant
connection.autoconnect:                 yes
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.gateway:                           10.10.10.1
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
infiniband.mtu:                         auto
infiniband.transport-mode:              datagram
"""

TESTCASE_INFINIBAND_STATIC_MODIFY_TRANSPORT_MODE = [
    {

        'type': 'infiniband',
        'conn_name': 'non_existent_nw_device',
        'transport_mode': 'connected',
        'state': 'present',
        '_ansible_check_mode': False,
    },
]

TESTCASE_INFINIBAND_STATIC_MODIFY_TRANSPORT_MODE_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              infiniband_non_existant
infiniband.transport_mode:              connected
"""

TESTCASE_MACVLAN = [
    {
        'type': 'macvlan',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'macvlan_non_existant',
        'macvlan': {
            'mode': '2',
            'parent': 'non_existent_parent',
        },
        'method4': 'manual',
        'ip4': '10.10.10.10/24',
        'method6': 'manual',
        'ip6': '2001:db8::1/128',
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_MACVLAN_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.type:                        macvlan
connection.interface-name:              macvlan_non_existant
connection.autoconnect:                 yes
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv6.method:                            manual
ipv6.addresses:                         2001:db8::1/128
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
macvlan.parent:                         non_existent_parent
macvlan.mode:                           2 (bridge)
macvlan.promiscuous:                    yes
macvlan.tap:                            no
"""

TESTCASE_VRF = [
    {
        'type': 'vrf',
        'conn_name': 'non_existent_nw_device',
        'ifname': 'vrf_not_exists',
        'ip4': '10.10.10.10/24',
        'gw4': '10.10.10.1',
        'table': 10,
        'state': 'present',
        '_ansible_check_mode': False,
    }
]

TESTCASE_VRF_SHOW_OUTPUT = """\
connection.id:                          non_existent_nw_device
connection.interface-name:              vrf_not_exists
connection.autoconnect:                 yes
ipv4.method:                            manual
ipv4.addresses:                         10.10.10.10/24
ipv4.gateway:                           10.10.10.1
ipv4.ignore-auto-dns:                   no
ipv4.ignore-auto-routes:                no
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv6.method:                            auto
ipv6.ignore-auto-dns:                   no
ipv6.ignore-auto-routes:                no
table:                                  10
802-3-ethernet.mtu:                     auto
"""


def mocker_set(mocker,
               connection_exists=False,
               execute_return=(0, "", ""),
               execute_side_effect=None,
               changed_return=None):
    """
    Common mocker object
    """
    get_bin_path = mocker.patch('ansible.module_utils.basic.AnsibleModule.get_bin_path')
    get_bin_path.return_value = '/usr/bin/nmcli'
    connection = mocker.patch.object(nmcli.Nmcli, 'connection_exists')
    connection.return_value = connection_exists
    execute_command = mocker.patch.object(nmcli.Nmcli, 'execute_command')
    if execute_return:
        execute_command.return_value = execute_return
    if execute_side_effect:
        execute_command.side_effect = execute_side_effect
    if changed_return:
        is_connection_changed = mocker.patch.object(nmcli.Nmcli, 'is_connection_changed')
        is_connection_changed.return_value = changed_return


@pytest.fixture
def mocked_generic_connection_create(mocker):
    mocker_set(mocker)


@pytest.fixture
def mocked_connection_exists(mocker):
    mocker_set(mocker, connection_exists=True)


@pytest.fixture
def mocked_generic_connection_modify(mocker):
    mocker_set(mocker,
               connection_exists=True,
               changed_return=(True, dict()))


@pytest.fixture
def mocked_generic_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_GENERIC_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_generic_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_GENERIC_MODIFY_ROUTING_RULES_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_generic_connection_dns_search_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_GENERIC_DNS4_SEARCH_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_generic_connection_dns_options_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_GENERIC_DNS4_OPTIONS_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_generic_connection_zone_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_GENERIC_ZONE_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_bond_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_BOND_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_bridge_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_BRIDGE_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_bridge_slave_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_BRIDGE_SLAVE_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_team_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_TEAM_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_team_runner_fast_rate_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_TEAM_RUNNER_FAST_RATE_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_team_slave_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_TEAM_SLAVE_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_vlan_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_VLAN_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_vxlan_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_VXLAN_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_gre_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_GRE_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_ipip_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_IPIP_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_sit_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_SIT_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_ethernet_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_ETHERNET_DHCP, ""))


@pytest.fixture
def mocked_ethernet_connection_dhcp_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_ETHERNET_DHCP_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_ethernet_connection_static_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_ETHERNET_STATIC_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_ethernet_connection_static_multiple_ip4_addresses_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_ETHERNET_STATIC_MULTIPLE_IP4_ADDRESSES_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_ethernet_connection_static_ip6_privacy_and_addr_gen_mode_unchange(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_ETHERNET_STATIC_IP6_PRIVACY_AND_ADDR_GEN_MODE_UNCHANGED_OUTPUT, ""))


@pytest.fixture
def mocked_ethernet_connection_static_multiple_ip6_addresses_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_ETHERNET_STATIC_MULTIPLE_IP6_ADDRESSES_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_ethernet_connection_static_modify(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_ETHERNET_STATIC_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_ethernet_connection_with_ipv6_static_address_static_route_create(mocker):
    mocker_set(mocker,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_ROUTE_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_ethernet_connection_with_ipv4_static_address_static_route_metric_modify(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_ETHERNET_MOD_IPV4_INT_WITH_ROUTE_AND_METRIC_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_ethernet_connection_with_ipv4_static_address_static_route_metric_clear(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_ETHERNET_MOD_IPV4_INT_WITH_ROUTE_AND_METRIC_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_ethernet_connection_with_ipv6_static_address_static_route_metric_modify(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_ETHERNET_MOD_IPV6_INT_WITH_ROUTE_AND_METRIC_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_ethernet_connection_with_ipv6_static_address_multiple_static_routes_create(mocker):
    mocker_set(mocker,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_MULTIPLE_ROUTES_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_ethernet_connection_with_sriov_vfs_create(mocker):
    mocker_set(mocker,
               execute_return=(0, TESTCASE_ETHERNET_ADD_SRIOV_VFS_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_ethernet_connection_with_ipv6_static_address_static_route_with_metric_create(mocker):
    mocker_set(mocker,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_ROUTE_AND_METRIC_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_ethernet_connection_with_ipv6_static_address_multiple_static_routes_with_metric_create(mocker):
    mocker_set(mocker,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_MULTIPLE_ROUTES_AND_METRIC_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_ethernet_connection_with_ipv6_address_static_modify(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_ETHERNET_STATIC_IP6_ADDRESS_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_ethernet_connection_dhcp_to_static(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_ETHERNET_DHCP_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_wireless_create(mocker):
    mocker_set(mocker,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_DEFAULT_WIRELESS_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_secure_wireless_create(mocker):
    mocker_set(mocker,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_DEFAULT_SECURE_WIRELESS_SHOW_OUTPUT, ""),
                   (0, "", ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_secure_wireless_create_failure(mocker):
    mocker_set(mocker,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_DEFAULT_SECURE_WIRELESS_SHOW_OUTPUT, ""),
                   (1, "", ""),
               ))


@pytest.fixture
def mocked_secure_wireless_modify(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_DEFAULT_SECURE_WIRELESS_SHOW_OUTPUT, ""),
                   (0, "", ""),
                   (0, "", ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_secure_wireless_modify_failure(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_DEFAULT_SECURE_WIRELESS_SHOW_OUTPUT, ""),
                   (0, "", ""),
                   (1, "", ""),
               ))


@pytest.fixture
def mocked_dummy_connection_static_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_DUMMY_STATIC_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_dummy_connection_static_without_mtu_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_DUMMY_STATIC_WITHOUT_MTU_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_dummy_connection_static_with_custom_mtu_modify(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_DUMMY_STATIC_WITH_CUSTOM_MTU_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_gsm_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_GSM_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_wireguard_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_WIREGUARD_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_vpn_l2tp_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_VPN_L2TP_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_vpn_pptp_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_VPN_PPTP_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_infiniband_connection_static_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_INFINIBAND_STATIC_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_infiniband_connection_static_transport_mode_connected_modify(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_INFINIBAND_STATIC_MODIFY_TRANSPORT_MODE_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_macvlan_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_MACVLAN_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_generic_connection_diff_check(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_GENERIC_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_loopback_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_LOOPBACK_SHOW_OUTPUT, ""))


@pytest.fixture
def mocked_loopback_connection_modify(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_LOOPBACK_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.fixture
def mocked_vrf_connection_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_VRF_SHOW_OUTPUT, ""))


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_BOND, indirect=['patch_ansible_module'])
def test_bond_connection_create(mocked_generic_connection_create, capfd):
    """
    Test : Bond connection created
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'bond'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'non_existent_nw_device'

    for param in ['ipv4.gateway', 'primary', 'connection.autoconnect',
                  'connection.interface-name', 'bond_non_existant',
                  'mode', 'active-backup', 'ipv4.addresses',
                  '+bond.options', 'xmit_hash_policy=layer3+4']:
        assert param in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_BOND, indirect=['patch_ansible_module'])
def test_bond_connection_unchanged(mocked_bond_connection_unchanged, capfd):
    """
    Test : Bond connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC, indirect=['patch_ansible_module'])
def test_generic_connection_create(mocked_generic_connection_create, capfd):
    """
    Test : Generic connection created
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'generic'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'non_existent_nw_device'

    for param in ['connection.autoconnect', 'ipv4.gateway', 'ipv4.addresses']:
        assert param in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC, indirect=['patch_ansible_module'])
def test_generic_connection_modify(mocked_generic_connection_modify, capfd):
    """
    Test : Generic connection modify
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    for param in ['ipv4.gateway', 'ipv4.addresses']:
        assert param in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC, indirect=['patch_ansible_module'])
def test_generic_connection_unchanged(mocked_generic_connection_unchanged, capfd):
    """
    Test : Generic connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC_MODIFY_ROUTING_RULES, indirect=['patch_ansible_module'])
def test_generic_connection_modify_routing_rules4(mocked_generic_connection_create, capfd):
    """
    Test : Generic connection modified with routing-rules4
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert 'ipv4.routing-rules' in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC_DNS4_SEARCH, indirect=['patch_ansible_module'])
def test_generic_connection_create_dns_search(mocked_generic_connection_create, capfd):
    """
    Test : Generic connection created with dns search
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert 'ipv4.dns-search' in args[0]
    assert 'ipv6.dns-search' in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC_DNS4_SEARCH, indirect=['patch_ansible_module'])
def test_generic_connection_modify_dns_search(mocked_generic_connection_create, capfd):
    """
    Test : Generic connection modified with dns search
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert 'ipv4.dns-search' in args[0]
    assert 'ipv6.dns-search' in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC_DNS4_SEARCH, indirect=['patch_ansible_module'])
def test_generic_connection_dns_search_unchanged(mocked_generic_connection_dns_search_unchanged, capfd):
    """
    Test : Generic connection with dns search unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC_DNS4_OPTIONS, indirect=['patch_ansible_module'])
def test_generic_connection_create_dns_options(mocked_generic_connection_create, capfd):
    """
    Test : Generic connection created with dns options
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert 'ipv4.dns-options' in args[0]
    assert 'ipv6.dns-options' in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC_DNS4_OPTIONS, indirect=['patch_ansible_module'])
def test_generic_connection_modify_dns_options(mocked_generic_connection_create, capfd):
    """
    Test : Generic connection modified with dns options
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert 'ipv4.dns-options' in args[0]
    assert 'ipv6.dns-options' in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC_DNS4_OPTIONS, indirect=['patch_ansible_module'])
def test_generic_connection_dns_options_unchanged(mocked_generic_connection_dns_options_unchanged, capfd):
    """
    Test : Generic connection with dns options unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_CONNECTION, indirect=['patch_ansible_module'])
def test_dns4_none(mocked_connection_exists, capfd):
    """
    Test if DNS4 param is None
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC_ZONE, indirect=['patch_ansible_module'])
def test_generic_connection_create_zone(mocked_generic_connection_create, capfd):
    """
    Test : Generic connection created with zone
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert 'connection.zone' in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC_ZONE, indirect=['patch_ansible_module'])
def test_generic_connection_modify_zone(mocked_generic_connection_create, capfd):
    """
    Test : Generic connection modified with zone
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert 'connection.zone' in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC_ZONE, indirect=['patch_ansible_module'])
def test_generic_connection_zone_unchanged(mocked_generic_connection_zone_unchanged, capfd):
    """
    Test : Generic connection with zone unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC_ZONE_ONLY, indirect=['patch_ansible_module'])
def test_generic_connection_modify_zone_only(mocked_generic_connection_modify, capfd):
    """
    Test : Generic connection modified with zone only
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert 'connection.zone' in args[0]
    assert 'ipv4.addresses' not in args[0]
    assert 'ipv4.gateway' not in args[0]
    assert 'ipv6.addresses' not in args[0]
    assert 'ipv6.gateway' not in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_CONNECTION, indirect=['patch_ansible_module'])
def test_zone_none(mocked_connection_exists, capfd):
    """
    Test if zone param is None
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_BRIDGE, indirect=['patch_ansible_module'])
def test_create_bridge(mocked_generic_connection_create, capfd):
    """
    Test if Bridge created
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'bridge'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['ipv4.addresses', '10.10.10.10/24', 'ipv4.gateway', '10.10.10.1', 'bridge.max-age', '100', 'bridge.stp', 'yes']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_BRIDGE, indirect=['patch_ansible_module'])
def test_mod_bridge(mocked_generic_connection_modify, capfd):
    """
    Test if Bridge modified
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1

    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['ipv4.addresses', '10.10.10.10/24', 'ipv4.gateway', '10.10.10.1', 'bridge.max-age', '100', 'bridge.stp', 'yes']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_BRIDGE, indirect=['patch_ansible_module'])
def test_bridge_connection_unchanged(mocked_bridge_connection_unchanged, capfd):
    """
    Test : Bridge connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_BRIDGE_SLAVE, indirect=['patch_ansible_module'])
def test_create_bridge_slave(mocked_generic_connection_create, capfd):
    """
    Test if Bridge_slave created
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'bridge-slave'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['bridge-port.path-cost', '100']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_BRIDGE_SLAVE, indirect=['patch_ansible_module'])
def test_mod_bridge_slave(mocked_generic_connection_modify, capfd):
    """
    Test if Bridge_slave modified
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['bridge-port.path-cost', '100']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_BRIDGE_SLAVE, indirect=['patch_ansible_module'])
def test_bridge_slave_unchanged(mocked_bridge_slave_unchanged, capfd):
    """
    Test : Bridge-slave connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_TEAM, indirect=['patch_ansible_module'])
def test_team_connection_create(mocked_generic_connection_create, capfd):
    """
    Test : Team connection created
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'team'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'non_existent_nw_device'

    for param in ['connection.autoconnect', 'connection.interface-name', 'team0_non_existant']:
        assert param in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_TEAM, indirect=['patch_ansible_module'])
def test_team_connection_unchanged(mocked_team_connection_unchanged, capfd):
    """
    Test : Team connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_TEAM_HWADDR_POLICY_FAILS, indirect=['patch_ansible_module'])
def test_team_connection_create_hwaddr_policy_fails(mocked_generic_connection_create, capfd):
    """
    Test : Team connection created
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert results.get('failed')
    assert results['msg'] == "Runner-hwaddr-policy is only allowed for runner activebackup"


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_TEAM_RUNNER_FAST_RATE, indirect=['patch_ansible_module'])
def test_team_runner_fast_rate_connection_create(mocked_generic_connection_create, capfd):
    """
    Test : Team connection created with runner_fast_rate parameter
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'team'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'non_existent_nw_device'

    for param in ['connection.autoconnect', 'connection.interface-name', 'team0_non_existant', 'team.runner', 'lacp', 'team.runner-fast-rate', 'yes']:
        assert param in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_TEAM_RUNNER_FAST_RATE, indirect=['patch_ansible_module'])
def test_team_runner_fast_rate_connection_unchanged(mocked_team_runner_fast_rate_connection_unchanged, capfd):
    """
    Test : Team connection unchanged with runner_fast_rate parameter
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_TEAM_RUNNER_FAST_RATE_FAILS, indirect=['patch_ansible_module'])
def test_team_connection_create_runner_fast_rate_fails(mocked_generic_connection_create, capfd):
    """
    Test : Team connection with runner_fast_rate enabled
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert results.get('failed')
    assert results['msg'] == "runner-fast-rate is only allowed for runner lacp"


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_TEAM_SLAVE, indirect=['patch_ansible_module'])
def test_create_team_slave(mocked_generic_connection_create, capfd):
    """
    Test if Team_slave created
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'team-slave'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'non_existent_nw_slaved_device'

    for param in ['connection.autoconnect', 'connection.interface-name', 'connection.master', 'team0_non_existant', 'connection.slave-type']:
        assert param in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_TEAM_SLAVE, indirect=['patch_ansible_module'])
def test_team_slave_connection_unchanged(mocked_team_slave_connection_unchanged, capfd):
    """
    Test : Team slave connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_VLAN, indirect=['patch_ansible_module'])
def test_create_vlan_con(mocked_generic_connection_create, capfd):
    """
    Test if VLAN created
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'vlan'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['ipv4.addresses', '10.10.10.10/24', 'ipv4.gateway', '10.10.10.1', 'vlan.id', '10']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_VLAN, indirect=['patch_ansible_module'])
def test_mod_vlan_conn(mocked_generic_connection_modify, capfd):
    """
    Test if VLAN modified
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['ipv4.addresses', '10.10.10.10/24', 'ipv4.gateway', '10.10.10.1', 'vlan.id', '10']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_VLAN, indirect=['patch_ansible_module'])
def test_vlan_connection_unchanged(mocked_vlan_connection_unchanged, capfd):
    """
    Test : VLAN connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_VXLAN, indirect=['patch_ansible_module'])
def test_create_vxlan(mocked_generic_connection_create, capfd):
    """
    Test if vxlan created
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'vxlan'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['connection.interface-name', 'vxlan-existent_nw_device',
                  'vxlan.local', '192.168.225.5', 'vxlan.remote', '192.168.225.6', 'vxlan.id', '11']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_VXLAN, indirect=['patch_ansible_module'])
def test_vxlan_mod(mocked_generic_connection_modify, capfd):
    """
    Test if vxlan modified
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['vxlan.local', '192.168.225.5', 'vxlan.remote', '192.168.225.6', 'vxlan.id', '11']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_VXLAN, indirect=['patch_ansible_module'])
def test_vxlan_connection_unchanged(mocked_vxlan_connection_unchanged, capfd):
    """
    Test : VxLAN connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_IPIP, indirect=['patch_ansible_module'])
def test_create_ipip(mocked_generic_connection_create, capfd):
    """
    Test if ipip created
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'ip-tunnel'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['connection.interface-name', 'ipip-existent_nw_device',
                  'ip-tunnel.local', '192.168.225.5',
                  'ip-tunnel.mode', 'ipip',
                  'ip-tunnel.parent', 'non_existent_ipip_device',
                  'ip-tunnel.remote', '192.168.225.6']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_IPIP, indirect=['patch_ansible_module'])
def test_ipip_mod(mocked_generic_connection_modify, capfd):
    """
    Test if ipip modified
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['ip-tunnel.local', '192.168.225.5', 'ip-tunnel.remote', '192.168.225.6']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_IPIP, indirect=['patch_ansible_module'])
def test_ipip_connection_unchanged(mocked_ipip_connection_unchanged, capfd):
    """
    Test : IPIP connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_SIT, indirect=['patch_ansible_module'])
def test_create_sit(mocked_generic_connection_create, capfd):
    """
    Test if sit created
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'ip-tunnel'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['connection.interface-name', 'sit-existent_nw_device',
                  'ip-tunnel.local', '192.168.225.5',
                  'ip-tunnel.mode', 'sit',
                  'ip-tunnel.parent', 'non_existent_sit_device',
                  'ip-tunnel.remote', '192.168.225.6']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_SIT, indirect=['patch_ansible_module'])
def test_sit_mod(mocked_generic_connection_modify, capfd):
    """
    Test if sit modified
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['ip-tunnel.local', '192.168.225.5', 'ip-tunnel.remote', '192.168.225.6']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_SIT, indirect=['patch_ansible_module'])
def test_sit_connection_unchanged(mocked_sit_connection_unchanged, capfd):
    """
    Test : SIT connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_DHCP, indirect=['patch_ansible_module'])
def test_eth_dhcp_client_id_con_create(mocked_generic_connection_create, capfd):
    """
    Test : Ethernet connection created with DHCP_CLIENT_ID
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert 'ipv4.dhcp-client-id' in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GRE, indirect=['patch_ansible_module'])
def test_create_gre(mocked_generic_connection_create, capfd):
    """
    Test if gre created
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'ip-tunnel'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['connection.interface-name', 'gre-existent_nw_device',
                  'ip-tunnel.local', '192.168.225.5',
                  'ip-tunnel.mode', 'gre',
                  'ip-tunnel.parent', 'non_existent_gre_device',
                  'ip-tunnel.remote', '192.168.225.6',
                  'ip-tunnel.input-key', '1',
                  'ip-tunnel.output-key', '2']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GRE, indirect=['patch_ansible_module'])
def test_gre_mod(mocked_generic_connection_modify, capfd):
    """
    Test if gre modified
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['ip-tunnel.local', '192.168.225.5', 'ip-tunnel.remote', '192.168.225.6']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GRE, indirect=['patch_ansible_module'])
def test_gre_connection_unchanged(mocked_gre_connection_unchanged, capfd):
    """
    Test : GRE connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_DHCP, indirect=['patch_ansible_module'])
def test_ethernet_connection_dhcp_unchanged(mocked_ethernet_connection_dhcp_unchanged, capfd):
    """
    Test : Ethernet connection with DHCP_CLIENT_ID unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_STATIC, indirect=['patch_ansible_module'])
def test_modify_ethernet_dhcp_to_static(mocked_ethernet_connection_dhcp_to_static, capfd):
    """
    Test : Modify ethernet connection from DHCP to static
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 2
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[1]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    for param in ['ipv4.method', 'ipv4.gateway', 'ipv4.addresses']:
        assert param in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_STATIC, indirect=['patch_ansible_module'])
def test_create_ethernet_static(mocked_generic_connection_create, capfd):
    """
    Test : Create ethernet connection with static IP configuration
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 2
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'ethernet'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))
    for param in ['connection.interface-name', 'ethernet_non_existant',
                  'ipv4.addresses', '10.10.10.10/24',
                  'ipv4.gateway', '10.10.10.1',
                  'ipv4.dns', '1.1.1.1,8.8.8.8']:
        assert param in add_args_text

    up_args, up_kw = arg_list[1]
    assert up_args[0][0] == '/usr/bin/nmcli'
    assert up_args[0][1] == 'con'
    assert up_args[0][2] == 'up'
    assert up_args[0][3] == 'non_existent_nw_device'

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_STATIC, indirect=['patch_ansible_module'])
def test_ethernet_connection_static_unchanged(mocked_ethernet_connection_static_unchanged, capfd):
    """
    Test : Ethernet connection with static IP configuration unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_MOD_IPV4_INT_WITH_ROUTE_AND_METRIC, indirect=['patch_ansible_module'])
def test_ethernet_connection_static_ipv4_address_static_route_with_metric_modify(
        mocked_ethernet_connection_with_ipv4_static_address_static_route_metric_modify, capfd):
    """
    Test : Modify ethernet connection with static IPv4 address and static route
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[1]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'modify'
    assert add_args[0][3] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))

    for param in ['ipv4.routes', '192.168.200.0/24 192.168.1.1',
                  'ipv4.route-metric', '10']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)

    assert results.get('changed') is True
    assert not results.get('failed')


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_MOD_IPV4_INT_WITH_ROUTE_AND_METRIC_CLEAR, indirect=['patch_ansible_module'])
def test_ethernet_connection_static_ipv4_address_static_route_with_metric_clear(
        mocked_ethernet_connection_with_ipv4_static_address_static_route_metric_clear, capfd):
    """
    Test : Modify ethernet connection with static IPv4 address and static route
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[1]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'modify'
    assert add_args[0][3] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))

    for param in ['ipv4.routes', '']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)

    assert 'ipv4.routes' in results['diff']['before']
    assert 'ipv4.routes' in results['diff']['after']

    assert results.get('changed') is True
    assert not results.get('failed')


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_ROUTE, indirect=['patch_ansible_module'])
def test_ethernet_connection_static_ipv6_address_static_route_create(mocked_ethernet_connection_with_ipv6_static_address_static_route_create, capfd):
    """
    Test : Create ethernet connection with static IPv6 address and static route
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'ethernet'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))

    for param in ['connection.interface-name', 'ethernet_non_existant',
                  'con-name', 'non_existent_nw_device',
                  'ipv6.addresses', '2001:beef:cafe:10::1/64',
                  'ipv6.method', 'manual',
                  'ipv6.routes', 'fd2e:446f:d85d:5::/64 2001:beef:cafe:10::2']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_MOD_IPV6_INT_WITH_ROUTE_AND_METRIC, indirect=['patch_ansible_module'])
def test_ethernet_connection_static_ipv6_address_static_route_metric_modify(
        mocked_ethernet_connection_with_ipv6_static_address_static_route_metric_modify, capfd):
    """
    Test : Modify ethernet connection with static IPv6 address and static route
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[1]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'modify'
    assert add_args[0][3] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))

    for param in ['ipv6.routes', 'fd2e:446f:d85d:5::/64 2001:beef:cafe:10::2',
                  'ipv6.route-metric', '10']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)

    assert results.get('changed') is True
    assert not results.get('failed')


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_MULTIPLE_ROUTES, indirect=['patch_ansible_module'])
def test_ethernet_connection_static_ipv6_address_multiple_static_routes_with_metric_create(
        mocked_ethernet_connection_with_ipv6_static_address_multiple_static_routes_with_metric_create, capfd):
    """
    Test : Create ethernet connection with static IPv6 address and multiple static routes
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'ethernet'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))

    for param in ['connection.interface-name', 'ethernet_non_existant',
                  'con-name', 'non_existent_nw_device',
                  'ipv6.addresses', '2001:beef:cafe:10::1/64',
                  'ipv6.method', 'manual',
                  'ipv6.routes', 'fd2e:446f:d85d:5::/64 2001:beef:cafe:10::2,fd2e:8890:abcd:25::/64 2001:beef:cafe:10::5']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_ADD_SRIOV_VFS, indirect=['patch_ansible_module'])
def test_ethernet_connection_sriov_vfs_create(
        mocked_ethernet_connection_with_sriov_vfs_create, capfd):
    """
    Test : Create ethernet connection with SR-IOV VFs
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'ethernet'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))

    for param in ['connection.interface-name', 'ethernet_non_existant',
                  'con-name', 'non_existent_nw_device',
                  'sriov.total-vfs', '16',
                  'sriov.vfs', '0 spoof-check=true vlans=100']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_ROUTE_AND_METRIC, indirect=['patch_ansible_module'])
def test_ethernet_connection_static_ipv6_address_static_route_with_metric_create(
        mocked_ethernet_connection_with_ipv6_static_address_static_route_with_metric_create, capfd):
    """
    Test : Create ethernet connection with static IPv6 address and static route with metric
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'ethernet'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))

    for param in ['connection.interface-name', 'ethernet_non_existant',
                  'con-name', 'non_existent_nw_device',
                  'ipv6.addresses', '2001:beef:cafe:10::1/64',
                  'ipv6.method', 'manual',
                  'ipv6.routes', 'fd2e:446f:d85d:5::/64 2001:beef:cafe:10::2',
                  'ipv6.route-metric', '5']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_ADD_IPV6_INT_WITH_MULTIPLE_ROUTES_AND_METRIC, indirect=['patch_ansible_module'])
def test_ethernet_connection_static_ipv6_address_static_route_create(mocked_ethernet_connection_with_ipv6_static_address_static_route_create, capfd):
    """
    Test : Create ethernet connection with static IPv6 address and multiple static routes with metric
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'ethernet'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))

    for param in ['connection.interface-name', 'ethernet_non_existant',
                  'con-name', 'non_existent_nw_device',
                  'ipv6.addresses', '2001:beef:cafe:10::1/64',
                  'ipv6.method', 'manual',
                  'ipv6.routes', 'fd2e:446f:d85d:5::/64 2001:beef:cafe:10::2,fd2e:8890:abcd:25::/64 2001:beef:cafe:10::5',
                  'ipv6.route-metric', '5']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_WIRELESS, indirect=['patch_ansible_module'])
def test_create_wireless(mocked_wireless_create, capfd):
    """
    Test : Create wireless connection
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 2
    arg_list = nmcli.Nmcli.execute_command.call_args_list

    get_available_options_args, get_available_options_kw = arg_list[0]
    assert get_available_options_args[0][0] == '/usr/bin/nmcli'
    assert get_available_options_args[0][1] == 'con'
    assert get_available_options_args[0][2] == 'edit'
    assert get_available_options_args[0][3] == 'type'
    assert get_available_options_args[0][4] == 'wifi'

    get_available_options_data = get_available_options_kw['data'].split()
    for param in ['print', '802-11-wireless',
                  'quit', 'yes']:
        assert param in get_available_options_data

    add_args, add_kw = arg_list[1]
    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'wifi'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))
    for param in ['connection.interface-name', 'wireless_non_existant',
                  'ipv4.addresses', '10.10.10.10/24',
                  '802-11-wireless.ssid', 'Brittany',
                  '802-11-wireless.mode', 'ap',
                  '802-11-wireless.hidden', 'yes']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_SECURE_WIRELESS, indirect=['patch_ansible_module'])
def test_create_secure_wireless(mocked_secure_wireless_create, capfd):
    """
    Test : Create secure wireless connection
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 3
    arg_list = nmcli.Nmcli.execute_command.call_args_list

    get_available_options_args, get_available_options_kw = arg_list[0]
    assert get_available_options_args[0][0] == '/usr/bin/nmcli'
    assert get_available_options_args[0][1] == 'con'
    assert get_available_options_args[0][2] == 'edit'
    assert get_available_options_args[0][3] == 'type'
    assert get_available_options_args[0][4] == 'wifi'

    get_available_options_data = get_available_options_kw['data'].split()
    for param in ['print', '802-11-wireless-security',
                  'quit', 'yes']:
        assert param in get_available_options_data

    add_args, add_kw = arg_list[1]
    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'wifi'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))
    for param in ['connection.interface-name', 'wireless_non_existant',
                  'ipv4.addresses', '10.10.10.10/24',
                  '802-11-wireless.ssid', 'Brittany',
                  '802-11-wireless-security.key-mgmt', 'wpa-psk']:
        assert param in add_args_text

    edit_args, edit_kw = arg_list[2]
    assert edit_args[0][0] == '/usr/bin/nmcli'
    assert edit_args[0][1] == 'con'
    assert edit_args[0][2] == 'edit'
    assert edit_args[0][3] == 'non_existent_nw_device'

    edit_kw_data = edit_kw['data'].split()
    for param in ['802-11-wireless-security.psk', 'VERY_SECURE_PASSWORD',
                  'save',
                  'quit']:
        assert param in edit_kw_data

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_SECURE_WIRELESS, indirect=['patch_ansible_module'])
def test_create_secure_wireless_failure(mocked_secure_wireless_create_failure, capfd):
    """
    Test : Create secure wireless connection w/failure
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 2
    arg_list = nmcli.Nmcli.execute_command.call_args_list

    get_available_options_args, get_available_options_kw = arg_list[0]
    assert get_available_options_args[0][0] == '/usr/bin/nmcli'
    assert get_available_options_args[0][1] == 'con'
    assert get_available_options_args[0][2] == 'edit'
    assert get_available_options_args[0][3] == 'type'
    assert get_available_options_args[0][4] == 'wifi'

    get_available_options_data = get_available_options_kw['data'].split()
    for param in ['print', '802-11-wireless-security',
                  'quit', 'yes']:
        assert param in get_available_options_data

    add_args, add_kw = arg_list[1]
    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'wifi'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))
    for param in ['connection.interface-name', 'wireless_non_existant',
                  'ipv4.addresses', '10.10.10.10/24',
                  '802-11-wireless.ssid', 'Brittany',
                  '802-11-wireless-security.key-mgmt', 'wpa-psk']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert results.get('failed')
    assert 'changed' not in results


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_SECURE_WIRELESS, indirect=['patch_ansible_module'])
def test_modify_secure_wireless(mocked_secure_wireless_modify, capfd):
    """
    Test : Modify secure wireless connection
    """

    with pytest.raises(SystemExit):
        nmcli.main()
    assert nmcli.Nmcli.execute_command.call_count == 4
    arg_list = nmcli.Nmcli.execute_command.call_args_list

    get_available_options_args, get_available_options_kw = arg_list[0]
    assert get_available_options_args[0][0] == '/usr/bin/nmcli'
    assert get_available_options_args[0][1] == 'con'
    assert get_available_options_args[0][2] == 'edit'
    assert get_available_options_args[0][3] == 'type'
    assert get_available_options_args[0][4] == 'wifi'

    get_available_options_data = get_available_options_kw['data'].split()
    for param in ['print', '802-11-wireless-security',
                  'quit', 'yes']:
        assert param in get_available_options_data

    show_args, show_kw = arg_list[1]
    assert show_args[0][0] == '/usr/bin/nmcli'
    assert show_args[0][1] == '--show-secrets'
    assert show_args[0][2] == 'con'
    assert show_args[0][3] == 'show'
    assert show_args[0][4] == 'non_existent_nw_device'

    add_args, add_kw = arg_list[2]
    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'modify'
    assert add_args[0][3] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))
    for param in ['connection.interface-name', 'wireless_non_existant',
                  'ipv4.addresses', '10.10.10.10/24',
                  '802-11-wireless.ssid', 'Brittany',
                  '802-11-wireless-security.key-mgmt', 'wpa-psk']:
        assert param in add_args_text

    edit_args, edit_kw = arg_list[3]
    assert edit_args[0][0] == '/usr/bin/nmcli'
    assert edit_args[0][1] == 'con'
    assert edit_args[0][2] == 'edit'
    assert edit_args[0][3] == 'non_existent_nw_device'

    edit_kw_data = edit_kw['data'].split()
    for param in ['802-11-wireless-security.psk', 'VERY_SECURE_PASSWORD',
                  'save',
                  'quit']:
        assert param in edit_kw_data

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_SECURE_WIRELESS, indirect=['patch_ansible_module'])
def test_modify_secure_wireless_failure(mocked_secure_wireless_modify_failure, capfd):
    """
    Test : Modify secure wireless connection w/failure
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 3
    arg_list = nmcli.Nmcli.execute_command.call_args_list

    get_available_options_args, get_available_options_kw = arg_list[0]
    assert get_available_options_args[0][0] == '/usr/bin/nmcli'
    assert get_available_options_args[0][1] == 'con'
    assert get_available_options_args[0][2] == 'edit'
    assert get_available_options_args[0][3] == 'type'
    assert get_available_options_args[0][4] == 'wifi'

    get_available_options_data = get_available_options_kw['data'].split()
    for param in ['print', '802-11-wireless-security',
                  'quit', 'yes']:
        assert param in get_available_options_data

    show_args, show_kw = arg_list[1]
    assert show_args[0][0] == '/usr/bin/nmcli'
    assert show_args[0][1] == '--show-secrets'
    assert show_args[0][2] == 'con'
    assert show_args[0][3] == 'show'
    assert show_args[0][4] == 'non_existent_nw_device'

    add_args, add_kw = arg_list[2]
    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'modify'
    assert add_args[0][3] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))
    for param in ['connection.interface-name', 'wireless_non_existant',
                  'ipv4.addresses', '10.10.10.10/24',
                  '802-11-wireless.ssid', 'Brittany',
                  '802-11-wireless-security.key-mgmt', 'wpa-psk']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert results.get('failed')
    assert 'changed' not in results


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_DUMMY_STATIC, indirect=['patch_ansible_module'])
def test_create_dummy_static(mocked_generic_connection_create, capfd):
    """
    Test : Create dummy connection with static IP configuration
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 2
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'dummy'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))
    for param in ['connection.interface-name', 'dummy_non_existant',
                  'ipv4.addresses', '10.10.10.10/24',
                  'ipv4.gateway', '10.10.10.1',
                  'ipv4.dns', '1.1.1.1,8.8.8.8',
                  'ipv6.addresses', '2001:db8::1/128']:
        assert param in add_args_text

    up_args, up_kw = arg_list[1]
    assert up_args[0][0] == '/usr/bin/nmcli'
    assert up_args[0][1] == 'con'
    assert up_args[0][2] == 'up'
    assert up_args[0][3] == 'non_existent_nw_device'

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_DUMMY_STATIC, indirect=['patch_ansible_module'])
def test_dummy_connection_static_unchanged(mocked_dummy_connection_static_unchanged, capfd):
    """
    Test : Dummy connection with static IP configuration unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_DUMMY_STATIC, indirect=['patch_ansible_module'])
def test_dummy_connection_static_without_mtu_unchanged(mocked_dummy_connection_static_without_mtu_unchanged, capfd):
    """
    Test : Dummy connection with static IP configuration and no mtu set unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_DUMMY_STATIC, indirect=['patch_ansible_module'])
def test_dummy_connection_static_with_custom_mtu_modify(mocked_dummy_connection_static_with_custom_mtu_modify, capfd):
    """
    Test : Dummy connection with static IP configuration and no mtu set modify
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 2

    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[1]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['802-3-ethernet.mtu', '0']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GSM, indirect=['patch_ansible_module'])
def test_create_gsm(mocked_generic_connection_create, capfd):
    """
    Test if gsm created
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'gsm'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['connection.interface-name', 'gsm_non_existant',
                  'gsm.apn', 'internet.telekom',
                  'gsm.username', 't-mobile',
                  'gsm.password', 'tm',
                  'gsm.pin', '1234']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GSM, indirect=['patch_ansible_module'])
def test_gsm_mod(mocked_generic_connection_modify, capfd):
    """
    Test if gsm modified
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['gsm.username', 't-mobile',
                  'gsm.password', 'tm']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GSM, indirect=['patch_ansible_module'])
def test_gsm_connection_unchanged(mocked_gsm_connection_unchanged, capfd):
    """
    Test if gsm connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_STATIC_MULTIPLE_IP4_ADDRESSES, indirect=['patch_ansible_module'])
def test_create_ethernet_with_multiple_ip4_addresses_static(mocked_generic_connection_create, capfd):
    """
    Test : Create ethernet connection with static IP configuration
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 2
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'ethernet'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))
    for param in ['connection.interface-name', 'ethernet_non_existant',
                  'ipv4.addresses', '10.10.10.10/32,10.10.20.10/32',
                  'ipv4.gateway', '10.10.10.1',
                  'ipv4.dns', '1.1.1.1,8.8.8.8']:
        assert param in add_args_text

    up_args, up_kw = arg_list[1]
    assert up_args[0][0] == '/usr/bin/nmcli'
    assert up_args[0][1] == 'con'
    assert up_args[0][2] == 'up'
    assert up_args[0][3] == 'non_existent_nw_device'

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_STATIC_MULTIPLE_IP6_ADDRESSES, indirect=['patch_ansible_module'])
def test_create_ethernet_with_multiple_ip6_addresses_static(mocked_generic_connection_create, capfd):
    """
    Test : Create ethernet connection with multiple IPv6 addresses configuration
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 2
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'ethernet'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))
    for param in ['connection.interface-name', 'ethernet_non_existant',
                  'ipv6.addresses', '2001:db8::cafe/128,2002:db8::cafe/128',
                  'ipv6.gateway', '2001:db8::cafa',
                  'ipv6.dns', '2001:4860:4860::8888,2001:4860:4860::8844']:
        assert param in add_args_text

    up_args, up_kw = arg_list[1]
    assert up_args[0][0] == '/usr/bin/nmcli'
    assert up_args[0][1] == 'con'
    assert up_args[0][2] == 'up'
    assert up_args[0][3] == 'non_existent_nw_device'

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_STATIC_MULTIPLE_IP4_ADDRESSES, indirect=['patch_ansible_module'])
def test_ethernet_connection_static_with_multiple_ip4_addresses_unchanged(mocked_ethernet_connection_static_multiple_ip4_addresses_unchanged, capfd):
    """
    Test : Ethernet connection with static IP configuration unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_STATIC_MULTIPLE_IP6_ADDRESSES, indirect=['patch_ansible_module'])
def test_ethernet_connection_static_with_multiple_ip6_addresses_unchanged(mocked_ethernet_connection_static_multiple_ip6_addresses_unchanged, capfd):
    """
    Test : Ethernet connection with multiple IPv6 addresses configuration unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_STATIC_MULTIPLE_IP4_ADDRESSES, indirect=['patch_ansible_module'])
def test_add_second_ip4_address_to_ethernet_connection(mocked_ethernet_connection_static_modify, capfd):
    """
    Test : Modify ethernet connection from DHCP to static
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 2
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[1]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    for param in ['ipv4.addresses', '10.10.10.10/32,10.10.20.10/32']:
        assert param in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_STATIC_IP6_PRIVACY_AND_ADDR_GEN_MODE, indirect=['patch_ansible_module'])
def test_create_ethernet_addr_gen_mode_and_ip6_privacy_static(mocked_generic_connection_create, capfd):
    """
    Test : Create ethernet connection with static IP configuration
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 2
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'ethernet'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))
    for param in ['connection.interface-name', 'ethernet_non_existant',
                  'ipv6.addresses', '2001:db8::cafe/128',
                  'ipv6.gateway', '2001:db8::cafa',
                  'ipv6.dns', '2001:4860:4860::8888',
                  'ipv6.ip6-privacy', 'prefer-public-addr',
                  'ipv6.addr-gen-mode', 'eui64']:
        assert param in add_args_text

    up_args, up_kw = arg_list[1]
    assert up_args[0][0] == '/usr/bin/nmcli'
    assert up_args[0][1] == 'con'
    assert up_args[0][2] == 'up'
    assert up_args[0][3] == 'non_existent_nw_device'

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_ETHERNET_STATIC_IP6_PRIVACY_AND_ADDR_GEN_MODE, indirect=['patch_ansible_module'])
def test_ethernet_connection_static_with_multiple_ip4_addresses_unchanged(mocked_ethernet_connection_static_ip6_privacy_and_addr_gen_mode_unchange, capfd):
    """
    Test : Ethernet connection with static IP configuration unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_WIREGUARD, indirect=['patch_ansible_module'])
def test_create_wireguard(mocked_generic_connection_create, capfd):
    """
    Test : Create wireguard connection with static IP configuration
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'wireguard'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))
    for param in ['connection.interface-name', 'wg_non_existant',
                  'ipv4.method', 'manual',
                  'ipv4.addresses', '10.10.10.10/24',
                  'ipv6.method', 'manual',
                  'ipv6.addresses', '2001:db8::1/128',
                  'wireguard.listen-port', '51820',
                  'wireguard.private-key', '<hidden>']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_WIREGUARD, indirect=['patch_ansible_module'])
def test_wireguard_connection_unchanged(mocked_wireguard_connection_unchanged, capfd):
    """
    Test : Wireguard connection with static IP configuration unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_WIREGUARD, indirect=['patch_ansible_module'])
def test_wireguard_mod(mocked_generic_connection_modify, capfd):
    """
    Test : Modify wireguard connection
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['wireguard.listen-port', '51820']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_VPN_L2TP, indirect=['patch_ansible_module'])
def test_vpn_l2tp_connection_unchanged(mocked_vpn_l2tp_connection_unchanged, capfd):
    """
    Test : L2TP VPN connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_VPN_PPTP, indirect=['patch_ansible_module'])
def test_vpn_pptp_connection_unchanged(mocked_vpn_pptp_connection_unchanged, capfd):
    """
    Test : PPTP VPN connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_VPN_L2TP, indirect=['patch_ansible_module'])
def test_create_vpn_l2tp(mocked_generic_connection_create, capfd):
    """
    Test : Create L2TP VPN connection
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'vpn'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'vpn_l2tp'

    add_args_text = list(map(to_text, add_args[0]))

    for param in ['connection.autoconnect', 'no',
                  'connection.permissions', 'brittany',
                  'vpn.data', 'vpn.service-type', 'org.freedesktop.NetworkManager.l2tp',
                  ]:
        assert param in add_args_text

    vpn_data_index = add_args_text.index('vpn.data') + 1
    args_vpn_data = add_args_text[vpn_data_index]
    for vpn_data in ['gateway=vpn.example.com', 'password-flags=2', 'user=brittany', 'ipsec-enabled=true', 'ipsec-psk=QnJpdHRhbnkxMjM=']:
        assert vpn_data in args_vpn_data

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_VPN_PPTP, indirect=['patch_ansible_module'])
def test_create_vpn_pptp(mocked_generic_connection_create, capfd):
    """
    Test : Create PPTP VPN connection
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'vpn'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'vpn_pptp'

    add_args_text = list(map(to_text, add_args[0]))

    for param in ['connection.autoconnect', 'no',
                  'connection.permissions', 'brittany',
                  'vpn.data', 'vpn.service-type', 'org.freedesktop.NetworkManager.pptp',
                  ]:
        assert param in add_args_text

    vpn_data_index = add_args_text.index('vpn.data') + 1
    args_vpn_data = add_args_text[vpn_data_index]
    for vpn_data in ['password-flags=2', 'gateway=vpn.example.com', 'user=brittany']:
        assert vpn_data in args_vpn_data

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_INFINIBAND_STATIC, indirect=['patch_ansible_module'])
def test_infiniband_connection_static_unchanged(mocked_infiniband_connection_static_unchanged, capfd):
    """
    Test : Infiniband connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_INFINIBAND_STATIC_MODIFY_TRANSPORT_MODE, indirect=['patch_ansible_module'])
def test_infiniband_connection_static_transport_mode_connected(
        mocked_infiniband_connection_static_transport_mode_connected_modify, capfd):
    """
    Test : Modify Infiniband connection to use connected as transport_mode
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[1]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'modify'
    assert add_args[0][3] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))

    for param in ['infiniband.transport-mode', 'connected']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)

    assert results.get('changed') is True
    assert not results.get('failed')


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_GENERIC_DIFF_CHECK, indirect=['patch_ansible_module'])
def test_bond_connection_unchanged(mocked_generic_connection_diff_check, capfd):
    """
    Test : Bond connection unchanged
    """

    module = AnsibleModule(
        argument_spec=dict(
            ignore_unsupported_suboptions=dict(type='bool', default=False),
            autoconnect=dict(type='bool', default=True),
            autoconnect_priority=dict(type='int'),
            autoconnect_retries=dict(type='int'),
            state=dict(type='str', required=True, choices=['absent', 'present']),
            conn_name=dict(type='str', required=True),
            conn_reload=dict(type='bool', required=False, default=False),
            master=dict(type='str'),
            slave_type=dict(type=str, choices=['bond', 'bridge', 'team']),
            ifname=dict(type='str'),
            type=dict(type='str',
                      choices=[
                          'bond',
                          'bond-slave',
                          'bridge',
                          'bridge-slave',
                          'dummy',
                          'ethernet',
                          'generic',
                          'gre',
                          'infiniband',
                          'ipip',
                          'sit',
                          'team',
                          'team-slave',
                          'vlan',
                          'vxlan',
                          'wifi',
                          'gsm',
                          'macvlan',
                          'wireguard',
                          'vpn',
                      ]),
            ip4=dict(type='list', elements='str'),
            gw4=dict(type='str'),
            gw4_ignore_auto=dict(type='bool', default=False),
            routes4=dict(type='list', elements='str'),
            routes4_extended=dict(type='list',
                                  elements='dict',
                                  options=dict(
                                      ip=dict(type='str', required=True),
                                      next_hop=dict(type='str'),
                                      metric=dict(type='int'),
                                      table=dict(type='int'),
                                      tos=dict(type='int'),
                                      cwnd=dict(type='int'),
                                      mtu=dict(type='int'),
                                      onlink=dict(type='bool')
                                  )),
            route_metric4=dict(type='int'),
            routing_rules4=dict(type='list', elements='str'),
            never_default4=dict(type='bool', default=False),
            dns4=dict(type='list', elements='str'),
            dns4_search=dict(type='list', elements='str'),
            dns4_options=dict(type='list', elements='str'),
            dns4_ignore_auto=dict(type='bool', default=False),
            method4=dict(type='str', choices=['auto', 'link-local', 'manual', 'shared', 'disabled']),
            may_fail4=dict(type='bool', default=True),
            dhcp_client_id=dict(type='str'),
            ip6=dict(type='list', elements='str'),
            gw6=dict(type='str'),
            gw6_ignore_auto=dict(type='bool', default=False),
            dns6=dict(type='list', elements='str'),
            dns6_search=dict(type='list', elements='str'),
            dns6_options=dict(type='list', elements='str'),
            dns6_ignore_auto=dict(type='bool', default=False),
            routes6=dict(type='list', elements='str'),
            routes6_extended=dict(type='list',
                                  elements='dict',
                                  options=dict(
                                      ip=dict(type='str', required=True),
                                      next_hop=dict(type='str'),
                                      metric=dict(type='int'),
                                      table=dict(type='int'),
                                      cwnd=dict(type='int'),
                                      mtu=dict(type='int'),
                                      onlink=dict(type='bool')
                                  )),
            route_metric6=dict(type='int'),
            method6=dict(type='str', choices=['ignore', 'auto', 'dhcp', 'link-local', 'manual', 'shared', 'disabled']),
            ip_privacy6=dict(type='str', choices=['disabled', 'prefer-public-addr', 'prefer-temp-addr', 'unknown']),
            addr_gen_mode6=dict(type='str', choices=['default', 'default-or-eui64', 'eui64', 'stable-privacy']),
            # Bond Specific vars
            mode=dict(type='str', default='balance-rr',
                      choices=['802.3ad', 'active-backup', 'balance-alb', 'balance-rr', 'balance-tlb', 'balance-xor', 'broadcast']),
            miimon=dict(type='int'),
            downdelay=dict(type='int'),
            updelay=dict(type='int'),
            xmit_hash_policy=dict(type='str'),
            fail_over_mac=dict(type='str', choices=['none', 'active', 'follow']),
            arp_interval=dict(type='int'),
            arp_ip_target=dict(type='str'),
            primary=dict(type='str'),
            # general usage
            mtu=dict(type='int'),
            mac=dict(type='str'),
            zone=dict(type='str'),
            # bridge specific vars
            stp=dict(type='bool', default=True),
            priority=dict(type='int', default=128),
            slavepriority=dict(type='int', default=32),
            forwarddelay=dict(type='int', default=15),
            hellotime=dict(type='int', default=2),
            maxage=dict(type='int', default=20),
            ageingtime=dict(type='int', default=300),
            hairpin=dict(type='bool'),
            path_cost=dict(type='int', default=100),
            # team specific vars
            runner=dict(type='str', default='roundrobin',
                             choices=['broadcast', 'roundrobin', 'activebackup', 'loadbalance', 'lacp']),
            # team active-backup runner specific options
            runner_hwaddr_policy=dict(type='str', choices=['same_all', 'by_active', 'only_active']),
            # team lacp runner specific options
            runner_fast_rate=dict(type='bool'),
            # vlan specific vars
            vlanid=dict(type='int'),
            vlandev=dict(type='str'),
            flags=dict(type='str'),
            ingress=dict(type='str'),
            egress=dict(type='str'),
            # vxlan specific vars
            vxlan_id=dict(type='int'),
            vxlan_local=dict(type='str'),
            vxlan_remote=dict(type='str'),
            # ip-tunnel specific vars
            ip_tunnel_dev=dict(type='str'),
            ip_tunnel_local=dict(type='str'),
            ip_tunnel_remote=dict(type='str'),
            # ip-tunnel type gre specific vars
            ip_tunnel_input_key=dict(type='str', no_log=True),
            ip_tunnel_output_key=dict(type='str', no_log=True),
            # 802-11-wireless* specific vars
            ssid=dict(type='str'),
            wifi=dict(type='dict'),
            wifi_sec=dict(type='dict', no_log=True),
            gsm=dict(type='dict'),
            macvlan=dict(type='dict'),
            wireguard=dict(type='dict'),
            vpn=dict(type='dict'),
            sriov=dict(type='dict'),
            # infiniband specific vars
            transport_mode=dict(type='str', choices=['datagram', 'connected']),
            infiniband_mac=dict(type='str'),
        ),
        mutually_exclusive=[['never_default4', 'gw4'],
                            ['routes4_extended', 'routes4'],
                            ['routes6_extended', 'routes6']],
        required_if=[("type", "wifi", [("ssid")])],
        supports_check_mode=True,
    )
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')

    nmcli_module = nmcli.Nmcli(module)

    changed, diff = nmcli_module.is_connection_changed()

    assert changed

    num_of_diff_params = 0
    for parameter, value in diff.get('before').items():
        if value != diff['after'][parameter]:
            num_of_diff_params += 1

    assert num_of_diff_params == 1


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_MACVLAN, indirect=['patch_ansible_module'])
def test_create_macvlan(mocked_generic_connection_create, capfd):
    """
    Test : Create macvlan connection with static IP configuration
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'macvlan'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'non_existent_nw_device'

    add_args_text = list(map(to_text, add_args[0]))
    for param in ['connection.interface-name', 'macvlan_non_existant',
                  'ipv4.method', 'manual',
                  'ipv4.addresses', '10.10.10.10/24',
                  'ipv6.method', 'manual',
                  'ipv6.addresses', '2001:db8::1/128',
                  'macvlan.mode', '2',
                  'macvlan.parent', 'non_existent_parent']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_MACVLAN, indirect=['patch_ansible_module'])
def test_macvlan_connection_unchanged(mocked_macvlan_connection_unchanged, capfd):
    """
    Test : Macvlan connection with static IP configuration unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_MACVLAN, indirect=['patch_ansible_module'])
def test_macvlan_mod(mocked_generic_connection_modify, capfd):
    """
    Test : Modify macvlan connection
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['macvlan.mode', '2']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


TESTCASE_SLAVE_TYPE_BRIDGE_CONNECTION = [
    {
        'type': 'ethernet',
        'conn_name': 'fake_conn',
        'ifname': 'fake_eth0',
        'state': 'present',
        'slave_type': 'bridge',
        'master': 'fake_br0',
        '_ansible_check_mode': False,
    }
]


TESTCASE_SLAVE_TYPE_BRIDGE_CONNECTION_SHOW_OUTPUT = """\
connection.id:                          fake_conn
connection.type:                        802-3-ethernet
connection.interface-name:              fake_eth0
connection.autoconnect:                 yes
connection.master:                      --
connection.slave-type:                  --
802-3-ethernet.mtu:                     auto
"""


TESTCASE_SLAVE_TYPE_BRIDGE_CONNECTION_UNCHANGED_SHOW_OUTPUT = """\
connection.id:                          fake_conn
connection.type:                        802-3-ethernet
connection.interface-name:              fake_eth0
connection.autoconnect:                 yes
connection.master:                      fake_br0
connection.slave-type:                  bridge
802-3-ethernet.mtu:                     auto
"""


@pytest.fixture
def mocked_slave_type_bridge_create(mocker):
    mocker_set(mocker,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_SLAVE_TYPE_BRIDGE_CONNECTION_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_SLAVE_TYPE_BRIDGE_CONNECTION, indirect=['patch_ansible_module'])
def test_create_slave_type_bridge(mocked_slave_type_bridge_create, capfd):
    """
    Test : slave for bridge created
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'ethernet'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'fake_conn'
    con_master_index = args[0].index('connection.master')
    slave_type_index = args[0].index('connection.slave-type')
    assert args[0][con_master_index + 1] == 'fake_br0'
    assert args[0][slave_type_index + 1] == 'bridge'

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.fixture
def mocked_create_slave_type_bridge_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_SLAVE_TYPE_BRIDGE_CONNECTION_UNCHANGED_SHOW_OUTPUT, ""))


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_SLAVE_TYPE_BRIDGE_CONNECTION, indirect=['patch_ansible_module'])
def test_slave_type_bridge_unchanged(mocked_create_slave_type_bridge_unchanged, capfd):
    """
    Test : Existent slave for bridge unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


TESTCASE_SLAVE_TYPE_BOND_CONNECTION = [
    {
        'type': 'ethernet',
        'conn_name': 'fake_conn',
        'ifname': 'fake_eth0',
        'state': 'present',
        'slave_type': 'bond',
        'master': 'fake_bond0',
        '_ansible_check_mode': False,
    }
]


TESTCASE_SLAVE_TYPE_BOND_CONNECTION_SHOW_OUTPUT = """\
connection.id:                          fake_conn
connection.type:                        802-3-ethernet
connection.interface-name:              fake_eth0
connection.autoconnect:                 yes
connection.master:                      --
connection.slave-type:                  --
802-3-ethernet.mtu:                     auto
"""


TESTCASE_SLAVE_TYPE_BOND_CONNECTION_UNCHANGED_SHOW_OUTPUT = """\
connection.id:                          fake_conn
connection.type:                        802-3-ethernet
connection.interface-name:              fake_eth0
connection.autoconnect:                 yes
connection.master:                      fake_bond0
connection.slave-type:                  bond
802-3-ethernet.mtu:                     auto
"""


@pytest.fixture
def mocked_slave_type_bond_create(mocker):
    mocker_set(mocker,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_SLAVE_TYPE_BOND_CONNECTION_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_SLAVE_TYPE_BOND_CONNECTION, indirect=['patch_ansible_module'])
def test_create_slave_type_bond(mocked_slave_type_bond_create, capfd):
    """
    Test : slave for bond created
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'ethernet'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'fake_conn'
    con_master_index = args[0].index('connection.master')
    slave_type_index = args[0].index('connection.slave-type')
    assert args[0][con_master_index + 1] == 'fake_bond0'
    assert args[0][slave_type_index + 1] == 'bond'

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.fixture
def mocked_create_slave_type_bond_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_SLAVE_TYPE_BOND_CONNECTION_UNCHANGED_SHOW_OUTPUT, ""))


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_SLAVE_TYPE_BOND_CONNECTION, indirect=['patch_ansible_module'])
def test_slave_type_bond_unchanged(mocked_create_slave_type_bond_unchanged, capfd):
    """
    Test : Existent slave for bridge unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


TESTCASE_SLAVE_TYPE_TEAM_CONNECTION = [
    {
        'type': 'ethernet',
        'conn_name': 'fake_conn',
        'ifname': 'fake_eth0',
        'state': 'present',
        'slave_type': 'team',
        'master': 'fake_team0',
        '_ansible_check_mode': False,
    }
]


TESTCASE_SLAVE_TYPE_TEAM_CONNECTION_SHOW_OUTPUT = """\
connection.id:                          fake_conn
connection.type:                        802-3-ethernet
connection.interface-name:              fake_eth0
connection.autoconnect:                 yes
connection.master:                      --
connection.slave-type:                  --
802-3-ethernet.mtu:                     auto
"""


TESTCASE_SLAVE_TYPE_TEAM_CONNECTION_UNCHANGED_SHOW_OUTPUT = """\
connection.id:                          fake_conn
connection.type:                        802-3-ethernet
connection.interface-name:              fake_eth0
connection.autoconnect:                 yes
connection.master:                      fake_team0
connection.slave-type:                  team
802-3-ethernet.mtu:                     auto
"""


@pytest.fixture
def mocked_slave_type_team_create(mocker):
    mocker_set(mocker,
               execute_return=None,
               execute_side_effect=(
                   (0, TESTCASE_SLAVE_TYPE_TEAM_CONNECTION_SHOW_OUTPUT, ""),
                   (0, "", ""),
               ))


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_SLAVE_TYPE_TEAM_CONNECTION, indirect=['patch_ansible_module'])
def test_create_slave_type_team(mocked_slave_type_team_create, capfd):
    """
    Test : slave for bond created
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'ethernet'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'fake_conn'
    con_master_index = args[0].index('connection.master')
    slave_type_index = args[0].index('connection.slave-type')
    assert args[0][con_master_index + 1] == 'fake_team0'
    assert args[0][slave_type_index + 1] == 'team'

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.fixture
def mocked_create_slave_type_team_unchanged(mocker):
    mocker_set(mocker,
               connection_exists=True,
               execute_return=(0, TESTCASE_SLAVE_TYPE_TEAM_CONNECTION_UNCHANGED_SHOW_OUTPUT, ""))


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_SLAVE_TYPE_TEAM_CONNECTION, indirect=['patch_ansible_module'])
def test_slave_type_team_unchanged(mocked_create_slave_type_team_unchanged, capfd):
    """
    Test : Existent slave for bridge unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_LOOPBACK, indirect=['patch_ansible_module'])
def test_create_loopback(mocked_generic_connection_create, capfd):
    """
    Test : Create loopback connection
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    add_args, add_kw = arg_list[0]

    assert add_args[0][0] == '/usr/bin/nmcli'
    assert add_args[0][1] == 'con'
    assert add_args[0][2] == 'add'
    assert add_args[0][3] == 'type'
    assert add_args[0][4] == 'loopback'
    assert add_args[0][5] == 'con-name'
    assert add_args[0][6] == 'lo'

    add_args_text = list(map(to_text, add_args[0]))
    for param in ['connection.interface-name', 'lo',
                  'ipv4.addresses', '127.0.0.1/8']:
        assert param in add_args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_LOOPBACK, indirect=['patch_ansible_module'])
def test_unchanged_loopback(mocked_loopback_connection_unchanged, capfd):
    """
    Test : loopback connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_LOOPBACK_MODIFY, indirect=['patch_ansible_module'])
def test_add_second_ip4_address_to_loopback_connection(mocked_loopback_connection_modify, capfd):
    """
    Test : Modify loopback connection
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 2
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[1]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'lo'

    for param in ['ipv4.addresses', '127.0.0.1/8,127.0.0.2/8']:
        assert param in args[0]

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_VRF, indirect=['patch_ansible_module'])
def test_create_vrf_con(mocked_generic_connection_create, capfd):
    """
    Test if VRF created
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'add'
    assert args[0][3] == 'type'
    assert args[0][4] == 'vrf'
    assert args[0][5] == 'con-name'
    assert args[0][6] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['ipv4.addresses', '10.10.10.10/24', 'ipv4.gateway', '10.10.10.1', 'table', '10']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_VRF, indirect=['patch_ansible_module'])
def test_mod_vrf_conn(mocked_generic_connection_modify, capfd):
    """
    Test if VRF modified
    """

    with pytest.raises(SystemExit):
        nmcli.main()

    assert nmcli.Nmcli.execute_command.call_count == 1
    arg_list = nmcli.Nmcli.execute_command.call_args_list
    args, kwargs = arg_list[0]

    assert args[0][0] == '/usr/bin/nmcli'
    assert args[0][1] == 'con'
    assert args[0][2] == 'modify'
    assert args[0][3] == 'non_existent_nw_device'

    args_text = list(map(to_text, args[0]))
    for param in ['ipv4.addresses', '10.10.10.10/24', 'ipv4.gateway', '10.10.10.1', 'table', '10']:
        assert param in args_text

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert results['changed']


@pytest.mark.parametrize('patch_ansible_module', TESTCASE_VRF, indirect=['patch_ansible_module'])
def test_vrf_connection_unchanged(mocked_vrf_connection_unchanged, capfd):
    """
    Test : VRF connection unchanged
    """
    with pytest.raises(SystemExit):
        nmcli.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get('failed')
    assert not results['changed']
