import netifaces as ni

def get(network = 'eth0'):
    ni_list = ni.interfaces()
    index = [i for i, s in enumerate(ni_list) if network in s]
    try:
        ni_name = ni_list[index[0]]
        return ni.ifaddresses(ni_name)[ni.AF_INET][0]['addr']
    except:
        return 'localhost'
    

def main():
    print(get())

if __name__ == '__main__':
    main() 