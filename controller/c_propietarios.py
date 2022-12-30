from flask import Flask, jsonify, request, Response,send_file
from recursos.re_excel import *
from recursos.re_otros import transformar_json
from bson import json_util
from bson.objectid import ObjectId
from conexion.conexion import *
from models.propietarios import Propietarios
from models.propiedad import Propiedad

#LISTAR
def listar_propietario():
    base_datos = obtener_bd()
    #base_datos = 'albertobd'
    session,engine=get_sesion(base_datos)
    #id_buscar = 2
    try:
        respuesta = session.query(Propiedad,Propietarios).join(Propietarios).all()#es una lista
        #respuesta = session.query(Propiedad,Propietarios).join(Propietarios).filter(Propietarios.idpropietarios == id_buscar).all()#es una lista
        result = [
        {
            "idpropiedad": x.idpropiedad, 
            "tipo_propietario": x.tipo_propietario, 
            "porcentaje_participacion": x.porcentaje_participacion, 
            "numero_deposito":x.numero_deposito,
            "numero_departamento":x.numero_departamento,
            "numero_estacionamiento":x.numero_estacionamiento,
            "finca_id":x.finca_id,
            "idpropietarios": y.idpropietarios, 
            "nombres_y_apellidos": y.nombres_y_apellidos,
            "tipodocumento":y.tipodocumento,
            "nro_documento": y.nro_documento, 
            "correo": y.correo,
            "telefono":y.telefono,
            "estado": y.estado
        } 
        for x,y in respuesta]#x → Propiedad , y → Propietarios, esto es una lista
        # Convert the list to JSON format
        json_result = json_util.dumps(result)
        return json_result
    except Exception as e:
        print('ERROR → ',e)
        json_result = str(e)
        return json_result 

def listar_propietario_ID(id):#P4
    propietario = conexion('finca').find_one({'_id': ObjectId(id)})
    response = json_util.dumps(propietario)
    print('RESPONSE :', response)
    return response

#REGISTRAR
def registrar_propietario(base_datos,lista_json):#P2
    duplicado_ID_Departamentos = ""
    duplicado_Numero_Estacionamiento = ""
    duplicado_Numero_Deposito = ""
    #REPETICIONES
    #solo se repite un solo dato
    repite_estacionamiento = False
    repite_departamento = False
    repite_deposito = False
    #caso Dpto y estacionamiento
    repite_ambos_v1 = False
    #caso Dpto y deposito
    repite_ambos_v2 = False
    #caso estacionamiento y deposito
    repite_ambos_v3 = False
    #caso los tres campos sean invalidos
    repite_todo = False
    try:
        nombres_y_apellidos = lista_json["nombres_y_apellidos"]
        tipodocumento = lista_json["tipodocumento"]
        nro_documento = lista_json["nro_documento"]
        correo = lista_json["correo"]
        telefono = lista_json["telefono"]
        #estado = lista_json["estado"]
        numero_deposito = lista_json["numero_deposito"]
        numero_departamento = lista_json["numero_departamento"]
        numero_estacionamiento = lista_json["numero_estacionamiento"]
        """ID_Departamentos = datos_propietarios[2]#validar que no se repita
        _id = request.json["_id"]
        Finca = request.json["Finca"]
        Nombres_y_Apellidos = request.json["Nombres_y_Apellidos"]
        Tipo_Documento = request.json["Tipo_Documento"]
        Nro_Documento = request.json["Nro_Documento"]
        Correo = request.json["Correo"]
        Telefono = request.json["Telefono"]
        array_departamentos = request.json["Departamentos"]
        ID_Departamentos = request.json["Departamentos"][0]['ID_Departamentos']#validar que no se repita
        Porcentaje_Participacion = request.json["Departamentos"][0]['Porcentaje_Participacion']#habilitar cuando ponga ID_Departamentos
        Estacionamientos = request.json["Estacionamientos"]
        Numero_Estacionamiento = request.json["Estacionamientos"][0]['Numero_Estacionamiento']#validar que no se repita
        estado = 'A'#activo por defecto
        Numero_deposito = request.json["Numero_deposito"]"""
        validacion_departamento = False
        validacion_estacionamiento = False
        validacion_deposito = False
        #defecto tipo_prop 1 dpto y estacionamiento, en caso sea valido
        #caso 1
        """if ID_Departamentos != "" and Numero_Estacionamiento!="" and Numero_deposito!="":#puso tanto departamento como estacionamiento
            #con esta condicional ya se asegura que ninguno de esos campos estan vacios
            validacion_departamento = validar_id_departamento(ID_Departamentos,base_datos,"A",Nombres_y_Apellidos)
            validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
            validacion_deposito = validar_id_deposito(Numero_deposito,Finca,"A")
            validacion_general = True
            lista_validaciones = list((validacion_departamento,validacion_estacionamiento,validacion_deposito))
            if False in lista_validaciones:"""
            #if validacion_departamento ==False or validacion_estacionamiento ==False or validacion_deposito ==False:
        """duplicado_ID_Departamentos = ID_Departamentos
            duplicado_Numero_Estacionamiento = Numero_Estacionamiento
            duplicado_Numero_deposito = Numero_deposito"""

        """validacion_general = False
                #para ver cual es el incorrecto
                if (validacion_departamento):#departamento esta bien
                    if(validacion_estacionamiento):#estacionamiento esta bien
                       #solo el numero de deposito esta mal
                       duplicado_Numero_Deposito = Numero_deposito
                       repite_deposito = True
                    else:#estacionamiento esta mal
                        if validacion_deposito:#pero deposito esta bien
                            duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                            repite_estacionamiento = True 
                        else:#tanto estacionamiento como deposito esta mal
                            duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                            duplicado_Numero_Deposito = Numero_deposito
                            repite_ambos_v3 = True
                else:#departamento esta mal
                    if(validacion_estacionamiento):#estacionamiento esta bien
                        if (validacion_deposito):#deposito esta bien
                            duplicado_ID_Departamentos= ID_Departamentos
                            repite_departamento = True
                        else:#esta mal tanto estacionamiento como deposito
                            duplicado_ID_Departamentos= ID_Departamentos
                            duplicado_Numero_Deposito = Numero_deposito
                            repite_ambos_v2 = True
                    else:#esta mal estacionamiento
                        if (validacion_deposito):#deposito esta bien
                            duplicado_ID_Departamentos= ID_Departamentos
                            duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                            repite_ambos_v1 = True
                        else:#esta mal los tres campos
                            duplicado_ID_Departamentos= ID_Departamentos
                            duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                            duplicado_Numero_Deposito = Numero_deposito
                            repite_todo = True
            else:
                tipo_propietario = 1#por defecto si tiene los tres campos llenos
        
        elif ID_Departamentos!="" and Numero_Estacionamiento!="":#puso solo dpto y estacionamiento
            validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
            validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
            validacion_general = True
            lista_validaciones = list((validacion_departamento,validacion_estacionamiento))
            if False in lista_validaciones:
                validacion_general = False
                if validacion_departamento:
                    repite_estacionamiento = True
                    duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                else:
                    if validacion_estacionamiento:
                        repite_departamento = True
                        duplicado_ID_Departamentos = ID_Departamentos
                    else:
                        repite_ambos_v1 = True
                        duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                        duplicado_ID_Departamentos = ID_Departamentos
            else:
                tipo_propietario = 1"""
            #caso 2
        """if (Numero_Estacionamiento!="" and Numero_deposito==""):
                    validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
                    validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                    if validacion_departamento ==False:
                        duplicado_ID_Departamentos = ID_Departamentos
                    else:
                        tipo_propietario = 1
                    validacion_general = validacion_departamento
                #caso 3
                elif  (Numero_Estacionamiento=="" and Numero_deposito!=""):
                    validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
                    validacion_deposito = validar_id_deposito(Numero_deposito,Finca,"A")
                    if validacion_departamento ==False:
                        duplicado_ID_Departamentos = ID_Departamentos
                    else:
                        tipo_propietario = 1
                    validacion_general = validacion_departamento
                else:#caso 4, solo departamento
                    validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
                    if validacion_departamento ==False:
                        duplicado_ID_Departamentos = ID_Departamentos
                    else:
                        tipo_propietario = 1
                    validacion_general = validacion_departamento"""
        """elif ID_Departamentos!="" and Numero_deposito!="":
            validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
            validacion_deposito = validar_id_deposito(Numero_deposito,Finca,"A")
            validacion_general = True
            lista_validaciones = list((validacion_departamento,validacion_deposito))
            if False in lista_validaciones:
                validacion_general = False
                if validacion_departamento:
                    repite_deposito = True
                    duplicado_Numero_Deposito = Numero_deposito
                else:
                    if validacion_deposito:
                        repite_departamento = True
                        duplicado_ID_Departamentos = ID_Departamentos
                    else:
                        repite_ambos_v2 = True
                        duplicado_Numero_Deposito = Numero_deposito
                        duplicado_ID_Departamentos = ID_Departamentos
            else:
                tipo_propietario = 1
        elif Numero_Estacionamiento!="" and Numero_deposito!="":
            validacion_deposito = validar_id_deposito(Numero_deposito,Finca,"A")   
            validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
            validacion_general = True
            lista_validaciones = list((validacion_deposito,validacion_estacionamiento))
            if False in lista_validaciones:
                validacion_general = False
                if validacion_estacionamiento:
                    repite_deposito = True
                    duplicado_Numero_Deposito = Numero_deposito
                else:
                    if validacion_deposito:
                        repite_estacionamiento = True
                        duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                    else:
                        repite_ambos_v3 = True
                        duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                        duplicado_Numero_Deposito = Numero_deposito
            else:
                tipo_propietario = 2
        elif ID_Departamentos!="":
            validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
            if validacion_departamento:
                validacion_general = True
                tipo_propietario = 1
            else:
                repite_departamento = True
                duplicado_ID_Departamentos = ID_Departamentos
                validacion_general = False
        elif Numero_Estacionamiento!="":
            validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
            if validacion_estacionamiento:
                validacion_general = True
                tipo_propietario = 2
            else:
                repite_estacionamiento = True
                duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                validacion_general = False 
        elif Numero_deposito!="":
            validacion_deposito = validar_id_deposito(Numero_deposito,Finca,"A")
            if validacion_deposito:
                validacion_general = True
                tipo_propietario = 3
            else:
                repite_deposito = True
                duplicado_Numero_Deposito = Numero_deposito
                validacion_general = False 
        else:
            validacion_general = False
            response = {"status": 201,'mensaje': 'Debe de llenar al menos un Departamento, Estacionamiento o Depósito',"error":True,"input_error":"todos"}
            return response"""
        """elif Numero_Estacionamiento!="":#caso 5
            if (Numero_deposito!=""):
                validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                validacion_deposito = validar_id_deposito(Numero_deposito,Finca,"A")
                if validacion_estacionamiento ==False:
                    duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                validacion_general = validacion_estacionamiento
                validacion_departamento = True
                tipo_propietario = 2
            else:#caso 6
                validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                if validacion_estacionamiento ==False:
                    duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                validacion_general = validacion_estacionamiento
                validacion_departamento = True
                tipo_propietario = 2

        elif Numero_deposito!="":#solo puso deposito
            #caso 7
            validacion_deposito = validar_id_deposito(Numero_deposito,Finca,"A")
            if validacion_deposito ==False:
                duplicado_Numero_deposito = Numero_deposito
            validacion_general = validacion_deposito
            validacion_deposito = True
            tipo_propietario = 3
        else:#mensaje en caso los campos Departamentos y Estacionamientos esten vacios
            validacion_general = False
            response = {"status": 400,'mensaje': 'Los campos de Departamento y Estacionamiento no pueden estar ambos vacios'}  
            #return response"""

        #if validacion_general:
            #if _id or Finca or Nombres_y_Apellidos or Tipo_Documento or Nro_Documento or Correo or Telefono or array_departamentos or Estacionamientos :
        modificacion = ''
        fecha = datetime.now()
        db = conexion('propietarios')
        db.insert_one(
            { "_id":_id,"Finca":Finca, "Nombres_y_Apellidos": Nombres_y_Apellidos, "Tipo_Documento": Tipo_Documento,
            "Nro_Documento": Nro_Documento, "Correo": Correo, "Telefono": Telefono, "Departamentos": array_departamentos,
            "Estacionamientos": Estacionamientos,"Fecha_creacion":fecha,"Fecha_modificacion":modificacion,"estado":estado,
            "tipo_propietario":tipo_propietario,"Numero_deposito":Numero_deposito})
        response = {
            "status": 200,
            "mensaje": "El usuario "+ Nombres_y_Apellidos+ " se registro satisfactoriamente"
        }
        #return response
       
        response = {"status": 201,'mensaje': 'Uno o mas datos a registrar son incorrectos'}  
        #return response
        """else:
            if repite_departamento:
                response = {"status": 201,'mensaje': 'El departamento ' + duplicado_ID_Departamentos +' ya esta siendo usado',"error":True,"input_error":"departamento"}
                #return json_util.dumps(response)
            elif repite_estacionamiento:
                response = {"status": 201,'mensaje': 'El estacionamiento ' + duplicado_Numero_Estacionamiento +' ya esta siendo usado',"error":True,"input_error":"estacionamiento"}
                #return json_util.dumps(response) 
            elif repite_deposito:
                response = {"status": 201,'mensaje': 'El Deposito ' + duplicado_Numero_Deposito +' ya esta siendo usado',"error":True,"input_error":"deposito"} 
            elif repite_ambos_v1:
                response = {"status": 201,'mensaje': 'El estacionamiento ' + Numero_Estacionamiento +' y el departamento '+ID_Departamentos+' ya esta siendo usado',"error":True,"input_error":"estacionamiento y departameto"}
                #return json_util.dumps(response)      
            elif repite_ambos_v2:
                response = {"status": 201,'mensaje': "El departamento "+ID_Departamentos+" y el deposito "+Numero_deposito+" ya esta siendo usado","error":True,"input_error":"departamento y deposito"} 
            elif repite_ambos_v3:
                response = {"status": 201,'mensaje': "El estacionamiento "+Numero_Estacionamiento+" y el deposito "+Numero_deposito+" ya esta siendo usado","error":True,"input_error":"estacionamiento y deposito"}
            elif repite_todo:
                response = {"status": 201,'mensaje': "El departamento "+ID_Departamentos+",el estacionamiento "+Numero_Estacionamiento+" y el deposito "+Numero_deposito+" ya esta siendo usado","error":True,"input_error":"todos"}
        contar_porc_participacion(Finca,estado)
        #return json_util.dumps(response)    
        return response"""
    except Exception as e:
        print(e)
        response = {
                "status": 500,
                "mensaje":"Hubo error al registrar → "+str(e)}
        return response

def buscar_propietario_tipo_documento():
    base_datos = obtener_bd()
    session,engine=get_sesion(base_datos)
    nro_documento = request.json['nro_documento']
    try: 
        respuesta = session.query(Propietarios).filter(Propietarios.nro_documento == nro_documento).all()
        result = [
        {
            "nombres_y_apellidos": x.nombres_y_apellidos,
            "correo": x.correo,
            "telefono":x.telefono
        } 
        for x in respuesta]
        # Convert the list to JSON format
        json_result = json_util.dumps(result)
        print(json_result)
        return json_result
    except Exception as e:
        print('ERROR → ',e)
        json_result = str(e)
        return json_result 

#ACTUALIZAR
def actualizar_propietario_ID():

    base_datos = obtener_bd()
    #base_datos = 'albertobd'
    session,engine=get_sesion(base_datos)
    id_buscar = request.json['']
    #id_buscar = 2
    try:
        #respuesta = session.query(Propiedad,Propietarios).join(Propietarios).all()#es una lista
        respuesta = session.query(Propiedad,Propietarios).join(Propietarios).filter(Propietarios.idpropietarios == id_buscar).all()#es una lista
        result = [
        {
            "idpropiedad": x.idpropiedad, 
            "tipo_propietario": x.tipo_propietario, 
            "porcentaje_participacion": x.porcentaje_participacion, 
            "numero_deposito":x.numero_deposito,
            "numero_departamento":x.numero_departamento,
            "numero_estacionamiento":x.numero_estacionamiento,
            "finca_id":x.finca_id,
            "idpropietarios": y.idpropietarios, 
            "nombres_y_apellidos": y.nombres_y_apellidos,
            "tipodocumento":y.tipodocumento,
            "nro_documento": y.nro_documento, 
            "correo": y.correo,
            "telefono":y.telefono,
            "estado": y.estado
        } 
        for x,y in respuesta]#x → Propiedad , y → Propietarios, esto es una lista
        # Convert the list to JSON format
        json_result = json_util.dumps(result)
        return json_result
    except Exception as e:
        print('ERROR → ',e)
        json_result = str(e)
        return json_result 

def actualizar_propietario_ID2():#P6
    duplicado_ID_Departamentos = ""
    duplicado_Numero_Estacionamiento = ""
    duplicado_Numero_Deposito = ""
    _id = request.json["_id"]
    #validacion = False
    estado = "A"
    try:
        Finca = request.json["Finca"]
        Nombres_y_Apellidos = request.json["Nombres_y_Apellidos"]
        Tipo_Documento = request.json["Tipo_Documento"]
        Nro_Documento = request.json["Nro_Documento"]
        Correo = request.json["Correo"]
        Telefono = request.json["Telefono"]
        array_departamentos = request.json["Departamentos"]
        Estacionamientos = request.json["Estacionamientos"]
        Numero_deposito = request.json["Numero_deposito"]

        ID_Departamentos = request.json["Departamentos"][0]['ID_Departamentos']#validar que no se repita
        Numero_Estacionamiento = request.json["Estacionamientos"][0]['Numero_Estacionamiento']#validar que no se repita
        
        #PARA EXTRAER DATOS ANTES DE HACER LOS CAMBIOS
        respuesta = conexion('propietarios').find({"$and": [
        {"_id": f'{_id}'},
        {"Finca": f'{Finca}'},
        {"estado": f'{estado}'}
        ]})
        response = json_util.dumps(respuesta)#es un string []
        consulta = json_util.loads(response)#diccionario
        valor_id_departamento_antes = consulta[0]['Departamentos'][0]['ID_Departamentos']
        valor_estacionamiento_antes = consulta[0]['Estacionamientos'][0]['Numero_Estacionamiento']
        valor_deposito_antes = consulta[0]['Numero_deposito']
        #-------------------------------------------------

        #INICIALIZAR LAS VALDIACIONES Y REPETICIONES
        #FALSE ya existe y TRUE cuando no existe
        validacion_departamento = False
        validacion_estacionamiento = False
        validacion_deposito = False
        validacion_general = False
        #REPETICIONES
        #solo se repite un solo dato
        repite_estacionamiento = False
        repite_departamento = False
        repite_deposito = False
        #caso Dpto y estacionamiento
        repite_ambos_v1 = False
        #caso Dpto y deposito
        repite_ambos_v2 = False
        #caso estacionamiento y deposito
        repite_ambos_v3 = False
        #caso los tres campos sean invalidos
        repite_todo = False
        #------------------------------------------
        #casos:
        # -- Todos
        # -- V1: Dpto y estacionamiento
        # -- V2: Dpto y deposito
        # -- V3: estacionamiento y deposito
        # -- Solo Dpto
        # -- Solo estacionamiento
        # -- Solo deposito
        #Todos
        if ID_Departamentos != "" and Numero_Estacionamiento!="" and Numero_deposito!="":#puso tanto departamento como estacionamiento
            print('TRES CAMPOS\n ')
            if ID_Departamentos== valor_id_departamento_antes and Numero_Estacionamiento== valor_estacionamiento_antes and Numero_deposito == valor_deposito_antes:
                print('NO CAMBIO NADA\n')
                #en caso no se haga ninguna modificacion
                #response = {"status": 201,'mensaje': 'El propietario ' + Nombres_y_Apellidos + ' ha sido actualizado satisfactoriamente'}
                validacion_general= True
                #return json_util.dumps(response)
            elif (ID_Departamentos== valor_id_departamento_antes):#no cambia el departamento
                if (Numero_Estacionamiento== valor_estacionamiento_antes):#cambia el deposito
                    print('SOLO CAMBIA EL DEPOSITO\n')
                    validacion_deposito=validar_id_deposito(Numero_deposito,Finca,"A")
                    if validacion_deposito:
                        validacion_general=True
                    else:
                        validacion_general=False
                        repite_deposito = True
                        duplicado_Numero_Deposito = Numero_deposito
                else:#cambio el estacionamiento
                    print('CAMBIO ESTACIONAMIENTO Y DEPOSITO\n')
                    validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                    if (Numero_deposito== valor_deposito_antes):#no cambia el deposito
                        if (validacion_estacionamiento):
                            validacion_general= True
                        else:
                            repite_estacionamiento = True
                            duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                    else:#tambien cambia el deposito
                        validacion_deposito=validar_id_deposito(Numero_deposito,Finca,"A")
                        if validacion_deposito and validacion_estacionamiento:
                            validacion_general=True
                        else:
                            validacion_general=False
                            if (validacion_deposito == False and validacion_estacionamiento==True):
                                repite_deposito = True
                                duplicado_Numero_Deposito = Numero_deposito
                            elif(validacion_deposito == True and validacion_estacionamiento==False):
                                repite_estacionamiento = True
                                duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                            else:
                                repite_ambos_v3 = True
            else:#cambio tambien departamento
                validacion_departamento=validar_id_departamento(ID_Departamentos,Finca,"A")
                if (Numero_Estacionamiento== valor_estacionamiento_antes):
                    if (Numero_deposito== valor_deposito_antes):#solo ha cambiado de departamento
                        if validacion_departamento:
                            validacion_general=True
                        else:
                            repite_departamento = True
                            duplicado_ID_Departamentos = ID_Departamentos
                    else:
                        validacion_deposito=validar_id_deposito(Numero_deposito,Finca,"A")
                        if validacion_deposito and validacion_departamento:
                            validacion_general=True
                        else:
                            validacion_general=False
                            if (validacion_departamento== False and validacion_deposito ==True):
                                repite_departamento = True
                                duplicado_ID_Departamentos = ID_Departamentos
                            elif(validacion_departamento== True and validacion_deposito ==False):
                                repite_deposito = True
                                duplicado_Numero_Deposito = Numero_deposito
                            else:
                                repite_ambos_v2 = True
                else:#cambio el estacionamiento
                    print('CAMBIO ESTACIONAMIENTO Y DEPARTAMENTO\n')
                    validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                    if (Numero_deposito== valor_deposito_antes):
                        if (validacion_departamento and validacion_estacionamiento):
                            validacion_general= True
                        else:
                            validacion_general= False
                            if(validacion_departamento== True and validacion_estacionamiento == False):
                                repite_estacionamiento = True
                                duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                            elif(validacion_departamento== False and validacion_estacionamiento == True):
                                repite_departamento = True
                                duplicado_ID_Departamentos = ID_Departamentos
                            else:
                                repite_ambos_v1= True
                    else:   
                        print('CAMBIO LOS TRES CAMPOS\n') 
                        validacion_deposito=validar_id_deposito(Numero_deposito,Finca,"A")
                        if validacion_deposito and validacion_estacionamiento and validacion_deposito:
                            validacion_general=True
                        else:#pueden errar los 3
                            validacion_general=False
                            if (validacion_departamento):
                                if (validacion_estacionamiento):
                                    repite_deposito = True
                                    duplicado_Numero_Deposito = Numero_deposito
                                else:
                                    if (validacion_deposito):
                                        repite_estacionamiento = True
                                        duplicado_Numero_Estacionamiento = Numero_Estacionamiento 
                                    else:
                                        repite_ambos_v3 = True
                                        duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                                        duplicado_Numero_Deposito = Numero_deposito
                            else:#dpto esta mal
                                if (validacion_estacionamiento):
                                    if (validacion_deposito):
                                        repite_departamento = True
                                        duplicado_ID_Departamentos = ID_Departamentos
                                    else:
                                        repite_ambos_v2 = True
                                        duplicado_ID_Departamentos = ID_Departamentos
                                        duplicado_Numero_Deposito = Numero_deposito
                                else:
                                    if (validacion_deposito):
                                        repite_ambos_v1 = True
                                        duplicado_ID_Departamentos = ID_Departamentos
                                        duplicado_Numero_Estacionamiento = Numero_Estacionamiento 
                                    else:
                                        repite_todo = True
                                        duplicado_ID_Departamentos = ID_Departamentos
                                        duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                                        duplicado_Numero_Deposito = Numero_deposito

        elif(ID_Departamentos != "" and Numero_Estacionamiento!=""):
            print('SOLO HAY DEPARTAMENTOS Y ESTACIONAMIENTO')
            if ID_Departamentos== valor_id_departamento_antes and Numero_Estacionamiento== valor_estacionamiento_antes:
                print('NO CAMBIO NADA\n')
                #en caso no se haga ninguna modificacion
                #response = {"status": 201,'mensaje': 'El propietario ' + Nombres_y_Apellidos + ' ha sido actualizado satisfactoriamente'}
                validacion_general= True
                #return json_util.dumps(response)
            elif(ID_Departamentos== valor_id_departamento_antes):
                print('CAMBIO SOLO ESTACIONAMIENTO\n')
                validacion_estacionamiento=validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                if validacion_estacionamiento:
                    validacion_general = True
                else:
                    validacion_general = False
                    repite_estacionamiento = True
                    duplicado_Numero_Estacionamiento = Numero_Estacionamiento   
            else:
                if(Numero_Estacionamiento == valor_estacionamiento_antes):
                    print('SOLO CAMBIA DEPARTAMENTO\n')
                    validacion_departamento=validar_id_departamento(ID_Departamentos,Finca,"A")  
                    if (validacion_departamento):
                        validacion_general = True
                    else:
                        validacion_general = False
                        repite_departamento = True
                        duplicado_ID_Departamentos= ID_Departamentos
                else:
                    print('CAMBIO ESTACIONAMIENTO Y DEPARTAMENTO\n')                    
                    validacion_estacionamiento=validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                    if (validacion_departamento and validacion_estacionamiento):
                        validacion_general = True
                    elif(validacion_departamento==False and validacion_estacionamiento == True ):
                        repite_departamento = True
                        duplicado_ID_Departamentos = ID_Departamentos
                        validacion_general = False
                    elif(validacion_departamento==True and validacion_estacionamiento == False ):
                        validacion_general = False
                        repite_estacionamiento = True
                        duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                    else:
                        validacion_general = False
                        repite_ambos_v1 = True
        elif(ID_Departamentos != "" and Numero_deposito!=""):  
            if ID_Departamentos== valor_id_departamento_antes and Numero_deposito== valor_deposito_antes:
                print('NO CAMBIO NADA\n')
                #en caso no se haga ninguna modificacion
                #response = {"status": 201,'mensaje': 'El propietario ' + Nombres_y_Apellidos + ' ha sido actualizado satisfactoriamente'}
                validacion_general= True
                #return json_util.dumps(response)
            elif(ID_Departamentos== valor_id_departamento_antes):
                print('SOLO CAMBIO EL NUMERO DE DEPOSITO\n')
                validacion_deposito=validar_id_deposito(Numero_deposito,Finca,"A")
                if validacion_deposito:
                    validacion_general = True
                else:
                    validacion_general = False
                    repite_deposito = True
                    duplicado_Numero_Deposito = Numero_deposito 
            else:#ha cambiado el numero de departamento
                if (Numero_deposito == valor_deposito_antes):
                    validacion_departamento=validar_id_departamento(ID_Departamentos,Finca,"A") 
                    if (validacion_departamento):
                        validacion_general = True
                    else:
                        repite_departamento = True
                        duplicado_ID_Departamentos = ID_Departamentos
                else: 
                    print('CAMBIO DEPOSITO Y DEPARTAMENTO\n') 
                    validacion_departamento=validar_id_departamento(ID_Departamentos,Finca,"A") 
                    validacion_deposito=validar_id_deposito(Numero_deposito,Finca,"A")      
                    if (validacion_deposito and validacion_departamento):
                        validacion_general = True
                    elif(validacion_deposito==True and validacion_departamento == False ):
                        validacion_general = False
                        repite_departamento = True
                        duplicado_ID_Departamentos = ID_Departamentos
                    elif(validacion_deposito==False and validacion_departamento == True ):
                        validacion_general = False
                        repite_deposito = True
                        duplicado_Numero_Deposito = Numero_deposito
                    else:
                        validacion_general = False
                        repite_ambos_v2 = True
        elif(Numero_Estacionamiento != "" and Numero_deposito!=""):  
            if Numero_Estacionamiento== valor_estacionamiento_antes and Numero_deposito== valor_deposito_antes:
                #en caso no se haga ninguna modificacion
                #response = {"status": 201,'mensaje': 'El propietario ' + Nombres_y_Apellidos + ' ha sido actualizado satisfactoriamente'}
                validacion_general= True
                #return json_util.dumps(response)
            elif(Numero_Estacionamiento== valor_estacionamiento_antes):
                validacion_deposito=validar_id_deposito(Numero_deposito,Finca,"A")
                if validacion_deposito:
                    validacion_general = True
                else:
                    validacion_general = False
                    repite_deposito = True
                    duplicado_Numero_Deposito = Numero_deposito 
            else:
                if (Numero_deposito == valor_deposito_antes):
                    validacion_estacionamiento=validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                    if validacion_estacionamiento:
                        validacion_general = True
                    else:
                        validacion_general = False
                        repite_estacionamiento = True
                        duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                else:        
                    validacion_deposito=validar_id_deposito(Numero_deposito,Finca,"A") 
                    validacion_estacionamiento=validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                    if (validacion_deposito and validacion_estacionamiento):
                        validacion_general = True
                    elif(validacion_deposito==False and validacion_estacionamiento == True ):
                        validacion_general = False
                        repite_departamento = True
                        duplicado_ID_Departamentos = ID_Departamentos
                    elif(validacion_deposito==True and validacion_estacionamiento == False ):
                        validacion_general = False
                        repite_estacionamiento = True
                        duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                    else:
                        validacion_general = False
                        repite_ambos_v3 = True
        elif(ID_Departamentos!=""):
            if ID_Departamentos == valor_id_departamento_antes:
                validacion_general = True
            else:
                validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
                if validacion_departamento:
                    validacion_general = True
                else:
                    validacion_general = False
                    repite_departamento = True
                    duplicado_ID_Departamentos = ID_Departamentos
        elif(Numero_Estacionamiento!=""):#numero estacionamiento
            if Numero_Estacionamiento == valor_estacionamiento_antes:
                validacion_general = True
            else:
                validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                if validacion_estacionamiento:
                    validacion_general = True
                else:
                    validacion_general = False
                    repite_estacionamiento = True
                    duplicado_Numero_Estacionamiento = Numero_Estacionamiento
        elif(Numero_deposito!=""):#deposito
            if Numero_deposito == valor_deposito_antes:
                validacion_general = True
            else:
                validacion_deposito = validar_id_deposito(Numero_deposito,Finca,"A")
                if validacion_deposito:
                    validacion_general = True
                else:
                    validacion_general = False
                    repite_deposito = True
                    duplicado_Numero_Deposito = Numero_deposito
            """#caso 3
                if(Numero_deposito== valor_deposito_antes):#solo cambio el numero de estacionamiento
                    validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                    if validacion_estacionamiento:
                        validacion_general=True
                    else:
                        validacion_general=False
                        repite_estacionamiento = True
                        duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                #caso 2
                elif(Numero_Estacionamiento== valor_estacionamiento_antes):#solo cambia el numero de deposito
                    validacion_deposito = validar_id_deposito(Numero_deposito,Finca,"A")
                    if validacion_deposito:
                        validacion_general=True
                    else:
                        validacion_general=False
                        repite_deposito = True
                        duplicado_Numero_Deposito = Numero_deposito
                    #solo cambia el numero de estacionamiento
                #caso 4
                elif(Numero_Estacionamiento== valor_estacionamiento_antes and Numero_deposito== valor_deposito_antes ):
                    validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                    validacion_deposito = validar_id_deposito(Numero_deposito,Finca,"A")
                    if validacion_deposito and validacion_estacionamiento:
                        validacion_general=True
                    else:
                        validacion_general=False
                        repite_deposito = True
                        duplicado_Numero_Deposito = Numero_deposito
            elif(ID_Departamentos!= valor_id_departamento_antes):
                
                validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
                #caso 5
                if (Numero_Estacionamiento!= valor_estacionamiento_antes and Numero_deposito!= valor_deposito_antes):
                    validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                    validacion_deposito = validar_id_deposito(Numero_deposito,Finca,"A")
                    if validacion_deposito and validacion_estacionamiento and validacion_departamento:
                        validacion_general=True
                    else:
                        validacion_general=False
                        repite_departamento = True
                        duplicado_ID_Departamentos = ID_Departamentos
                #caso 6
                elif(Numero_Estacionamiento== valor_estacionamiento_antes and Numero_deposito== valor_deposito_antes):
                    if validacion_departamento:
                        validacion_general=True
                    else:
                        validacion_general=False
                        repite_departamento = True
                        duplicado_ID_Departamentos = ID_Departamentos
                #caso 7
                elif (Numero_Estacionamiento!= valor_estacionamiento_antes and Numero_deposito== valor_deposito_antes):
                    if validacion_departamento:
                        validacion_general=True
                    else:
                        validacion_general=False
                        repite_departamento = True
                        duplicado_ID_Departamentos = ID_Departamentos
                #caso 8
                elif (Numero_Estacionamiento== valor_estacionamiento_antes and Numero_deposito!= valor_deposito_antes):
                    if validacion_departamento:
                        validacion_general=True
                    else:
                        validacion_general=False
                        repite_departamento = True
                        duplicado_ID_Departamentos = ID_Departamentos

            elif (ID_Departamentos== valor_id_departamento_antes and Numero_Estacionamiento!= valor_estacionamiento_antes):
                #no cambia de departamento, solo de estacionamiento
                validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                if validacion_estacionamiento:
                    validacion_general= True
                else:
                    validacion_general=False
                    repite_estacionamiento = True
                    duplicado_Numero_Estacionamiento = Numero_Estacionamiento

            elif (ID_Departamentos== valor_id_departamento_antes and Numero_Estacionamiento!= valor_estacionamiento_antes):
                validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                if validacion_estacionamiento:
                    validacion_general= True
                else:
                    validacion_general=False
                    repite_estacionamiento = True
                    duplicado_Numero_Estacionamiento = Numero_Estacionamiento
            else:#cambia los dos campos
                validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
                validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                if validacion_departamento and validacion_estacionamiento:
                    validacion_general= True
                else:
                    validacion_general = False
                    repite_ambos_v1 = True
                    duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                    duplicado_ID_Departamentos = ID_Departamentos

        elif ID_Departamentos!="" and Numero_deposito!="":#solo puso departamento
            if ID_Departamentos== valor_id_departamento_antes and Numero_deposito== valor_deposito_antes:
                validacion_general=True
            else:
                validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
                if validacion_departamento ==False:
                    repite_departamento = True
                    duplicado_ID_Departamentos = ID_Departamentos
                validacion_general = validacion_departamento
            
        elif Numero_Estacionamiento!="":#solo puso estacionamiento
            if Numero_Estacionamiento == valor_estacionamiento_antes:
                validacion_general=True
            else:
                validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
                if validacion_estacionamiento ==False:
                    repite_estacionamiento = True
                    duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                validacion_general = validacion_estacionamiento"""
        else:#mensaje en caso los campos Departamentos y Estacionamientos esten vacios
            validacion_general = False
            response = {"status": 400,'mensaje': 'Los campos de Departamento y Estacionamiento no pueden estar ambos vacios'}  
            #return json_util.dumps(response)

        if validacion_general:
            if _id or Finca or Nombres_y_Apellidos or Tipo_Documento or Nro_Documento or Correo or Telefono or array_departamentos or Estacionamientos:
                modificacion = datetime.now()
                conexion('propietarios').update_one(
                    {'_id': _id}, {'$set': {
                                            "_id": _id,
                                            "Finca": Finca,
                                            "Nombres_y_Apellidos": Nombres_y_Apellidos,
                                            "Tipo_Documento": Tipo_Documento,
                                            "Nro_Documento": Nro_Documento,
                                            "Correo": Correo,
                                            "Telefono":Telefono,
                                            "Departamentos":array_departamentos,
                                            "Estacionamientos":Estacionamientos,
                                            "Numero_deposito":Numero_deposito,
                                            "Fecha_modificacion": modificacion}})
                response = {"status": 200,'mensaje': 'El propietario ' + Nombres_y_Apellidos + ' ha sido actualizado satisfactoriamente'}
                #return json_util.dumps(response)
            else:
                response ={
                    "status": 400,
                    "mensaje":"Uno o mas datos a actualizar son incorrectos"}
                #return json_util.dumps(response)
        else:
            if repite_departamento:
                response = {"status": 201,'mensaje': 'El departamento ' + duplicado_ID_Departamentos +' ya esta siendo usado',"error":True,"input_error":"departamento"}
                #return json_util.dumps(response)
            elif repite_estacionamiento:
                response = {"status": 201,'mensaje': 'El estacionamiento ' + duplicado_Numero_Estacionamiento +' ya esta siendo usado',"error":True,"input_error":"estacionamiento"}
                #return json_util.dumps(response) 
            elif repite_deposito:
                response = {"status": 201,'mensaje': 'El Deposito ' + duplicado_Numero_Deposito +' ya esta siendo usado',"error":True,"input_error":"deposito"} 
            elif repite_ambos_v1:
                response = {"status": 201,'mensaje': 'El estacionamiento ' + Numero_Estacionamiento +' y el departamento '+ID_Departamentos+' ya esta siendo usado',"error":True,"input_error":"estacionamiento y departameto"}
                #return json_util.dumps(response)      
            elif repite_ambos_v2:
                response = {"status": 201,'mensaje': "El departamento "+ID_Departamentos+" y el deposito "+Numero_deposito+" ya esta siendo usado","error":True,"input_error":"departamento y deposito"} 
            elif repite_ambos_v3:
                response = {"status": 201,'mensaje': "El estacionamiento "+Numero_Estacionamiento+" y el deposito "+Numero_deposito+" ya esta siendo usado","error":True,"input_error":"estacionamiento y deposito"}
            elif repite_todo:
                response = {"status": 201,'mensaje': "El departamento "+ID_Departamentos+",el estacionamiento "+Numero_Estacionamiento+" y el deposito "+Numero_deposito+" ya esta siendo usado","error":True,"input_error":"todos"}
        contar_porc_participacion(Finca,estado)
        return json_util.dumps(response)
    except Exception as e:
        print(e)
        response = {
                "status": 500,
                "mensaje":"Hubo error al actualizar los datos → "+str(e)}
        return json_util.dumps(response)

#ELIMINAR
def eliminar_propietario_ID():#P5
    try:
        _id = request.json["_id"]
        Nombres_y_Apellidos = request.json["Nombres_y_Apellidos"]
        conexion('propietarios').update_one(
                {'_id': _id}, 
                {'$set': {"estado":'N'}})
        response = {"status": 201,'mensaje': 'El propietario '+Nombres_y_Apellidos+' ha sido eliminado satisfactoriamente'}
        return json_util.dumps(response)
    except Exception as e:    
        print(e)
        response = {
                "status": 500,
                "mensaje":"Hubo error al eliminar al propietario "+Nombres_y_Apellidos+"  → "+str(e)}
        return json_util.dumps(response)