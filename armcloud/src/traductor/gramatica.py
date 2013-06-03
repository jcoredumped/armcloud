# -*- coding: utf-8 -*-

from lexico import tokens

import sys
import string

lineaFichero = 1

numInstruccion = 1

listaword = []              # Una lista para solventar el problema del word

listaspace = []             # necesitamos otra lista para solventar el problema del orden de space

ESPACIOS = " " * 2  # Valor usado para insertar espacios en blanco en los 
                    # strings la idea es usar el %s y luego ESPACIOS, 
                    # para no tener tantos errores en sangrado

# Arbol sintactico

# s: resto sig1
#  | sig1
#  ;

def p_s(p):
    '''s : resto sig1
         | sig1
    
    '''

# sig1: global resto sig2
#     ;

def p_sig1(p):
    '''sig1 : global resto sig2 
    '''

# global: PUNTO GLOBAL ETIQUETA
#       ;

def p_global(p):
    ''' global : PUNTO GLOBAL ETIQUETA 
    '''

# sig2: PUNTO DATA resto listazonadata
#     | sig3
#     ;

def p_sig2(p):
    ''' sig2 : PUNTO DATA resto listazonadata
             | sig3
    '''

# listazonadata: tipodata listazonadata
#              | tipodata sig3
#              ;

def p_listazonadata(p):
    ''' listazonadata : tipodata listazonadata
                      | tipodata sig3
    '''

# tipodata: equ rzd
#         | word listaword resto
#         ;

def p_tipodata(p):
    ''' tipodata : equ rzd
                 | word listaword resto  
    '''
    global salida
    global listaword
    if len(p) == 3: # Cuando es un equ
        salida += "constantes['%s'] = %s\n" % (p[1], p[2])

    else: ## Cuando es un word
        salida += "etiq['%s'] = direc\n" %p[1]
        for word in listaword:
            if word[1] == "DIRHEXA":
                salida += "memoria[direc] = string.atoi('%s', 16)\n" %word[0]
            else:
                salida += "memoria[direc] = string.atoi('%s')\n" %word[0]
            salida += "direc = direc + 4\n"
        listaword=[] # vaciamos de nuevo la lista
        



# rzd: ENTERO resto
#    | ENTERONEGATIVO resto
#    | DIRHEXA resto
#    ;

def p_rzd_enteros(p):
    ''' rzd : ENTERO resto
            | ENTERONEGATIVO resto
    '''
    p[0] = "string.atoi('%s')" % p[1]

def p_rzd_dirhexa(p):
    '''rzd : DIRHEXA resto
    '''
    p[0] = "string.atoi('%s', 16)" % p[1]

# equ: PUNTO EQU ETIQUETA COMA
#    ;

def p_equ(p):
    ''' equ : PUNTO EQU ETIQUETA COMA
    '''
    p[0] = p[3] # nos quedamos con la ETIQUETA


# word: ETIQUETA DP PUNTO WORD
#     ;

def p_word(p):
    ''' word : ETIQUETA DP PUNTO WORD
    '''
    p[0] = p[1] # Nos quedamos con la etiqueta

# listaword: DIRHEXA COMA listaword
#          | DIRHEXA
#          | ENTERO COMA listaword
#          | ENTERO
#          | ENTERONEGATIVO COMA listaword
#          | ENTERONEGATIVO
#          ;

def p_listaword_dirhexa(p):
    ''' listaword : DIRHEXA COMA listaword
                  | DIRHEXA
    '''
    listaword.insert(0, [p[1], "DIRHEXA"])



def p_listaword_enteros(p):
    ''' listaword : ENTERO COMA listaword
                  | ENTERO 
                  | ENTERONEGATIVO COMA listaword
                  | ENTERONEGATIVO
    '''
    
    listaword.insert(0, [p[1], "ENTEROS"])


# sig3: PUNTO BSS resto listazonabss sig4
#     | sig4
#     ;

def p_sig3(p):
    ''' sig3 : PUNTO BSS resto listazonabss sig4
             | sig4
    '''

# listazonabss: ETIQUETA DP PUNTO SPACE enterohexa resto listazonabss
#             | ETIQUETA DP PUNTO SPACE enterohexa resto
#

def p_listazonabss(p):
    ''' listazonabss : space  resto listazonabss
                     | space  resto
    '''

def p_space(p):
    ''' space : ETIQUETA DP PUNTO SPACE enterohexa
    '''
    global salida
    #print p[1], p[5]
    salida += "\netiq['%s'] = direc\n" %p[1]
    salida += "\nfor i in range(%d):\n\n%smemoria[direc] = 0\n%sdirec = direc + 4\n\n" \
            % (p[5], ESPACIOS, ESPACIOS)

# enterohexa: ENTERO
#           | DIRHEXA
#           ;

def p_enterohexa_entero(p):
    ''' enterohexa : ENTERO
    '''
    p[0] = string.atoi(p[1])
    

def p_enterohexa_dirhexa(p):
    ''' enterohexa : DIRHEXA 
    '''
    p[0] = string.atoi(p[1], 16)

# sig4: PUNTO TEXT resto inst resto
#     ;

def p_sig4(p):
    ''' sig4 : PUNTO TEXT resto inst resto
    '''

# inst: etiqueta resto inst
#     | etiqueta instruccion resto inst
#     | instruccion resto inst
#     | fin
#     ;


def p_inst(p):
    ''' inst : etiqueta resto inst
             | etiqueta instruccion resto inst
             | instruccion resto inst
             | fin
    '''

def p_etiqueta(p):
    '''etiqueta : ETIQUETA DP
    '''
    global salida
    global numInstruccion

    salida += "etiq['%s'] = %d\n" \
    % (p[1], numInstruccion)    # guardamos el numero de instruccion


# instruccion: AND REGISTRO COMA REGISTRO COMA REGISTRO
#            | AND REGISTRO COMA REGISTRO COMA ALMOADILLA DIRHEXA
#            | AND REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERO
#            | AND REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERONEGATIVO
#            | AND REGISTRO COMA REGISTRO COMA ALMOADILLA ETIQUETA
#            | ORR REGISTRO COMA REGISTRO COMA REGISTRO
#            | ORR REGISTRO COMA REGISTRO COMA ALMOADILLA DIRHEXA
#            | ORR REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERO
#            | ORR REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERONEGATIVO
#            | ORR REGISTRO COMA REGISTRO COMA ALMOADILLA ETIQUETA
#            | EOR REGISTRO COMA REGISTRO COMA REGISTRO
#            | EOR REGISTRO COMA REGISTRO COMA ALMOADILLA DIRHEXA
#            | EOR REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERO
#            | EOR REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERONEGATIVO
#            | EOR REGISTRO COMA REGISTRO COMA ALMOADILLA ETIQUETA
#            | ADD REGISTRO COMA REGISTRO COMA REGISTRO
#            | ADD REGISTRO COMA REGISTRO COMA ALMOADILLA DIRHEXA
#            | ADD REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERO
#            | ADD REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERONEGATIVO
#            | ADD REGISTRO COMA REGISTRO COMA ALMOADILLA ETIQUETA
#            | SUB REGISTRO COMA REGISTRO COMA REGISTRO
#            | SUB REGISTRO COMA REGISTRO COMA ALMOADILLA DIRHEXA
#            | SUB REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERO
#            | SUB REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERONEGATIVO
#            | SUB REGISTRO COMA REGISTRO COMA ALMOADILLA ETIQUETA
#            | RSB REGISTRO COMA REGISTRO COMA REGISTRO
#            | RSB REGISTRO COMA REGISTRO COMA ALMOADILLA DIRHEXA
#            | RSB REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERO
#            | RSB REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERONEGATIVO
#            | RSB REGISTRO COMA REGISTRO COMA ALMOADILLA ETIQUETA
#            | MOV REGISTRO COMA REGISTRO
#            | MOV REGISTRO COMA ALMOADILLA DIRHEXA
#            | MOV REGISTRO COMA ALMOADILLA ENTERO
#            | MOV REGISTRO COMA ALMOADILLA ENTERONEGATIVO
#            | MOV REGISTRO COMA ALMOADILLA ETIQUETA
#            | CMP REGISTRO COMA REGISTRO
#            | CMP REGISTRO COMA ALMOADILLA DIRHEXA
#            | CMP REGISTRO COMA ALMOADILLA ENTERO
#            | CMP REGISTRO COMA ALMOADILLA ENTERONEGATIVO
#            | MOV REGISTRO COMA ALMOADILLA ETIQUETA
#            | MUL REGISTRO COMA REGISTRO COMA REGISTRO
#            | MLA REGISTRO COMA REGISTRO COMA REGISTRO COMA REGISTRO
#            | LDR REGISTRO COMA CA REGISTRO COMA REGISTRO CC
#            | LDR REGISTRO COMA CA REGISTRO COMA ALMOADILLA DIRHEXA CC
#            | LDR REGISTRO COMA CA REGISTRO COMA ALMOADILLA ENTERO CC
#            | LDR REGISTRO COMA CA REGISTRO COMA ALMOADILLA ENTERONEGATIVO CC
#            | LDR REGISTRO COMA CA REGISTRO CC
#            | LDR REGISTRO COMA IGUAL ETIQUETA
#            | LDR REGISTRO COMA ETIQUETA
#            | STR REGISTRO COMA CA REGISTRO COMA REGISTRO CC
#            | STR REGISTRO COMA CA REGISTRO COMA ALMOADILLA DIRHEXA CC
#            | STR REGISTRO COMA CA REGISTRO COMA ALMOADILLA ENTERO CC
#            | STR REGISTRO COMA CA REGISTRO COMA ALMOADILLA ENTERONEGATIVO CC
#            | STR REGISTRO COMA CA REGISTRO CC
#            | STR REGISTRO COMA ETIQUETA
#            | B ETIQUETA
#            | B PUNTO ENTERO
#            | B PUNTO ENTERONEGATIVO
#            | B PUNTO DIRHEXA
#            | BEQ ETIQUETA
#            | BEQ PUNTO ENTERO
#            | BEQ PUNTO ENTERONEGATIVO
#            | BEQ PUNTO DIRHEXA
#            | BNE ETIQUETA
#            | BNE PUNTO ENTERO
#            | BNE PUNTO ENTERONEGATIVO
#            | BNE PUNTO DIRHEXA
#            | BHI ETIQUETA
#            | BHI PUNTO ENTERO
#            | BHI PUNTO ENTERONEGATIVO
#            | BHI PUNTO DIRHEXA
#            | BLS ETIQUETA
#            | BLS PUNTO ENTERO
#            | BLS PUNTO ENTERONEGATIVO
#            | BGE ETIQUETA
#            | BGE PUNTO ENTERO
#            | BGE PUNTO ENTERONEGATIVO
#            | BGE PUNTO DIRHEXA
#            | BLT ETIQUETA
#            | BLT PUNTO ENTERO
#            | BLT PUNTO ENTERONEGATIVO
#            | BLT PUNTO DIRHEXA
#            | BGT ETIQUETA
#            | BGT PUNTO ENTERO
#            | BGT PUNTO ENTERONEGATIVO
#            | BGT PUNTO DIRHEXA
#            | BLE ETIQUETA
#            | BLE PUNTO ENTERO
#            | BLE PUNTO ENTERONEGATIVO
#            | BLE PUNTO DIRHEXA
#            ;

def p_instruccion_and(p):
    ''' instruccion : AND REGISTRO COMA REGISTRO COMA REGISTRO
                    | AND REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERO
                    | AND REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERONEGATIVO
                    | AND REGISTRO COMA REGISTRO COMA ALMOADILLA DIRHEXA
    '''
    global numInstruccion
    global salida
    if len(p) == 8:
        salida += "programa[%d] = 'iand(pc, registros, %d, %d, \"%s\")'\n"\
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]),\
                p[7])
    else:
        salida += "programa[%d] = 'iand(pc, registros, %d, %d, %d)'\n"\
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]),\
                obtenerIndice(p[6]))
    numInstruccion += 1


def p_instruccion_and_constante(p):
    ''' instruccion : AND REGISTRO COMA REGISTRO COMA ALMOADILLA ETIQUETA
    '''
    global numInstruccion
    global salida
    salida += "programa[%d] = 'iand(pc, registros, %d, %d, \"%s\", constantes)'\n"\
            %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]), \
            p[7])
    numInstruccion += 1




def p_instruccion_orr(p):
    ''' instruccion : ORR REGISTRO COMA REGISTRO COMA REGISTRO
                    | ORR REGISTRO COMA REGISTRO COMA ALMOADILLA DIRHEXA
                    | ORR REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERO
                    | ORR REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERONEGATIVO
    '''
    global numInstruccion
    global salida
    if len(p) == 8:
        salida += "programa[%d] = 'iorr(pc, registros, %d, %d, \"%s\")'\n"\
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]),\
                p[7])
    else:
        salida += "programa[%d] = 'iorr(pc, registros, %d, %d, %d)'\n"\
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]),\
                obtenerIndice(p[6]))
    numInstruccion += 1

def p_instruccion_orr_constante(p):
    ''' instruccion : ORR REGISTRO COMA REGISTRO COMA ALMOADILLA ETIQUETA
    '''
    global numInstruccion
    global salida
    salida += "programa[%d] = 'iorr(pc, registros, %d, %d, \"%s\", constantes)'\n"\
            %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]), \
            p[7])
    numInstruccion += 1


def p_instruccion_eor(p):
    ''' instruccion : EOR REGISTRO COMA REGISTRO COMA REGISTRO
                    | EOR REGISTRO COMA REGISTRO COMA ALMOADILLA DIRHEXA
                    | EOR REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERO
                    | EOR REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERONEGATIVO
    '''
    global numInstruccion
    global salida
    if len(p) == 8:
        salida += "programa[%d] = 'ieor(pc, registros, %d, %d, \"%s\")'\n"\
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]),\
                p[7])
    else:
        salida += "programa[%d] = 'ieor(pc, registros, %d, %d, %d)'\n"\
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]),\
                obtenerIndice(p[6]))
    numInstruccion += 1

def p_instruccion_eor_constante(p):
    ''' instruccion : EOR REGISTRO COMA REGISTRO COMA ALMOADILLA ETIQUETA
    '''
    global numInstruccion
    global salida
    salida += "programa[%d] = 'ieor(pc, registros, %d, %d, \"%s\", constantes)'\n"\
            %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]), \
            p[7])
    numInstruccion += 1


def p_instruccion_add(p):
    ''' instruccion : ADD REGISTRO COMA REGISTRO COMA REGISTRO
                    | ADD REGISTRO COMA REGISTRO COMA ALMOADILLA DIRHEXA
                    | ADD REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERO
                    | ADD REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERONEGATIVO
    '''
    global numInstruccion
    global salida
    if len(p) == 8:
        salida += "programa[%d] = 'iadd(pc, registros, %d, %d, \"%s\")'\n"\
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]),\
                p[7])
    else:
        salida += "programa[%d] = 'iadd(pc, registros, %d, %d, %d)'\n"\
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]),\
                obtenerIndice(p[6]))
    numInstruccion += 1

def p_instruccion_add_constante(p):
    '''instruccion : ADD REGISTRO COMA REGISTRO COMA ALMOADILLA ETIQUETA
    '''
    global numInstruccion
    global salida
    salida += "programa[%d] = 'iadd(pc, registros, %d, %d, \"%s\", constantes)'\n"\
            %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]), \
            p[7])
    numInstruccion += 1


def p_instruccion_sub(p):
    ''' instruccion : SUB REGISTRO COMA REGISTRO COMA REGISTRO
                    | SUB REGISTRO COMA REGISTRO COMA ALMOADILLA DIRHEXA
                    | SUB REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERO
                    | SUB REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERONEGATIVO
    '''
    global numInstruccion
    global salida
    if len(p) == 8:
        salida += "programa[%d] = 'isub(pc, registros, %d, %d, \"%s\")'\n"\
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]),\
                p[7])
    else:
        salida += "programa[%d] = 'isub(pc, registros, %d, %d, %d)'\n"\
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]),\
                obtenerIndice(p[6]))
    numInstruccion += 1

def p_instruccion_sub_constante(p):
    ''' instruccion : SUB REGISTRO COMA REGISTRO COMA ALMOADILLA ETIQUETA
    '''
    global numInstruccion
    global salida
    salida += "programa[%d] = 'isub(pc, registros, %d, %d, \"%s\", constantes)'\n"\
            %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]), \
            p[7])
    numInstruccion += 1


def p_instruccion_rsb(p):
    ''' instruccion : RSB REGISTRO COMA REGISTRO COMA REGISTRO
                    | RSB REGISTRO COMA REGISTRO COMA ALMOADILLA DIRHEXA
                    | RSB REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERO
                    | RSB REGISTRO COMA REGISTRO COMA ALMOADILLA ENTERONEGATIVO
    '''
    global numInstruccion
    global salida
    if len(p) == 8:
        salida += "programa[%d] = 'irsb(pc, registros, %d, %d, \"%s\")'\n"\
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]),\
                p[7])
    else:
        salida += "programa[%d] = 'irsb(pc, registros, %d, %d, %d)'\n"\
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]),\
                obtenerIndice(p[6]))
    numInstruccion += 1

def p_instruccion_rsb_constante(p):
    ''' instruccion : RSB REGISTRO COMA REGISTRO COMA ALMOADILLA ETIQUETA
    '''
    global numInstruccion
    global salida
    salida += "programa[%d] = 'irsb(pc, registros, %d, %d, \"%s\", constantes)'\n"\
            %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]), \
            p[7])
    numInstruccion += 1

def p_instruccion_mov(p):
    ''' instruccion : MOV REGISTRO COMA REGISTRO
                    | MOV REGISTRO COMA ALMOADILLA DIRHEXA
                    | MOV REGISTRO COMA ALMOADILLA ENTERO
                    | MOV REGISTRO COMA ALMOADILLA ENTERONEGATIVO
    '''
    global numInstruccion
    global salida
    if len(p) == 6:
        salida += "programa[%d] = 'imov(pc, registros, %d, \"%s\")'\n"\
                %(numInstruccion, obtenerIndice(p[2]), p[5])
    else:
        salida += "programa[%d] = 'imov(pc, registros, %d, %d)'\n"\
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]))
    numInstruccion += 1

def p_instruccion_mov_constante(p):
    ''' instruccion : MOV REGISTRO COMA ALMOADILLA ETIQUETA
    '''
    global numInstruccion
    global salida
    salida += "programa[%d] = 'imov(pc, registros, %d, \"%s\", constantes)'\n"\
            %(numInstruccion, obtenerIndice(p[2]), p[5])
    numInstruccion += 1

def p_instruccion_cmp(p): # necesitaremos el diccionario de estados
    ''' instruccion : CMP REGISTRO COMA REGISTRO
                    | CMP REGISTRO COMA ALMOADILLA DIRHEXA
                    | CMP REGISTRO COMA ALMOADILLA ENTERO
                    | CMP REGISTRO COMA ALMOADILLA ENTERONEGATIVO
    '''
    global numInstruccion
    global salida
    if len(p) == 6:
        salida += "programa[%d] = 'icmp(pc, registros, estados, %d, \"%s\")'\n"\
                %(numInstruccion, obtenerIndice(p[2]), p[5])
    else:
        salida += "programa[%d] = 'icmp(pc, registros, estados, %d, %d)'\n"\
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]))
    numInstruccion += 1

def p_instruccion_cmp_constante(p):
    ''' instruccion : CMP REGISTRO COMA ALMOADILLA ETIQUETA
    '''
    global numInstruccion
    global salida
    salida += "programa[%d] = 'icmp(pc, registros, estados, %d, \"%s\", constantes)'\n"\
            %(numInstruccion, obtenerIndice(p[2]), p[5])
    numInstruccion += 1


def p_instruccion_mul(p):
    ''' instruccion : MUL REGISTRO COMA REGISTRO COMA REGISTRO
    '''
    global numInstruccion
    global salida
    salida += "programa[%d] = 'imul(pc, registros, %d, %d, %d)'\n"\
            %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]), obtenerIndice(p[6]))
    numInstruccion += 1

def p_instruccion_mla(p):
    ''' instruccion : MLA REGISTRO COMA REGISTRO COMA REGISTRO COMA REGISTRO
    '''
    global numInstruccion
    global salida
    salida += "programa[%d] = 'imla(pc, registros, %d, %d, %d, %d)'\n"\
            %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[4]), obtenerIndice(p[6]),\
              obtenerIndice(p[8]))
    numInstruccion += 1

def p_instruccion_ldr(p):
    ''' instruccion : LDR REGISTRO COMA CA REGISTRO COMA REGISTRO CC
                    | LDR REGISTRO COMA CA REGISTRO COMA ALMOADILLA DIRHEXA CC
                    | LDR REGISTRO COMA CA REGISTRO COMA ALMOADILLA ENTERO CC
                    | LDR REGISTRO COMA CA REGISTRO COMA ALMOADILLA ENTERONEGATIVO CC
                    | LDR REGISTRO COMA CA REGISTRO CC
                    | LDR REGISTRO COMA IGUAL ETIQUETA
                    | LDR REGISTRO COMA ETIQUETA
    '''
    global numInstruccion
    global salida
    if len(p) == 9: # Caso que todo son registros
        salida += "programa[%d] = 'ildr(pc, registros, memoria, etiq, %d, %d, %d)'\n" \
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[5]), obtenerIndice(p[7]))
                
    elif len(p) == 10 : # casos de almoadilla
        salida += "programa[%d] = 'ildr(pc, registros, memoria, etiq, %d, %d, \"%s\")'\n" \
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[5]), p[8])
    elif len(p) == 7: # caso que no hay desplazamiento
        salida += "programa[%d] = 'ildr(pc, registros, memoria, etiq, %d, %d, \"0\")'\n" \
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[5]))
    elif len(p) == 6:
        salida += "programa[%d] = 'ildr(pc, registros, memoria, etiq, %d, \"0\", \"%s\", \"=\")'\n" \
                %(numInstruccion, obtenerIndice(p[2]), p[5])
    else: # último caso
        salida += "programa[%d] = 'ildr(pc, registros, memoria, etiq, %d, \"0\", \"%s\", \"ETIQUETA\")'\n" \
                %(numInstruccion, obtenerIndice(p[2]), p[5])
    
    
    numInstruccion += 1


def p_instruccion_str(p):
    ''' instruccion : STR REGISTRO COMA CA REGISTRO COMA REGISTRO CC
                    | STR REGISTRO COMA CA REGISTRO COMA ALMOADILLA DIRHEXA CC
                    | STR REGISTRO COMA CA REGISTRO COMA ALMOADILLA ENTERO CC
                    | STR REGISTRO COMA CA REGISTRO COMA ALMOADILLA ENTERONEGATIVO CC
                    | STR REGISTRO COMA CA REGISTRO CC
                    | STR REGISTRO COMA ETIQUETA
    '''
    global numInstruccion
    global salida
    
    if len(p) == 9: # caso que todo son registros
        salida += "programa[%d] = 'istr(pc, registros, memoria, etiq, %d, %d, %d)'\n" \
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[5]), obtenerIndice(p[7]))
    elif len(p) == 10: # casos de almoadilla
        salida += "programa[%d] = 'istr(pc, registros, memoria, etiq, %d, %d, \"%s\")'\n" \
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[5]), p[8])
    elif len(p) == 7: # caso que hay dos registros
        salida += "programa[%d] = 'istr(pc, registros, memoria, etiq, %d, %d, \"0\")'\n" \
                %(numInstruccion, obtenerIndice(p[2]), obtenerIndice(p[5]))
    else: # caso que cargamos en memoria un elemento que esta en memoria
        salida += "programa[%d] = 'str(pc, registros, memoria, etiq, %d, \"0\", \"%s\", \"ETIQUETA\")'\n" \
                %(numInstruccion, obtenerIndice(p[2]), p[5])
                
    numInstruccion += 1


def p_instruccion_b(p):
    ''' instruccion : B ETIQUETA
                    | B PUNTO ENTERO
                    | B PUNTO ENTERONEGATIVO
                    | B PUNTO DIRHEXA
    '''
    global numInstruccion
    global salida
    
    if len(p) == 3:
        salida += "programa[%d] = 'ib(pc, etiq, \"%s\", \"ETIQUETA\")'\n" \
                                %(numInstruccion, p[2])
    else:
        salida += "programa[%d] = 'ib(pc, etiq, \"%s\")'\n" \
                                %(numInstruccion, p[3])
    numInstruccion += 1

def p_instruccion_beq(p):
    ''' instruccion : BEQ ETIQUETA
                    | BEQ PUNTO ENTERO
                    | BEQ PUNTO ENTERONEGATIVO
                    | BEQ PUNTO DIRHEXA
    '''
    global numInstruccion
    global salida
    
    if len(p) == 3:
        salida += "programa[%d] = 'ibeq(pc, etiq, estados, \"%s\", \"ETIQUETA\")'\n" \
                                %(numInstruccion, p[2])
    else:
        salida += "programa[%d] = 'ibeq(pc, etiq, estados, \"%s\")'\n" \
                                %(numInstruccion, p[3])
    numInstruccion += 1

def p_instruccion_bne(p):
    ''' instruccion : BNE ETIQUETA
                    | BNE PUNTO ENTERO
                    | BNE PUNTO ENTERONEGATIVO
                    | BNE PUNTO DIRHEXA
    '''
    global numInstruccion
    global salida
    
    if len(p) == 3:
        salida += "programa[%d] = 'ibne(pc, etiq, estados, \"%s\", \"ETIQUETA\")'\n" \
                                %(numInstruccion, p[2])
    else:
        salida += "programa[%d] = 'ibne(pc, etiq, estados, \"%s\")'\n" \
                                %(numInstruccion, p[3])
    numInstruccion += 1

def p_instruccion_bhi(p):
    ''' instruccion : BHI ETIQUETA
                    | BHI PUNTO ENTERO
                    | BHI PUNTO ENTERONEGATIVO
                    | BHI PUNTO DIRHEXA
    '''
    global numInstruccion
    global salida
    
    if len(p) == 3:
        salida += "programa[%d] = 'ibhi(pc, etiq, estados, \"%s\", \"ETIQUETA\")'\n" \
                                %(numInstruccion, p[2])
    else:
        salida += "programa[%d] = 'ibhi(pc, etiq, estados, \"%s\")'\n" \
                                %(numInstruccion, p[3])
    numInstruccion += 1

def p_instruccion_bls(p):
    ''' instruccion : BLS ETIQUETA
                    | BLS PUNTO ENTERO
                    | BLS PUNTO ENTERONEGATIVO
                    | BLS PUNTO DIRHEXA
    '''
    global numInstruccion
    global salida
    
    if len(p) == 3:
        salida += "programa[%d] = 'ibls(pc, etiq, estados, \"%s\", \"ETIQUETA\")'\n" \
                                %(numInstruccion, p[2])
    else:
        salida += "programa[%d] = 'ibls(pc, etiq, estados, \"%s\")'\n" \
                                %(numInstruccion, p[3])
    numInstruccion += 1

def p_instruccion_bge(p):
    ''' instruccion : BGE ETIQUETA
                    | BGE PUNTO ENTERO
                    | BGE PUNTO ENTERONEGATIVO
                    | BGE PUNTO DIRHEXA
    '''
    global numInstruccion
    global salida
    
    if len(p) == 3:
        salida += "programa[%d] = 'ibge(pc, etiq, estados, \"%s\", \"ETIQUETA\")'\n" \
                                %(numInstruccion, p[2])
    else:
        salida += "programa[%d] = 'ibge(pc, etiq, estados, \"%s\")'\n" \
                                %(numInstruccion, p[3])
    numInstruccion += 1

def p_instruccion_blt(p):
    ''' instruccion : BLT ETIQUETA
                    | BLT PUNTO ENTERO
                    | BLT PUNTO ENTERONEGATIVO
                    | BLT PUNTO DIRHEXA
    '''
    global numInstruccion
    global salida
    
    if len(p) == 3:
        salida += "programa[%d] = 'iblt(pc, etiq, estados, \"%s\", \"ETIQUETA\")'\n" \
                                %(numInstruccion, p[2])
    else:
        salida += "programa[%d] = 'iblt(pc, etiq, estados, \"%s\")'\n" \
                                %(numInstruccion, p[3])
    numInstruccion += 1

def p_instruccion_bgt(p):
    ''' instruccion : BGT ETIQUETA
                    | BGT PUNTO ENTERO
                    | BGT PUNTO ENTERONEGATIVO
                    | BGT PUNTO DIRHEXA
    '''
    global numInstruccion
    global salida
    
    if len(p) == 3:
        salida += "programa[%d] = 'ibgt(pc, etiq, estados, \"%s\", \"ETIQUETA\")'\n" \
                                %(numInstruccion, p[2])
    else:
        salida += "programa[%d] = 'ibgt(pc, etiq, estados, \"%s\")'\n" \
                                %(numInstruccion, p[3])
    numInstruccion += 1

def p_instruccion_ble(p):
    ''' instruccion : BLE ETIQUETA
                    | BLE PUNTO ENTERO
                    | BLE PUNTO ENTERONEGATIVO
                    | BLE PUNTO DIRHEXA
    '''
    global numInstruccion
    global salida
    
    if len(p) == 3:
        salida += "programa[%d] = 'ible(pc, etiq, estados, \"%s\", \"ETIQUETA\")'\n" \
                                %(numInstruccion, p[2])
    else:
        salida += "programa[%d] = 'ible(pc, etiq, estados, \"%s\")'\n" \
                                %(numInstruccion, p[3])
    numInstruccion += 1


# fin: ETIQUETA DP B PUNTO resto PUNTO END
#    | B PUNTO resto PUNTO END
#    ;





def p_fin(p):
    ''' fin : ETIQUETA DP B PUNTO resto PUNTO END
            | B PUNTO resto PUNTO END
    '''
    global salida
    global numInstruccion

    if len(p) == 8:

        salida += "etiq['%s'] = %d\n" %(p[1], numInstruccion)
        salida += "posfinal = %d\n" %numInstruccion
    else: # en caso que no haya etiqueta
        salida += "posfinal = %d\n" %numInstruccion





# resto: FL resto
#      | FL
#      ;

def p_resto(p):
    ''' resto : FL resto
              | FL
    '''
    global lineaFichero
    lineaFichero += 1

def p_error(p):
    print "Error de sintaxys en la linea %s" %(lineaFichero)



#### Fin del yacc

# Funciones auxiliares

def obtenerIndice(reg):
    reg = string.upper(reg)   # Ponemos a mayuscula para poder comparar
    if reg== 'R0':
        return 0
    elif reg == 'R1':
        return 1
    elif reg == 'R2':
        return 2
    elif reg == 'R3':
        return 3
    elif reg == 'R4':
        return 4
    elif reg == 'R5':
        return 5
    elif reg == 'R6':
        return 6
    elif reg == 'R7':
        return 7
    elif reg == 'R8':
        return 8
    elif reg == 'R9':
        return 9
    elif reg == 'R10':
        return 10
    elif reg == 'R11':
        return 11
    elif reg == 'R12':
        return 12
    elif reg == 'R13':
        return 13
    elif reg == 'R14':
        return 14
    elif reg == 'R15':
        return 15
    elif reg == 'R16':
        return 16
    elif reg == 'R17':
        return 17
    elif reg == 'R18':
        return 18
    elif reg == 'R19':
        return 19
    elif reg == 'R20':
        return 20
    elif reg == 'R21':
        return 21
    elif reg == 'R22':
        return 22
    elif reg == 'R23':
        return 23
    elif reg == 'R24':
        return 24
    elif reg == 'R25':
        return 25
    elif reg == 'R26':
        return 26
    elif reg == 'R27':
        return 27
    elif reg == 'R28':
        return 28
    elif reg == 'R29':
        return 29
    elif reg == 'R30':
        return 30
    elif reg == 'R31':
        return 31







def ficheroACadena(ficheroARM):
    salida=""
    try:
      fichero=open(ficheroARM, 'r')
      for linea in fichero:
        salida += linea

      fichero.close()
    except IOError:
      print "El fichero no existe"
    return salida



def traduccion():
    global salida   # Declaramos la variable salida como global
    salida = ""
    salida += "# -*- coding: utf-8 -*-\n"
    salida += "import string\nfrom instARM import *\n" # librerias
    
    salida += "\n" * 3 
    # inicializacion de los diccionarios
    salida += "# inicializacion de los diccionarios"
    salida += "\netiq = {}\nprograma = {}\nmemoria = {}\nregistros = {}\n"

    salida += "constantes={}\n\n"
    salida += "# inicializando el diccionario de estados\n"
    salida += "estados = initEstados()\n"
    
    # todos los registros se ponen a 0
    salida +="# todos los registros se ponen a 0\n"
    salida += "\nfor i in range(32):\n%sregistros[i]=0\n" %(ESPACIOS)

    # inicializamos el pc
    salida +="# inicializamos el pc\n"
    salida += "pc = 1\n"
    
    salida += "direc = string.atoi('0x00000000', 16)\n"


    import ply.yacc as yacc

    parser = yacc.yacc(debug=1)
    programa = ficheroACadena(sys.argv[1])
    parser.parse(programa)

    ## codigo que se traduce despues de que acabe el arbol de derivaciones

    salida += "\n\n"
    salida += "#bucle principal de evaluacion\n"
    salida += "while pc != posfinal:\n%s pc = eval(programa[pc])\n\n"\
            %(ESPACIOS)

    salida += "imprimirResultado(registros, memoria)\n"

    return salida



if __name__ == "__main__":



    if len(sys.argv) == 2:
        print traduccion()
    else:
        print "Falta pasar por argumento el fichero"
        print "Usage: %s fichero" % sys.argv[0]

