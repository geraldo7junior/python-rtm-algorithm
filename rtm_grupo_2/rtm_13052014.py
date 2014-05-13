'''
############################################################
UFRPE - BSI
Topicos em ambientes computacionais de alto desempenho
Start do algoritmo RTM
Alunos:
Geraldo Gomes da Cruz Junior;
Larissa Karollyne de Melo Ferreira;
Rafaella Leandra Souza do Nascimento.
#############################################################
'''
print "Calculo para o algoritmo RTM"

#Matrizes
vel = {}
ppf = {}
cpf = {}
npf = {}
lista_npf = []

#Inserir tamanho da matriz
i=input ("Informe o numero de linhas da matriz: ")
j=input ("Informe o numero de colunas da matriz: ")

#Inserir quantidade de intecoes do algoritmo
iteracoes=input ("Informe a quantidade de iteracoes do algoritmo: ")

#Fixando valores da matriz inicial
linha = i
coluna = j

#Pegando posicao central de uma matriz quadrada
centro = (i-1)/2

#Preenchendo as matrizes - Matriz de i linhas e j colunas
for a  in range(0,i):
    for b in range(0,j):
        vel[(a,b)] = 2000.0
        ppf[(a,b)]=0.0
        cpf[(a,b)]=0.0
        npf[(a,b)]=0.0

#Pegando o tamanho da matriz
tamanho = len(vel)

#Calculando para o FAT 
FC = 125.0
ALPHA = 9.0
BETA = 5.0
VMAX = 2000.0
H = VMAX/(ALPHA*FC)
DT = H/(BETA*VMAX)
FAT = (DT*DT)/(H*H*12.0)

#Calculando TF
from math import exp, sqrt, pi
TF = (2*sqrt(pi))/FC

#Contador
iteracao = 0.0

#Funcao Pulso Sismico
def calculaPulsoSismico(iteracao, FC, DT,TF):
    time = (iteracao*DT)-TF
    alpha = sqrt(0.5) * pi * FC
    aux = (time*alpha)**2.0
    r = (1.0-(2.0*aux))*exp(-aux)
    return r

#Laco para cada iteracao de tempo(matriz completa) - Informar numero de iteracoes
for passo_tempo in range(0,iteracoes):    

    explo = calculaPulsoSismico(iteracao,FC,DT,TF)
    cpf[(centro,centro)] += explo

#Laco para correr as matrizes considerando as posicoes validas para o calculo 
    for i in range(linha-4):
        for j in range (coluna-4):
                    
                a = i+2
                b = j+2

#Condicao para nao estourar a matriz
                if (a+2 < linha-1) and (b+2 < coluna-1):

#Gambi para deixar a equacao pequena - Jogando as posicoes das matrizes em variaveis       
                    cpfa = cpf[(a,b)]
                    ppfa = ppf[(a,b)]
                    vela = vel[(a,b)]

                    cpfb = cpf[(a,b+1)]
                    cpfc = cpf[(a,b-1)]
                    cpfd = cpf[(a+1,b)]
                    cpfe = cpf[(a-1,b)]

                    cpff = cpf[(a,b+2)]
                    cpfg = cpf[(a,b-2)]
                    cpfh = cpf[(a+2,b)]
                    cpfi = cpf[(a-2,b)]

#Equacao para calcular uma posicao na matriz NPF
                    resposta = 2*cpfa-ppfa+((vela*vela*FAT)*((16 * (cpfb + cpfc + cpfd+ cpfe)) -1*(cpff + cpfg + cpfh + cpfi) - 60 * cpfa))                
                    npf[(a,b)] = resposta
#Manha para printar sem os zeros, so para comparacao
                   # if npf[(a,b)] != 0.0:
                    lista_npf.append(npf[(a,b)])      
    
#salvando binario em arquivo
    from array import array
    output_file = open('npf.bin', 'wb')
    float_array = array('f', lista_npf)
    float_array.tofile(output_file)
    output_file.close()

#salvando no txt
    saida_float = open('npf.txt', 'a')
    for i in lista_npf:
            saida_float.write('\n'+str(i))
    saida_float.write("\n")
    saida_float.close()

#Para printar as matrizes 
#    for i in range (0,linha):
#        for j in range (0,coluna):
#            print npf[(i,j)],
#        print
#    print

#Transicao dos valores das matrizes para um novo Passo de tempo       
    ppf = cpf
    cpf = npf
    npf = ppf
        

#Zerando a npf para a nova iteracao       
#    for a in range(0,linha):
#        for b in range(0,coluna):
#            npf[(a,b)]=0.0
            
#Incremento para a nova iteracao                        
    iteracao += 1.0
    lista_npf = []

    


   


  





