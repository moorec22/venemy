import requests, argparse, json, time, os, configparser
from random import randint
from venmo_api import Client
from auth_api import AuthenticationApi
from api_client import ApiClient
from api_util import validate_access_token
from manager import *

requests.packages.urllib3.disable_warnings()

#Script Arguments
parser = argparse.ArgumentParser(description="Venemy: An Intel Tool For Venmo - Use at your own risk")
parser.add_argument('-u', '--user', required=False, help='Grabs basic info of user')
parser.add_argument('-f', '--friends',required=False,help='Get friends')
parser.add_argument('-t', '--trans',required=False,help="Get transactions of users")
parser.add_argument('-a', '--all',required=False,help="Grab basic info, transactions, and friends of target's profile and crawl one level of friends")
parser.add_argument('-c', '--crawl',required=False,help="Crawl one level of friends (foaf) - this is incredibly noisy!!! See README before running")
parser.add_argument('-p', '--pics',required=False,action='store_true',help="Download user's public photos")
parser.add_argument('-A', '--auth',required=False,action='store_true',help="Authenticate to the API for an oAuth token")
parser.add_argument('-n', '--noauth',required=False,help="Check if username exists via the web")
parser.add_argument('-b', '--brute-force',required=False,help="Brute Force variation's of person's name")
args = parser.parse_args()

#Grab our configurations from our .ini file
config = configparser.ConfigParser()
config.read('venmo.ini')


######Main#######

if args.auth:
    authenticate()

if args.noauth:
    no_auth(args.noauth)

if args.brute_force:
    brute_force(args.brute_force)


#Get basic info on target profile
if args.user:
    dir_check(args.user)
    output_user_info_file(args.user)

#Get friends of target profile
if args.friends:
    dir_check(args.friends)
    output_friends_file(args.friends)

#Get transactions of target profile
if args.trans:
    dir_check(args.trans)
    output_transactions_file(args.trans)

#Do all the things for a target profile
if args.all:
    user=args.all
    dir_check(user)
    print("[+] Gathering User info...")
    output_user_info_file(user)
    #Go find friends of the target profile
    print("[+] Gathering friend info...")
    output_friends_file(user)
    #Go find transactions of target profile
    print("[+] Gathering transaction info...")
    output_transactions_file(user)
    print("[+] Done! Info located at " + os.getcwd())

if args.crawl:
    output_crawl_file(args.crawl)

