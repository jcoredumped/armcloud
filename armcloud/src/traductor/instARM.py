#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string

def imprimirResultado(registros, memoria):
    # imprimimos el diccionario de registros
    print "Registros:"
    for i in range(32):
        print "\tr%d => %d" %(i, registros[i])
    
    print "\n\nMemoria:"
    direcciones = memoria.keys()
    direcciones.sort() # las ordenamos
    for elemento in direcciones:
        print "\t0x%08x -> %d" % (elemento, memoria[elemento])
    
    
def initEstados():

    ### Idea de diccionario de estados

    ## Un diccionario tal que la clave sea lo que representa

    estados = {
                'N' : '0',       #Indica ultima op dio resultado negativo N=1 o positivo N=0
                'Z' : '0',      # Indica si el resultado de la op fue zero Z=1 o no Z=0
                'C' : '0',     # Para suma o comparacion C=1 si hubo carry, para las operaciones de desplazamiento toma el valor del bit saliente
                'V' : '0'
              }
    return estados

# Condiciones asociadas a las instrucciones de salto... B{sufijo}

# EQ  Igual                           Z=1
# NE Distinto                         Z=0
# HI Mayor que (sin signo)            C=1 & Z=0
# LS Menor o igual que (sin signo)    C=0 | Z=1
# GE Mayor o igual que (con signo)    N == V
# LT Menor que con signo              N != V
# GT Mayor que con signo              Z=0 & N==V
# LE Menor o igual que (con signo)    Z=1 | N != V

def isEQ(estados):
    '''función que devuelve True o False en funcion de los bits de estado para el caso de 
    igual'''
    if estados['Z'] == 1:
        return True
    else:
        return False
    
def isNE(estados):
    '''función que devuelve True o False en funcion de los bits de estado para el caso de 
    distinto'''
    if estados['Z'] == 0:
        return True
    else:
        return False

def isHI(estados):
    '''función que devuelve True o False en funcion de los bits de estado para el caso de 
    mayor que (sin signo)'''
    if estados['C'] == 1 and estados['Z'] == 0:
        return True
    else:
        return False 
def isLS(estados):
    '''función que devuelve True o False en funcion de los bits de estado para el caso de
    menor o igual que'''
    if estados['C'] == 0 or estados['Z'] == 1:
        return True
    else:
        return False
def isGE(estados):
    '''función que devuelve True o False en funcion de los bits de estado para el caso de 
    mayor o igual que (con signo)'''
    if estados['N'] == estados['V']:
        return True
    else:
        return False
    
def isLT(estados):
    '''función que devuelve True o False en funcion de los bits de estado para el caso de 
    menor que con signo'''
    if estados['N'] != estados['V']:
        return True
    else:
        return False
    
def isGT(estados):
    '''función que devuelve True o False en funcion de los bits de estado para el caso de
    mayor que con signo'''
    if estados['Z'] == 0 and estados['N'] == estados['V']:
        return True
    else:
        return False
    
def isLE(estados):
    '''función que devuelve True o False en funcion de los bits de estado para el caso de
    menor o igual que (con signo)'''
    if estados['Z'] == 1 or estados['N'] != estados['V']:
        return True
    else:
        return False
    








# Las instrucciones aritmeticologicas tienen un parametro opcional que indica si se trata de una constante o no




######## instrucciones aritmeticas
def iand(pc, registros, rd, rs, shift, constantes=0):

    if type(constantes) == type({}): # si constantes es un diccionario es que es una constante
        operand = constantes[shift]
    elif type(shift) == type(1): # si es un entero es que es un registro
        operand = registros[shift]
    elif shift[:2] == "0X": # si es un numero en hexa
        operand = string.atoi(shift, 16)
    else: # si es un entero
        operand = string.atoi(shift)

    registros[rd] = registros[rs] & operand #AND
    return pc + 1

def iorr (pc, registros, rd, rs, shift, constantes=0):
    if type(constantes) == type({}): # si constantes es un diccionario es que es una constante
        operand = constantes[shift]
    elif type(shift) == type(1): # si es un entero es que es un registro
        operand = registros[shift]
    elif shift[:2] == "0X": # si es un numero en hexa
        operand = string.atoi(shift, 16)
    else: # si es un entero
        operand = string.atoi(shift)
    
    registros[rd] = registros[rs] | operand # OR

    return pc + 1


def ieor (pc, registros, rd, rs, shift, constantesi=0):
    if type(constantes) == type({}): # si constantes es un diccionario es que es una constante
        operand = constantes[shift]
    elif type(shift) == type(1): # si es un entero es que es un registro
        operand = registros[shift]
    elif shift[:2] == "0X": # si es un numero en hexa
        operand = string.atoi(shift, 16)
    else: # si es un entero
        operand = string.atoi(shift)

    registros[rd] = registros[rs] ^ operand # XOR

    return pc + 1



def iadd (pc, registros, rd, rs, shift, constantes=0):
    if type(constantes) == type({}): # si constantes es un diccionario es que es una constante
        operand = constantes[shift]
    elif type(shift) == type(1): # si es un entero es que es un registro
        operand = registros[shift]
    elif shift[:2] == "0X": # si es un numero en hexa
        operand = string.atoi(shift, 16)
    else: # si es un entero
        operand = string.atoi(shift)
    registros[rd] = registros[rs] + operand
    return pc + 1

def isub(pc, registros, rd, rs, shift, constantes=0):
    
    if type(constantes) == type({}): # si constantes es un diccionario es que es una constante
        operand = constantes[shift]
    elif type(shift) == type(1): # si es un entero es que es un registro
        operand = registros[shift]
    elif shift[:2] == "0X": # si es un numero en hexa
        operand = string.atoi(shift, 16)
    else: # si es un entero
        operand = string.atoi(shift)

    registros[rd] = registros[rs] - operand
    return pc + 1

def irsb(pc, registros, rd, rs, shift, constantes=0):
    if type(constantes) == type({}): # si constantes es un diccionario es que es una constante
        operand = constantes[shift]
    elif type(shift) == type(1): # si es un entero es que es un registro
        operand = registros[shift]
    elif shift[:2] == "0X": # si es un numero en hexa
        operand = string.atoi(shift, 16)
    else: # si es un entero
        operand = string.atoi(shift)

    registros[rd] = operand - registros[rs]
    return pc + 1

def imov(pc, registros, rd, shift, constantes=0):
    if type(constantes) == type({}): # si constantes es un diccionario es que es una constante
        operand = constantes[shift]
    elif type(shift) == type(1): # si es un entero es que es un registro
        operand = registros[shift]
    elif shift[:2] == "0X": # si es un numero en hexa
        operand = string.atoi(shift, 16)
    else: # si es un entero
        operand = string.atoi(shift)
    registros[rd] = operand    # movemos shift a registros[rd]
    return pc + 1

def icmp(pc, registros, estados, rd, shift, constantes=0):
    if type(constantes) == type({}): # si constantes es un diccionario es que es una constante
        operand = constantes[shift]
    elif type(shift) == type(1): # si es un entero es que es un registro
        operand = registros[shift]
    elif shift[:2] == "0X": # si es un numero en hexa
        operand = string.atoi(shift, 16)
    else: # si es una cadena pero no es hexa es que es un ENTERO o ENTERONEGATIVO
        operand = string.atoi(shift)
    
    conSigno = registros[rd] - operand
    
    sinSigno = abs(registros[rd]) - abs(operand)
    
    
    if conSigno == 0: # es que son iguales
        estados['Z'] = 1
    else:
        estados['Z'] = 0
    if conSigno > 0 or conSigno == 0:
        estados['N'] = 0
        estados['V'] = 0
    else:
        estados['N'] = 1
        estados['V'] = 0
    
    if sinSigno > 0:
        estados['C'] = 1
    else:
        estados['C'] = 0
        
    return pc + 1    


######## instrucciones de multiplicacion

def imul(pc, registros, rd, rs, rt):
    registros[rd] = registros[rs] * registros[rt]
    return pc + 1

def imla(pc, registros, rd, rs, rt, rn):
    registros[rd] = registros[rs]*registros[rt] + rn
    return pc + 1
    

### instrucciones de acceso a memoria



def ildr(pc, registros, memoria, etiq, rd, rb, desp, accion=""):
    
    # casos especiales los distinguimos por el valor de etiqueta
    
    if accion == "=": # Caso que tenemos que almacenar en rd etiq[desp]
        registros[rd] = etiq[desp]
    elif accion == "ETIQUETA": # almacenamos en rd lo que hay en memoria[etiq[desp]]
        registros[rd] = memoria[etiq[desp]]
    else:
        if type(rb) == type(1) == type(desp): # si son todo registros
            desp = registros[desp]
        elif desp[:2] == "0X": # si desp es una cadena hexa la convertimos a entero
            desp = string.atoi(desp, 16)
        else: # si es una cadena pero no es hexa puede ser ENTERO ENTERONEGATIVO
            desp = string.atoi(desp)

        registros[rd] = memoria[registros[rb] + desp]
            
    
    return pc + 1

def istr(pc, registros, memoria, etiq, rf, rb, desp, accion=""):
    
    # caso especial
    if accion == "ETIQUETA": # almacenamos en memoria[registros[rb]+etiq[desp]] el valor de registros[rf]
        memoria[memoria[etiq[desp]]] = registros[rf]
    else:
        if type(rb) == type(1) == type(desp): # si son registros
            desp = registros[desp]
        elif desp[:2] == "0X": # desp es una cadena hexa la convertimos a entero
            desp = string.atoi(desp, 16)
        else: # si es una cadena pero no es un hexa puede ser ENTERO ENTERONEGATIVO
            desp = string.atoi(desp)
        
        memoria[registros[rb] + desp] = registros[rf] 
    
    return pc + 1


####### instrucciones de salto

#ib(pc, etiq, \"%s\", \"ETIQUETA\")

def ib(pc, etiq, valor, opcion=""):
    if opcion == "ETIQUETA":
        salto = etiq[valor]
    else: # si no es una etiqueta es decir es del tipo b . VALOR
        if valor[:2] == "0X": # valor es una cadena hexa
            valor = string.atoi(valor, 16)
        else: # valor es una cadena pero no es hexa
            valor = string.atoi(valor)
        salto = pc + valor
    return salto
    

def ibeq(pc, etiq, estados, valor, opcion=""):
    if isEQ(estados) == True:
        salto = ib(pc, etiq, valor, opcion)
    else:
        salto = pc + 1
    return salto

def ibne(pc, etiq, estados, valor, opcion=""):
    if isNE(estados) == True:
        salto = ib(pc, etiq, valor, opcion)
    else:
        salto = pc + 1
    return salto

def ibhi(pc, etiq, estados, valor, opcion=""):
    if isHI(estados) == True:
        salto = ib(pc, etiq, valor, opcion)
    else:
        salto = pc + 1
    return salto

def ibls(pc, etiq, estados, valor, opcion=""):
    if isLS(estados) == True:
        salto = ib(pc, etiq, valor, opcion)
    else:
        salto = pc + 1
    return salto

def ibge(pc, etiq, estados, valor, opcion=""):
    if isGE(estados) == True:
        salto = ib(pc, etiq, valor, opcion)
    else:
        salto = pc + 1
    return salto

def iblt(pc, etiq, estados, valor, opcion=""):
    if isLT(estados) == True:
        salto = ib(pc, etiq, valor, opcion)
    else:
        salto = pc + 1
    return salto

def ibgt(pc, etiq, estados, valor, opcion=""):
    if isGT(estados) == True:
        salto = ib(pc, etiq, valor, opcion)
    else:
        salto = pc + 1
    return salto

def ible(pc, etiq, estados, valor, opcion=""):
    if isLE(estados) == True:
        salto = ib(pc, etiq, valor, opcion)
    else:
        salto = pc + 1
    return salto
