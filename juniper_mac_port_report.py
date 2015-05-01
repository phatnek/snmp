#!/usr/bin/python

import os

# get tables from the switch
#get table of vlan IDs
raw_vlans = os.popen('snmpwalk -v2c -c public sw-ctl-cryoctlrm-0.ctlnetman.nscl.msu.edu 1.3.6.1.2.1.17.7.1.4.3.1.1').read()
# get table of ports(not switch interfaces)
raw_ports = os.popen('snmpwalk -v2c -c public sw-ctl-cryoctlrm-0.ctlnetman.nscl.msu.edu 1.3.6.1.2.1.17.1.4.1.2').read()
# get table of ports-to-interface names
raw_ifs = os.popen('snmpwalk -v2c -c public sw-ctl-cryoctlrm-0.ctlnetman.nscl.msu.edu 1.3.6.1.2.1.2.2.1.2').read()

ifs_list = {}
#print raw_vlans
for ifs_line in raw_ifs.splitlines():
  parts = ifs_line.split()
  ifs_parts=parts[0].rsplit(".",1)
  #print "{0} {1}".format(ifs_parts[1],parts[3])
  ifs_list.update({ifs_parts[1]:parts[3]})
print ifs_list
#exit()

ports_list = {}
#print raw_vlans
for ports_line in raw_ports.splitlines():
  parts = ports_line.split()
  ports_parts=parts[0].rsplit(".",1)
  #print "{0} {1}".format(ports_parts[1],parts[3])
  ports_list.update({ports_parts[1]:parts[3]})
print ports_list
#exit()

vlans_list = {}
#print raw_vlans
for vlans_line in raw_vlans.splitlines():
  parts = vlans_line.split()
  vlans_parts=parts[0].rsplit(".",1)
  #print "{0} {1}".format(vlans_parts[1],parts[3])
  vlans_list.update({vlans_parts[1]:parts[3]})
print vlans_list
#exit()

# get mac learning table (forwarding table)
# This table has a line for each mac: oid.<vlan_id>.<mac.as.decimal>=<portid>
# Note that to get the switch interface, you need to look up the portid in ports
# table to get the port number, then look up the portnumber in the interfaces
# table to get the interface name.
raw_mac = os.popen('snmpwalk -v2c -c public sw-ctl-cryoctlrm-0.ctlnetman.nscl.msu.edu 1.3.6.1.2.1.17.7.1.2.2.1.2').read()

mac_list = {}
for mac_line in raw_mac.splitlines():
  parts = mac_line.split()

  #reconstruct the mac address
  mac=":"
  mac_parts=parts[0].rsplit(".",7)
  for idx in range(2,8):
    #print "mac_parts["+str(idx)+"]="+mac_parts[idx]
    mac_parts[idx] = '{0:02x}'.format(int(mac_parts[idx]))
    #print "hex mac_parts["+str(idx)+"]="+mac_parts[idx]
  mac = mac.join(mac_parts[2:8])
  #print parts[0].rsplit(".",6)

  # ignore port zero
  #print "processing port "+parts[3]
  if parts[3] == "0": continue
  mac_list.update({mac:{'port':ifs_list[ports_list[parts[3]]],'vlan':vlans_list[mac_parts[1]]}})

  #print mac_line
  print "{0}{1}".format(mac,mac_list[mac])
