import bcrypt

def byte_a_string(palabra):#en byte
    palabra = palabra.decode("utf-8")
    return palabra

def string_a_byte(palabra):#en string
    palabra = str.encode(palabra)
    return palabra

def encriptar(password):#en encriptar
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    print(type(hashed))
    return hashed
