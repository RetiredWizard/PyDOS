checkGlobVar = input("Enter the variable name to check: ")
try:
    print("Value:",eval(checkGlobVar))
except:
    print("Variable not defined")
