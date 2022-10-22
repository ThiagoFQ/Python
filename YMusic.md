# Y.Music

# Índice <a id='back'></a>

* [Introdução](#intro) 
* [Etapa 1. Visão geral dos dados](#data_review)
    * [Conclusões](#data_review_conclusions)
* [Etapa 2. Pré-processamento de dados](#data_preprocessing)
    * [2.1 Estilo do cabeçalho](#header_style)
    * [2.2 Valores ausentes](#missing_values)
    * [2.3 Duplicatas](#duplicates)
    * [2.4 Conclusões](#data_preprocessing_conclusions)
* [Etapa 3. Testando as hipóteses](#hypotheses)
    * [3.1 Hipótese 1: comparando o comportamento dos usuários em duas cidades](#activity)
    * [3.2 Hipótese 2: música no começo e no fim da semana](#week)
    * [3.3 Hipótese 3: preferências em Springfield e Shelbyville](#genre)
* [Conclusões](#end)

## Introdução <a id='intro'></a>
Quando fala-se em _Data Science_ é inevitável falar em Python, já que um dos focos principais do campo da Ciência de Dados é a conversão desses dados em informações significativas que agreguem valor para negócios. A linguagem de programação Python é a tecnologia mais popular e fácil de usar entre as ferramentas disponíveis para análise de dados.

Nesse sentido, trago pra vocês um projeto desenvolvido por mim, que demonstra meu avanço inicial no aprendizado da linguagem de programação em Python.

Esse projeto visa comparar as preferências musicais dos habitantes Springfield (Oregon, EUA) e Shelbyville (Indiana, EUA). São dados reais da aplicação [Y.Music](https://ymusic.io/) e atemporais — a base de dados foi cedida pela Practicum sem informação de data de ocorrência.

Os principais objetivos, descritos adiante, direcionam à formulação de hipóteses que levam a comparar o comportamento dos usuários da aplicação nas duas cidades estadunidenses. Vale ressaltar que algumas hipóteses podem ser aceitas, e outras podem ser rejeitadas. Pois na ótica dos negócios, para se fazer as escolhas certas, deve-se ser capaz de entender se estamos fazendo as suposições certas. 

Reforço que esse projeto inicial está focado na manipulação dos dados através da biblioteca `pandas` e verificação dessas informações com os objetivos propostos, não chega por si, a ser considerado uma _EDA_ — Análise Exploratória de Dados. Além das hipóteses aqui mencionadas não se referirem aos testes de hipóteses sobre a ótica da análise estatística de dados.

### Objetivo: 
Para cumprir os objetivos centrais desse projeto, vamos analisar as seguintes hipótese:
1. A atividade dos usuários é diferente dependendo do dia da semana e da cidade.
2. Durante as manhãs de segunda-feira, os moradores de Springfield e Shelbyville escutam diferentes gêneros. Isso também é verdadeiro para noites de sexta-feira.
3. Os ouvintes de Springfield e Shelbyville têm diferentes preferências. Em Springfield, as pessoas preferem pop, enquanto Shelbyville tem mais fãs de rap.

### Etapas 
Os dados sobre o comportamento dos usuários estão armazenados no arquivo _music_project_en.csv_. Como não há informação sobre a qualidade dos dados, é preciso examiná-los antes de testar as hipóteses.

Primeiro, é preciso verificar a qualidade dos dados, ver se existem problemas e, se existirem, verificar se esses problemas são realmente significativos para o teste das hipóteses. Depois, durante o pré-processamento de dados, é preciso tratar os problemas mais críticos que surgirem.
 
O projeto consiste de três etapas:
 1. Visão geral dos dados  
 2. Pré-processamento de dados  
 3. Testando hipóteses  
 
[Voltar ao Índice](#back)

## Etapa 1. Visão geral dos dados <a id='data_review'></a>

O primeiro passo é abrir a base de dados do Y.Music e explorar através da biblioteca `pandas`.


```python
# Importando a biblioteca pandas
import pandas as pd 
```

Criar um DataFrame com o arquivo `music_project_en.csv` da pasta `/datasets/` e salvar na variável `df`:


```python
# lendo o arquivo e armazenando em df
df = pd.read_csv('/datasets/music_project_en.csv') 
display(df.describe())
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>userID</th>
      <th>Track</th>
      <th>artist</th>
      <th>genre</th>
      <th>City</th>
      <th>time</th>
      <th>Day</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>65079</td>
      <td>63736</td>
      <td>57512</td>
      <td>63881</td>
      <td>65079</td>
      <td>65079</td>
      <td>65079</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>41748</td>
      <td>39666</td>
      <td>37806</td>
      <td>268</td>
      <td>2</td>
      <td>20392</td>
      <td>3</td>
    </tr>
    <tr>
      <th>top</th>
      <td>A8AE9169</td>
      <td>Brand</td>
      <td>Kartvelli</td>
      <td>pop</td>
      <td>Springfield</td>
      <td>08:14:07</td>
      <td>Friday</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>76</td>
      <td>136</td>
      <td>136</td>
      <td>8850</td>
      <td>45360</td>
      <td>14</td>
      <td>23149</td>
    </tr>
  </tbody>
</table>
</div>


É importante exibir as primeiras linhas da tabela para ter uma noção inicial dos dados a se trabalhar:


```python
# obtenha as 10 primeiras linhas da tabela df
display(df.head(10)) 
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>userID</th>
      <th>Track</th>
      <th>artist</th>
      <th>genre</th>
      <th>City</th>
      <th>time</th>
      <th>Day</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>FFB692EC</td>
      <td>Kamigata To Boots</td>
      <td>The Mass Missile</td>
      <td>rock</td>
      <td>Shelbyville</td>
      <td>20:28:33</td>
      <td>Wednesday</td>
    </tr>
    <tr>
      <th>1</th>
      <td>55204538</td>
      <td>Delayed Because of Accident</td>
      <td>Andreas Rönnberg</td>
      <td>rock</td>
      <td>Springfield</td>
      <td>14:07:09</td>
      <td>Friday</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20EC38</td>
      <td>Funiculì funiculà</td>
      <td>Mario Lanza</td>
      <td>pop</td>
      <td>Shelbyville</td>
      <td>20:58:07</td>
      <td>Wednesday</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A3DD03C9</td>
      <td>Dragons in the Sunset</td>
      <td>Fire + Ice</td>
      <td>folk</td>
      <td>Shelbyville</td>
      <td>08:37:09</td>
      <td>Monday</td>
    </tr>
    <tr>
      <th>4</th>
      <td>E2DC1FAE</td>
      <td>Soul People</td>
      <td>Space Echo</td>
      <td>dance</td>
      <td>Springfield</td>
      <td>08:34:34</td>
      <td>Monday</td>
    </tr>
    <tr>
      <th>5</th>
      <td>842029A1</td>
      <td>Chains</td>
      <td>Obladaet</td>
      <td>rusrap</td>
      <td>Shelbyville</td>
      <td>13:09:41</td>
      <td>Friday</td>
    </tr>
    <tr>
      <th>6</th>
      <td>4CB90AA5</td>
      <td>True</td>
      <td>Roman Messer</td>
      <td>dance</td>
      <td>Springfield</td>
      <td>13:00:07</td>
      <td>Wednesday</td>
    </tr>
    <tr>
      <th>7</th>
      <td>F03E1C1F</td>
      <td>Feeling This Way</td>
      <td>Polina Griffith</td>
      <td>dance</td>
      <td>Springfield</td>
      <td>20:47:49</td>
      <td>Wednesday</td>
    </tr>
    <tr>
      <th>8</th>
      <td>8FA1D3BE</td>
      <td>L’estate</td>
      <td>Julia Dalia</td>
      <td>ruspop</td>
      <td>Springfield</td>
      <td>09:17:40</td>
      <td>Friday</td>
    </tr>
    <tr>
      <th>9</th>
      <td>E772D5C0</td>
      <td>Pessimist</td>
      <td>NaN</td>
      <td>dance</td>
      <td>Shelbyville</td>
      <td>21:20:49</td>
      <td>Wednesday</td>
    </tr>
  </tbody>
</table>
</div>


A função `.info()` nos traz as informações gerais sobre a tabela:


```python
# obtendo informações gerais sobre os dados em df
print(df.info()) 
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 65079 entries, 0 to 65078
    Data columns (total 7 columns):
     #   Column    Non-Null Count  Dtype 
    ---  ------    --------------  ----- 
     0     userID  65079 non-null  object
     1   Track     63736 non-null  object
     2   artist    57512 non-null  object
     3   genre     63881 non-null  object
     4     City    65079 non-null  object
     5   time      65079 non-null  object
     6   Day       65079 non-null  object
    dtypes: object(7)
    memory usage: 3.5+ MB
    None


Agora sabemos que a tabela contém sete colunas. Elas armazenam o mesmo tipo de dados: objetos.

De acordo com a documentação, temos:
- `'userID'` — identificação do usuário
- `'Track'` — título da música
- `'artist'` — nome do artista
- `'genre'` — o gênero
- `'City'` — cidade do usuário
- `'time'` — tempo exato que a música foi tocada
- `'Day'` — dia da semana 

Nós podemos ver três problemas com o estilo nos nomes das colunas:
1. Alguns nomes estão com letra maiúscula, alguns com letra minúscula.
2. Há espaços em alguns nomes.
3. Coluna com mais de um nome sem estar no estilo snake_case.

Outro ponto a se observar é que a quantidade de valores das colunas é diferente. Isso significa que os dados contém valores ausentes. Vamos verificar mais adiante.


### Conclusões <a id='data_review_conclusions'></a> 

Cada linha na tabela armazena dados sobre uma música que foi tocada em um determinado horário por um usuário em uma das duas cidades. Algumas colunas descrevem as informações sobre a música: seu título, artista e gênero. Outras colunas contém informações sobre os usuários: a cidade de onde eles moram, a quantidade de vezes que a música foi tocada. O restante revela o horário e o dia da semana em que foram tocadas por esses usuários da aplicação.

Está claro que os dados são suficientes para testar as hipóteses. Entretanto, há valores ausentes que precisam ser tratados. Além dos nomes das colunas estarem em formatação indevida, que acaba por prejudicar as chamadas e manipulação dos dados.

Para seguir adiante, precisamos pré-processar esses dados.

[Voltar ao Índice](#back)

## Etapa 2. Pré-processar dados <a id='data_preprocessing'></a>
Corrigir a formatação no cabeçalho da coluna e tratar os valores ausentes é essencial nesse primeiro momento. A seguir, verificar a existência de dados duplicados e, caso existam, removê-los.

### Estilo do cabeçalho <a id='header_style'></a>
Exibir o cabeçalho da coluna:


```python
# a lista dos nomes das colunas na tabela df
print(df.columns) 
```

    Index(['  userID', 'Track', 'artist', 'genre', '  City  ', 'time', 'Day'], dtype='object')


As boas práticas de estilo ajudam no tratamento e visualização dos dados, os nomes das colunas estão ferindo essas práticas nos seguintes aspectos:
* O nome contém várias palavras e não está no estilo _snake case_ (user_id).
* Vários nomes com letras maísculas, os caracteres precisam estar com letras minúsculas (track, city, day).
* Deve-se remover os espaços contidos nos nomes das colunas.


```python
# renomeando colunas
df = df.rename(columns ={
    '  userID': 'user_id',
    'Track': 'track',
    '  City  ': 'city',
    'Day': 'day'
}) 
```

Após renomear as colunas, verifica-se o resultado exibindo os nomes das colunas mais uma vez:


```python
# checando o resultado: a lista dos nomes das colunas
print(df.columns) 
```

    Index(['user_id', 'track', 'artist', 'genre', 'city', 'time', 'day'], dtype='object')


[Voltar ao Índice](#back)

### Valores ausentes <a id='missing_values'></a>
Já na tratativa de valores ausentes, o primeiro passo é encontrar a quantidade desses valores na tabela. Para fazer isso, usa-se dois métodos `pandas`:


```python
# calculando valores ausentes
print(df.isna().sum()) 
```

    user_id       0
    track      1343
    artist     7567
    genre      1198
    city          0
    time          0
    day           0
    dtype: int64


Nem todos os valores ausentes afetam a pesquisa. Por exemplo, os valores ausentes na música (_track_) e artista (_artist_) não são decisivos, pois as hipóteses estão focadas no gênero (_genre_) musical. Desse modo, é possível apenas substituí-los por marcadores claros, como por exemplo _unknown_.

Porém, valores ausentes em _'genre'_ podem afetar significativamente a comparação de preferências musicais de Springfield e Shelbyville. Em um contexto mais próximo da realidade, seria útil e de extrema importância descobrir as razões pelas quais os dados estão ausentes e tentar compensá-los. Mas como não há essa possibilidade neste projeto, teremos que:
* Preencher os valores ausentes com marcadores (_unknown_).
* Avaliar o quanto os valores ausentes podem afetar os resultados.

Para substituir os valores ausentes em 'track', 'artist', e 'genre' com a string 'unknown' é preciso criar uma lista (columns_to_replace) que percorra-a com o ciclo _for_, e substitua os valores ausentes em cada uma das colunas:


```python
# percorrendo os nomes das colunas e substituindo valores ausentes com 'unknown'
columns_to_replace = ['track', 'artist', 'genre']
for i in df[columns_to_replace]:
        df[i] = df[i].fillna('unknown') 
```

Para certificar-se de que a tabela não contenha mais valores ausentes é preciso contar esses valores ausentes.


```python
# contando os valores ausentes
print(df.isna().sum()) 
```

    user_id    0
    track      0
    artist     0
    genre      0
    city       0
    time       0
    day        0
    dtype: int64


[Voltar ao Índice](#back)

### Duplicatas <a id='duplicates'></a>
Para encontrar o número de duplicatas óbvias na tabela, aquelas em que linhas duplicadas têm o valor `True`,usa-se o método _duplicated()_:


```python
# contando duplicatas óbvias
print(df.duplicated().sum()) 
```

    3826


Desse modo, podemos utilizar o método `pandas` para se livrar das duplicatas óbvias:


```python
# removendo duplicatas óbvias
df = df.drop_duplicates().reset_index(drop = True) 
```

E agora podemos contar as duplicatas óbvias mais uma vez, certificando que todas foram removidas:


```python
# verificando duplicatas
print(df.duplicated().sum()) 
```

    0


Agora, devemos analisar a coluna _genre_ para tentarmos localizar possíveis duplicatas implícitas, uma vez que as hipóteses a serem analisadas possuem foco na coluna _genre_.

Para fazer isso, é preciso exibir a lista de nomes de gêneros únicos, organizados em ordem alfabética para facilitar a localização das duplicatas implícitas. Assim, deve-se:
* Recuperar o DataFrame da coluna pretendida.
* Aplicar um método de ordenamento para facilitar a identificação.
* Para a coluna selecionada, chamar o método que irá retornar todos os valores únicos das colunas.


```python
#visualizando nomes de gêneros únicos
print(df['genre'].sort_values().unique()) 
```

    ['acid' 'acoustic' 'action' 'adult' 'africa' 'afrikaans' 'alternative'
     'ambient' 'americana' 'animated' 'anime' 'arabesk' 'arabic' 'arena'
     'argentinetango' 'art' 'audiobook' 'avantgarde' 'axé' 'baile' 'balkan'
     'beats' 'bigroom' 'black' 'bluegrass' 'blues' 'bollywood' 'bossa'
     'brazilian' 'breakbeat' 'breaks' 'broadway' 'cantautori' 'cantopop'
     'canzone' 'caribbean' 'caucasian' 'celtic' 'chamber' 'children' 'chill'
     'chinese' 'choral' 'christian' 'christmas' 'classical' 'classicmetal'
     'club' 'colombian' 'comedy' 'conjazz' 'contemporary' 'country' 'cuban'
     'dance' 'dancehall' 'dancepop' 'dark' 'death' 'deep' 'deutschrock'
     'deutschspr' 'dirty' 'disco' 'dnb' 'documentary' 'downbeat' 'downtempo'
     'drum' 'dub' 'dubstep' 'eastern' 'easy' 'electronic' 'electropop' 'emo'
     'entehno' 'epicmetal' 'estrada' 'ethnic' 'eurofolk' 'european'
     'experimental' 'extrememetal' 'fado' 'film' 'fitness' 'flamenco' 'folk'
     'folklore' 'folkmetal' 'folkrock' 'folktronica' 'forró' 'frankreich'
     'französisch' 'french' 'funk' 'future' 'gangsta' 'garage' 'german'
     'ghazal' 'gitarre' 'glitch' 'gospel' 'gothic' 'grime' 'grunge' 'gypsy'
     'handsup' "hard'n'heavy" 'hardcore' 'hardstyle' 'hardtechno' 'hip'
     'hip-hop' 'hiphop' 'historisch' 'holiday' 'hop' 'horror' 'house' 'idm'
     'independent' 'indian' 'indie' 'indipop' 'industrial' 'inspirational'
     'instrumental' 'international' 'irish' 'jam' 'japanese' 'jazz' 'jewish'
     'jpop' 'jungle' 'k-pop' 'karadeniz' 'karaoke' 'kayokyoku' 'korean'
     'laiko' 'latin' 'latino' 'leftfield' 'local' 'lounge' 'loungeelectronic'
     'lovers' 'malaysian' 'mandopop' 'marschmusik' 'meditative'
     'mediterranean' 'melodic' 'metal' 'metalcore' 'mexican' 'middle'
     'minimal' 'miscellaneous' 'modern' 'mood' 'mpb' 'muslim' 'native'
     'neoklassik' 'neue' 'new' 'newage' 'newwave' 'nu' 'nujazz' 'numetal'
     'oceania' 'old' 'opera' 'orchestral' 'other' 'piano' 'pop'
     'popelectronic' 'popeurodance' 'post' 'posthardcore' 'postrock' 'power'
     'progmetal' 'progressive' 'psychedelic' 'punjabi' 'punk' 'quebecois'
     'ragga' 'ram' 'rancheras' 'rap' 'rave' 'reggae' 'reggaeton' 'regional'
     'relax' 'religious' 'retro' 'rhythm' 'rnb' 'rnr' 'rock' 'rockabilly'
     'romance' 'roots' 'ruspop' 'rusrap' 'rusrock' 'salsa' 'samba' 'schlager'
     'self' 'sertanejo' 'shoegazing' 'showtunes' 'singer' 'ska' 'slow'
     'smooth' 'soul' 'soulful' 'sound' 'soundtrack' 'southern' 'specialty'
     'speech' 'spiritual' 'sport' 'stonerrock' 'surf' 'swing' 'synthpop'
     'sängerportrait' 'tango' 'tanzorchester' 'taraftar' 'tech' 'techno'
     'thrash' 'top' 'traditional' 'tradjazz' 'trance' 'tribal' 'trip'
     'triphop' 'tropical' 'türk' 'türkçe' 'unknown' 'urban' 'uzbek' 'variété'
     'vi' 'videogame' 'vocal' 'western' 'world' 'worldbeat' 'ïîï']


A lista possui duplicatas implícitas do gênero hiphop. Percebam que são nomes escritos incorretamente, ou nomes alternativos para o mesmo gênero.

Temos as seguintes duplicatas implícitas:
* hip
* hop
* hip-hop

Para se livrar deles, declara-se uma função replace_wrong_genres() com dois parâmetros: 
* wrong_genres= — a lista de duplicatas
* correct_genre= — a string com o valor correto

A função deve corrigir os nomes na coluna _'genre'_ da tabela df, isto é, substituindo cada valor da lista wrong_genres por valores de correct_genre.


```python
# função para substituir duplicatas implícitas
def replace_wrong_genres(wrong_genres, correct_genre): # passando uma lista de valores incorretos e uma string com o valor correto na entrada da função
    for wrong_genre in wrong_genres: # percorrendo com um ciclo os nomes mal escrito
        df['genre'] = df['genre'].replace(wrong_genre, correct_genre) # chamando replace() para cada nome errado
```

Agora, devemos chamar replace_wrong_genres() e passar argumentos para que possa eliminar as duplicatas implícitas (hip, hop, e hip-hop) e substituí-los por hiphop:


```python
# removendo duplicatas implícitas
duplicates = ['hip', 'hop', 'hip-hop'] # uma lista de nomes mal escritos
name = 'hiphop' # nome correto
replace_wrong_genres(duplicates, name) # chamada da função
```

No fim, devemos nos certificar que os nomes duplicados foram removidos. Basta exibir a lista de valores únicos da coluna:


```python
# verificando valores duplicados
print(df['genre'].sort_values().unique()) 
```

    ['acid' 'acoustic' 'action' 'adult' 'africa' 'afrikaans' 'alternative'
     'ambient' 'americana' 'animated' 'anime' 'arabesk' 'arabic' 'arena'
     'argentinetango' 'art' 'audiobook' 'avantgarde' 'axé' 'baile' 'balkan'
     'beats' 'bigroom' 'black' 'bluegrass' 'blues' 'bollywood' 'bossa'
     'brazilian' 'breakbeat' 'breaks' 'broadway' 'cantautori' 'cantopop'
     'canzone' 'caribbean' 'caucasian' 'celtic' 'chamber' 'children' 'chill'
     'chinese' 'choral' 'christian' 'christmas' 'classical' 'classicmetal'
     'club' 'colombian' 'comedy' 'conjazz' 'contemporary' 'country' 'cuban'
     'dance' 'dancehall' 'dancepop' 'dark' 'death' 'deep' 'deutschrock'
     'deutschspr' 'dirty' 'disco' 'dnb' 'documentary' 'downbeat' 'downtempo'
     'drum' 'dub' 'dubstep' 'eastern' 'easy' 'electronic' 'electropop' 'emo'
     'entehno' 'epicmetal' 'estrada' 'ethnic' 'eurofolk' 'european'
     'experimental' 'extrememetal' 'fado' 'film' 'fitness' 'flamenco' 'folk'
     'folklore' 'folkmetal' 'folkrock' 'folktronica' 'forró' 'frankreich'
     'französisch' 'french' 'funk' 'future' 'gangsta' 'garage' 'german'
     'ghazal' 'gitarre' 'glitch' 'gospel' 'gothic' 'grime' 'grunge' 'gypsy'
     'handsup' "hard'n'heavy" 'hardcore' 'hardstyle' 'hardtechno' 'hiphop'
     'historisch' 'holiday' 'horror' 'house' 'idm' 'independent' 'indian'
     'indie' 'indipop' 'industrial' 'inspirational' 'instrumental'
     'international' 'irish' 'jam' 'japanese' 'jazz' 'jewish' 'jpop' 'jungle'
     'k-pop' 'karadeniz' 'karaoke' 'kayokyoku' 'korean' 'laiko' 'latin'
     'latino' 'leftfield' 'local' 'lounge' 'loungeelectronic' 'lovers'
     'malaysian' 'mandopop' 'marschmusik' 'meditative' 'mediterranean'
     'melodic' 'metal' 'metalcore' 'mexican' 'middle' 'minimal'
     'miscellaneous' 'modern' 'mood' 'mpb' 'muslim' 'native' 'neoklassik'
     'neue' 'new' 'newage' 'newwave' 'nu' 'nujazz' 'numetal' 'oceania' 'old'
     'opera' 'orchestral' 'other' 'piano' 'pop' 'popelectronic' 'popeurodance'
     'post' 'posthardcore' 'postrock' 'power' 'progmetal' 'progressive'
     'psychedelic' 'punjabi' 'punk' 'quebecois' 'ragga' 'ram' 'rancheras'
     'rap' 'rave' 'reggae' 'reggaeton' 'regional' 'relax' 'religious' 'retro'
     'rhythm' 'rnb' 'rnr' 'rock' 'rockabilly' 'romance' 'roots' 'ruspop'
     'rusrap' 'rusrock' 'salsa' 'samba' 'schlager' 'self' 'sertanejo'
     'shoegazing' 'showtunes' 'singer' 'ska' 'slow' 'smooth' 'soul' 'soulful'
     'sound' 'soundtrack' 'southern' 'specialty' 'speech' 'spiritual' 'sport'
     'stonerrock' 'surf' 'swing' 'synthpop' 'sängerportrait' 'tango'
     'tanzorchester' 'taraftar' 'tech' 'techno' 'thrash' 'top' 'traditional'
     'tradjazz' 'trance' 'tribal' 'trip' 'triphop' 'tropical' 'türk' 'türkçe'
     'unknown' 'urban' 'uzbek' 'variété' 'vi' 'videogame' 'vocal' 'western'
     'world' 'worldbeat' 'ïîï']


Verificamos que não há mais duplicados implícitos.

[Voltar ao Índice](#back)

### Conclusões <a id='data_preprocessing_conclusions'></a>
Nessa etapa de pré-processamento dos dados foi possível identificar alguns problemas:

- Estilo de cabeçalho incorreto.
- Valores ausentes.
- Duplicatas óbvias e implícitas.

O cabeçalho foi limpo para fazer o processamento da tabela mais simples e claro.

Todos os valores ausentes foram substituídos por 'unkown'. Mas ainda é necessário ver se os valores ausentes em 'genre' afetará os nossos resultados.

A ausência de duplicatas deixará os resultados mais precisos e mais fáceis de entender.

Agora podemos seguir para testar as hipóteses.

[Voltar ao Índice](#back)

## Etapa 3. Testando hipóteses <a id='hypotheses'></a>

### Hipótese 1: comparando o comportamento dos usuários em duas cidades <a id='activity'></a>

De acordo com a primeira hipótese, usuários de Springfield e Shelbyville escutam música de forma diferente. O teste dessa hipótese será usando os dados de três dias da semana: segunda-feira, quarta-feira, e sexta-feira.

Para tal, precisamos:

* Dividir os usuários de cada cidade em grupos.
* Comparar quantas músicas cada grupo escutou na segunda-feira, quarta-feira e sexta-feira.

Por uma questão de prática, cada um desses cálculos é feito separadamente. 

A atividade dos usuários em cada cidade será avaliada e esses dados estarão agrupados por cidade com a contagem do número de músicas tocadas em cada grupo.


```python
# Contando as músicas tocadas em cada cidade
df.groupby('city')
print(df.groupby('city').count())
print('='*56)
print(df.groupby('city')['track'].count())
```

                 user_id  track  artist  genre   time    day
    city                                                    
    Shelbyville    18512  18512   18512  18512  18512  18512
    Springfield    42741  42741   42741  42741  42741  42741
    ========================================================
    city
    Shelbyville    18512
    Springfield    42741
    Name: track, dtype: int64


Springfield tem mais músicas tocadas (42741) do que Shelbyville (18512). Mas isso não quer dizer que os cidadãos de Springfield escutam música com mais frequência. Essa cidade é somente maior, e tem mais usuários. Springfield com população superior a 62 mil, e Shelbyville com população de quase 19 mil — dados de 2020.

Agora, para verificar o comportamento dos usuários nos dias da semana, agrupa-se os dados para encontrar a quantidade de músicas tocadas na segunda, quarta e sexta-feira.


```python
# Calculando as músicas escutadas em cada um desses três dias
print(df.groupby('day').count())
print('='*54)
print(df.groupby('day')['track'].count())
```

               user_id  track  artist  genre   city   time
    day                                                   
    Friday       21840  21840   21840  21840  21840  21840
    Monday       21354  21354   21354  21354  21354  21354
    Wednesday    18059  18059   18059  18059  18059  18059
    ======================================================
    day
    Friday       21840
    Monday       21354
    Wednesday    18059
    Name: track, dtype: int64


Quarta-feira é o dia mais calmo em geral. Mas se considerarmos as duas cidades separadamente, devemos chegar a uma conclusão diferente.

Para tal, vamos agrupar por cidade __e__ dia da semana, os dois critérios serão levados em consideração.

A função number_tracks() é criada para calcular o número de músicas tocadas em um determinado dia da semana e em cada cidade. Essa função terá dois parâmetros necessários:
* dia da semana.
* nome da cidade.

Na função, devemos ter a variável para armazenar as linhas da tabela original, onde:
* o valor da coluna 'day' é igual ao parâmetro dia.
* o valor da coluna 'city' é igual ao parâmetro cidade.

Será necessários aplicar os filtros consecutivos com indexação lógica.

Assim, será possível calcular os valores da coluna 'user_id' na tabela resultante, além de armazenar o resultado na nova variável. É importante retornar essa variável da função para ser utilizada nas chamadas consecutivas.


```python
# <criando a função number_tracks()>
def number_tracks(day, city):                          
    track_list = df.loc[(df.loc[:,'day'] == day)&(df.loc[:,'city'] == city)]
    track_list_count = 0
    for row in track_list['user_id']:
        track_list_count += 1
    return track_list_count
```

Agora, vamos chamar a função `number_tracks()` seis vezes, uma vez para cada combinação de seus parâmetros: duas cidades para cada um dos três dias.


```python
# a quantidade de músicas tocadas em Springfield na segunda-feira
print(number_tracks(day='Monday', city='Springfield')) 
```

    15740



```python
# a quantidade de músicas tocadas em Shelbyville na segunda-feira
print(number_tracks(day='Monday', city='Shelbyville')) 
```

    5614



```python
# a quantidade de músicas tocadas em Springfield na quarta-feira
print(number_tracks(day='Wednesday', city='Springfield')) 
```

    11056



```python
# a quantidade de músicas tocadas em Shelbyville na quarta-feira
print(number_tracks(day='Wednesday', city='Shelbyville')) 
```

    7003



```python
# a quantidade de músicas tocadas em Springfield na sexta-feira
print(number_tracks(day='Friday', city='Springfield')) 
```

    15945



```python
# a quantidade de músicas tocadas em Shelbyville na sexta-feira
print(number_tracks(day='Friday', city='Shelbyville')) 
```

    5895


Usa-se pd.DataFrame para criar uma tabela, onde:
* Os nomes das colunas são: ['city', 'monday', 'wednesday', 'friday']`.
* Os dados são o resultado do retorno de number_tracks().


```python
col = ['city', 'monday', 'wednesday', 'friday']
number_track = [['Springfield', number_tracks(day='Monday', city='Springfield'), number_tracks(day='Wednesday', city='Springfield'), number_tracks(day='Friday', city='Springfield')],
                ['Shelbyville', number_tracks(day='Monday', city='Shelbyville'), number_tracks(day='Wednesday', city='Shelbyville'), number_tracks(day='Friday', city='Shelbyville')]
               ]
hypothesis_1 = pd.DataFrame(data=number_track, columns=col) # tabela com resultados
print(hypothesis_1)
```

              city  monday  wednesday  friday
    0  Springfield   15740      11056   15945
    1  Shelbyville    5614       7003    5895


**Conclusões**

Os dados revelam diferenças no comportamento dos usuários:

- Em Springfield, a quantidade de músicas tocadas tem seu auge nas segundas e sextas-feiras, enquanto na quarta-feira há uma diminuição na atividade.
- Em Shelbyville, ao contrário, usuários escutam mais música na quarta-feira. A atividade na segunda e sexta-feira é pequena.

Então a primeira hipótese, que visa identificar a diferença na atividade dos usuários de cada cidade durante os dias da semana, demonstra-se correta.

[Voltar ao Índice](#back)

### Hipótese 2: música no começo e no fim da semana <a id='week'></a>

De acordo com a segunda hipótese, na segunda-feira de manhã e sexta-feira à noite, habitantes de Springfield escutam gêneros que diferem dos gêneros musicais ouvidos pelos usuários em Shelbyville.

Para essa análise, faz-se necessário a criação de duas tabelas, um para cada cidade:
* Para Springfield — criaremos a tebela `spr_general`.
* Para Shelbyville — crairemos a tabela `shel_general`.


```python
# obtendo a tabela spr_general a partir das linhas df, onde o valor na coluna 'city' é 'Springfield'
spr_general = df.loc[df.loc[:,'city'] == 'Springfield'] 
```


```python
# obtendo os shel_general a partir das linhas df, onde os valores na coluna 'city' é Shelbyville'
shel_general = df.loc[df.loc[:,'city'] == 'Shelbyville']
```

Depois da criação das tabelas e, de forma a analisar os gêneros mais populares, cria-se a função genre_weekday() com os seguintes parâmetros:
* Uma tabela para dados (`df`).
* O dia da semana (`day`).
* O primeiro carimbo de hora, no formato 'HH:MM' (`time1`).
* O último carimbo de hora, no formato 'HH:MM' (`time2`).

Essa função vai retornar informações sobre os gêneros mais populares (apenas os 15 primeiros) em um determinado dia, dentro do período entre os dois carimbos de hora — intervalo entre `time1` e `time2`.


```python
def genre_weekday(data, day, time1, time2):
    # filtragem consecutiva
    # genre_df armazenará apenas as linhas df onde o dia é igual a day=
    genre_df = data.loc[data.loc[:,'day'] == day] 
    # genre_df armazenará apenas as linhas onde o tempo é maior que time1=
    genre_df = genre_df.loc[genre_df.loc[:,'time'] > time1] 
    # genre_df armazenará apenas as linhas onde o tempo é menor que time2=
    genre_df = genre_df.loc[genre_df.loc[:,'time'] < time2] 
    # o DataFrame filtrado pela coluna com nomes dos gêneros será agrupado
    genre_df_grouped = genre_df.groupby('genre')['user_id'].count()
    # o resultado será armazenado em ordem decrescente, para que os gêneros mais populares fiquem no topo
    genre_df_sorted = genre_df_grouped.sort_values(ascending=False) 
    # o objeto Serie é retornado com os 15 gêneros mais populares em um determinado dia, dentro de um determinado tempo
    return genre_df_sorted[:15]
```

Agora vamos comparar os resultados da função `genre_weekday()` para Springfield e Shelbyville na segunda-feira de manhã (de 7hs à 11hs) e na sexta-feira de tarde (das 17hs às 23hs):


```python
# chamando a função para segunda-feira de manha em Springfield
print(genre_weekday(spr_general, 'Monday', '07:00', '11:00'))
```

    genre
    pop            781
    dance          549
    electronic     480
    rock           474
    hiphop         286
    ruspop         186
    world          181
    rusrap         175
    alternative    164
    unknown        161
    classical      157
    metal          120
    jazz           100
    folk            97
    soundtrack      95
    Name: user_id, dtype: int64



```python
# chamando a função para segunda-feira de manhã em Shelbyville
print(genre_weekday(shel_general, 'Monday', '07:00', '11:00'))
```

    genre
    pop            218
    dance          182
    rock           162
    electronic     147
    hiphop          80
    ruspop          64
    alternative     58
    rusrap          55
    jazz            44
    classical       40
    world           36
    rap             32
    soundtrack      31
    rnb             27
    metal           27
    Name: user_id, dtype: int64



```python
# chamando a função para sexta-feira à tarde em Springfield
print(genre_weekday(spr_general, 'Friday', '17:00', '23:00'))
```

    genre
    pop            713
    rock           517
    dance          495
    electronic     482
    hiphop         273
    world          208
    ruspop         170
    classical      163
    alternative    163
    rusrap         142
    jazz           111
    unknown        110
    soundtrack     105
    rnb             90
    metal           88
    Name: user_id, dtype: int64



```python
# chamando a função para sexta-feira à tarde em Shelbyville
print(genre_weekday(shel_general, 'Friday', '17:00', '23:00'))
```

    genre
    pop            256
    rock           216
    electronic     216
    dance          210
    hiphop          97
    alternative     63
    jazz            61
    classical       60
    rusrap          59
    world           54
    unknown         47
    ruspop          47
    soundtrack      40
    metal           39
    rap             36
    Name: user_id, dtype: int64


**Conclusão**

Tendo comparado os 15 gêneros mais ouvidos na segunda-feira de manhã, nós podemos tirar as seguintes conclusões:

1. Usuários de Springfield e Shelbyville escutam músicas semelhantes. Os cinco gêneros mais ouvidos são os mesmos. Apenas rock e música eletrônica trocaram de preferências na segunda-feira entre as cidades, enquanto dança e eletrônica trocam de preferências na sexta-feira.

2. Nas duas cidades, a quantidade de valores ausentes acabaram por serem tantos que o valor 'unknown' veio entre as primeiras 15 posições. Isso significa que valores ausentes tiveram uma considerável porção dos dados, que pode ser a base para questionamentos à confiabilidade das conclusões.

Assim, a segunda hipótese foi parcialmente provada:
* Usuários escutam gêneros musicais parecidos no começo e no fim da semana.
* Não há grande diferença entre Springfield e Shelbyville. Nas duas cidades, pop é o gênero mais popular.

No entanto, o número de valores ausentes faz esse resultado ser questionável. Nas duas cidades, há tantos que eles afetaram o top 15. Se houvesse informações desses valores, as coisas poderiam ser diferentes.

[Voltar ao Índice](#back)

### Hipótese 3: preferências em Springfield e Shelbyville <a id='genre'></a>

A terceira hipótese traz que os usuários da aplicação em Shelbyville amam o gênero musical rap. Enquanto os cidadãos de Springfield preferem ouvir mais pop.

Para analisar essa hipótese, agrupa-se a tabela spr_general por gênero para encontrar o número de músicas tocadas para cada gênero — utilizando o método count(). Depois deve-se organizar o resultado em ordem decrescente.


```python
# agrupando a tabela spr_general pela coluna 'genre', contando os valores de 'genre' no agrupamento e 
# organizando o objeto Series resultante em ordem decrescente
spr_genres = spr_general.groupby('genre')['genre'].count().sort_values(ascending=False) 
```

Exibindo as primeiras 10 linhas de spr_genres:


```python
# exibindo as primeiras 10 linhas de spr_genres
display(spr_genres[:10])
```


    genre
    pop            5892
    dance          4435
    rock           3965
    electronic     3786
    hiphop         2096
    classical      1616
    world          1432
    alternative    1379
    ruspop         1372
    rusrap         1161
    Name: genre, dtype: int64


Agora fazemos o mesmo com os dados de Shelbyville.


```python
# agrupando a tabela shel_general pela coluna 'genre', contando os valores de 'genre' no agrupamento e 
# organizando o objeto Series resultante em ordem decrescente
shel_genres = shel_general.groupby('genre')['genre'].count().sort_values(ascending=False)
```

Exibindo as primeiras 10 linhas de shel_genres:


```python
# exibindo as primeiras 10 linhas de shel_genres
display(shel_genres[:10])
```


    genre
    pop            2431
    dance          1932
    rock           1879
    electronic     1736
    hiphop          960
    alternative     649
    classical       646
    rusrap          564
    ruspop          538
    world           515
    Name: genre, dtype: int64


**Conclusão**

A hipótese foi parcialmente provada:
* Música pop é o gênero mais ouvido em Springfield.
* Entretanto, música pop acabou por ser igualmente popular em Springfield e Shelbyville, e rap não estava no top 5 em nenhuma cidade.

[Voltar ao Índice](#back)

# Conclusões <a id='end'></a>

Foram testadas as seguintes hipóteses:

1. A atividade dos usuários é diferente dependendo do dia da semana e da cidade.
2. Durante as manhãs de segunda-feira, os moradores de Springfield e Shelbyville escutam diferentes gêneros. Isso também é verdadeiro para noites de sexta-feira.
3. Os ouvintes de Springfield e Shelbyville têm diferentes preferências. Em Springfield, as pessoas preferem pop, enquanto Shelbyville tem mais fãs de rap.

Depois de analisar os dados, conclui-se que:

1. A atividade dos usuários em Springfield e Shelbyville realmente depende do dia da semana, embora as cidades variam de formas diferentes. 

A primeira hipótese é totalmente aceita.

2. As preferências musicais não variam significativamente ao decorrer da semana, tanto em Springfield como em Shelbyville é possível ver pequenas diferenças na ordem nos dias da semana, mas:
* Em Springfield e Shelbyville, as pessoas escutam mais música pop.

Essa hipótese é parcialmente aceita, ou até mesmo pode ser considerada rejeitada. Pois devemos também ter em mente que o resultado pode ter sido diferente se não fosse pelos valores ausentes.

3. Acontece que preferências musicais dos usuários de Springfield e Shelbyville são bastante parecidas.

A terceira hipótese foi rejeitada. Se há alguma diferença nas preferências, ela não pode ser vista nesses dados.

[Voltar ao Índice](#back)
