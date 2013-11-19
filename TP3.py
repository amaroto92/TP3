##prueba
##ejemplo
##ver_exp_let(["val","x","=","if","True","then","2","else","3","val","y","=","True","val","z","=","[1,2,3,4,5]","val","A","=","if","x<3","then","[True,False,True,False]","else","0"])
print
print("   Bienvenido al analizador de ambientes Estaticos y Dinamicos")

global LE
LE=[]

def Inicio():
	print
	NombreArchivo=raw_input("Ingrese el nombre del archivo que desea analizar: ")
	return LeerArchivo(NombreArchivo)

def LeerArchivo(NombreArchivo):
	Archivo=open(NombreArchivo,"r")
	Lineas=Archivo.read()
	Archivo.close()
	return Analizador(Lineas)

def Analizador(Lineas): # Aca es donde se empieza a buscar y analizar las variables

		X=Lineas.replace("\n"," ")
		X=X.replace("\t"," ")		
		X=X.replace("  "," ")		
		X=X.split(" ")
		LE=X[1:-1]
		return ver_exp_let(LE)


global nivel
nivel=0
global variable
global valor
global tipo

global listaDINAMICO
global listaESTATICO
global lista
global listaNumeros
global listaBool
listaDINAMICO=[]
listaESTATICO=[]
lista=[]
listaNumeros=('1','2','3','4','5','6','7','8','9','0')
listaBool=("True","False")

def imprimir(ld,le):
    print('\n'+'\t'+'TABLA DINAMICA')
    for i in range(0,len(ld)):
        print('\t'+ld[i][0]+'\t'+ld[i][1])
        
    print('\n'+'\t'+'TABLA ESTATICA')
    for i in range(0,len(le)):
        print('\t'+le[i][0]+'\t'+le[i][1])
    print('\n',lista)

def ver_exp_let(LE):
    if LE==[]:
        return imprimir(listaDINAMICO,listaESTATICO)
    elif LE[0].lower()=="let":
        nivel+=1
        return ver_exp_val(LE[1:])
    elif LE[0].lower()=="val":
        return ver_exp_var(LE[1:])
    elif LE[0].lower()=="end":
        nivel-=1
        return ver_exp_var(LE[1:])
    else:
        return ver_exp_let(LE[1:])


def ver_exp_let_aux(LE):
    var=LE[0]
    valor=LE[2]
    lugarIN=0
    lugarEND=0
    listaELEMENTOS.append([var,valor])
    for i in range(3,len(LE)):
        if LE[i]=="in":
            lugarIN=i
            break
    for i in range(lugarIN,len(LE)):
        if LE[i]=="end":
            lugarEND=i
            break

def ver_exp_val(LE):
    if LE[0].lower()=="val":
        return ver_exp_var(LE[1:])
    else:
        return ver_exp_let((LE[1:]))


def ver_exp_var(LE):
    var=LE[0]
    
    if LE[2].lower()=="if":
        lugarIF=2
        lugarTHEN=0
        for i in range(lugarIF+1,len(LE)):
            if LE[i]=="then":
                lugarTHEN=i
                break
        if resuelveIF(LE[3:lugarTHEN],var,0):
            valor=LE[lugarTHEN+1]
            agregarD(var,valor)
            agregarE(var,valor)
            lista.append([var,valor,nivel])
            return ver_exp_let(LE[lugarTHEN+4:])
        else:
            valor=LE[lugarTHEN+3]
            agregarD(var,valor)
            agregarE(var,valor)
            lista.append([var,valor,nivel])
            return ver_exp_let(LE[lugarTHEN+4:])

    else:
        if len(LE[2])==1:
            if (LE[2]  in listaNumeros):
                valor=LE[2]
                agregarD(var,valor)
                agregarE(var,valor)
                lista.append([var,valor,nivel])
                return ver_exp_let(LE[3:])
            else:
                valor=val_en_if(lista,LE[2],nivel)
                agregarD(var,valor)
                agregarE(var,valor)
                lista.append([var,valor,nivel])
                return ver_exp_let(LE[3:])

        elif len(LE[2])!=1:
            if LE[2][0]==("[" or "("):
                valor=LE[2]
                agregarD(var,valor)
                agregarE(var,valor)
                lista.append([var,valor,nivel])
                return ver_exp_let(LE[3:])
            elif (LE[2][0] in listaNumeros) or (LE[2][0] in listaBool):
                valor=LE[2]
                agregarD(var,valor)
                agregarE(var,valor)
                lista.append([var,valor,nivel])
                return ver_exp_let(LE[3:])
            elif (LE[2] in listaNumeros) or (LE[2] in listaBool):
                valor=LE[2]
                agregarD(var,valor)
                agregarE(var,valor)
                lista.append([var,valor,nivel])
                return ver_exp_let(LE[3:])
            else:
                valor=val_en_if(lista,LE[2],nivel)
                agregarD(var,valor)
                agregarE(var,valor)
                lista.append([var,valor,nivel])
                return ver_exp_let(LE[3:])


def resuelveIF(LE,var,nivel):
    if LE[0]=="True":
        return True
    
    elif LE[0]=="False":
        return False
    
    elif len(LE[0])==1:
        return eval(val_en_if(lista,LE[0],nivel))
    
    elif len(LE[0])==3:
        return eval(val_en_if(lista,LE[0][0],nivel)+LE[0][1]+LE[0][2])
    
    elif len(LE[0])==4:
        return eval((val_en_if(lista,LE[0][0],nivel))+LE[0][1]+LE[0][2]+LE[0][3])


def agregarE(var,valor):
    listaESTATICO.append([var,averiguarTIPO(valor)])

    
def agregarD(var,valor):
    listaDINAMICO.append([var,valor])

   
def averiguarTIPO(elemento):
    if isinstance(eval(elemento),bool):
        return ('bool')
    elif isinstance(eval(elemento),int):
        return ('int')
    elif isinstance(eval(elemento),list):
        return averiguarTIPO(str(eval(elemento)[0]))+' list'
    elif isinstance(eval(elemento),tuple):
        return TipoDatoTupla(eval(elemento))


def TipoDatoTupla(tupla):
    Tipo = "("
    print(Tipo)
    for i in range(0,len(tupla)):
        if i==len(tupla)-1:
            Tipo+=(averiguarTIPO(str(tupla[i])))
        else:
            Tipo+=(averiguarTIPO(str(tupla[i])))+"*"
    return Tipo+")"


def val_en_if(listaVals,elem_comp, nivel):
    print(listaVals)
    temp = (len(listaVals)-1)
    bandera = False
    while (bandera!=True):
        if (listaVals[temp][0] == elem_comp) and (listaVals[temp][2] == nivel):
            bandera = True
            return listaVals[temp][1]
        else:
            temp -= 1
    return True



    
Inicio()
