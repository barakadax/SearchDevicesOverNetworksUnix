import os
import subprocess
from ipaddress import IPv4Network

def getMyIpAndSubnetMask():
   listOfIps = []
   try:
      data = subprocess.check_output(['ip', 'a']).decode('utf-8')
   except subprocess.CalledProcessError:
      return None
   data = data.split('\n')
   for i in data:
      if "inet" in i and "inet6" not in i:
         listOfIps.append(i.strip().split(' ')[1])
   return listOfIps
   # O(N)

def getGateWaysFromGivenIp(myLocalIpandSubnet):
   myLocalGateways = []
   for i in myLocalIpandSubnet:
      splittedIpAndSub = i.split('/')
      splitedIp = splittedIpAndSub[0].split('.')
      if int(splitedIp[0]) == 127:
         continue
      if int(splittedIpAndSub[1]) >= 8 and int(splittedIpAndSub[1]) <= 15:
         splitedIp[1] = splitedIp[2] = splitedIp[3] = '0'
         splittedIpAndSub[1] = "/8"
      elif int(splittedIpAndSub[1]) >= 16 and int(splittedIpAndSub[1]) <= 23:
         splitedIp[2] = splitedIp[3] = '0'
         splittedIpAndSub[1] = "/16"
      else:
         splitedIp[3] = '0'
         splittedIpAndSub[1] = "/24"
      myLocalGateways.append('.'.join(splitedIp) + splittedIpAndSub[1])
   return myLocalGateways
   # O(N)
   
def findLocalUsers(myLocalGateways):
   usersInNetworks = {}
   for i in myLocalGateways:
      usersInNetworks[i] = []
      for ip in IPv4Network(i):
         if os.system("ping -c 1 " + str(ip)) == 0:
            usersInNetworks[i].append(str(ip))
   return usersInNetworks
   # O(N**2)

def breakIntoOnlyIP(myLocalIpandSubnet):
   for i in range(0, len(myLocalIpandSubnet)):
      myLocalIpandSubnet[i] = myLocalIpandSubnet[i].split('/')[0]
   return myLocalIpandSubnet
   # O(N)

def printNetworksFound(usersPerNetwork, myLocalIpandSubnet):
   os.system('cls' if os.name == 'nt' else 'clear')
   myLocalIpandSubnet = breakIntoOnlyIP(myLocalIpandSubnet)
   for key in usersPerNetwork.keys():
      print("Network: " + key.split('/')[0] + " found:")
      for found in usersPerNetwork[key]:
         if found in myLocalIpandSubnet:
            print(found, "- yourself")
         else:
            print(found)
   # O(N**2)

def main():
   myLocalIpandSubnet = getMyIpAndSubnetMask()
   if (myLocalIpandSubnet):
      myLocalGateways = getGateWaysFromGivenIp(myLocalIpandSubnet)
      usersPerNetwork = findLocalUsers(myLocalGateways)
      printNetworksFound(usersPerNetwork, myLocalIpandSubnet)
   else:
      print("Not connected to internet...")
   # O(1)

if __name__ == "__main__":
   main()

