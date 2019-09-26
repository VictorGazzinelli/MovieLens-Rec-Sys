# Imports

from google.colab import files
from math import sqrt

#Functions

def getListaDeFilmesAvaliadosEmComum(usu,usuSim):
  return set(filmsRatedByUser[usu]).intersection(filmsRatedByUser[usuSim])

def getListaDeUsuariosAvaliadosEmComum(film,filmSim):
  return set(usersThatRatedFilm[film]).intersection(usersThatRatedFilm[filmSim])

def getItensComunsEntreListas(list1, list2):
  return set(list1).intersection(list2)

def getDistEuclidianaFilme(filmeOrigem,filmeFim):
  soma = 0
  usuariosAvaliados = getListaDeUsuariosAvaliadosEmComum(filmeOrigem,filmeFim)
  if(not usuariosAvaliados): return 0
  for userId in usuariosAvaliados:
    notaFilOri = userRating[userId][filmeOrigem]
    notaFilFim = userRating[userId][filmeFim]
    soma += pow((notaFilOri-notaFilFim),2)
  return 1/(1+sqrt(soma))

def getDistEuclidianaUsuario(usuarioOrigem,usuarioFim):  
  soma = 0
  filmsSeen = getListaDeFilmesAvaliadosEmComum(usuarioOrigem,usuarioFim)
  if(not filmsSeen): return 0
  for filmId in filmsSeen:
    notaUsuOri = userRating[usuarioOrigem][filmId]
    notaUsuFim = userRating[usuarioFim][filmId]
    soma += pow((notaUsuOri-notaUsuFim),2)
  return 1/(1+sqrt(soma))

def getEucFilmesSimilares(filme, k):
  similaridade = [(getDistEuclidianaFilme(filme, outro), outro)
                  for outro in range(len(userRating[0])) if outro != filme] 
  similaridade.sort()
  similaridade.reverse() 
  return similaridade[0:k] 

def getEucUsuariosSimilares(usuario, k):
  similaridade = [(getDistEuclidianaUsuario(usuario, outro), outro)
                  for outro in range(len(userRating)) if outro != usuario] 
  similaridade.sort()
  similaridade.reverse() 
  return similaridade[0:k] 

def getMediaDeNotasFilmeGeral(film):
  soma = 0
  for userId in usersThatRatedFilm[film]:
    soma += userRating[userId][film]
  return ( float(soma)/ len(usersThatRatedFilm[film]) )

def getMediaDeNotasUsuarioGeral(usu):
  soma = 0
  for filmId in filmsRatedByUser[usu]:
    soma += userRating[usu][filmId]
  return ( float(soma)/ len(filmsRatedByUser[usu]) )

def getMediaDeNotasFilme(film, usuariosEmComum):
  soma = 0
  for userId in usuariosEmComum:
    soma += userRating[userId][film]
  return ( float(soma)/ len(usuariosEmComum) )

def getMediaDeNotasUsuario(usu, filmesEmComum):
  soma = 0
  for filmId in filmesEmComum:
    soma += userRating[usu][filmId]
  return ( float(soma)/ len(filmesEmComum) )

def getDesvioPadraoFilmeGeral(fil):
  soma = 0
  media = getMediaDeNotasFilmeGeral(fil)
  for userId in usersThatRatedFilm[fil]:
    soma += pow((userRating[userId][fil] - media), 2)
  return sqrt(float(soma))

def getDesvioPadraoUsuarioGeral(usu):
  soma = 0
  media = getMediaDeNotasUsuarioGeral(usu)
  for filmId in filmsRatedByUser[usu]:
    soma += pow((userRating[usu][filmId] - media), 2)
  return sqrt(float(soma))

def getDesvioPadraoFilme(fil, usuariosEmComum):
  soma = 0
  media = getMediaDeNotasFilme(fil, usuariosEmComum)
  for userId in usuariosEmComum:
    soma += pow((userRating[userId][fil] - media), 2)
  return sqrt(float(soma))

def getDesvioPadraoUsuario(usu, filmesEmComum):
  soma = 0
  media = getMediaDeNotasUsuario(usu, filmesEmComum)
  for filmId in filmesEmComum:
    soma += pow((userRating[usu][filmId] - media), 2)
  return sqrt(float(soma))

def getDistPearsonFilme(filOri,filDes):
  soma = 0
  usuariosEmComum = getListaDeUsuariosAvaliadosEmComum(filOri,filDes)
  if(not usuariosEmComum): return 0
  medFilOri = getMediaDeNotasFilme(filOri, usuariosEmComum)
  medFilDes = getMediaDeNotasFilme(filDes, usuariosEmComum)
  desPadOri = getDesvioPadraoFilme(filOri, usuariosEmComum)
  desPadDes = getDesvioPadraoFilme(filDes, usuariosEmComum)
  for userId in usuariosEmComum:
    soma += ( (float(userRating[userId][filOri]) - medFilOri) * (float(userRating[userId][filDes]) - medFilDes) )
  return( float(soma)/(1+( (desPadOri) * (desPadDes)  ) ))

def getDistPearsonUsuario(usuOri,usuDes):
  soma = 0
  filmesEmComum = getListaDeFilmesAvaliadosEmComum(usuOri,usuDes)
  if(not filmesEmComum): return 0
  medUsuOri = getMediaDeNotasUsuario(usuOri, filmesEmComum)
  medUsuDes = getMediaDeNotasUsuario(usuDes, filmesEmComum)
  desPadOri = getDesvioPadraoUsuario(usuOri, filmesEmComum)
  desPadDes = getDesvioPadraoUsuario(usuDes, filmesEmComum)
  for filmId in filmesEmComum:
    soma += ( (float(userRating[usuOri][filmId]) - medUsuOri) * (float(userRating[usuDes][filmId]) - medUsuDes) )
  return( float(soma)/(1+( (desPadOri) * (desPadDes)  ) ) )


def getPeaFilmesSimilares(fil, k):
  similaridade = []
  for outro in range(len(userRating[0])):
    usuariosEmComum = getListaDeUsuariosAvaliadosEmComum(fil,outro)
    if(outro == 0 or outro == fil): continue
    similaridade.append((getDistPearsonFilme(fil, outro), outro))
  similaridade.sort()
  similaridade.reverse() 
  return similaridade[0:k] 

def getPeaUsuariosSimilares(usu, k):
  similaridade = []
  for outro in range(len(userRating)):
    filmesEmComum = getListaDeFilmesAvaliadosEmComum(usu,outro)
    if(outro == 0 or outro == usu): continue
    similaridade.append((getDistPearsonUsuario(usu, outro), outro))
  similaridade.sort()
  similaridade.reverse() 
  return similaridade[0:k] 

def getEucRecomendacoesUsuario(usuario):
    totais={}
    somaSimilaridade={}
    for userId in range(len(userRating)):
        if userId == usuario: continue
        similaridade = getDistEuclidianaUsuario(usuario, userId)
        if similaridade <= 0: continue 
        for filmId in filmsRatedByUser[userId]:
            if userRating[usuario][filmId] == 0 : 
                totais.setdefault(filmId, 0)
                totais[filmId] += userRating[userId][filmId] * similaridade
                somaSimilaridade.setdefault(filmId, 0)
                somaSimilaridade[filmId] += similaridade
    rankings=[(total / somaSimilaridade[filmId], filmId) for filmId, total in totais.items()]
    rankings.sort()
    rankings.reverse() 
    return rankings

def getEucRecomendacoesFilme(filme):
    totais={}
    somaSimilaridade={}
    for filmId in range(len(userRating[0])):
        if filmId == filme: continue
        similaridade = getDistEuclidianaFilme(filme, filmId)
        if similaridade <= 0: continue 
        for userId in usersThatRatedFilm[filmId]:
            if userRating[userId][filme] == 0 : 
                totais.setdefault(userId, 0)
                totais[userId] += userRating[userId][filmId] * similaridade
                somaSimilaridade.setdefault(userId, 0)
                somaSimilaridade[userId] += similaridade
    rankings=[(total / somaSimilaridade[userId], userId) for userId, total in totais.items()]
    rankings.sort()
    rankings.reverse() 
    return rankings
  
def getPearsonRecomendacoesUsuario(usuario):
    totais={}
    somaSimilaridade={}
    for userId in range(len(userRating)):
        if userId == usuario: continue
        similaridade = getDistPearsonUsuario(usuario, userId)
        if similaridade <= 0: continue 
        for filmId in filmsRatedByUser[userId]:
            if userRating[usuario][filmId] == 0 : 
                totais.setdefault(filmId, 0)
                totais[filmId] += userRating[userId][filmId] * similaridade
                somaSimilaridade.setdefault(filmId, 0)
                somaSimilaridade[filmId] += similaridade
    rankings=[(total / somaSimilaridade[filmId], filmId) for filmId, total in totais.items()]
    rankings.sort()
    rankings.reverse() 
    return rankings

def getPearsonRecomendacoesFilme(filme):
    totais={}
    somaSimilaridade={}
    for filmId in range(len(userRating[0])):
        if filmId == filme: continue
        similaridade = getDistPearsonFilme(filme, filmId)
        if similaridade <= 0: continue 
        for userId in usersThatRatedFilm[filmId]:
            if userRating[userId][filme] == 0 : 
                totais.setdefault(userId, 0)
                totais[userId] += userRating[userId][filmId] * similaridade
                somaSimilaridade.setdefault(userId, 0)
                somaSimilaridade[userId] += similaridade
    rankings=[(total / somaSimilaridade[userId], userId) for userId, total in totais.items()]
    rankings.sort()
    rankings.reverse() 
    return rankings

def getNotaPrevistaEucUsuario(usuario,filme):
    total = 0
    somaSimilaridade = 0
    for userId in range(len(userRating)):
        if userId == 0 or userId == usuario: continue
        similaridade = getDistEuclidianaUsuario(usuario, userId)
        if similaridade <= 0: continue 
        if userRating[userId][filme] == 0 : continue
        total += userRating[userId][filme] * similaridade
        somaSimilaridade += similaridade
    if(somaSimilaridade == 0):
      return -1.00 # coldStart
    ranking=(total / somaSimilaridade)
    return ranking

def getNotaPrevistaEucFilme(filme,usuario):
  total = 0
  somaSimilaridade = 0
  for filmId in range(len(userRating[0])):
    if filmId == 0 or filmId == filme: continue
    similaridade = getDistEuclidianaFilme(filme, filmId)
    if similaridade <= 0: continue 
    if userRating[usuario][filmId] == 0 : continue
    total += userRating[usuario][filmId] * similaridade
    somaSimilaridade += similaridade
  if(somaSimilaridade == 0):
      return -1.00 # coldStart
  ranking=(total / somaSimilaridade)
  return ranking

def getNotaPrevistaPeaUsuario(usuario,filme):
  total = 0
  somaSimilaridade = 0
  for userId in range(len(userRating)):
    if userId == 0 or userId == usuario: continue
    similaridade = getDistPearsonUsuario(usuario, userId)
    if similaridade <= 0: continue 
    if userRating[userId][filme] == 0 : continue
    total += userRating[userId][filme] * similaridade
    somaSimilaridade += similaridade
  if(somaSimilaridade == 0):
      return -1.00 # coldStart
  ranking=(total / somaSimilaridade)
  return ranking

def getNotaPrevistaPeaFilme(filme,usuario):
  total = 0
  somaSimilaridade = 0
  for filmId in range(len(userRating[0])):
    if filmId == 0 or filmId == filme: continue
    similaridade = getDistPearsonFilme(filme, filmId)
    if similaridade <= 0: continue 
    if userRating[usuario][filmId] == 0 : continue
    total += userRating[usuario][filmId] * similaridade
    somaSimilaridade += similaridade
  if(somaSimilaridade == 0):
      return -1.00 # coldStart
  ranking=(total / somaSimilaridade)
  return ranking

# Upload de arquivos de treino e teste 
!rm /content/*

# Fazer o upload do arquivo de treino
uploaded = files.upload() # Upload Do Arquivo de Entrada

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))
  trainFilePath = '/content/' + fn # Nome do Diretorio orgiem do documento com a base de dados

# Fazer o upload do arquivo de teste
uploaded = files.upload() # Upload Do Arquivo de Entrada

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))
  testFilePath = '/content/' + fn # Nome do Diretorio orgiem do documento com a base de dados

# Metadados dos arquivos
#baseLocation = testFilePath
baseLocation = trainFilePath
lastUserId, lastFilmId = 0, 0
filmsRated = {}
for linha in open(baseLocation):
  content = linha.split('\t')[0:3] # Separacao do conteudo em idUsu,idFil e nota
  idUsu = int(content[0])
  idFil = int(content[1])
  nota = int(content[2])
  if(idFil not in filmsRated.keys()):
    filmsRated[idFil] = 1
  if(idUsu > lastUserId):
    lastUserId = idUsu
  if(idFil > lastFilmId):
    lastFilmId = idFil
numTotalUsu = lastUserId
numTotalFil = lastFilmId
print("Numero Total de Usuarios : %d"%(lastUserId))
print("Numero Total de Filmes : %d"%(lastFilmId))
print("Numero Total de Filmes Avaliados : %d"%(len(filmsRated)))

# Modelagem das Estruturas de Dados
userRating = [[0 for x in range(numTotalFil+1)] for y in range(numTotalUsu+1)] # uma matriz usuarioxFilme com a nota e com index inicial = 1
filmsRatedByUser = [ [] for x in range(numTotalUsu+1)] # Vetor com todos os filmes avaliados pra cada usuario com index inicial = 1
usersThatRatedFilm = [ [] for x in range(numTotalFil+1)] # Vetor com todos os usuarios que avaliaram o filme com index inicial = 1
for linha in open(trainFilePath):
  (idUsu, idFil, nota) = linha.split()[0:3]
  idUsu, idFil , nota = int(idUsu), int(idFil), int(nota)
  userRating[idUsu][idFil] = nota
  filmsRatedByUser[idUsu].append(idFil)
  usersThatRatedFilm[idFil].append(idUsu)

# Testes
#print(getListaDeFilmesAvaliadosEmComum(1,2))
#print(getListaDeUsuariosAvaliadosEmComum(3,4))
#print(getDistEuclidianaFilme(1,2))
#print(getDistEuclidianaUsuario(3,4))
#print(getEucFilmesSimilares(1,5))
#print(getEucUsuariosSimilares(3,5))
#print(getMediaDeNotasFilmeGeral(1))
#print(getMediaDeNotasUsuarioGeral(3))
#print(getDesvioPadraoFilmeGeral(1))
#print(getDesvioPadraoUsuarioGeral(3))
#filmesEmComum = getListaDeFilmesAvaliadosEmComum(1,2)
#usuariosEmComum = getListaDeUsuariosAvaliadosEmComum(3,4)
#print(getMediaDeNotasFilme(1,usuariosEmComum))
#print(getMediaDeNotasUsuario(3,filmesEmComum))
#print(getDesvioPadraoFilme(1,usuariosEmComum))
#print(getDesvioPadraoUsuario(3,filmesEmComum))
#print(getDistPearsonFilme(1,2))
#print(getDistPearsonUsuario(3,4))
#print(getPeaFilmesSimilares(1,5))
#print(getPeaUsuariosSimilares(3,5))
#print(getEucRecomendacoesFilme(1)[0:5])
#print(getPearsonRecomendacoesFilme(1)[0:5])
#print(getEucRecomendacoesUsuario(3)[0:5])
#print(getPearsonRecomendacoesUsuario(3)[0:5])
#print(getNotaPrevistaEucFilme(1,849))
#print(getNotaPrevistaPeaFilme(1,688))
#print(getNotaPrevistaEucUsuario(3,1653))
#print(getNotaPrevistaPeaUsuario(3,1643))

