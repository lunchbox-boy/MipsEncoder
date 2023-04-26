import re

instructions = "Choose operation \n add \n sub\n or\n and\n sll\n"

funct_dict = {
    # function: (function, ({rs} argument Position), ({rt} argument Position), ({rd} argument Position), ({shift amount} argument Position))
    # position of -1 means it is not used
    "add": (32, 2, 3, 1, -1),
    "sub": (34, 2, 3, 1, -1),
    "sll": (0, -1, 2, 1, 3),

    "and": (36, 2, 3, 1, -1),
    "or": (37, 2, 3, 1, -1),
}

register_dict = {
    'r': 0,
    'v': 2,
    'a': 4,
    't': 8,
    's': 16,
}

def numberOfFunctionArguments(function):
    count = 0
    for num in funct_dict[function]:
        if num > -1:
            count += 1
    #remove the function itself
    
    return count - 1

def numberOfInputArguments(command):
    
    return len(command) - 1

def noObviousErrors(command):
    print("running")
    function = command[0]
    if function not in funct_dict:
        print(f"The function {function} cannot be encoded")
        return False
    if numberOfInputArguments(command) > numberOfFunctionArguments(function):
        print("Too many arguments")
        return False
    if numberOfInputArguments(command) < numberOfFunctionArguments(function):
        print("Too few arguments")
        return False
    return True



def decimal_to_binary(decimal, num_bits):
    # Convert decimal to a binary string with num_bits bits
    binary_str = format(decimal, f"0{num_bits}b")
    return binary_str

registerWithChar = r"^[a-zA-Z]\d+$"
def parse_register(register):
    if register.startswith("$"):
        register = register[1:]

    # if the string is a register with a char at the front
    if re.match(registerWithChar, register):
        char = register[0]
        # if the register char doesn't exist
        if char not in register_dict:
            print("Invalid Register")
            return False
        registerNum = register_dict[char] + int(register[1:])
        # check register is still valid
        if not (0 <= registerNum <= 23):
            print("Invalid Register")
            return False
        return decimal_to_binary(registerNum, 5)


    # if its just a digit
    elif register.isdigit():
        registerNum = int(register)
        # check register is still valid
        if not (0 <= registerNum <= 23):
            print("Invalid Register")
            return False
        return decimal_to_binary(registerNum, 5)
        
    # if it is an invalid register
    else:
        print ("Invalid Register") 
        return False
    
    
def getRegister(command,registerType):
    function = command[0]
    argPos = funct_dict[function][registerType]
    # if it isn't used
    if argPos == -1:
        return "00000"
    register = parse_register(command[argPos])
    if register is False:
        return False
    return register

#opcode is always 000000 for R-encoding, which is the only encoding this encoder does
def getOpcode():
    return "000000"
def getrs(command):
    register = getRegister(command,1)
    if register is False:
        return False
    return register
def getrt(command):
    register = getRegister(command,2)
    if register is False:
        return False
    return register
def getrd(command):
    register = getRegister(command,3)
    if register is False:
        return False
    return register
def getshamt(command):
    function = command[0]
    argPos = funct_dict[function][4]
    if argPos == -1:
        return "00000"
    arg = command[argPos]
    if not arg.isdigit():
        print("Shift Amount must be a number")
        return False
    return decimal_to_binary(int(arg), 5)
def getfunct(command):
    function = command[0]
    return decimal_to_binary(funct_dict[function][0], 6)

def getEncoding(command):
    if noObviousErrors(command):
        opcode = getOpcode()
        rs = getrs(command)
        rt = getrt(command)
        rd = getrd(command)
        shamt = getshamt(command)
        funct = getfunct(command)

        #if there were no errors
        if opcode and rs and rt and rd and shamt and funct:
            return opcode + rs + rt + rd + shamt + funct
    
    # return an empty string if something went wrong
    return ""



while True:
    command = input(instructions)
    command = command.rstrip()
    # splits on "," or ", " or " "
    command = re.split(', |,| ', command)
    res = getEncoding(command)
    print(res)
    print("\n")
    print("\n")