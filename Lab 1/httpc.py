import argparse

parser = argparse.ArgumentParser(
description='httpc is our take on a curl-like application restricted to the HTTP protocol.',
epilog="Use \"httpc help -[command]\" for more information about a command", add_help=False)
subparser = parser.add_subparsers(dest='command')
get = subparser.add_parser('get',add_help=False, help='Get executes a HTTP GET request for a given URL.')
post = subparser.add_parser('post',add_help=False, help='Post executes a HTTP POST request for a given URL with inline data or from file.')
help = subparser.add_parser('help',add_help=False)

get.add_argument('-v', action='store_true', help= 'Prints the detail of the response such as protocol, status, and headers.')
get.add_argument('-h', type=str,help= 'Associates headers to HTTP Request with the format \'key:value\'')
get.add_argument('url', type=str,help= 'hostname')

post.add_argument('-v', action='store_true',help= 'Prints the detail of the response such as protocol, status, and headers.')
post.add_argument('-h', type=str,help= 'Associates headers to HTTP Request with the format \'key:value\'')
notBoth = post.add_mutually_exclusive_group()
notBoth.add_argument('-d', type=str, help= 'Associates an inline data to the body HTTP POST request.')
notBoth.add_argument('-f', type=str, help= 'Associates the content of a file to the body HTTP POST')
post.add_argument('url', type=str,help= 'hostname')

help.add_argument('-get', action='store_true')
help.add_argument('-post', action='store_true')


args = parser.parse_args()

if args.command == 'get':
    v = False
    h = None
    if args.v: v = True
    if args.h: # or just h = args.h
        try:
            temp = args.h.split(":")
            h = {temp[0],temp[1]}
        except:
            print("Not in \'key:value\' format")
            exit()
    print("get(%s,%s,%s)" % (v, h, args.url))

if args.command == 'post':
    v = False
    h = None
    d = None
    f = None
    if args.v: v = True
    if args.h: # or just h = args.h
        try:
            temp = args.h.split(":")
            h = {temp[0],temp[1]}
        except:
            print("Not in \'key:value\' format")
            exit()
    if args.d: d = args.d
    if args.f: # or just f = args.f
        try:
            with open(args.d, 'rb') as file:
                f={args.d: file}
        except:
            print("File could not be opened")
            exit()
    print("post(%s,%s,%s,%s,%s)" % (v, h, d, f, args.url))

if args.command == 'help':
    if args.get:
        get.print_help()
    elif args.post:
        post.print_help()
    else:
        parser.print_help()
