#imports-------------------------------------------------
from array import array
from math import *


#funcoes-------------------------------------------------
def calculaPulsoSismico(timeIndex,tf,fc,dt):
    time = (timeIndex*dt)-tf    
    alpha = sqrt(0.5)*pi*fc
    aux = (time*alpha)**2
    r = (1-(2*aux))*(e**(-aux))
    return r

#variaveis-----------------------------------------------
matrizVel = {}
matrizPpf = {}
matrizCpf = {}
matrizNpf = {}
listaColuna = []
listaLinha = []
fat = 1
borda = 0
bordaConta = 2
tempo = 1001
valorVel = 2000.0
linhaGera = 500
colunaGera = 500
pulsoX = (linhaGera/2)-1
pulsoY = (colunaGera/2)-1

#calculo de FAT------------------------------------------
fc = 125.0
alfa = 9.0
beta = 5.0
vmax = 2000.0
h = vmax/(alfa*fc)
dt = h/(beta*vmax)
fat = (dt*dt)/(h*h*12.0)

'''
print "h= " + str(h)
print "dt= " + str(dt)
print "fat= " + str(fat)
'''

#calculo de tf------------------------------------------
tf = (2*sqrt(pi))/fc


#gerando matriz velocidade em arquivo--------------------
criarVel = open("arquivoVel.txt","w")

for i in range(linhaGera):
    for j in range(colunaGera):
        criarVel.write(str(valorVel) + " ")
    criarVel.write("\n")
    
criarVel.close()


#salvando linhas do arquivo em lista para contabilizar linhas e colunas
vel = open("arquivoVel.txt")
listaLinha = vel.readlines()
vel.close()

#utilizado se nao for dado borda-------------------------
valorVel = 2000.0
pulsoX = (linhaGera/2)-1
pulsoY = (colunaGera/2)-1

#culculo de FAT---------
listaColuna = listaLinha[0].split(" ")
listaColuna.remove("\n")

#inicializando matrizes----------------------------------
for i in range(len(listaLinha)+(2*borda)):
    for j in range (len(listaColuna)+(2*borda)):
        matrizVel[i,j] = valorVel
        matrizPpf[i,j] = 0.0
        matrizCpf[i,j] = 0.0
        matrizNpf[i,j] = 0.0

'''
#carregando a matrizVel com o modelo de velocidade-------
for i in range(len(listaLinha)):
    #linha = listaLinha[i]
    #listaColuna = linha.split(" ")
    for j in range(len(listaColuna)):
        matrizVel[i+borda,j+borda] = float(listaColuna[j])
'''

#print "pulso sis= " + str(calculaPulsoSismico(0.0,tf,fc,dt))
#calculo de plotagem-------------------------------------
for timeIndex in range(tempo):
    matrizCpf [pulsoX,pulsoY] += calculaPulsoSismico(timeIndex,tf,fc,dt) 
   
    print "Timestep=" + str(timeIndex)
    print "Pulso Sismico= "+ str(calculaPulsoSismico(timeIndex,tf,fc,dt))
    
    for i in range(bordaConta,len(listaLinha)-bordaConta):
        for j in range(bordaConta,len(listaColuna)-bordaConta):
            matrizNpf[i,j]=2*matrizCpf[i,j]-matrizPpf[i,j]+(matrizVel[i,j]**2*fat*
                                                            (16*(matrizCpf[i,j+1]+matrizCpf[i,j-1]+matrizCpf[i+1,j]+matrizCpf[i-1,j])-1*
                                                             (matrizCpf[i,j+2]+matrizCpf[i,j-2]+matrizCpf[i+2,j]+matrizCpf[i-2,j])-60*matrizCpf[i,j]))
            
            #if (matrizNpf[i,j] != 0.0):
                #print "matrizNpf= " + str(matrizNpf[i,j])      

    matrizPpf = matrizCpf
    matrizCpf = matrizNpf
    matrizNpf = matrizPpf

    '''for i in range(0,len(listaLinha)):
        for j in range(0,len(listaColuna)):
            print str(abs(matrizCpf[i,j]))[0:3],
        print
    print'''

    #plotando em txt em 10 passos------------------------
    floatArray = array('f',[])
    
    if (timeIndex % 100 == 0):
        arqFinal = open("arquivoFinal"+str(timeIndex)+".txt","w")
        arqFinalBin = open("arquivoFinalBin"+str(timeIndex),"wb")
        for i in range(len(listaLinha)+(2*borda)):
            for j in range (len(listaColuna)+(2*borda)):
                arqFinal.write(str(matrizCpf[i,j]) + " ")
                floatArray.append(matrizCpf[i,j])
            arqFinal.write("\n")
        arqFinal.close()
        floatArray.tofile(arqFinalBin)
        arqFinalBin.close()

'''
#escrevendo matriz em arquivo----------------------------
arqFinal = open("arquivoFinal.exe","wb")

for i in range(len(listaLinha)+(2*borda)):
    for j in range (len(listaColuna)+(2*borda)):
        arqFinal.write(str(matrizCpf[i,j]) + " ")
    arqFinal.write("\n")

arqFinal.close()
'''
