import publisher, argparse, datetime, sys, time


def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()
    # add positional arguments in that order
    parser.add_argument ("topic", help="Topic")
    parser.add_argument ("id", help="ID")
    # parse the args
    args = parser.parse_args ()
    return args

def main():
    args = parseCmdLineArgs ()
    pub1 = publisher.Publisher(args.topic,args.id)
    for i in range(200):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S.%f")
        pub1.send(str(i) + ',' + current_time)
        print(str(i) + ',' + current_time)
        sys.stdout.flush()
        time.sleep(.01)

#----------------------------------------------
if __name__ == '__main__':
    main ()

