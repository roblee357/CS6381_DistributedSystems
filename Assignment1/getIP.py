import netifaces as ni

def get(network = 'eth0'):
    ni_list = ni.interfaces()
    try:
        index = [i for i, s in enumerate(ni_list) if network in s]
        ni_name = ni_list[index[0]]
    except:
        index = [i for i, s in enumerate(ni_list) if 'enp' in s]
        ni_name = ni_list[index[0]]
    return ni.ifaddresses(ni_name)[ni.AF_INET][0]['addr']

def main():
    print(get('enp'))

if __name__ == '__main__':
    main()