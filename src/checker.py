import re

class RuleChecker:
    def __init__(self):
        # Define deterministic rules using regex patterns and checks
        self.rules = [
            {
                "id": "R001",
                "type": "INTERFACE_ADMINISTRATIVELY_DOWN",
                "severity": "HIGH",
                "pattern": r'([A-Za-z0-9/\.\-]+)\s+is administratively down',
                "recommendation": "Enter interface configuration mode for {0} and execute 'no shutdown'."
            },
            {
                "id": "R002",
                "type": "INTERFACE_LINK_DOWN",
                "severity": "HIGH",
                "pattern": r'([A-Za-z0-9/\.\-]+)\s+is down,\s+line protocol is down(?!\s+\(disabled\))',
                "recommendation": "Check physical cabling, port security, or clock rate on {0}."
            },
            {
                "id": "R003",
                "type": "DUPLICATE_IP_ADDRESS",
                "severity": "CRITICAL",
                "pattern": r'%IP-4-DUP[_]?ADDR: Duplicate address ([0-9\.]+) on ([A-Za-z0-9/\.\-]+)',
                "recommendation": "Change IP address on {1} or the conflicting device to resolve the duplication of {0}."
            },
            {
                "id": "R004",
                "type": "INCORRECT_SUBNET_MASK",
                "severity": "HIGH",
                "pattern": r'overlaps with ([A-Za-z0-9/\.\-]+)',
                "recommendation": "Adjust subnet mask or IP address to prevent overlapping networks on {0}."
            },
            {
                "id": "R005",
                "type": "GATEWAY_MISMATCH",
                "severity": "HIGH",
                "pattern": r'Default gateway is not set|Gateway of last resort is not set|Default Gateway IP Misconfiguration|Outside subnet boundary',
                "recommendation": "Configure a valid default gateway in the correct subnet."
            },
            {
                "id": "R006",
                "type": "MISSING_VLAN",
                "severity": "HIGH",
                "pattern": r'VLAN ([0-9]+) does not exist in|missing from allowed list',
                "recommendation": "Create the missing VLAN or add it to the trunk allowed list."
            },
            {
                "id": "R007",
                "type": "VLAN_MISMATCH",
                "severity": "HIGH",
                "pattern": r'%CDP-4-NATIVE_VLAN_MISMATCH: Native VLAN mismatch|Native VLAN Mismatch on trunk link|Native VLAN Mismatch',
                "recommendation": "Ensure both ends of the trunk link have the same native VLAN configured."
            },
            {
                "id": "R008",
                "type": "MISSING_ROUTES",
                "severity": "HIGH",
                "pattern": r'Network not in table|Next-hop IP .* unreachable',
                "recommendation": "Verify routing protocol configuration or add a valid static route for the missing network."
            },
            {
                "id": "R009",
                "type": "DHCP_PROBLEMS",
                "severity": "HIGH",
                "pattern": r'ip helper-address is not configured|missing ip helper-address|DHCP pool exhausted|zero available',
                "recommendation": "Configure 'ip helper-address' on the router interface or expand the DHCP pool size."
            },
            {
                "id": "R010",
                "type": "DNS_CONFIGURATION_PROBLEMS",
                "severity": "WARNING",
                "pattern": r'Translating ".*"\.\.\.domain server \(255\.255\.255\.255\)|not active|no ip domain-lookup',
                "recommendation": "Configure a valid DNS server using 'ip name-server' or disable DNS lookup."
            },
            {
                "id": "R011",
                "type": "ACL_INDICATORS",
                "severity": "WARNING",
                "pattern": r'denied by (access-list|ACL) ([0-9A-Za-z_-]+)|administratively prohibited|deny tcp|missing port|Overly permissive ACL',
                "recommendation": "Review the access-list rules to ensure required traffic is permitted."
            },
            {
                "id": "R012",
                "type": "NAT_INDICATORS",
                "severity": "HIGH",
                "pattern": r'overload is missing|NAT pool exhausted|missing overload keyword|missing ip nat inside',
                "recommendation": "Add 'overload' keyword for PAT or expand NAT pool/verify NAT inside/outside interface assignments."
            },
            {
                "id": "R013",
                "type": "TRUNK_CONFIGURATION_INDICATORS",
                "severity": "HIGH",
                "pattern": r'Command rejected: An interface whose trunk encapsulation is "Auto" can not be configured to "trunk" mode.|configured as access instead of trunk',
                "recommendation": "Manually set the trunk encapsulation and ensure the port is configured as a trunk."
            },
            {
                "id": "R014",
                "type": "OSPF_MISMATCH",
                "severity": "HIGH",
                "pattern": r'OSPF Hello Timer Mismatch|passive-interface|missing subnets keyword',
                "recommendation": "Check OSPF hello/dead timers, ensure active interfaces are not passive, and use 'subnets' for redistribution."
            },
            {
                "id": "R015",
                "type": "PORT_SECURITY",
                "severity": "MEDIUM",
                "pattern": r'PSECURE_VIOLATION',
                "recommendation": "Check port security max limit and connected MAC addresses."
            }
        ]

    def check(self, case_data):
        output = case_data.get('show_command_output', '')
        if not isinstance(output, str):
            output = str(output)
            
        findings = []

        for rule in self.rules:
            # Use ignorecase for broader matching
            matches = list(re.finditer(rule['pattern'], output, re.IGNORECASE))
            for match in matches:
                # Handle duplicated reports for admin down vs link down
                if rule["id"] == "R002" and "administratively down" in match.group(0).lower():
                    continue

                groups = match.groups()
                # Format recommendation with capture groups if available
                recommendation = rule['recommendation']
                try:
                    if groups:
                        recommendation = recommendation.format(*groups)
                except IndexError:
                    pass

                findings.append({
                    "rule_id": rule['id'],
                    "type": rule['type'],
                    "severity": rule['severity'],
                    "evidence": match.group(0).strip(),
                    "recommendation": recommendation
                })

        status = "ERRORS_DETECTED" if findings else "PASS"
        # Optional: check if any warnings exist, but ERRORS takes precedence
        if status == "PASS" and any(f["severity"] == "WARNING" for f in findings):
            status = "WARNING"

        return {
            "status": status,
            "findings": findings
        }

def check_rules(case_data):
    checker = RuleChecker()
    return checker.check(case_data)
