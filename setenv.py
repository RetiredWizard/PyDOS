envline = {}
paramlist = ['CIRCUITPY_WIFI_SSID','CIRCUITPY_WIFI_PASSWORD','CIRCUITPY_WEB_API_PASSWORD']

defaults = True
try:
    envfile = open('/settings.toml')
except:
    defaults = False

if defaults:
    for line in envfile:
        try:
            envline[line.split('=')[0].strip()] = line.split('=')[1].strip()
        except:
            pass
    envfile.close()

ans = ""
while ans.upper() != "Y" and ans.upper() != "A":

    for param in paramlist:
        temp = input(param+": ["+envline.get(param,"")+"] ").strip()
        if temp != "":
            if temp[0] != '"':
                temp = '"'+temp
            if temp[-1] != '"':
                temp = temp+'"'
            envline[param] = temp

    print("\n/settings.toml file about to be created:\n")
    for param in envline:
        print(param+"="+envline.get(param,""))

    print()
    ans = ""
    while ans.upper() != "Y" and ans.upper() != "N" and ans.upper() != "A":
        ans = input("Does this look correct (Y/N/(A)bort)?: ")
        if ans.upper() != "Y" and ans.upper() != "N" and ans.upper() != "A":
            print("Invalid response, please answer Y, N or A")

if ans.upper() != "A":
    with open('/settings.toml','w') as envfile:
        for param in envline:
            envfile.write(param+"="+envline.get(param,"")+"\n")
