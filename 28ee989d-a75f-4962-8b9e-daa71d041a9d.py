#!/usr/bin/env python
# coding: utf-8

# Olá, Thiago!
# 
# Meu nome é Ramon e te ajudarei neste projeto. Fico feliz em rever seu projeto hoje.
# 
# Ao ao longo do texto farei algumas observações sobre melhorias no código e também farei comentários sobre suas percepções sobre o assunto. Estarei aberta a feedbacks e discussões sobre o tema.
# 
# Você encontrará meus comentários abaixo - **por favor, não os mova, modifique ou exclua**.
# 
# Você pode encontrar meus comentários em caixas verdes, amarelas ou vermelhas como esta:
# 
# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Sucesso. Tudo foi feito corretamente.
# </div>
# 
# 
# 
# <div class="alert alert-block alert-warning">
# <b>Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Observações. Algumas recomendações.
# </div>
# 
# <div class="alert alert-block alert-danger">
# 
# <b>Comentário do revisor: </b> <a class="tocSkip"></a>
#     
# Precisa de correções. O bloqueio requer algumas correções. O trabalho não pode ser aceito com os comentários em vermelho.
# </div>
# 
# Você pode me responder usando isso:
# 
# <div class="alert alert-block alert-info">
# <b>Resposta do Aluno.</b> <a class="tocSkip"></a>
# </div>

# # Análise de Risco de Inadimplência de Clientes
# 
# Segue-se um relatório para a divisão de empréstimos de um banco.
# A ideia aqui é tratar os dados para responder algumas perguntas.
# * Será que o estado civil de um cliente e o número de filhos têm impacto sobre a inadimplência nos empréstimos realizados?
# * Existem motivações para adquirir empréstimos mais arriscadas que outras?
# * O nível de renda afeta os pagamentos de empréstimos em dia?
# * Como a finalidade do crédito afeta a taxa de inadimplência?
# 
# O banco já tem alguns dados sobre a capacidade de crédito dos clientes.

# In[1]:


# Carregando todas as bibliotecas e abrir o local do arquivo
import pandas as pd
import datetime as dt
import numpy as np
# Carregue os dados
df = pd.read_csv('/datasets/credit_scoring_eng.csv')


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# ## Exploração de Dados
# 
# **Descrição dos dados**
# - `children` - o número de crianças na família
# - `days_employed` - experiência de trabalho em dias
# - `dob_years` - idade do cliente em anos
# - `education` - educação do cliente
# - `education_id` - identificador de educação
# - `family_status` - estado civil do cliente
# - `family_status_id` - identificador de estado civil
# - `gender` - gênero do cliente
# - `income_type` - tipo de emprego
# - `debt` - havia alguma dívida no pagamento do empréstimo
# - `total_income` - renda mensal
# - `purpose` - o objetivo de obter um empréstimo
# 
# Agora vamos explorar nossos dados para verificar possíveis problemas com eles.

# In[2]:


# Verificar quantas linhas e colunas nosso conjunto de dados tem
print(f'O DataFrame contém {df.shape[0]} linhas e {df.shape[1]} colunas.')


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[3]:


# vamos exibir as primeiras N linhas
display(df.head(10))


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[4]:


# Verificar as principais variáveis descritivas
display(df.describe())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[5]:


# Explorar os valores discrepantes
boxplot = df.boxplot(column=['children', 'days_employed', 'dob_years', 'debt', 'total_income'])


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# - `days_employed` e `total_income` são as variáveis que mais precisam atenção no tratamento, seus dados são bem dispersos e possuem ambas desvio padrão muito acentuado.
# 
# - Em `children` deve-se avaliar se há valores discrepantes.  Essa variável atinge seu valor máximo em 20 e valor mínimo em -1. Essa variável só deve aceitar valores inteiros e positivos.
# 
# - Em `days_employed` há números negativos e valores extremos. A variável é definida como experiência de trabalhos em dias, logo compreende-se que não se deve haver dias negativos e nem mesmo dias fracionados. Essa variável deve ser inteira e positiva. Porém, no mínimo, 75% dos dados são números negativos.
# 
# - Em `dob_years` deve-se avaliar se há valores discrepantes. Essa variável só deve aceitar valores inteiros e positivos. Porém assume valor mínimo em 0, assim, deve-se avaliar juntamente com outras variáveis se são dados de contas de clientes com menos de 1 ano de vida — muitos bancos abrem contas de crianças com responsáveis sendo os próprios pais. 
# 
# - Em `education` há variáveis qualitativas duplicatas implícitas. A correção pode ser verificada com a variável `education_id`.
# 
# - Em `family_status` deve-se avaliar se não há dados duplicados de forma implícita. A correção pode ser verificada com a variável `family_status_id`.
# 
# - Em `gender` deve-se avaliar se não há dados duplicados de forma implícita.
# 
# - Em `income_type` deve-se avaliar se não há dados duplicados de forma implícita.
# 
# - Em `debt` só aceita-se valores 1 ou 0. Para 1 se já deixou de pagar um empréstimo e 0 para quem sempre pagou empréstimo ou nunca adquiriu um.
# 
# - Em `total_income` há apenas valores positivos. Uma vez que a renda não pode ser negativa.
# 
# - Em `purpose` deve-se avaliar se há alguma variável qualitativa duplicada de forma implícita.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[6]:


# Obter informações sobre dados
df.info()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# - Há valores ausentes nas variáveis `days_employed` e `total_income`. 
# 
# - Em `days_employed`, seus valores ausentes podem estar relacionados a ausência de experiência de trabalho ou falta de resposta. Comparar com a variável `income_type` pode sugerir qual a opção correta.
# 
# - Em `total_income` esses valores podem estar ausentes por falta de renda ou recusa em apresentar essas informações por parte dos clientes. É interessante comparar com a variável `income_type` para distinguir entre as duas opções.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[7]:


# Vejamos a tabela filtrada com valores ausentes na primeira coluna com dados ausentes
display(df[df['days_employed'].isna()])


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Os valores ausentes em `days_employed` e em `total_income` parecem sugerir uma simetria e correlação. Faz sentido quando paramos para pensar que a falta de experiência de trabalho está relacionada a falta de renda. A ausência desses dados pode ser por esse fator. Os testes para comprovar essa suposição serão feitos adiante.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[8]:


#Verificar se os valores NaN em days_employed correspondem as mesmas linhas em total_income
nan_df = df[df['days_employed'].isna()]
nan_income = nan_df['total_income'].isna().count()
df_nan_income = df['total_income'].isna().sum()
print(f'Num DataFrame criado com os valores nulos em days_employed, a quantidade de linhas com valor nulo em total_income é: {nan_income}. A mesma quantidade de valores NaN no DataFrame original na variável total_income ({df_nan_income})')


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[9]:


# Verificar o tipo de emprego que os clientes com valores nulos em renda e em dias de trabalho possuem
print(nan_df['income_type'].value_counts())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto. Como é o último (na verdade, o único) comando, você não precis do print()
# 
# </div>
# 

# In[10]:


# Aplicar várias condições para filtrar dados e observar o número de linhas na tabela filtrada.
(df.isna()
 .mean()
 .sort_values(ascending=False)
 .reset_index()
 .rename(columns = {'index' : 'Variables', 0: 'Missing'})
).T


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# **Conclusão intermediária**
# 
# Conclui-se que a tabela filtrada corresponde a mesma quantidade de linhas de valores ausentes para as duas variáveis com valores ausentes, `days_employed` e `total_income`.
# 
# Valores ausentes nas duas variáveis correspondem a 10.09% do total de dados das suas respectivas variáveis, um valor bastante expressivo. Nesse sentido, a melhor forma de tratá-los é preencher esses valores ausentes. Assim, é importante considerar características específicas do cliente, como o tipo de emprego, sexo e educação.
# 
# Os próximos passos envolvem realizar testes e agrupamentos para verificar se os valores ausentes surgiram de forma aleatória.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# **Possíveis motivos para valores ausentes nos dados**
# 
# A suposição de que a falta de experiência de dias de trabalho contribui para a falta de renda parece ser verdadeira. Porém há muitos clientes sem experiência de trabalho e sem renda informada que estão empregados, são empresários ou funcionários públicos. Os dados sugerem que as informações desses clientes foram coletados muito cedo, de forma que ainda não computaram experiência e nem renda nos seus tipos de emprego — o que acho improvável. O mais provável é que houve falta de informação intencional, já que renda é um dado sensível.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[11]:


# Distribuição do conjunto de dados em children
df_children = df['children'].value_counts(dropna=False, normalize=True)
nan_df_children = nan_df['children'].value_counts(dropna=False, normalize=True)
print(df_children - nan_df_children)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[12]:


# Distribuição do conjunto de dados em dob_years
df_dob_years = df['dob_years'].value_counts(dropna=False, normalize=True)
nan_df_dob_years = nan_df['dob_years'].value_counts(dropna=False, normalize=True)
print(df_dob_years - nan_df_dob_years)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto. Porém, um gráfico facilita a visualização
# 
# </div>
# 

# In[13]:


# Distribuição do conjunto de dados em education_id
df_education_id = df['education_id'].value_counts(dropna=False, normalize=True)
nan_df_education_id = nan_df['education_id'].value_counts(dropna=False, normalize=True)
print(df_education_id - nan_df_education_id)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[14]:


# Distribuição do conjunto de dados em family_status_id
df_family_status_id = df['family_status_id'].value_counts(dropna=False, normalize=True)
nan_df_family_status_id = nan_df['family_status_id'].value_counts(dropna=False, normalize=True)
print(df_family_status_id - nan_df_family_status_id)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[15]:


# Distribuição do conjunto de dados em gender
df_gender = df['gender'].value_counts(dropna=False, normalize=True)
nan_df_gender = nan_df['gender'].value_counts(dropna=False, normalize=True)
print(df_gender - nan_df_gender)
print()
print(nan_df_gender)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[16]:


# Distribuição do conjunto de dados em debt
df_debt = df['debt'].value_counts(dropna=False, normalize=True)
nan_df_debt = nan_df['debt'].value_counts(dropna=False, normalize=True)
print(nan_df_debt)
print()
print(df_debt - nan_df_debt)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# A variação das colunas `children`, `dob_years`,`education_id`,`family_status_id`, `debt` do DataFrame original com as mesmas colunas do DataFrame de valores ausentes não chega a 1% em cada um dos seus respectivos elementos. Não há sinais de um padrão na relação que afete os valores ausentes. Na coluna `gender`, apesar de haver um percentual maior de valores ausentes quando analisamos os dados das mulheres, a proporção se mantém quando analisamos a variação dos valores no DataFrame orginal e o DataFrame de valores ausentes.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# **Conclusão intermediária**
# 
# A distribuição no conjunto de dados original é semelhante à distribuição da tabela filtrada. Pois essa variação não chega a 1%.
# 
# Estamos cientes também que todos os valores ausentes na variável `total_income` correspondem a valores ausentes na variável `days_employed`, porém é possível imaginar que certos tipos de empregos (`income_type`) possam contribuir ou favorecer o surgimento de valores ausentes, como para os tipos estudantes e desempregados.
# 
# É importante verificar se os clientes que possuem idade igual a zero contribuem para a existência de valores ausentes em experiência em dias de emprego e renda.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[17]:


# Para valores ausentes provenientes de certos tipos de emprego
print(df['income_type'].value_counts())
print()
# Para valores ausentes provenientes de clientes com idade igual a zero
print(nan_df[nan_df['dob_years']==0].count())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# **Conclusão intermediária**
# 
# Desse modo, podemos afirmar que os valores ausentes parece serem acidentais quando não levamos em conta a relação entre as variáveis `days_employed` e `total_income`. Nem a presença de clientes com idade igual a zero e nem mesmo a pouca expressividade de valores em tipo de emprego estudante e desempregado na variável `income_type`, foram suficientes para nortear ou sugerir um padrão no surgimento de valores ausentes na base de dados.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# **Conclusões**
# 
# As análises realizadas sugerem que não há padrões nos dados que gerem valores ausentes para além da relação estabelecida entre as variáveis `days_employed` e `total_income`. Cada variável do DataFrame foi testada conforme sua distribuição original e a sua distribuição do DataFrame filtrado em valores ausentes, mas não houve variações nos dados superiores a 1%.
# 
# Desse modo, as próximas etapas envolvem preencher os valores ausentes em `days_employed` e em `total_income`. Para `days_employed` deve-se tratar os números negativos e valores extremos, a mediana deve-se ajustar melhor que a média. Como a variável é definida como experiência de trabalhos em dias, logo compreende-se que não se deve haver dias negativos e nem mesmo dias fracionados. Essa variável deve ser inteira e positiva.
# 
# já em `total_income`, preencher os valores ausentes levando em consideração as variações entre sexo e anos de estudo. Pois estudos sugerem que existem diferenças salariais entre gênero e que a renda aumenta conforme a quantidade de anos de estudo que o indivíduo possui.
# 
# Além do preenchimento dos valores ausentes, vai ser imprescindível para uma boa análise, o tratamento de duplicatas, diferença de registros e de valores incorretos.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# ## Transformação de Dados
# 
# O objetivo é analisar as colunas, variáveis, para identificar possíveis problemas como duplicatas.

# In[18]:


# Verificar todos os valores na coluna de educação para ver quais grafias precisarão ser corrigidas
print(df['education'].sort_values().unique())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[19]:


# Corrigindo os registros
df['education'] = df['education'].str.lower()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[20]:


# Verificar todos os valores na coluna para ter certeza de que houve a correção
print(df['education'].sort_values().unique())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto. Não preicsa de print() por ser o último comando
# 
# </div>
# 

# Verificando os dados na coluna `children`.

# In[21]:


# Verificando a distribuição de valores na coluna `children`
print(df['children'].value_counts(dropna=False, normalize=True))
print(df['children'].shape[0])


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# A porcentagem de dados problemáticos da variável `children` é a soma do percentual quando há 20 (0.35%) e -1 (0.21%) filhos, aproximadamente 0.57%. Apesar dos erros serem bem baixos na variável, é de fácil entendimento que o erro está relacionado com o sinal negativo em -1, pois não há filhos negativos, e um adicional de um zero em 20, dese modo, faço os seguintes ajustes:

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[22]:


df['children'] = df['children'].replace(20,2) # Considero que o outlier 20 seja um erro de digitação
df['children'] = df['children'].replace(-1,1) # Considero que o número negativo de filhos seja um erro de digitação
boxplot = df.boxplot(column='children') # Visualizar dados discrepantes
display(df['children'].describe())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[23]:


# Verificar a coluna `children` novamente para ter certeza de que está tudo corrigido
df['children'] = df['children'].astype('int')
print(df['children'].value_counts())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Na variável idade em anos do cliente, `dob_years`, temos valores 0 (zero) em algumas poucas linhas, mas é importante tratá-los, pois essa variável servirá para corrigir valores em `days_employed`. Desse modo, a melhor forma de corrigir é utilizando a média inteira para substituir os valores nulos.
# 
# Num primeiro momento foi pensado que poderia tratar-se de crianças que ainda não tinham 1 ano de vida, porém outras variáveis dessas linhas sugerem se tratar de erro de inserção de valores, uma vez que muitas linhas de idade 0 (zero) estão como empregados, aposentados e níveis educacionais mais avançados.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto. Porém, veja que média é sensível a outliers
# 
# </div>
# 

# In[24]:


# Corrigir as idades 0 em dob_years
df['dob_years'] = np.where(df['dob_years']==0, np.nan, df['dob_years'])
# Definir a média em dob_years, valores inteiros
mean_dob_years = int((df['dob_years']).mean())
# Substituir valores ausentes pela média inteira de dob_years
df['dob_years'].fillna(int(df['dob_years'].mean()), inplace = True)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[25]:


# Checar se ainda há valores ausentes
print(df['dob_years'].isna().mean())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[26]:


# Verificar o resultado
print(len(df[df['dob_years']==0]))
print()
print(df['dob_years'].describe())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Em `days_employed` temos valores ausentes, números extremos — dias de trabalho que superam os dias de vida dos clientes —, bem como números negativos (não há dias trabalhados negativos).

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[27]:


# Dados problemáticos, valores negativos
df_neg_days = df.loc[df.loc[:,'days_employed']<0]
display(df_neg_days)
print('='*100)
perc_neg_days = df_neg_days['days_employed'].shape[0] / df['days_employed'].shape[0]
print(f'A porcentagem de valores negativos é {perc_neg_days:.2%}.')


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[28]:


#Corrigir valores negativos
df['days_employed'] = abs(df['days_employed']) # Transformando esses valores em valores absolutos
df_neg_days = df.loc[df.loc[:,'days_employed']<0] # Verificando se a correção foi feita
display(df_neg_days.count())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[29]:


# Dados problemáticos, dias trabalhados superiores aos dias de vida
df_outlier_days = df.loc[df.loc[:,'days_employed']>(df['dob_years']*365)] # Aplicando a lógica
display(df_outlier_days)
print('='*100)
# Mostrando o percentual de valores extremos
perc_outlier_days = df_outlier_days['days_employed'].shape[0] / df['days_employed'].shape[0]
print(f'A porcentagem de dias trabalhados que superam a idade do cliente é {perc_outlier_days:.2%}.')


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[30]:


# Analisar os dados problemáticos, dias de trabalhos superiores ao dias de vida
display(df_outlier_days.groupby('income_type')['days_employed'].count())
print()
display(df.groupby('income_type')['days_employed'].count())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Os clientes com informações de dias trabalhados que superam seus dias de vida estão concentrados, em sua totalidade, no grupo `retiree`.
# Até 2022, para se aposentar nos Estados Unidos era necessário trabalhar por no mínimo 10 anos e ter 62 anos ou mais. Apesar de ser possível trabalhar com menos de 18 anos nos Estados Unidos, esses trabalhos raramente recolhem impostos ou possuem contratos que garantem os critérios para se aposentar. Desse modo, os valores a serem substituídos em `days_employed` devem variar entre 3650 e a multiplicação de 365 dias com idade atual do cliente menos 18 anos — (`dob_years` - 18)*365.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[31]:


# Encontrar a média e a mediana de days_employed desconsiderando os valores extremos
dif_days = df.loc[df.loc[:,'days_employed']<(df['dob_years']*365)]
values_dmean_employed = dif_days.groupby('income_type')['days_employed'].mean()
display(values_dmean_employed)
values_dmedian_employed = dif_days.groupby('income_type')['days_employed'].median()
display(values_dmedian_employed)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[32]:


# Criar função para substituir valores
def preencher_days_employed(row):
    if row['income_type']=='retiree' or row['income_type']=='unemployed':
        max_day = (row['dob_years']*365-(18*365))
        return max_day
    else:
        return row['days_employed']


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[33]:


# Testar a função com a primeira linha dos valores extremos
df[df['days_employed']>(df['dob_years']*365)].iloc[0]


# In[34]:


# Testar a função, o resultado deve ser (53-18)*365 = 12775
preencher_days_employed(df[df['days_employed']>(df['dob_years']*365)].iloc[0])


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[35]:


# Aplicar a função inteira no DataFrame
df['days_employed'] = df.apply(preencher_days_employed, axis = 1)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[36]:


# Verificar se ainda temos dias trabalhados superiores a dias de vida
df_outlier_days = df.loc[df.loc[:,'days_employed']>(df['dob_years']*365)]
display(df_outlier_days.groupby('income_type')['days_employed'].count())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Verificar agora a idade do cliente, `dob_years`, e corrigir possíveis problemas que possam surgir.

# In[37]:


# Verificar `dob_years` para valores suspeitos e contar a porcentagem
df['dob_years'] = df['dob_years'].astype('int')
up_years = df[df['dob_years']>=100].shape[0] / df['dob_years'].shape[0]
do_years = df[df['dob_years']<=0].shape[0] / df['dob_years'].shape[0]
print(f'A porcentagem de clientes com idade superior a 100 anos é {up_years:.2%}.')
print(f'A porcentagem de clientes com idade igual ou inferior a 0 (zero) anos é {do_years:.2%}.')


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Verificar a coluna `family_status` e resolver possíveis problemas.

# In[38]:


# Verificar os valores da coluna
print(df['family_status'].unique())
print()
print(df['family_status'].describe())
print()
print(df.groupby('family_status')['family_status_id'].count())
print()
fstatus_pivot = df.pivot_table(index='family_status', values='family_status_id', aggfunc='mean')
print(fstatus_pivot)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Num primeiro momento, não há problemáticas apresentadas por essa variável. Apesar das leis brasileiras considerarem união civil (`civil partnership`) algo intrínseco ao casamento (`married`), devemos levar em consideração a coleta dos dados ter sido feito no idioma inglês. Desse modo, o órgão governamental norte americano CDC — _Center for Disease Control and Prevention_, através da _National Center for Health Statistics_ mantém as mesmas indicações em seus relatórios anuais.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Verificar a coluna `gender` e resolver possíveis problemas.

# In[39]:


# Verificar os valores na coluna
print(df['gender'].unique())
print()
print(df['gender'].describe())
print()
print(df.groupby('gender')['family_status'].count())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Há apenas um valor discrepante, sem indicação de gênero. Nesse caso, realiza-se a exclusão da linha por não ter representatividade na quantidade total dos dados.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[40]:


# remover a linha problemática
df.drop(df[df['gender']=='XNA'].index, inplace = True)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[41]:


# Verificar o resultado
print(df['gender'].unique())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Verificar a coluna `income_type` e resolver possíveis problemas.

# In[42]:


# Verificar os valores na coluna
print(df['income_type'].unique())
print()
print(df['income_type'].describe())
print()
print(df.groupby('income_type')['gender'].count())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Vale ressaltar que `income_type` representa o tipo de emprego que o cliente do banco possui. Temos aqui a existência de duplicatas implícitas, uma vez que `business` e `entrepreneur` representam clientes do banco que possuem empresas — empresários. Nesse caso, a melhor tratativa é unir esses dados apenas na variável `business`, pois é a mais representativa no conjunto de dados.
# 
# Outro ponto a corrigir é a inexpressiva quantidade de clientes em `unemployed`, `student` e `paternity / maternity leave`, não justificando a criação de variáveis para essas categorias. Assim, excluo essas três categorias, totalizando quatro linhas, uma vez que não representam um tipo de emprego que a variável `income_type` descreve.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[43]:


# Agrupar entrepreneur à business
df['income_type'] = np.where(df['income_type']=='entrepreneur','business', df['income_type'])

# Excluir linhas que não representam a variável income_type
df['income_type']=np.where(df['income_type']=='unemployed', np.nan, df['income_type'])
df['income_type']=np.where(df['income_type']=='student', np.nan, df['income_type'])
df['income_type']=np.where(df['income_type']=='paternity / maternity leave', np.nan, df['income_type'])
df = df.dropna(subset=['income_type'])


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[44]:


# Verifcar o resultado
print(df['income_type'].unique())
print()
print(df['income_type'].describe())
print()
print(df.groupby('income_type')['gender'].count())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Verificar se temos duplicatas nos dados.

# In[45]:


# Verificar duplicatas
display(df[df.duplicated()])


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Apesar de identificarmos 71 linhas com valores duplicados, não é correto fazer a exclusão deles, uma vez que não temos nenhuma variável de identificação única do cliente, como um `client_id` por exemplo. Além disso, essas duplicatas se concentram, em sua maioria, por causa da normalização realizada nos valores extremos de `days_employed`, bem como na ausência de valores em `total_income`, que poderiam nos ajudar a identificar se essas duplicatas são dos mesmos clientes ou aleatoriedade dos dados.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto. Concordo com sua justificativa.
# 
# </div>
# 

# In[46]:


#Verifique o tamanho do conjunto de dados que você tem agora após suas primeiras manipulações com ele
df.info()


# Depois das primeiras tratativas nos dados, temos um DataFrame com quatro linhas nulas, que serão tratas adiante. As variáveis `days_employed` e `total_income` ainda possuem valores ausentes e estão com o tipo _float_, devemos alterar o tipo de dados para inteiros também. As alterações realizadas não chegam a 2% do total dos dados.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# ## Trabalhando com valores ausentes

# Tabelas de referências auxiliam na consulta de dados. Duas variáveis possuem atributos associados aos seus IDs. É importante verificar se temos coerência entre esses atributos. As variáveis são `family_status_id` e `education_id`.

# In[47]:


# Verificar dicionários de variáveis
print(df.groupby('education_id')['education'].unique())
print()
print(df.groupby('family_status_id')['family_status'].unique())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto. Porém, você não precisa do groupby. Basta df['education'].unique()
# 
# </div>
# 

# Assim, verificamos que temos apenas valores únicos relacionados a um único id em suas variáveis correspondentes.

# ### Restaurar valores ausentes em `total_income`

# Os valores ausentes estão concentrados nas variáveis `days_employed` e `total_income`. Devemos excluir as linhas com todos os valores nulos do DataFrame e preencher os valores faltantes nas variáveis com valores ausentes.
# 
# É importante criar categoria de dados para os clientes, assim facilitamos as estratégias e cálculos para os valores ausentes. Nesse sentido, uma forma de categorizar a idade dos clientes, na variável `days_employed`, segundo _Statistique Canada_, é agrupar nas seguintes maneiras:
# * children: clientes de 0-14 anos.
# * youth: clientes de 15-24 anos.
# * adults: clientes de 25-64 anos.
# * seniors: clientes acima de 65 anos.

# In[48]:


# Função que calcula a categoria de idade
def age_group(age):
    if age < 15:
        return 'children'
    elif (age > 14) and (age < 25):
        return 'youth'
    elif (age > 24) and (age < 65):
        return 'adults'
    else:
        return 'seniors'    


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[49]:


# Testar a função
print(age_group(10))
print(age_group(17))
print(age_group(60))
print(age_group(73))


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[50]:


# Criar coluna nova com base na função
df['age_group'] = df['dob_years'].apply(age_group)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[51]:


# Verificar como os valores na nova coluna
df['age_group']


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Das variáveis disponíveis no DataFrame, os fatores que podem influenciar o nível de renda do indivíduo, num primeiro momento, são:
# * Escolaridade (`education`): quanto maior o grau acadêmico, maior a tendência de ter melhores salários.
# * Sexo (`gender`): inúmeros estudos comporvam a discrepância entre salários de trabalhadores de sexo diferente.
# * Tipo de Renda (`income_type`): certos cargos, empregos e hierarquias patronais possibilitam alcançar patamares superiores de renda quando comparados aos trabalhadores comuns.
# 
# Dias Trabalhados (`days_employed`) é uma variável que se supõe imaginar que, quanto mais se trabalha, mais se ganha. Porém essa variável também necessita ter seus valores ausentes preenchidos, de tal modo que não podemos utilizá-la, pois estaríamos correndo o risco de viés nos dados.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[52]:


# Matriz de correlão entre as variáveis númericas
display(df.corr())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# As variáveis númericas que mais se correlacionam com `toal_income` são `education_id` e `days_employed`.
# Agora vamos criar uma tabela que tenha apenas dados sem valores ausentes. Esses dados serão usados para restaurar os valores ausentes, através de suas estatísticas descritivas.

# In[53]:


# Criar uma tabela sem valores ausentes
df_not_nan = df[df['total_income'].isnull()==False]
print(df_not_nan.head())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[54]:


# Verificar que não há valores ausentes
df_not_nan.isna().sum()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[55]:


# Valores médios de renda com base na educação
print(df_not_nan.groupby('education')['total_income'].mean())
print('*'*35)
# Valores medianos de renda com base na educação
print(df_not_nan.groupby('education')['total_income'].median())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Fica evidente que as menores rendas estão concentradas na educação primária e secundária — 21144 e 24596, respectivamente —, enquanto as maiores rendas estão centradas em clientes que possuem algum nível superior. Essa variável será levada em consideração para cálculo de preenchimento dos valores ausentes.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[56]:


# Valores médios de renda com base no grupo de idade
print(df_not_nan.groupby('age_group')['total_income'].mean())
print('*'*35)
# Valores medianos de renda com base no grupo de idade
print(df_not_nan.groupby('age_group')['total_income'].median())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Apesar do grupo de adultos terem renda média superior aos grupos restantes, isso se deve pelo intervalo desse grupo ser o maior entre todos, compreende os anos de 25 a 64 anos. A base de dados também não favorece os outros dois grupos: os dados para _youth_ só iniciam da idade 19, enquanto os dados para _seniors_ só atingem a idade 73. Essa variável **não** será levada em consideração para cálculo de preenchimento dos valores ausentes.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[57]:


# Valores médios de renda com base em gênero
print(df_not_nan.groupby('gender')['total_income'].mean())
print('*'*35)
# Valores medianos de renda com base em gênero
print(df_not_nan.groupby('gender')['total_income'].median())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# É perceptível que clientes do sexo feminino possuem renda até 20% inferior que a renda dos clientes masculinos. Variável será levada em consideração para cálculo de preenchimento dos valores ausentes.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[58]:


# Valores médios de renda com base no tipo da renda
print(df_not_nan.groupby('income_type')['total_income'].mean())
print('*'*35)
# Valores medianos de renda com base no tipo da renda
print(df_not_nan.groupby('income_type')['total_income'].median())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Empresários são os tipos de renda que mais ganham, enquanto aposentados são os que menos ganham. Desse modo, confirmam os dados de que aposentados sofrem com reduções substanciais em suas rendas. Essa variável será levada em consideração para cálculo de preenchimento dos valores ausentes.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[59]:


# Valores médios de renda com base no status familiar
print(df_not_nan.groupby('family_status')['total_income'].mean())
print('*'*35)
# Valores medianos de renda com base no status familiar
print(df_not_nan.groupby('family_status')['total_income'].median())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Há um nivelamento da renda quando a ótica é o status familiar, não há indícios de que a renda do indivíduo possa ser influenciada por seu status familiar. Essa variável **não** será levada em consideração para cálculo de preenchimento dos valores ausentes.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Já sabemos que características como o tipo de trabalho `income_type`, nível educacional `education` e gênero `gender` influenciam a renda do indivíduo.
# Como a variável `total_income` possui valores com grande variação entre mínimo e máximo, a literatura sugere a utilização da mediana para atenuar os valores extremos. A média ficaria muito influenciada por esses valores discrepantes.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[60]:


# Verificar a mediana dos dados considerando as variáveis de estudo
df.groupby(['education','gender','income_type'])['total_income'].median()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[61]:


# Criar os valores para substituir os valores ausentes
values_total_income = df.groupby(['education','gender','income_type'])['total_income'].transform('median')
print(values_total_income)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[62]:


# Substituir os valores ausentes
df['total_income'].fillna(values_total_income, inplace = True)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[63]:


# Verificar se há valores ausentes
df['total_income'].isna().sum()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[64]:


# Verificar se há algum erro
display(df.head(20))


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Difícil encontrar algum erro visualizando apenas 20 linhas. O ideal seria criar funções para validar.
# 
# </div>
# 

# In[65]:


# Verificar o número de entradas nas colunas
df.info()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# A variável `total_income` foi preenchida com a mediana do grupo das variáveis `education`, `gender` e `income_type`, tornando a variável livre de valores ausentes. `total_income` possui a mesma quantidade de entradas que as outras variáveis, com excessão de `days_employed` que trataremos adiante.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# ###  Restaurar valores em `days_employed`

# A variável `days_employed` representa a quantidade de dias trabalhados pelos clientes da base de dados. Essa variável deve ser positiva e inteira.
# As variáveis que podem sugerir uma melhor correlação com o número de dias trabalhado por alguém, são:
# * `children`: uma vez que a existência de filhos acarreta afastamento do trabalho, em sua esmagadora maioria para as mulheres.
# * `age_group`: entende-se que pessoas mais jovens possuem menos dias de trabalho.
# * `education`: pessoas com menos nível de estudo podem estar sujeitas ao risco do desemprego.
# * `gender`: mulheres que possuem filhos tendem a se afastar por mais tempo do mercado de trabalho.
# * `income_type`: trabalhadores públicos tendem a ficar mais tempo nos empregos, reformados e aposentados possuem como exigências um montante elevado de dias trabalhados.
# 
# Nesse sentido, vamos analisar a correlação entre as variáveis e `days_employed`.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[66]:


# matriz de correlação
display(df.corr())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# A variável `days_employed` possui maiores correlações absolutas com `dob_years`, `children` e `education_id`.
# Em parte, a alta correlação entre `dob_years` e `days_employed` se deve pelo ajuste realizado na quantidade de dias trabalhado que superavam os dias de vida dos clientes. Esse ajuste realizado nos clientes, que tinham mais dias trabalhados que dias de vida, acabou por fortalecer essa correlação.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[67]:


# Verificar se há valores ausentes
df['days_employed'].isna().sum()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[68]:


# Valores médios de dias de trabalho com base na quantidade de filhos
print(df_not_nan.groupby('children')['days_employed'].mean())
print('*'*35)
# Valores medianos de dias de trabalho com base na quantidade de filhos
print(df_not_nan.groupby('children')['days_employed'].median())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Então, não ter filhos parece justificar o aumento considerável na quantidade de dias trabalhado, quando comparado com pessoas com filhos (qualquer quantidade). Criar uma variável binária que represente se o indivíduo tem ou não filhos pode ser uma boa solução para a utilização dessa variável.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[69]:


# Criar a coluna "parents"
df['parents'] = np.where(df['children']>0, 1, 0)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto. Porém, pode ser mais direto: df['parents'] = df['children']>0
# 
# </div>
# 

# In[70]:


# Valores médios de dias de trabalho com base se tem ou não filhos
print(df.groupby('parents')['days_employed'].mean())
print('*'*35)
# Valores medianos de dias de trabalho com base na quantidade de filhos
print(df.groupby('parents')['days_employed'].median())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Agora já podemos usar a nova variável `parents` para auxiliar no preenchimento dos valores ausentes em `day_employed`.

# In[71]:


# Valores médios de dias de trabalho com base no grupo de idade
print(df.groupby('age_group')['days_employed'].mean())
print('*'*35)
# Valores medianos de dias de trabalho com base no grupo de idade
print(df.groupby('age_group')['days_employed'].median())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Como esperado, maiores idades correspondem a uma maior quantidade de dias trabalhados. `age_group` será utilizada.

# In[72]:


# Valores médios de dias de trabalho com base em educação
print(df.groupby('education')['days_employed'].mean())
print('*'*35)
# Valores medianos de dias de trabalho com base em gênero
print(df.groupby('education')['days_employed'].median())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Em média, pessoas com educação primária tem quase tantos dias de trabalho quanto pessoas com nível superior. Os dados não sugerem, de forma tão contundente, que os dias trabalhados possam estar diretamente correlacionados com o nível acadêmico. Essa variável **não** será utilizada.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[73]:


# Valores médios de dias trabalhados com base no tipo de emprego
print(df.groupby('income_type')['days_employed'].mean())
print('*'*35)
# Valores medianos de dias trabalhados com base no tipo de emprego
print(df.groupby('income_type')['days_employed'].median())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Como esperado, reformados possuem mais dias de trabalho que outros tipos de trabalhos. Funcionários públicos também tendem a ficar mais tempo. Essa variável será utilizada.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[74]:


# Valores médios de dias trabalhados com base no gênero
print(df.groupby('gender')['days_employed'].mean())
print('*'*35)
# Valores medianos de dias trabalhados com base no gênero
print(df.groupby('gender')['days_employed'].median())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Homens possuem mais dias trabalhados que mulheres, uma das causas principais pode ser por causa dos filhos. Nesse sentido, tanto a variável `gender` como a variável `parents` serão utilizados para preencher valores ausentes em `days_employed`.
# 
# A mediana ainda é a melhor estatística para substituir os valores ausentes em `days_employed`, uma vez que suavizaria os dados e evitaria a influência dos _outliers_ caso utilizássemos a média.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[75]:


# Verificar a mediana dos dados considerando as variáveis de estudo
df.groupby(['income_type','age_group','gender', 'parents'])['days_employed'].median()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# O agrupamento acima revela que as variáveis `parents` e `gender` são bem similares e possuem maiores discrepâncias nos grupos de idade mais jovens. Para evitar multicolinariedade entre essas duas variáveis é preferível remover uma delas. Desse modo, ficaremos apenas com as variáveis `income_type`, `age_group` e `gender` para preencher os valores ausentes.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[76]:


# Verificar a mediana com as variáveis propostas
df.groupby(['income_type','age_group','gender'])['days_employed'].median()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[77]:


# Criar os valores para substituir os valores ausentes
values_days_employed = df.groupby(['income_type','age_group','gender'])['days_employed'].transform('median')
print(values_days_employed)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[78]:


# Verificar se há valores ausentes
df['days_employed'].isna().sum()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[79]:


# Substituir os valores ausentes
df['days_employed'].fillna(values_days_employed, inplace = True)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[80]:


# Verificar se há valores ausentes
df['days_employed'].isna().sum()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Desse modo, temos todos os valores preenchidos e ausência de valores faltantes.

# In[81]:


# Alterar o tipo de dados em "days_employed" para inteiros
df['days_employed'] = df['days_employed'].astype('int')


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[82]:


# Verificar o número de entradas nas colunas
df.info()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# ## Categorização de Dados
# 
# Existem alguns dados que precisam ser categorizados para que os objetivos do estudo sejam atingidos. Até o momento já categorizamos:
# * `dob_years` agrupado em intervalos de idade através de `age_group`.
# * `children` transformada em variável binária, com ou sem filho, na varável `parents`.
# 
# Adiante serão categorizadas as variáveis `purpose` e `total_income`.

# In[83]:


# Exibir os valores dos dados selecionados para categorização
df['purpose'].value_counts()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[84]:


# Exibir valores únicos
print(df['purpose'].unique())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# Com base nas características únicas da variável `purpose`, podemos observar que existem quatro categorias principais nas quais podem resumir todos os dados dessa variável. Os quatro grupos são:
# * car: clientes que desejam adquirir um carro.	
# * house: clientes que desejam adquirir, renovar e/ou construir imóveis.
# * wedding: clientes que desejam casar-se.
# * education: clientes que desejam estudar.
# 
# Faz-se necessário categorizar os dados baseados nesses grupos.

# In[85]:


# Função para categorizar os dados com base em tópicos comuns
def purpose_categories(row):
    if 'car' in row['purpose']:
        return 'car'
    if 'hous' in row['purpose'] or 'prop' in row['purpose'] or 'real est' in row['purpose']:
        return 'house'
    if 'wedd' in row['purpose']:
        return 'wedding'
    if 'educ' in row['purpose'] or 'uni' in row['purpose']:
        return 'education'


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto. Parabéns. Elegante e eficiente!
# 
# </div>
# 

# In[86]:


# Coluna com as categorias
df['purpose_categories'] = df.apply(purpose_categories, axis=1)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[87]:


# Examinar todos os dados numéricos em sua coluna selecionada para categorização
df['purpose_categories'].value_counts()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[88]:


# Obter estatísticas resumidas para a coluna
print(df['purpose_categories'].describe())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# A categorização por renda será feita de acordo com os relatórios emitidos pela _Bureau of Economic Analysis_, departamento do comércio do governo norte americano.
# Temos uma divisão da renda individual, ou pessoal, da seguinte forma:
# * _rich_: clientes que estão no grupo de 1% renda mais elevadas. Quartil superior a 0.99.
# * _high middle class_: grupo de clientes no intervalo de renda entre os quartis 0.85 e 0.99.
# * _middle class_: grupo de clientes no intervalo de renda entre os quartis 0.6 e 0.85.
# * _lower middle class_: grupo de clientes no intervalo de renda entre os quartis 0.25 e 0.6.
# * _poor_: grupo de clientes com as 25% menores rendas. Quartil inferior a 0.25.

# In[89]:


# Quartis da renda
print(df['total_income'].quantile([0.1,0.25,0.5,0.6, 0.85,0.99]))
print()
print(df.boxplot(column=['total_income']))


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[90]:


# Função para categorização em diferentes grupos numéricos com base em intervalos
def income_class(income):
    if income < 17235:
        return 'poor'
    if (income >= 17235) and (income < 25707):
        return 'lower middle class'
    if (income >= 25707) and (income < 37957):
        return 'middle class'
    if (income >= 37957) and (income < 80819):
        return 'high middle class'
    if (income >= 80819):
        return 'rich'


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto. Porém, o ideal era não ter valores fixos
# 
# </div>
# 

# In[91]:


# Coluna com categorias
df['income_class'] = df['total_income'].apply(income_class)
#df['purpose_categories'] = df.apply(purpose_categories, axis=1)


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[92]:


# Valores de cada categoria para ver a distribuição
df['income_class'].value_counts()


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# ## Verificar as Hipóteses
# 

# **Existe uma correlação entre a quantidade de filhos e do pagamento em dia?**

# In[93]:


# Verificar os dados das crianças e do pagamento em dia
print(df.groupby(['children', 'parents'])['debt'].sum())
print('*'*35)
print(df.groupby(['children', 'parents'])['debt'].count())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[94]:


# Tabela com informações baseadas em "children"
pivot_children = df.pivot_table(index='children', columns='debt', values='days_employed', aggfunc='count')
pivot_children['defaulter_percent'] = pivot_children[1] / (pivot_children[1] + pivot_children[0])*100
pivot_children.sort_values(by='defaulter_percent')


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[95]:


# Tabela com informações baseadas em "parents"
pivot_parents = df.pivot_table(index='parents', columns='debt', values='days_employed', aggfunc='count')
pivot_parents['defaulter_percent'] = pivot_parents[1] / (pivot_parents[1] + pivot_parents[0])*100
pivot_parents.sort_values(by='defaulter_percent')


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# **Conclusão**
# 
# De acordo com os dados, não ter filhos aumentam ligeiramente suas chances de ser um bom adimplente. A quantidade de filhos não parece influenciar de forma significativa a inadimplência.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# **Existe uma correlação entre o status familiar e o pagamento em dia?**

# In[96]:


# Verificar os dados de status da família e do pagamento em dia
print(df.groupby('family_status')['debt'].sum())
print('*'*35)
print(df.groupby('family_status')['debt'].count())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[97]:


# Tabela com informações baseadas em "family_status"
pivot_status = df.pivot_table(index='family_status', columns='debt', values='days_employed', aggfunc='count')
pivot_status['defaulter_percent'] = pivot_status[1] / (pivot_status[1] + pivot_status[0])*100
pivot_status.sort_values(by='defaulter_percent')


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# **Conclusão**
# 
# Pessoas solteiras possuem uma propensão ligeiramente superior de inadimplência quando comparamos às pessoas casadas. Viúvos(as) são os que possuem menores índices de inadimplência.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# **Existe uma correlação entre o nível de renda e o pagamento em dia?**

# In[98]:


# Verificar os dados do nível de renda e do pagamento em dia
print(df.groupby('income_class')['debt'].sum())
print('*'*35)
print(df.groupby('income_class')['debt'].count())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[99]:


# Tabela com informações baseadas em "income_class"
pivot_class = df.pivot_table(index='income_class', columns='debt', values='days_employed', aggfunc='count')
pivot_class['defaulter_percent'] = pivot_class[1] / (pivot_class[1] + pivot_class[0])*100
pivot_class.sort_values(by='defaulter_percent')


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# **Conclusão**
# 
# Conforme a divisão de classes em `total_income` que produziu a variável `income_class`, temos que o nível de inadimplência não varia tanto entre as classes. Apesar dos ricos e da classe média alta estarem com os melhores índices de adimplência.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# **Como a finalidade do crédito afeta a taxa de inadimplência?**

# In[100]:


# Verificar os dados da finalidade de crédito e do pagamento em dia
print(df.groupby('purpose_categories')['debt'].sum())
print('*'*35)
print(df.groupby('purpose_categories')['debt'].count())


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[101]:


# Tabela com informações baseadas em "purpose_categories"
pivot_purpose = df.pivot_table(index='purpose_categories', columns='debt', values='days_employed', aggfunc='count')
pivot_purpose['defaulter_percent'] = pivot_purpose[1] / (pivot_purpose[1] + pivot_purpose[0])*100
pivot_purpose.sort_values(by='defaulter_percent')


# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# **Conclusão**
# 
# Os empréstimos com finalidade imobiliária, em sua maioria para aquisição de imóvel, possuem as menores taxas de inadimplência do conjunto de dados. Isso deve-se a garantia de crédito vinculada aos empréstimos imobiliários, uma vez que os imóveis podem ser liquidados para quitação desses mesmos empréstimos.
# 
# Porém, os empréstimos com finalidade de adquirir carros são os com maiores taxas de inadimplência, apesar da garantia do crédito ser o próprio carro, há uma depreciação enorme sobre o valor do bem, que muitas vezes mesmo após a liquidação do veículo, o dinheiro remanescente ainda é inferior ao saldo devedor do empréstimo contratado.
# 
# Empréstimos para educação e casamento não possuem garantias associadas, porém, este último, geralmente conta com a renda de duas pessoas para pagar as parcelas do empréstimo. Deixando assim, os empréstimos para educação com um dos índices mais altos de inadimplência junto com os empréstimos para aquisição de carros.

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Correto
# 
# </div>
# 

# In[102]:


df.info()


# ## Conclusão Geral 
# 
# Primeiramente foi iniciada a exploração dos dados, no qual foi possível ver os dados discrepantes e perceber a ausência de alguns valores nas variáveis. Após essa análise superficial, foi elencado as principais alterações que deveriam ser realizadas nas varáveis para que se consiga responder as questões propostas.
# 
# Ausência de valores, valores negativos, valores extremos e duplicatas explícitas e implícitas foram alguns dos problemas encontrados. Algumas suposições foram criadas, como por exemplo que os valores com idade igual a zero deviam ser por tratar-se de clientes que ainda não tinham atingido um ano de vida, porém conforme avançava na análise, entendeu-se que outras variáveis não corroboravam com a ideia inicial, como o fato desse cliente ter filho ou ser formado, por exemplo.
# 
# Os valores ausentes estavam concentrados e correlacionados com as variáveis de renda e dias de trabalho, possuíam as mesmas linhas com valores ausentes. Como esses valores ausentes correspondiam a 10.09% dos dados, decidiu-se por preenchê-los. Os valores ausentes não possuíam um padrão observável para sua existência na base de dados.
# 
# Os valores negativos foram tratados como valores absolutos, pois não há como tratar filhos negativos ou dias trabalhados negativos.
# 
# Em `days_employed` temos valores ausentes, números extremos — dias de trabalho que superam os dias de vida dos clientes —, bem como números negativos (não há dias trabalhados negativos). Esse percentual de valores negativos atinge 73.9% dos dados em dias trabalhados. Já a porcentagem de dias trabalhados que superam a idade do cliente é 16.00%.
# 
# Foi verificado que os clientes com informações de dias trabalhados que superam seus dias de vida estão concentrados, em sua totalidade, no grupo `retiree`. Foi utilizado a fórmula (`dob_years` - 18)*365 para substituir esses valores, baseados nos critérios do mercado de trabalho norte americano.
# 
# As 71 linhas duplicadas não foram tratadas por não haver indicações nos dados de que realmente os dados são dos mesmos clientes, uma vez que não temos um id_client.
# 
# Para manipular dados e responder as questões propostas, fez-se necessário categorizar a idade dos clientes em grupos. A categorização na motivação para conseguir empréstimo também foi realizada, já que havia duplicatas implícitas na variável `purpose`. Grupo de classes sociais foi categorizado e criado através da variável de renda, segundo os critérios da _Bureau of Economic Analysis_.
# 
# As variáveis que representam o tipo de trabalho `income_type`, nível educacional `education` e gênero `gender` influenciam a renda do indivíduo e foram utilizadas para preencher os valores ausentes em `total_income`.
# 
# Como a variável `total_income` possui valores com grande variação entre mínimo e máximo, a literatura sugere a utilização da mediana para atenuar os valores extremos. A média ficaria muito influenciada por esses valores discrepantes.
# 
# Grupo de idade, gênero e tipo de renda foram utilizados para preencher os valores ausentes em dias de trabalho `days_employed`.
# 
# As principais conclusões foram:
# 
# * Existe uma correlação entre a quantidade de filhos e do pagamento em dia?
# De acordo com os dados, não ter filhos aumentam ligeiramente suas chances de ser um bom adimplente. A quantidade de filhos não parece influenciar de forma significativa a inadimplência.
# 
# * Existe uma correlação entre o status familiar e o pagamento em dia?
# Pessoas solteiras possuem uma propensão ligeiramente superior de inadimplência quando comparamos às pessoas casadas. Viúvos(as) são os que possuem menores índices de inadimplência.
# 
# * Existe uma correlação entre o nível de renda e o pagamento em dia?
# Conforme a divisão de classes em `total_income` que produziu a variável `income_class`, temos que o nível de inadiplência não varia tanto entre as classes. Apesar dos ricos e da classe média alta estarem com os melhores índices de adimplência.
# 
# * Como a finalidade do crédito afeta a taxa de inadimplência?
# Os empréstimos com finalidade imobiliária, em sua maioria para aquisição de imóvel, possuem as menores taxas de inadimplência do conjunto de dados. Isso deve-se a garantia de crédito vinculada aos empréstimos imobiliários, uma vez que os imóveis podem ser liquidados para quitação desses mesmos empréstimos.
# 
# Porém, os empréstimos com finalidade de adquirir carros são os com maiores taxas de inadimplência, apesar da garantia do crédito ser o próprio carro, há uma depreciação enorme sobre o valor do bem, que muitas vezes mesmo após a liquidação do veículo, o dinheiro remanescente ainda é inferior ao saldo devedor do empréstimo contratado.
# 
# Empréstimos para educação e casamento não possuem garantias associadas, porém, este último, geralmente conta com a renda de duas pessoas para pagar as parcelas do empréstimo. Deixando assim, os empréstimos para educação com um dos índices mais altos de inadimplência junto com os empréstimos para aquisição de carros.
# 

# 
# <div class="alert alert-block alert-success">
# <b>Comentário Geral do Revisor</b> <a class="tocSkip"></a>
# 
# Obrigado por enviar seu projeto. 
#     
# Parabéns, você fez um excelente trabalho. Você responeu corretamente.
# 
# Você demonstrou conhecimento, boas habilidades investigativas e de codificação.úvida, não hesite em me contactar.
#     
# Desejo sucesso na jornada!
# </div>

# ## REFERÊNCIAS
# 
# * Bureau of Economic Analysis: Acesso em 20 de novmebro de 2022, em https://www.bea.gov/news/2022/personal-income-and-outlays-september-2022
# 
# * Center for Disease Control and Prevention: Acesso em 19 de novembro de 2022, em https://www.cdc.gov/nchs/hus/sources-definitions/marital-status.htm
# 
# * Statistique Canada: Acesso em 20 de nomvembro de 2022, em https://www.statcan.gc.ca/en/concepts/definitions/age2
# 
# 

# <div class="alert alert-block alert-success">
# <b> Comentário do revisor: </b> <a class="tocSkip"></a>
# 
# Muito legal a seção de referências, pois ajuda a dar credibilidade ao trabalho.
# 
# </div>
# 
