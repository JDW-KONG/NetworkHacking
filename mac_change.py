#!/usr/bin/python3

# import fg from colored for colored terminal output
from colored import fg

# import subprocess to run system commands
import subprocess


# changes mac address
def change_mac(interface, mac):
    # bring interface down
    subprocess.call(['ifconfig', interface,'down'])

    # change mac address
    subprocess.call(['ifconfig', interface, 'hw', 'ether', mac])

    # bring interface back up
    subprocess.call(['ifconfig', interface, 'up'])


def main():
    # clear screen
    subprocess.call(['clear'])

    # greet the user
    greeting = print('%s[$] Welcome to the MAC Changer' % (fg(226)))

    # collect desired interface and MAC address from user
    interface = input('[?] Please enter the interface: ')
    new_mac = input('[?] Please enter the new MAC address: ')

    # open ip link process to print original network info
    prev_info = subprocess.Popen(('ip', 'link'), stdout=subprocess.PIPE)
    
    # pass output of ip link to grep and store result
    # greps for line containing the MAC address
    prev_mac = subprocess.check_output(['grep', 'ether'], stdin=prev_info.stdout)
    
    # pass interface and new MAC address to change_mac
    change_mac(interface, new_mac)
    
    print('%s\n[?] Changing MAC address, please wait...' % (fg(226)))
    
    # sleep for three seconds to allow interface to come back up
    subprocess.call(['sleep', '3'])
    
    # open ip link process to print new network info
    next_info = subprocess.Popen(('ip', 'link'), stdout=subprocess.PIPE)
    
    # greps ip link output for line containing new MAC address
    next_mac = subprocess.check_output(['grep', 'ether'], stdin=next_info.stdout)
    
    # print previous MAC address
    print('%s\n[*] Previous MAC address: ' % (fg(199)))
    print(prev_mac.decode('utf-8'))
    
    # print new MAC address
    print('%s[*] New MAC address: ' % (fg(14)))
    print(next_mac.decode('utf-8'))

    # if previous MAC address is the same as the new MAC address
    if prev_mac == next_mac:
        print('%s[-] Failed to change MAC address to: {}'.format(new_mac) % (fg(196)))
    # if previous and new MAC addresses are different
    else:
        print('%s[+] MAC address changed to: {} on interface {}'.format(new_mac, interface) % (fg(118)))


main()


