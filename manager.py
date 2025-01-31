import requests, argparse, json, time, os, configparser
from random import randint
from venmo_api import Client
from auth_api import AuthenticationApi
from api_client import ApiClient
from api_util import validate_access_token

#Grab our configurations from our .ini file
config = configparser.ConfigParser()
config.read('venmo.ini')

def no_auth(username):
    url = 'https://venmo.com/{0}'.format(username)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    headers = {'User-Agent':user_agent}
    response = requests.get(url, headers=headers,verify=False)
    if response.status_code==200:
        print("[+] "+username+" Exists - " + url)
    else:
        print("[-] "+username+" Does Not Exists")

def authenticate():
    access_token = Client.get_access_token(username=config['venmo.com']['username'],password=config['venmo.com']['password'])
    venmo = Client(access_token=access_token)

# Setting up and Making the Web Call
def GetDataFromVenmo(url):
    try:
        api_key = config['venmo.com']['api_token']
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        headers = {'User-Agent':user_agent, 'Authorization': 'Bearer '+ api_key}
        response = requests.get(url, headers=headers,verify=False)
        return response

    except Exception as e:
        print('[!]   ERROR - Venmo issue: {}'.format(str(e)))
        exit(1)

#Grab Basic Info for User
def GetBasicInfo(passed_user):
    try:
        url = 'https://api.venmo.com/v1/users/{0}'.format(passed_user)
        response = GetDataFromVenmo(url)
        if response.status_code==200:
            data = response.json()
            return data['data']
        elif response.status_code==400:
            print("That user profile doesn't exist - make sure you have it right. If you're trying to find the profile of someone, use the brute force option first")
    except Exception as e:
        print(str(e))

#Grab the list of friends
def GetFriendList(passed_user):
    url = 'https://api.venmo.com/v1/users/{0}/friends?limit=1337'.format(passed_user)
    response = GetDataFromVenmo(url)
    data = response.json()
    if response.status_code==200:
        return data['data']
    else:
        print("Mistakes Were Made...")

#Grab a user's transactions
def GetUserTransactions(passed_user,url):
    if url is None:
        url = 'https://api.venmo.com/v1/stories/target-or-actor/{0}?limit=50'.format(passed_user)
    else:
        url = url
    response = GetDataFromVenmo(url)
    data = response.json()
    if response.status_code==200:
        if data['pagination'] is not None:
            nurl = data['pagination']['next']
        else:
            nurl = None
        return data,nurl
    else:
        print("Mistakes Were Made...")

def Paginate(nurl):
    url = nurl
    response = GetDataFromVenmo(url)
    data = response.json()
    if response.status_code==200:
        if data['pagination'] is not None:
            nurl = data['pagination']['next']
        else:
            nurl = None
        return data,nurl
    else:
        print("Mistakes Were Made...")

#Grab Internal ID for User
def GetInternalId(passed_user):
    url = 'https://api.venmo.com/v1/users/{0}'.format(passed_user)
    response = GetDataFromVenmo(url)
    if response.status_code==200:
        data = response.json()
        user_id = data['data']['id']
        return user_id
    else:
        print("Mistakes Were Made...")

#Parse the Facebook ID
def GetFbId(passed_user):
    if "facebook" in passed_user:
        fb_id = passed_user.split("/")[4]
    else:
        fb_id = "N/A"
    return fb_id

#Function for making a request to download the profile picture
def get_profile_pic(pic,file_name):
    request = requests.get(pic,verify=False)
    with open(file_name,'wb') as f:
        f.write(request.content)
        #file_check(file_name+'.jpg')

def dir_check(user):
    if not os.path.isdir('./'+user):
        os.mkdir(user)
    os.chdir(user)

def brute_force(username):
    barray = []
    barray.append(username.replace(' ','')) #UserName
    barray.append(username.replace(' ','-')) #User-Name
    barray.append(username.replace(' ','_')) #User_Name
    barray.append(username[0:1]+username.split(" ")[1]) #UName
    barray.append(username.split(" ")[0]+username.split(" ")[1][0:1]) #UserN
    barray.append(username.split(" ")[1]+username.split(" ")[0]) #NameUser
    barray.append(username.replace(' ','-')+'-1') #User-Name-1
    barray.append(username.replace(' ','-')+'-2') #User-Name-2
    barray.append(username.replace(' ','-')+'-3') #User-Name-3
    barray.append(username.replace(' ','')+'1') #UserName
    barray.append(username.replace(' ','')+'2') #UserName
    barray.append(username.replace(' ','')+'3') #UserName
    for uname in barray:
        no_auth(uname)
        time.sleep(1.5)

def output_user_info_file(user):
    info = GetBasicInfo(user) #Go find basic info of the target profile
    if info:
        with open(user + '.csv','w') as f:
            id = info['id']
            username = info['username']
            display_name = info['display_name']
            friends_count = info['friends_count']
            phone = info['phone']
            date_joined = info['date_joined']
            email = info['email']
            f.write("venmo_id,username,display_name,friends_count,phone,date_joined,email\n")
            f.write("{0},{1},{2},{3},{4},{5},{6}".format(id,username,display_name,friends_count,phone,date_joined,email))
            if "venmopics" in info['profile_picture_url'] or "facebook" in info['profile_picture_url']:
                pic = info['profile_picture_url']
                get_profile_pic(pic,info['username'])

def output_friends_file(user):
    #if user.isdigit() is not True: #If the user variable is username and not an internal ID code, go find the internal_id code
    #	user = GetInternalId(user)#Call function to get internal_Id and assign to user variable
    info = GetFriendList(user)
    if info:
        with open(user + '_friends.csv','w') as f:
            f.write("fvalue,venmo_id,username,display_name,friends_count,phone,date_joined,email\n")
            for friend in info:
                fvalue = user
                id = friend['id']
                username = friend['username']
                display_name = friend['display_name']
                friends_count = friend['friends_count']
                phone = friend['phone']
                date_joined = friend['date_joined']
                email = friend['email']
                f.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(fvalue,id,username,display_name,friends_count,phone,date_joined,email))

def output_transactions_file(user):
    if user.isdigit() is not True: #If the user variable is username and not an internal ID code, go find the internal_id code
        user_id = GetInternalId(user)#Call function to get internal_Id and assign to user variable
    nurl = None
    trans,nurl = GetUserTransactions(user_id,nurl) #Go find transactions of the target profile
    if trans:
        with open(user + '_trans.csv','w') as f:
            #f.write(str(trans))
            f.write("id,date_updated,app_used,payee,payor,item\n")
            for i in trans['data']:
                try:
                    id = str(i['id'])
                    dt = str(i['date_updated'])
                    app = i['app']['description']
                    payee = i['payment']['target']['user']['username']
                    payor = i['payment']['actor']['username']
                    note = i['payment']['note']
                    f.write("{0},{1},{2},{3},{4},{5}\n".format(id,dt,app,payee,payor,note))
                except:
                    pass
    while nurl is not None:
        data,nurl = Paginate(nurl)
        if nurl is None:
            break
        else:
            with open(user + '_trans.csv','a') as f:
                for i in data['data']:
                    try:
                        id = str(i['id'])
                        dt = str(i['date_updated'])
                        app = i['app']['description']
                        payee = i['payment']['target']['user']['username']
                        payor = i['payment']['actor']['username']
                        note = i['payment']['note']
                        f.write("{0},{1},{2},{3},{4},{5}\n".format(id,dt,app,payee,payor,note))
                    except:
                        pass
        time.sleep(randint(1,5))

def output_crawl_file(user):
    if user.isdigit() is not True:#If the user variable is username and not an internal ID code, go find the internal_id code
        user_id = GetInternalId(user) #Call function to get internal_Id and assign to user variable
    friends = GetFriendList(user_id)
    if friends:
        with open(user+'_foaf.csv','w') as f:
            f.write("fvalue,venmo_id,username,display_name,friends_count,phone,date_joined,email\n")
            for i in friends:
                print("Fetching list for "+i['id'])
                foaf = GetFriendList(i['id'])
                #print (foaf)
                if foaf:
                    for friend in foaf:
                        fvalue = user_id
                        id = friend['id']
                        username = friend['username']
                        display_name = friend['display_name']
                        friends_count = friend['friends_count']
                        phone = friend['phone']
                        date_joined = friend['date_joined']
                        email = friend['email']
                        f.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(fvalue,id,username,display_name,friends_count,phone,date_joined,email))
                time.sleep(randint(1,5))
