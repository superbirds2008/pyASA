import pytest
from netaddr import IPNetwork

from pyASA.address import Address
from pyASA.rule import rule_from_dict, RuleGeneric, RuleTCPUDP, RuleICMP, ServiceComparator
from pyASA.rulelogging import RuleLogging, LogLevel


class Test_RuleGeneric(object):
    @pytest.fixture
    def generic_rule(self):
        rule = RuleGeneric()
        rule.src = "192.168.23.0/24"
        rule.dst = "192.168.24.0/24"
        rule.permit = True
        rule.active = False
        rule.objectid = 1234567
        rule.is_access_rule = True
        rule.logging.interval = 60
        rule.logging.level = "Debugging"
        rule.protocol = 88
        rule.remark = "EIGRP Test Rule"
        rule.position = 17
        return rule

    def test_get_src(self, generic_rule: RuleGeneric):
        assert generic_rule.src == Address("192.168.23.0/24")

    def test_set_src(self, generic_rule: RuleGeneric):
        generic_rule.src = Address("10.4.5.6")
        assert generic_rule.src == Address("10.4.5.6")
        generic_rule.src = IPNetwork("10.1.2.0/24")
        assert generic_rule.src == Address("10.1.2.0/24")
        with pytest.raises(ValueError):
            generic_rule.src = "something strange"
        with pytest.raises(TypeError):
            generic_rule.src = None

    def test_get_dst(self, generic_rule: RuleGeneric):
        assert generic_rule.dst == Address("192.168.24.0/24")

    def test_set_dst(self, generic_rule: RuleGeneric):
        generic_rule.dst = Address("10.4.5.6")
        assert generic_rule.dst == Address("10.4.5.6")
        generic_rule.dst = IPNetwork("10.1.2.0/24")
        assert generic_rule.dst == Address("10.1.2.0/24")
        with pytest.raises(ValueError):
            generic_rule.dst = "something strange"
        with pytest.raises(TypeError):
            generic_rule.dst = None

    def test_get_permit(self, generic_rule: RuleGeneric):
        assert generic_rule.permit is True

    def test_set_permit(self, generic_rule: RuleGeneric):
        generic_rule.permit = False
        assert generic_rule.permit is False
        with pytest.raises(TypeError):
            generic_rule.permit = "bullshit"
        with pytest.raises(TypeError):
            generic_rule.permit = None

    def test_get_active(self, generic_rule: RuleGeneric):
        assert generic_rule.active is False

    def test_set_active(self, generic_rule: RuleGeneric):
        generic_rule.active = False
        assert generic_rule.active is False
        with pytest.raises(TypeError):
            generic_rule.active = "bullshit"
        with pytest.raises(TypeError):
            generic_rule.active = None

    def test_get_objectid(self, generic_rule: RuleGeneric):
        assert generic_rule.objectid == 1234567

    def test_set_objectid(self, generic_rule: RuleGeneric):
        generic_rule.objectid = 55
        assert generic_rule.objectid == 55
        with pytest.raises(ValueError):
            generic_rule.objectid = -1
        with pytest.raises(ValueError):
            generic_rule.objectid = None
        with pytest.raises(ValueError):
            generic_rule.objectid = "test"

    def test_get_is_access_rule(self, generic_rule: RuleGeneric):
        assert generic_rule.is_access_rule is True

    def test_set_is_access_rule(self, generic_rule: RuleGeneric):
        generic_rule.is_access_rule = False
        assert generic_rule.is_access_rule is False
        with pytest.raises(ValueError):
            generic_rule.is_access_rule = None
        with pytest.raises(ValueError):
            generic_rule.is_access_rule = 5
        with pytest.raises(ValueError):
            generic_rule.is_access_rule = "testing"

    def test_get_logging(self, generic_rule: RuleGeneric):
        assert generic_rule.logging == RuleLogging(LogLevel.DEBUGGING, 60)

    def test_set_logging(self, generic_rule: RuleGeneric):
        generic_rule.logging = RuleLogging()
        assert generic_rule.logging.interval == 300
        assert generic_rule.logging.level == LogLevel.DEFAULT
        generic_rule.logging = None
        assert generic_rule.logging.interval == 300
        assert generic_rule.logging.level == LogLevel.DEFAULT
        with pytest.raises(TypeError):
            generic_rule.logging = 6

    def test_get_protocol(self, generic_rule: RuleGeneric):
        assert generic_rule.protocol == 88

    def test_set_protocol(self, generic_rule: RuleGeneric):
        generic_rule.protocol = "5"
        assert generic_rule.protocol == 5
        with pytest.raises(ValueError):
            generic_rule.protocol = "icmp"
        with pytest.raises(ValueError):
            generic_rule.protocol = "icmp6"
        with pytest.raises(ValueError):
            generic_rule.protocol = "tcp"
        with pytest.raises(ValueError):
            generic_rule.protocol = "udp"
        with pytest.raises(ValueError):
            generic_rule.protocol = "something wrong"
        with pytest.raises(ValueError):
            generic_rule.protocol = 1
        with pytest.raises(ValueError):
            generic_rule.protocol = 6
        with pytest.raises(ValueError):
            generic_rule.protocol = 17
        with pytest.raises(ValueError):
            generic_rule.protocol = 58
        with pytest.raises(ValueError):
            generic_rule.protocol = -37
        with pytest.raises(TypeError):
            generic_rule.protocol = None

    def test_get_protocol_alias(self, generic_rule: RuleGeneric):
        assert generic_rule.protocol_alias == "eigrp"
        generic_rule.protocol = 237
        assert generic_rule.protocol_alias == "237"

    def test_get_remark(self, generic_rule: RuleGeneric):
        assert generic_rule.remark == ["EIGRP Test Rule"]

    def test_set_remark(self, generic_rule: RuleGeneric):
        generic_rule.remark = "Test"
        assert generic_rule.remark == ["Test"]
        generic_rule.remark = ["Line 1", "Line 2"]
        assert generic_rule.remark == ["Line 1", "Line 2"]
        generic_rule.remark = None
        assert generic_rule.remark == []
        with pytest.raises(TypeError):
            generic_rule.remark = 6
        with pytest.raises(TypeError):
            generic_rule.remark = {1: "Line", 2: "Line"}

    def test_get_position(self, generic_rule: RuleGeneric):
        assert generic_rule.position == 17

    def test_set_position(self, generic_rule: RuleGeneric):
        generic_rule.position = 53
        assert generic_rule.position == 53
        with pytest.raises(ValueError):
            generic_rule.position = -1
        with pytest.raises(ValueError):
            generic_rule.position = None
        with pytest.raises(ValueError):
            generic_rule.position = "5"

    def test_parse_protocol_json(self):
        assert RuleGeneric._parse_protocol_json("eigrp") == 88
        assert RuleGeneric._parse_protocol_json("64") == 64
        with pytest.raises(ValueError):
            RuleGeneric._parse_protocol_json("echo")

    def test_to_cli(self, generic_rule: RuleGeneric):
        assert generic_rule.to_cli() == "extended permit eigrp 192.168.23.0 255.255.255.0 192.168.24.0 255.255.255.0 log debugging interval 60 inactive"
        assert generic_rule.to_cli("TEST") == "access-list TEST extended permit eigrp 192.168.23.0 255.255.255.0 192.168.24.0 255.255.255.0 log debugging interval 60 inactive"

    def test_from_dict(self, generic_rule: RuleGeneric):
        data = {'permit': True, 'sourceAddress': {'kind': 'IPv4Network', 'value': '192.168.23.0/24'},
                'destinationAddress': {'kind': 'IPv4Network', 'value': '192.168.24.0/24'},
                'sourceService': {'kind': 'NetworkProtocol', 'value': 'eigrp'},
                'destinationService': {'kind': 'NetworkProtocol', 'value': 'eigrp'}, 'active': False,
                'remarks': ['EIGRP Test Rule'], 'ruleLogging': {'logStatus': 'Debugging', 'logInterval': 60},
                'position': 17, 'isAccessRule': True, 'objectId': 1234567}
        print(generic_rule)
        print(rule_from_dict(data))
        assert generic_rule == rule_from_dict(data)

    def test_to_dict(self, generic_rule: RuleGeneric):
        data = {'permit': True, 'sourceAddress': {'kind': 'IPv4Network', 'value': '192.168.23.0/24'},
                'destinationAddress': {'kind': 'IPv4Network', 'value': '192.168.24.0/24'},
                'sourceService': {'kind': 'NetworkProtocol', 'value': 'eigrp'},
                'destinationService': {'kind': 'NetworkProtocol', 'value': 'eigrp'}, 'active': False,
                'remarks': ['EIGRP Test Rule'], 'ruleLogging': {'logStatus': 'Debugging', 'logInterval': 60},
                'position': 17, 'isAccessRule': True, 'objectId': 1234567}
        assert generic_rule.to_dict() == data

    def test_equals(self, generic_rule: RuleGeneric):
        assert generic_rule is not None
        assert not generic_rule == "Bla"
        assert not generic_rule == 6
        assert not generic_rule == RuleGeneric()

    def test_contains(self, generic_rule: RuleGeneric):
        rule = generic_rule.clone()
        assert rule in generic_rule
        generic_rule.protocol = 0
        assert rule in generic_rule
        rule.is_access_rule = False
        assert rule in generic_rule
        rule.remark = None
        assert rule in generic_rule
        rule.position = 0
        assert rule in generic_rule
        generic_rule.src = "192.168.22.0/23"
        assert rule in generic_rule
        generic_rule.src = "192.168.22.0/24"
        assert rule not in generic_rule
        rule.src = "192.168.22.17"
        assert rule in generic_rule
        rule.permit = False
        assert rule not in generic_rule
        rule.permit = True
        rule.active = True
        assert rule not in generic_rule

    def test_contains_tcpudp(self, generic_rule: RuleGeneric):
        ruletcpudp = RuleTCPUDP()
        ruletcpudp.src = "192.168.23.1"
        ruletcpudp.dst = "192.168.24.1"
        ruletcpudp.permit = True
        ruletcpudp.active = False
        ruletcpudp.objectid = 1234567
        ruletcpudp.is_access_rule = True
        ruletcpudp.logging.interval = 60
        ruletcpudp.logging.level = "Debugging"
        ruletcpudp.remark = "EIGRP Test Rule"
        ruletcpudp.position = 17
        assert ruletcpudp not in generic_rule
        generic_rule.protocol = 0
        assert ruletcpudp in generic_rule


class Test_RuleTCPUDP(object):
    @pytest.fixture
    def generic_rule(self):
        rule = RuleTCPUDP()
        rule.src = "192.168.23.31"
        rule.dst = "192.168.24.0/24"
        rule.src_port = "any"
        rule.dst_port = "ssh"
        rule.permit = True
        rule.active = False
        rule.objectid = 1234567
        rule.is_access_rule = True
        rule.logging.interval = 60
        rule.logging.level = "Debugging"
        rule.protocol = "tcp"
        rule.remark = "SSH Test Rule"
        rule.position = 17
        return rule

    def test_get_src_port(self, generic_rule: RuleTCPUDP):
        assert generic_rule.src_port == -1

    def test_set_src_port(self, generic_rule: RuleTCPUDP):
        generic_rule.src_port = 53
        assert generic_rule.src_port == 53
        generic_rule.src_port = "any"
        assert generic_rule.src_port == -1
        generic_rule.src_port = "17"
        assert generic_rule.src_port == 17
        with pytest.raises(ValueError):
            generic_rule.src_port = "wrong"
        with pytest.raises(ValueError):
            generic_rule.src_port = 0
        with pytest.raises(ValueError):
            generic_rule.src_port = -2
        with pytest.raises(ValueError):
            generic_rule.src_port = 65536
        with pytest.raises(TypeError):
            generic_rule.src_port = None

    def test_get_dst_port(self, generic_rule: RuleTCPUDP):
        assert generic_rule.dst_port == 22

    def test_set_dst_port(self, generic_rule: RuleTCPUDP):
        generic_rule.dst_port = "any"
        assert generic_rule.dst_port == -1
        generic_rule.dst_port = 53
        assert generic_rule.dst_port == 53
        generic_rule.dst_port = "any"
        assert generic_rule.dst_port == -1
        generic_rule.dst_port = "17"
        assert generic_rule.dst_port == 17
        with pytest.raises(ValueError):
            generic_rule.dst_port = "wrong"
        with pytest.raises(ValueError):
            generic_rule.dst_port = 0
        with pytest.raises(ValueError):
            generic_rule.dst_port = -2
        with pytest.raises(ValueError):
            generic_rule.dst_port = 65536
        with pytest.raises(TypeError):
            generic_rule.dst_port = None

    def test_get_protocol(self, generic_rule: RuleTCPUDP):
        assert generic_rule.protocol == 6

    def test_set_protocol(self, generic_rule: RuleTCPUDP):
        generic_rule.protocol = "17"
        assert generic_rule.protocol == 17
        with pytest.raises(ValueError):
            generic_rule.protocol = "icmp"
        with pytest.raises(ValueError):
            generic_rule.protocol = "icmp6"
        with pytest.raises(ValueError):
            generic_rule.protocol = "eigrp"
        with pytest.raises(ValueError):
            generic_rule.protocol = "ospf"
        with pytest.raises(ValueError):
            generic_rule.protocol = "something wrong"
        with pytest.raises(ValueError):
            generic_rule.protocol = 0
        with pytest.raises(ValueError):
            generic_rule.protocol = 9
        with pytest.raises(ValueError):
            generic_rule.protocol = 1
        with pytest.raises(ValueError):
            generic_rule.protocol = 58
        with pytest.raises(ValueError):
            generic_rule.protocol = -37
        with pytest.raises(ValueError):
            generic_rule.protocol = None

    def test_get_src_port_alias(self, generic_rule: RuleTCPUDP):
        generic_rule.src_port = -1
        assert generic_rule.src_port_alias == "any"
        generic_rule.src_port = 22
        assert generic_rule.src_port_alias == "ssh"
        generic_rule.src_port = 3859
        assert generic_rule.src_port_alias == "3859"

    def test_get_dst_port_alias(self, generic_rule: RuleTCPUDP):
        generic_rule.dst_port = -1
        assert generic_rule.dst_port_alias == "any"
        generic_rule.dst_port = 22
        assert generic_rule.dst_port_alias == "ssh"
        generic_rule.dst_port = 3859
        assert generic_rule.dst_port_alias == "3859"

    def test_src_comparator(self, generic_rule: RuleTCPUDP):
        assert generic_rule.src_comp == ServiceComparator.EQUAL
        generic_rule.src_comp = ServiceComparator.LESSER
        assert generic_rule.src_comp == ServiceComparator.LESSER
        generic_rule.src_comp = ">"
        assert generic_rule.src_comp == ServiceComparator.GREATER
        with pytest.raises(ValueError):
            generic_rule.src_comp = None
        with pytest.raises(ValueError):
            generic_rule.src_comp = "<<"

    def test_dst_comparator(self, generic_rule: RuleTCPUDP):
        assert generic_rule.dst_comp == ServiceComparator.EQUAL
        generic_rule.dst_comp = ServiceComparator.LESSER
        assert generic_rule.dst_comp == ServiceComparator.LESSER
        generic_rule.dst_comp = ">"
        assert generic_rule.dst_comp == ServiceComparator.GREATER
        with pytest.raises(ValueError):
            generic_rule.dst_comp = None
        with pytest.raises(ValueError):
            generic_rule.dst_comp = "<<"

    def test_parse_port_json(self):
        data = {"kind": "NetworkProtocol", "value": "tcp"}
        assert RuleTCPUDP._parse_port_json(data) == ("tcp", "any", ServiceComparator.EQUAL)
        data = {"kind": "TcpUdpService", "value": ">udp/3456"}
        assert RuleTCPUDP._parse_port_json(data) == ("udp", 3456, ServiceComparator.GREATER)
        with pytest.raises(ValueError):
            RuleTCPUDP._parse_port_json({"kind": "TcpUdpService", "value": "udp/$%f!"})
        with pytest.raises(ValueError):
            RuleTCPUDP._parse_port_json({"kind": "TcpUdpService", "value": "<>tcp/ssh"})
        with pytest.raises(ValueError):
            RuleTCPUDP._parse_port_json({"kind": "TcpUdpService", "value": "tcp/!=22"})

    def test_to_cli(self, generic_rule: RuleTCPUDP):
        assert generic_rule.to_cli() == "extended permit tcp host 192.168.23.31 192.168.24.0 255.255.255.0 eq ssh log debugging interval 60 inactive"
        assert generic_rule.to_cli("TEST") == "access-list TEST extended permit tcp host 192.168.23.31 192.168.24.0 255.255.255.0 eq ssh log debugging interval 60 inactive"

    def test_from_dict(self):
        data = {"permit": True, "sourceAddress": {"kind": "IPv6Address", "value": "::1"},
                "destinationAddress": {"kind": "IPv6Network", "value": "::1/128"},
                "sourceService": {"kind": "NetworkProtocol", "value": "tcp"},
                "destinationService": {"kind": "TcpUdpService", "value": "!=tcp/sqlnet"}, "active": True, "remarks": []}
        assert isinstance(rule_from_dict(data), RuleTCPUDP)

    def test_to_dict(self, generic_rule: RuleTCPUDP):
        data = {'permit': True, 'sourceAddress': {'kind': 'IPv4Address', 'value': '192.168.23.31'},
                'destinationAddress': {'kind': 'IPv4Network', 'value': '192.168.24.0/24'},
                'sourceService': {'kind': 'NetworkProtocol', 'value': 'tcp'},
                'destinationService': {'kind': 'TcpUdpService', 'value': 'tcp/ssh'}, 'active': False,
                'remarks': ['SSH Test Rule'], 'ruleLogging': {'logStatus': 'Debugging', 'logInterval': 60},
                'position': 17, 'isAccessRule': True, 'objectId': 1234567}
        assert generic_rule.to_dict() == data
        generic_rule.src_port = 22
        generic_rule.dst_port = "any"
        data = {'permit': True, 'sourceAddress': {'kind': 'IPv4Address', 'value': '192.168.23.31'},
                'destinationAddress': {'kind': 'IPv4Network', 'value': '192.168.24.0/24'},
                'sourceService': {'kind': 'TcpUdpService', 'value': 'tcp/ssh'},
                'destinationService': {'kind': 'NetworkProtocol', 'value': 'tcp'}, 'active': False,
                'remarks': ['SSH Test Rule'], 'ruleLogging': {'logStatus': 'Debugging', 'logInterval': 60},
                'position': 17, 'isAccessRule': True, 'objectId': 1234567}
        assert generic_rule.to_dict() == data

    def test_contains(self, generic_rule: RuleTCPUDP):
        rule = generic_rule.clone()
        assert rule in generic_rule
        generic_rule.src = "any"
        assert rule in generic_rule
        rule.dst = "192.168.24.255"
        assert rule in generic_rule
        generic_rule.dst = "any4"
        assert rule in generic_rule
        rule.src_port = "80"
        assert rule in generic_rule
        rule.src_comp = ServiceComparator.NOT_EQUAL
        assert rule in generic_rule
        generic_rule.dst_port = 21
        assert rule not in generic_rule
        generic_rule.dst_comp = ServiceComparator.GREATER
        assert rule in generic_rule
        rule.dst_comp = ServiceComparator.LESSER
        assert rule not in generic_rule
        rule.dst_port = -1
        assert rule not in generic_rule
        rule.dst_port = 80
        assert rule not in generic_rule
        generic_rule.dst_port = "any"
        assert rule in generic_rule
        rule.dst_comp = ServiceComparator.NOT_EQUAL
        rule.dst_port = 17
        assert rule in generic_rule
        generic_rule.dst_comp = ServiceComparator.LESSER
        generic_rule.dst_port = 36
        assert rule not in generic_rule
        rule.dst_comp = ServiceComparator.EQUAL
        assert rule in generic_rule
        rule.objectid = 7654321
        rule.is_access_rule = False
        rule.logging.interval = 120
        rule.logging.level = LogLevel.ALERTS
        rule.remark = "other Test Rule"
        rule.position = 99
        assert rule in generic_rule
        rule.protocol = "udp"
        assert rule not in generic_rule

    def test_contains_other(self, generic_rule: RuleTCPUDP):
        rule = RuleGeneric()
        rule.src = "192.168.23.31"
        rule.dst = "192.168.24.1"
        rule.permit = True
        rule.active = False
        assert rule not in generic_rule
        rule = RuleICMP()
        rule.src = "192.168.23.31"
        rule.dst = "192.168.24.1"
        rule.permit = True
        rule.active = False
        assert rule not in generic_rule


class Test_RuleICMP(object):
    @pytest.fixture
    def generic_rule(self):
        rule = RuleICMP()
        rule.src = "192.168.23.31"
        rule.dst = "192.168.24.0/24"
        rule.icmp_type = "echo"
        rule.icmp_code = "5"
        rule.permit = True
        rule.active = False
        rule.objectid = 1234567
        rule.is_access_rule = True
        rule.logging.interval = 60
        rule.logging.level = "Debugging"
        rule.protocol = "icmp"
        rule.remark = "ICMP Test Rule"
        rule.position = 17
        return rule

    def test_protocol(self, generic_rule: RuleICMP):
        assert generic_rule.protocol == 1
        generic_rule.protocol = "58"
        assert generic_rule.protocol == 58
        with pytest.raises(ValueError):
            generic_rule.protocol = 6
        with pytest.raises(ValueError):
            generic_rule.protocol = 17
        with pytest.raises(ValueError):
            generic_rule.protocol = "tcp"
        with pytest.raises(ValueError):
            generic_rule.protocol = "udp"
        with pytest.raises(ValueError):
            generic_rule.protocol = 0
        with pytest.raises(ValueError):
            generic_rule.protocol = "eigrp"
        with pytest.raises(ValueError):
            generic_rule.protocol = None
        with pytest.raises(ValueError):
            generic_rule.protocol = dict()

    def test_protocol_alias(self, generic_rule: RuleICMP):
        assert generic_rule.protocol_alias == "icmp"
        generic_rule.protocol = 58
        assert generic_rule.protocol_alias == "icmp6"

    def test_icmp_type(self, generic_rule: RuleICMP):
        assert generic_rule.icmp_type == 8
        generic_rule.icmp_type = "echo-reply"
        assert generic_rule.icmp_type == 0
        generic_rule.icmp_type = 255
        assert generic_rule.icmp_type == 255
        generic_rule.icmp_type = -1
        assert generic_rule.icmp_type == -1
        generic_rule.icmp_type = "7"
        assert generic_rule.icmp_type == 7
        generic_rule.icmp_type = "any"
        assert generic_rule.icmp_type == -1
        with pytest.raises(ValueError):
            generic_rule.icmp_type = -2
        with pytest.raises(ValueError):
            generic_rule.icmp_type = 256
        with pytest.raises(ValueError):
            generic_rule.icmp_type = "wrong"
        with pytest.raises(ValueError):
            generic_rule.icmp_type = None
        with pytest.raises(ValueError):
            generic_rule.icmp_type = dict()

    def test_icmp_type_alias(self, generic_rule: RuleICMP):
        assert generic_rule.icmp_type_alias == "echo"
        generic_rule.icmp_type = 253
        assert generic_rule.icmp_type_alias == "253"

    def test_icmp_code(self, generic_rule: RuleICMP):
        assert generic_rule.icmp_code == 5
        generic_rule.icmp_code = 0
        assert generic_rule.icmp_code == 0
        generic_rule.icmp_code = 250
        assert generic_rule.icmp_code == 250
        generic_rule.icmp_code = "any"
        assert generic_rule.icmp_code == -1
        generic_rule.icmp_code = "7"
        assert generic_rule.icmp_code == 7
        generic_rule.icmp_code = -1
        assert generic_rule.icmp_code == -1
        with pytest.raises(ValueError):
            generic_rule.icmp_code = -2
        with pytest.raises(ValueError):
            generic_rule.icmp_code = 256
        with pytest.raises(ValueError):
            generic_rule.icmp_code = "wrong"
        with pytest.raises(ValueError):
            generic_rule.icmp_code = None
        with pytest.raises(ValueError):
            generic_rule.icmp_code = dict()

    def test_parse_icmp_json(self):
        assert RuleICMP._parse_icmp_json({"kind": "NetworkProtocol", "value": "icmp"}) == ("icmp", -1, -1)
        assert RuleICMP._parse_icmp_json({"kind": "ICMPService", "value": "icmp/7"}) == ("icmp", 7, -1)
        assert RuleICMP._parse_icmp_json({"kind": "ICMPService", "value": "icmp/echo/5"}) == ("icmp", "echo", 5)
        with pytest.raises(ValueError):
            RuleICMP._parse_icmp_json({"kind": "ICMPService", "value": "imp/7"})
        with pytest.raises(ValueError):
            RuleICMP._parse_icmp_json({"kind": "NetworkProtocol", "value": "icm"})

    def test_from_dict(self):
        data = {"permit": True, "sourceAddress": {"kind": "AnyIPAddress", "value": "any"},
                "destinationAddress": {"kind": "AnyIPAddress", "value": "any"},
                "sourceService": {"kind": "NetworkProtocol", "value": "icmp"},
                "destinationService": {"kind": "ICMPService", "value": "icmp/echo-reply/5"}, "active": True,
                "remarks": []}
        assert isinstance(rule_from_dict(data), RuleICMP)

    def test_to_cli(self, generic_rule: RuleICMP):
        assert generic_rule.to_cli() == "extended permit icmp host 192.168.23.31 192.168.24.0 255.255.255.0 echo 5 log debugging interval 60 inactive"
        assert generic_rule.to_cli("TEST") == "access-list TEST extended permit icmp host 192.168.23.31 192.168.24.0 255.255.255.0 echo 5 log debugging interval 60 inactive"

    def test_to_dict(self, generic_rule: RuleICMP):
        data = {'permit': True, 'sourceAddress': {'kind': 'IPv4Address', 'value': '192.168.23.31'},
                'destinationAddress': {'kind': 'IPv4Network', 'value': '192.168.24.0/24'},
                'sourceService': {'kind': 'NetworkProtocol', 'value': 'icmp'},
                'destinationService': {'kind': 'ICMPService', 'value': 'icmp/echo/5'}, 'active': False,
                'remarks': ['ICMP Test Rule'], 'ruleLogging': {'logStatus': 'Debugging', 'logInterval': 60},
                'position': 17, 'isAccessRule': True, 'objectId': 1234567}
        assert generic_rule.to_dict() == data
        generic_rule.protocol = "icmp6"
        generic_rule.icmp_type = 129
        generic_rule.icmp_code = -1
        data = {'permit': True, 'sourceAddress': {'kind': 'IPv4Address', 'value': '192.168.23.31'},
                'destinationAddress': {'kind': 'IPv4Network', 'value': '192.168.24.0/24'},
                'sourceService': {'kind': 'NetworkProtocol', 'value': 'icmp6'},
                'destinationService': {'kind': 'ICMP6Service', 'value': 'icmp6/echo-reply'}, 'active': False,
                'remarks': ['ICMP Test Rule'], 'ruleLogging': {'logStatus': 'Debugging', 'logInterval': 60},
                'position': 17, 'isAccessRule': True, 'objectId': 1234567}
        assert generic_rule.to_dict() == data
        generic_rule.icmp_type = -1
        data = {'permit': True, 'sourceAddress': {'kind': 'IPv4Address', 'value': '192.168.23.31'},
                'destinationAddress': {'kind': 'IPv4Network', 'value': '192.168.24.0/24'},
                'sourceService': {'kind': 'NetworkProtocol', 'value': 'icmp6'},
                'destinationService': {'kind': 'NetworkProtocol', 'value': 'icmp6'}, 'active': False,
                'remarks': ['ICMP Test Rule'], 'ruleLogging': {'logStatus': 'Debugging', 'logInterval': 60},
                'position': 17, 'isAccessRule': True, 'objectId': 1234567}
        assert generic_rule.to_dict() == data

    def test_contains(self, generic_rule: RuleICMP):
        rule = generic_rule.clone()
        assert rule in generic_rule
        rule.icmp_code = -1
        assert rule not in generic_rule
        rule.icmp_type = -1
        assert rule not in generic_rule
        rule.icmp_code = 5
        assert rule not in generic_rule
        generic_rule.icmp_code = -1
        assert rule not in generic_rule
        generic_rule.icmp_type = "any"
        assert rule in generic_rule

    def test_contains_other(self, generic_rule: RuleICMP):
        rule = RuleGeneric()
        rule.src = "192.168.23.31"
        rule.dst = "192.168.24.1"
        rule.permit = True
        rule.active = False
        assert rule not in generic_rule
        rule = RuleTCPUDP()
        rule.src = "192.168.23.31"
        rule.dst = "192.168.24.1"
        rule.permit = True
        rule.active = False
        assert rule not in generic_rule
        rule.icmp_type = "echo"
        rule.icmp_code = 5
        assert rule not in generic_rule
