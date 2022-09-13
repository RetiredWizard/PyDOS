envline = {}
paramlist = ['CIRCUITPY_WIFI_SSID','CIRCUITPY_WIFI_PASSWORD','CIRCUITPY_WEB_API_PASSWORD']

defaults = True
try:
    envfile = open('/.env')
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
        temp = input(param+": ["+envline.get(param,"")+"] ")
        if temp != "":
            envline[param] = temp

    print("\n/.env file about to be created:\n")
    for param in paramlist:
        print(param+"="+envline.get(param,""))

    print()
    ans = ""
    while ans.upper() != "Y" and ans.upper() != "N" and ans.upper() != "A":
        ans = input("Does this look correct (Y/N/(A)bort)?: ")
        if ans.upper() != "Y" and ans.upper() != "N" and ans.upper() != "A":
            print("Invalid response, please answer Y, N or A")

if ans.upper() != "A":
    envfile = open('/.env','w')
    for param in paramlist:
        envfile.write(param+"="+envline.get(param,"")+"\n")
    envfile.close()
