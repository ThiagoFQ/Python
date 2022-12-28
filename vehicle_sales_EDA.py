#!/usr/bin/env python
# coding: utf-8

# # Quais fatores que influenciam a venda de um veículo?
# 
# A base de dados para análise, trata-se de centenas de anúncios gratuitos de veículos publicados diariamente ao longo de um ano, maio de 2018 a abril de 2019. o objetivo aqui é determinar quais os principais fatores, dentro da base de dados, que influenciam o preço do veículo.

# Para atingir esse objetivo, é preciso explorar os dados, cuidar de valores problemáticos, como valores ausentes ou duplicados. Além de criar variáveis e gráficos que facilitem a leitura e compreensão das análises. Tratar os valores atípicos também será imprescindível.

# ## Introdução

# In[1]:


# Bibliotecas
import pandas as pd
pd.set_option('display.max_columns', 999)
import numpy as np
import datetime as dt

# Bibliotecas de plots
import matplotlib.pyplot as plt
import seaborn as sns

# Formatação de estilo
sns.set_style('darkgrid')
sns.set_palette('hls')
sns.set_context("notebook", font_scale = 1.5, rc={"lines.linewidth": 2})


# ### Dados

# In[2]:


# Carregar o arquivo com os dados em um DataFrame
df = pd.read_csv('/datasets/vehicles_us.csv')


# ### Explorando os dados iniciais

# As características dos veículos são do momento em que o anúncio foi publicado no site.
# O conjunto de dados contém os seguintes campos:
# - `price` — preço do veículo.
# - `model_year` — ano de fabricação.
# - `model` — modelo do veículo.
# - `condition` — condição de conservação do veículo.
# - `cylinders` — quantidade de cilindros existentes no motor do veículo.
# - `fuel` — tipo de combustível utilizado no veículo.
# - `odometer` — quilometragem do veículo.
# - `transmission` — tipo de transmissão existente no veículo.
# - `type` — tipo da carroceria do veículo.
# - `paint_color` — cor predominante do veículo.
# - `is_4wd` — se o veículo é 4 por 4.
# - `date_posted` — data que o anúncio foi publicado.
# - `days_listed` — quantidade de dias da publicação a retirada do anúncio.

# In[3]:


# Informações gerais/resumidas sobre o DataFrame
print(df.info())


# In[4]:


# Amostragem dos dados
display(df)


# Temos um DataFrame com 51525 linhas e 13 colunas. 
# As seguintes variáveis possuem valores ausentes ou estão com seus tipos classificados de forma errada:
# * `model_year`: valores ausentes, seu tipo deve ser datetime.
# * `cylinders`: valores ausentes, seu tipo deve ser inteiro.
# * `odometer`: valores ausentes, seu tipo deve ser inteiro.
# * `paint_color`: valores ausentes.
# * `is_4wd`: valores ausentes, seu tipo deve ser booleano.
# * `date_posted`: seu tipo deve ser datetime.
# * `days_listed`: seu tipo deve ser datetime.
# 
# As variáveis `fuel`, `transmission` e `is_4wd` sugerem ser do tipo lógico (boolean), será preciso investigá-las melhor. Tembém é preciso veirificar a existência de duplicatas.

# ### Existência de duplicatas

# In[5]:


# Verificar a existência de duplicatas
df.duplicated().sum()


# In[6]:


# Verificar a existência de duplicatas implícitas em 'model'
df['model'].sort_values().unique()


# A variável `model` apresenta duplicatas implícitas em:
# * ford f150: ford f-150.
# * ford f250: ford f-250.
# * ford f250 sd: ford f250 super duty, ford f-250 super duty, ford f-250 sd.
# * ford f350: ford f-350.
# * ford f350 sd: ford f-350 sd, ford f350 super duty.

# In[7]:


# Corrigir duplicatas implícitas
df['model'] = df['model'].replace('ford f-150', 'ford f150')
df['model'] = df['model'].replace('ford f-250', 'ford f250')
df['model'] = df['model'].replace(['ford f250 super duty','ford f-250 super duty', 'ford f-250 sd'], 'ford f250 sd')
df['model'] = df['model'].replace('ford f-350', 'ford f350')
df['model'] = df['model'].replace(['ford f350 super duty','ford f-350 sd'], 'ford f350 sd')


# In[8]:


# Verificar a existência de duplicatas implícitas em 'condition'
df['condition'].sort_values().unique()


# In[9]:


# Verificar a existência de duplicatas implícitas em 'cylinders'
df['cylinders'].sort_values().unique()


# In[10]:


# Verificar a existência de duplicatas implícitas em 'fuel'
df['fuel'].sort_values().unique()


# In[11]:


# Verificar a existência de duplicatas implícitas em 'transmission'
df['transmission'].sort_values().unique()


# In[12]:


# Verificar a existência de duplicatas implícitas em 'type'
df['type'].sort_values().unique()


# In[13]:


# Verificar a existência de duplicatas implícitas em 'paint_color'
df['paint_color'].sort_values().unique()


# In[14]:


# Verificar a existência de duplicatas implícitas em 'is_4wd'
df['is_4wd'].sort_values().unique()


# Entre todas as variáveis passíveis de duplicatas implícitas, apenas a variável `model` as possuia. Depois da correção, o DataFrame ficou livre de duplicatas. Porém, em `is_4wd` pode-se observar a presença de apenas um valor único, sugerindo que os valores ausentes são os dados 0 (zero) de uma variável lógica (booleana). 
# 
# Já as variáveis `fuel` e `transmission` revelam que não são do tipo *bool*, e sim *string*.

# ### Existência de valores ausentes

# In[15]:


# Verificar o percentual de valores ausentes
df.isna().mean()


# Apenas cinco colunas apresentam valores ausentes. A variável `is_4wd` possui mais de 50% de seus dados ausentes, enquanto a variável `model_year` possui apenas 7% de valores ausentes.

# ### Conclusões e próximos passos
# 
# Com a existência de valores ausentes será necessário uma análise aprofundada para um possível preenchimento desses valores.
# 
# O tipo dos dados das variáveis também merecem atenção e serão tratados adiante, uma vez que muitas colunas estão com dados com tipos incorretos.
# 
# Uma outra análise que será realizada é o tratamento dos valores atípicos.

# ## Valores ausentes

# As seguintes colunas possuem valores ausentes: `model_year`, `cylinders`, `odometer`, `paint_color` e `is_4wd`.

# In[16]:


# Correlação entre as variáveis do DataFrame
print(df.corr())


# In[17]:


# Verificar a existência de tendência que justifique os valores ausentes em 'model_year'
print(f'O percentual de valores ausentes na coluna model_year: {df["model_year"].isna().mean():.2%}.')
display(df[df['model_year'].isna()])
print((df[df["model_year"].isna()]["model"].value_counts()/df["model"].value_counts()).sort_values(ascending=False))


# In[18]:


# Verificar a mediana dos dados
print(df.groupby(['model'])['model_year'].median())


# In[19]:


# Substituir os valores ausentes
values_model_year = df.groupby(['model'])['model_year'].transform('median')
df['model_year'].fillna(values_model_year, inplace = True)
df['model_year'].isna().sum()


# É razoável pensar que algum modelo de veículo esteja dominando os valores ausentes na variável `model_year`. Porém, após análise, não parece existir alguma tendência que justifique a falta de valores na variável que representa o ano do modelo do veículo. Poucos são os modelos de veículos (`model`) que possuem percentual superior a média de valores nulos em `model_year`.
# 
# É consenso comum inferir que o modelo do veículo (`model`) inclui algumas características típicas, como a quantidade de cilindros (`cylinders`), o tipo de combustível (`fuel`), o tipo de transmissão (`transmission`) e se o veículo é ou não 4x4 (`is_4wd`). A variável modelo (`model`) é uma forte candidata a ser utilizada para preencher valores ausentes em `model_year`. O preço do veículo (`price`) também sofre enorme influência das características do veículo, bem como o estado de conservação (`condition`) e o ano do modelo (`model_year`).

# In[20]:


# Verificar a existência de tendência que justifique os valores ausentes em 'cylinders'
print(f'O percentual de valores ausentes na coluna cylinders: {df["cylinders"].isna().mean():.2%}.')
display(df[df['cylinders'].isna()])
print((df[df["cylinders"].isna()]["model"].value_counts()/df["model"].value_counts()).sort_values(ascending=False))


# In[21]:


# Verificar a mediana dos dados
print(df.groupby(['model'])['cylinders'].median())


# In[22]:


# Substituir os valores ausentes
values_cylinders = df.groupby(['model'])['cylinders'].transform('median')
df['cylinders'].fillna(values_cylinders, inplace = True)
df['cylinders'].isna().sum()


# Mais uma vez, utiliza-se o modelo dos veículos para preencher os valores ausentes em `cylinders`, uma vez que os modelos determinam a fabricação e características do motor, como por exemplo a quantidade de cilindros.

# In[23]:


# Verificar a existência de tendência que justifique os valores ausentes em 'odometer'
print(f'O percentual de valores ausentes na coluna odometer: {df["odometer"].isna().mean():.2%}.')
display(df[df['odometer'].isna()])
print((df[df["odometer"].isna()]["model"].value_counts()/df["model"].value_counts()).sort_values(ascending=False))


# In[24]:


# Verificar a mediana dos dados
print(df.groupby(['condition'])['odometer'].median())


# In[25]:


# Substituir os valores ausentes
values_odometer = df.groupby(['condition'])['odometer'].transform('median')
df['odometer'].fillna(values_odometer, inplace = True)
df['odometer'].isna().sum()


# Entende-se que a conservação do veículo revela o estado de preservação e, consequentemente, o nível de desgaste que o veículo sofreu ao longo dos anos. Um dos maiores fatores que afetam a depreciação do veículo é a quilometragem, uma vez que grandes quantidades de distâncias percorridas por um veículo ocasiona a entropia nas peças e acessórios do carro. 
# 
# Logo, um veículo com baixa quilometragem mantém seu estado de "novo" por mais tempo, enquanto um veículo com alta quilometragem está sujeito aos danos ocasionados pela depreciação. Assim, utiliza-se a variável `condition` para preencher os valores ausentes em `odometer`.

# In[26]:


# Verificar a existência de tendência que justifique os valores ausentes em 'paint_color'
print(f'O percentual de valores ausentes na coluna paint_color: {df["paint_color"].isna().mean():.2%}.')
display(df[df['paint_color'].isna()])
print((df[df["paint_color"].isna()]["model"].value_counts()/df["model"].value_counts()).sort_values(ascending=False))


# In[27]:


# Verificar a moda dos dados
print(df.groupby(['model'])['paint_color'].agg(pd.Series.mode))


# In[28]:


# Substituir os valores ausentes
values_paint_color = df.groupby(['model'])['paint_color'].transform(lambda x : x.mode()[0])
df['paint_color'].fillna(values_paint_color, inplace = True)
df['paint_color'].isna().sum()


# O preenchimento dos valores nulos dessa variável é o mais complexo, uma vez que os mesmos modelos de carros podem ter variadas cores, sem falar que os proprietários podem alterar a cor original que sai com a fabricação do modelo do carro.
# 
# Nesse sentido, e de forma a não precisar excluir quase 18% das linhas do DataFrame ou excluir a coluna `paint_color`, ou até mesmo definir como *unknown* os valores ausentes, utiliza-se um preenchimento baseado na cor do modelo do carro que mais aparece entre as cores do modelo daquele veículo — com maior frequência absoluta (moda).
# 
# Poderíamos pensar que bastava a exclusão da coluna `paint_color` para continuar a análise, ou qualquer umas das saídas sugeridas acima, porém, conforme estudo realizado pela *IseeCars* em 2022, a cor do carro usado influência no preço de venda. Então, segundo o estudo, carros com cores mais tradicionais são mais procurados, assim afetando o preço da venda pela demanda produzida por aquela cor, em contrapartida carros com cores mais exóticas e diferentes sofrem com dificuldades no pós-venda.

# In[29]:


# Verificar a existência de tendência que justifique os valores ausentes em 'is_4wd'
print(f'O percentual de valores ausentes na coluna is_4wd: {df["is_4wd"].isna().mean():.2%}.')
display(df[df['is_4wd'].isna()])
print(df["is_4wd"].unique())


# In[30]:


# Substituir os valores ausentes
df['is_4wd'].fillna(0, inplace = True)
df['is_4wd'].isna().sum()


# A variável `is_4wd` é do tipo *boolean* e assume apenas valores 1 (o veículo é um 4x4), ou 0 (o veículo não é um 4x4). Desse modo, entende-se que todos os valores ausentes dessa variável devam ser substituídos por 0 (zero).

# In[31]:


# Verificar valores ausentes
df.isna().sum()


# ## Tipos de dados

# Segue-se com a alteração do tipo dos dados das variáveis:
# * `model_year` — data.
# * `cylinders` — apenas pode assumir valores inteiros positivos.
# * `odometer` — apenas pode assumir valores inteiros positivos.
# * `is_4wd` — variável lógica de presença ou ausência de característica.
# * `date_posted` — data.

# In[32]:


# Alterar o tipo das variáveis
df['model_year'] = pd.to_datetime(arg=df['model_year'], format="%Y")
df['cylinders'] = df['cylinders'].astype('int')
df['odometer'] = df['odometer'].astype('int')
df['is_4wd'] = df['is_4wd'].astype('bool')
df['date_posted'] = pd.to_datetime(arg=df['date_posted'], format="%Y-%m-%d")


# ## Melhorando os dados

# Faz-se necessário a criação de novas variáveis para facilitar a manipulação dos dados e resoluções de problemas.

# In[33]:


# Adicionar coluna de 'week_day', 'month' e 'year' quando da postagem do anúncio
df['year_posted'] = df['date_posted'].dt.year
df['month_posted'] = df['date_posted'].dt.month
df['week_day_posted'] = df['date_posted'].dt.day_name()


# In[34]:


# Adicionar a idade do veículo, em anos, quando da postagem do anúncio
df['vehicle_age_year'] = (df['date_posted']-df['model_year'])/pd.Timedelta(days=365)

# Evitar a divisão por zero
for age in df['vehicle_age_year']:
    if age==0:
        df['vehicle_age_year'] = df['vehicle_age_year']+0.00001
    else:
        df['vehicle_age_year'] = df['vehicle_age_year']


# In[35]:


# Adicionar a quilometragem média por ano
df['odometer_year'] = (df['odometer']/df['vehicle_age_year']).round()
df['odometer_year'] = df['odometer_year'].astype('int')


# In[36]:


# Função para substituir os valores em 'condition' por categorias numéricas ordenadas
def condition_categorical(condition):
    if condition == 'new':
        return 5
    elif condition == 'like new':
        return 4
    elif condition == 'excellent':
        return 3
    elif condition == 'good':
        return 2
    elif condition == 'fair':
        return 1
    elif condition == 'salvage':
        return 0


# In[37]:


# Substituir valores em 'condition'
df['condition'] = df['condition'].apply(condition_categorical)
df['condition'] = df['condition'].astype('str')


# ## Dados limpos

# Agora com os dados limpos, é importante ver o que temos para realizar as análises futuras.

# In[38]:


# imprima as informações gerais/resumidas sobre o DataFrame
df.info()


# In[39]:


# imprima uma amostragem dos dados
display(df)


# ## Parâmetros fundamentais
# 
# Para visualizar os parâmetros a seguir, utiliza-se de gráficos de contagem e de quartis, histogramas e boxplots.
# 
# Os parâmetros são:
# - Preço: `price`.
# - A idade do veículo quando a propaganda foi colocada: `vehicle_age_year`.
# - Quilometragem: `odometer`.
# - Número de cilindros: `cylinders`.
# - Condição: `condition`.

# In[67]:


# Histograma dos parâmetros
plt.figure(figsize = ((22, 16)))
plt.suptitle("Histogramas", fontsize = 26)
# Parâmetro 'price'
plt.subplot(2, 3, 1)
plt.hist(df['price'], bins=100, color='b')
plt.title("Contagem de Preço", fontsize = 16)
plt.ylabel('Veículos')
plt.xlabel('Preço (usd)')
# Parâmetro 'vehicle_age_year'
plt.subplot(2, 3, 2)
plt.hist(df['vehicle_age_year'], bins=30, color='b')
plt.title('Contagem de Idade do Veículo', fontsize = 16)
plt.ylabel('Veículos')
plt.xlabel('Idade (anos)')
# Parâmetro 'odometer'
plt.subplot(2, 3, 5)
plt.hist(df['odometer'], bins=30, color='b')
plt.title('Contagem de Quilometragem', fontsize = 16)
plt.ylabel('Veículos')
plt.xlabel('Quilometragem');
# Parâmetro 'cylinders'
plt.subplot(2, 3, 4)
df.groupby('cylinders')['model'].count().plot(kind='bar')
plt.title('Contagem de Cilindros', fontsize = 16)
plt.ylabel('Veículos')
plt.xticks(rotation = 0)
plt.xlabel('Cilindros');
# Parâmetro 'condition'
plt.subplot(1, 3, 3)
df.groupby('condition')['model'].count().plot(kind='bar')
plt.title(f'Contagem de Condição', fontsize = 16)
plt.ylabel('Veículos')
plt.xlabel('Condição')
plt.xticks(rotation = 0);

plt.show()


# Os histogramas acima revelam valores atípicos nas variáveis `price`, `odometer` e `vehicle_age_year`, variáveis com barras em azul. A seguir identifica-se esses valores atípicos, remove-os e cria-se uma DataFrame com os dados filtrados.

# In[41]:


# Boxplot dos parâmetros
plt.figure(figsize = ((16, 10)))
plt.suptitle("Boxplots", fontsize = 26)
# Parâmetro 'price'
plt.subplot(3, 1, 3)
sns.boxplot(data=df[["price"]], orient="h", showmeans=True);
plt.title(f'Contagem de Preço', fontsize = 16)
plt.yticks(rotation = 90)
plt.subplot(2, 2, 1)
sns.boxplot(data=df[["odometer"]], orient="h", showmeans=True);
plt.title(f'Contagem de Quilometragem', fontsize = 16)
plt.yticks(rotation = 90)
plt.subplot(2, 2, 2)
sns.boxplot(data=df[["vehicle_age_year"]], orient="h", showmeans=True);
plt.title(f'Contagem de Idade do Veículo', fontsize = 16)
plt.yticks(rotation = 90)
plt.show()


# ## Valores atípicos
# 
# Uma das melhores formas de encontrar os valores atípicos é observar os valores mínimos e máximos através do intervalo interquartil (IQR). Sua fórmula é: IQR = 3Q - 1Q.

# ![image.png](attachment:image.png)

# In[42]:


# Calcular IQR das variáveis
IQR_price = (df['price'].quantile(0.75))-(df['price'].quantile(0.25))
IQR_vehicle_age_year = (df['vehicle_age_year'].quantile(0.75))-(df['vehicle_age_year'].quantile(0.25))
IQR_odometer = (df['odometer'].quantile(0.75))-(df['odometer'].quantile(0.25))


# In[43]:


# Determinar o limite inferior para valores atípicos
price_min = df['price'].quantile(0.25)-1.5*IQR_price
vehicle_age_year_min = df['vehicle_age_year'].quantile(0.25)-1.5*IQR_vehicle_age_year
odometer_min = df['odometer'].quantile(0.25)-1.5*IQR_odometer

print(f'O preço dos veículos possuem um limite inferior de {price_min} dólares. A idade dos veículos até o anúncio ser postado tem limite inferior de {vehicle_age_year_min:.2} anos. O limite inferior da quilometragem dos veículos é {odometer_min}km.')


# Como os valores do limite inferior são negativos e não há possibilidade dessas variáveis assumirem valores negativos, pode-se afirmar que não há valores extremos/atípicos inferior.

# In[44]:


# Determinar o limite superior para valores atípicos
price_max = df['price'].quantile(0.75)+1.5*IQR_price
vehicle_age_year_max = df['vehicle_age_year'].quantile(0.75)+1.5*IQR_vehicle_age_year
odometer_max = df['odometer'].quantile(0.75)+1.5*IQR_odometer

print(f'O preço dos veículos possuem um limite superior de {price_max} dólares. A idade dos veículos até o anúncio ser postado tem limite superior de {vehicle_age_year_max:.3} anos. O limite superior da quilometragem dos veículos é {odometer_max}km.')


# In[45]:


# Armazenar os dados sem os valores atípicos em um DataFrame separado
df_standard = df.query('(price<@price_max) and (vehicle_age_year<@vehicle_age_year_max) and (odometer<@odometer_max)')


# In[46]:


# Tamanho do DataFrame
print(f'O DataFrame filtrado df_standard possui {(len(df_standard)/len(df)):.2%} do Dataframe original, df.')


# ## Parâmetros fundamentais sem valores atípicos

# Com o novo DataFrame filtrado sem os valores atípicos, faz-se necessário criar novamente os gráficos e comparar com os gráficos anteriores.

# In[47]:


# Boxplot dos parâmetros sem valores atípicos
plt.figure(figsize = ((16, 10)))
plt.suptitle("Boxplots", fontsize = 26)
# Parâmetro 'price'
plt.subplot(3, 1, 3)
sns.boxplot(data=df_standard[["price"]], orient="h", showmeans=True);
plt.title(f'Contagem de Preço', fontsize = 16)
plt.yticks(rotation = 90)
plt.subplot(2, 2, 1)
sns.boxplot(data=df_standard[["odometer"]], orient="h", showmeans=True);
plt.title(f'Contagem de Quilometragem', fontsize = 16)
plt.yticks(rotation = 90)
plt.subplot(2, 2, 2)
sns.boxplot(data=df_standard[["vehicle_age_year"]], orient="h", showmeans=True);
plt.title(f'Contagem de Idade do Veículo', fontsize = 16)
plt.yticks(rotation = 90)
plt.show()


# Ao realizar o gráfico de caixa, torna-se nítida a diferença com o boxplot do DataFrame original, com valores extremos. Agora há menos valores atípicos no limite superior, além das caixas dos gráficos, intervalo entre o quartis Q1 e Q3, serem mais visíveis com escalas mais suaves.

# In[48]:


# Histograma dos parâmetros sem valores atípicos
plt.figure(figsize = ((12, 9)))
plt.suptitle("Histogramas", fontsize = 26)
# Parâmetro 'price'
plt.subplot(3, 1, 3)
plt.hist(df_standard['price'], bins=30)
plt.title("Contagem de Preço", fontsize = 16)
plt.ylabel('Veículos')
plt.xlabel('Preço (usd)')
# Parâmetro 'vehicle_age_year'
plt.subplot(2, 2, 1)
plt.hist(df_standard['vehicle_age_year'], bins=30)
plt.title('Contagem de Idade do Veículo', fontsize = 16)
plt.ylabel('Veículos')
plt.xlabel('Idade (anos)')
# Parâmetro 'odometer'
plt.subplot(2, 2, 2)
plt.hist(df_standard['odometer'], bins=30)
plt.title('Contagem de Quilometragem', fontsize = 16)
plt.ylabel('Veículos')
plt.xticks(rotation = 90)
plt.xlabel('Quilometragem');

plt.show()


# Com o gráfico de histograma não seria diferente, com escalas menores há a possibilidade de ver o comportamento da distribuição das variáveis analisadas. A seguir, temos os histogramas dos dois Dataframes sobrepostos.

# In[49]:


# Histograma dos parâmetros dos DataFrames sobrepostos
plt.figure(figsize = ((12, 9)))
plt.suptitle("Histogramas", fontsize = 26)
# Parâmetro 'price'
plt.subplot(3, 1, 3)
plt.hist(df['price'], bins=30, range=(0,350000))
plt.hist(df_standard['price'], bins=30, range=(0,350000))
plt.title("Contagem de Preço", fontsize = 16)
plt.ylabel('Veículos')
plt.xlabel('Preço (usd)')
# Parâmetro 'vehicle_age_year'
plt.subplot(2, 2, 1)
plt.hist(df['vehicle_age_year'], bins=30, range=(0,100))
plt.hist(df_standard['vehicle_age_year'], bins=30, range=(0,100))
plt.title('Contagem de Idade do Veículo', fontsize = 16)
plt.ylabel('Veículos')
plt.xlabel('Idade (anos)')
# Parâmetro 'odometer'
plt.subplot(2, 2, 2)
plt.hist(df['odometer'], bins=30, range=(0,1000000))
plt.hist(df_standard['odometer'], bins=30, range=(0,1000000))
plt.title('Contagem de Quilometragem', fontsize = 16)
plt.ylabel('Veículos')
plt.xlabel('Quilometragem');

plt.show()


# Com esse gráfico acima, podemos perceber a sutil diferença entre os DataFrames mesmo estando na mesma escala.
# Enquanto a idade dos veículos anunciados atingem seu limite superior logo após 20 anos, a quilometragem dos veículos do anúncio não costumam ultrapassar os 250000km. O limite superior dos preços dos veículos nos anúncios não costumam ultrapassar os 35 mil dólares.

# ## Tempo de vida das propagandas
# 
# Verifica-se a seguir, a quantidade média de dias da duração de um anúncio na plataforma. Também conseguimos analisar os anúncios que foram removidos rapidamente e os que foram listados por um tempo anormalmente longo.

# In[50]:


# Parâmetro 'days_listed'
plt.figure(figsize = ((6, 4)))
plt.hist(df_standard['days_listed'], bins=30)
plt.title('Contagem de Dias do Anúncio', fontsize = 20)
plt.ylabel('Veículos')
plt.xlabel('Dias do Anúncio');


# O histograma acima revela anúncios que passam enormes quantidades de tempo até serem removidos, indicados pela calda longa à direita.

# In[51]:


# Tempo de exibição médio dos anúncios
listed_mean = df_standard['days_listed'].mean()
listed_median = df_standard['days_listed'].median()
print(f'Em média as propagandas ficam por {listed_mean:.3} dias até serem removidas. Por outro lado, 50% das propagandas são removidas em até {listed_median:.3} dias após suas postagens.')


# In[52]:


# Cálculo do IQR da variável 'days_listed'
Q1_days = df_standard['days_listed'].quantile(0.25)
Q3_days = df_standard['days_listed'].quantile(0.75)
IQR_days = Q3_days - Q1_days


# In[53]:


# Bloxpot de 'days_listed'
plt.figure(figsize = ((16, 4)))
sns.boxplot(data=df_standard[['days_listed']], orient='h', showmeans=True);
plt.vlines(x=[Q1_days-1.5*IQR_days, Q3_days+1.5*IQR_days], ymin=-1, ymax=1, color='red')
plt.yticks(rotation = 90)
print(f'O limite superior do tempo, em dias, que o anúncio fica disponível até ser removido é de {Q3_days+1.5*IQR_days} dias.');
print(f'O limite inferior do tempo, em dias, que o anúncio fica disponível até ser removido é de {Q1_days-1.5*IQR_days} dias, porém essa variável só assume valores positivos.');


# In[54]:


# Anúncios que foram removidos rapidamente, mesmo dia ou no dia seguinte
df_listed_fast = df_standard.query('-1 <days_listed < 2')
df_listed_fast.hist('days_listed', bins=2)
plt.title('Contagem de Dias do Anúncio', fontsize = 16)
plt.ylabel('Veículos')
plt.xlabel('Dias de Anúncio');
len_fast = len(df_standard[df_standard['days_listed']<=1])
print(f'{len_fast} anúncios foram removidos em até 1 dia após sua publicação.');


# In[55]:


# Contagem, média e mediana do tipo de veículos com anúncios rápidos
display(df_listed_fast.pivot_table(index=['type', 'condition'], values='days_listed', aggfunc=['count','mean', 'median']))


# Os tipos de veículos (`type`) que dominaram a rápida remoção de seus anúncios foram os do tipo *truck*, *sedan*, *SUV* e *pickup*. Sugerindo uma preferência dos consumidores para essas categorias de veículos, considerando que os dados sejam uma amostra significativa dos hábitos de consumo local.

# In[56]:


# Anúncios listados por um tempo anormalmente longo
tlong = Q3_days+1.5*IQR_days
df_listed_tlong = df_standard.query('days_listed >= @tlong')

df_listed_tlong.hist('days_listed')
plt.title('Contagem de Dias do Anúncio', fontsize = 16)
plt.ylabel('Veículos')
plt.xlabel('Dias de Anúncio');
len_tlong = len(df_standard[df_standard['days_listed']<=tlong])
print(f'{len_tlong} anúncios só foram removidos após passarem, no mínimo, {tlong} dias depois de suas publicações.');


# In[57]:


# Contagem, média e mediana do tipo de veículos com anúncios demorados
display(df_listed_tlong.pivot_table(index=['type','condition'], values='days_listed', aggfunc=['count','mean', 'median']))


# Os tipos de veículos (type) que mais demoraram a terem a remoção de seus anúncios, também foram os mesmos que tiveram seus anúncios removidos rapidamentedo (truck, sedan, SUV e pickup). Sugerindo, desse modo, que outras características são responsáveis pela preferência dos consumidores em comprarem rápido ou não essas categorias de veículos, variáveis como o preço, quilometragem ou estado de conservação.

# In[58]:


# Tipos de veículos com a maior quantidade de anúncios
display(df_standard.pivot_table(index='type', values='days_listed', aggfunc='count').sort_values(by=['days_listed'], ascending=False).T)

# Gráfico do parâmetro 'type'
plt.figure(figsize = ((16, 4)))
df.groupby('type')['days_listed'].count().plot(kind='bar')
plt.title(f'Categoria de Veículo por Anúncios', fontsize = 16)
plt.ylabel('Anúncios')
plt.xlabel('Categoria')
plt.xticks(rotation = 90);


# Os tipos de veículos com as maiores quantidades de anúncios foram os sedan e SUV, com 11.991 e 11.848 anúncios, respectivamente.

# ## Média de preços por cada tipo de veículo

# Aqui analisa-se o número médio do tempo do anúncio e preço, bem como a mediana das mesmas variáveis. Um gráfico de histograma revela a relação entre as duas variáveis.

# In[59]:


# Tabela agrupada
df_standard.pivot_table(index='type', values=['price','days_listed'], aggfunc=['sum','mean','median'])


# Acima temos o somatório da quantidade de dias e preço totais de cada categoria de veículo, bem como a média do tempo dos anúncios e do valor comercializado para cada categoria.

# In[60]:


# Tipos de veículos com a maior soma de preço negociados
display(df_standard.pivot_table(index='type', values='price', aggfunc='sum').sort_values(by=['price'], ascending=False).T)

# Gráfico do parâmetro 'type' e 'price'
plt.figure(figsize = ((16, 4)))
df.groupby('type')['price'].sum().plot(kind='bar')
plt.title(f'Categoria de Veículo por Anúncios', fontsize = 16)
plt.ylabel('Anúncios')
plt.xlabel('Categoria')
plt.xticks(rotation = 90);


# A categoria `truck` e `SUV` são as duas com maiores montantes de preço anunciados pela plataforma, com mais de 167 e 124 milhões de dólares, respectivamente. O preço médio da categoria `truck` é 15217.24 dólares, enquanto a categoria `SUV` possui um preço médio de 10484.35 dólares.

# ## Fatores de preço

# Agora veremos os fatores que mais afetam o preço nos anúncios dos veículos.

# In[61]:


# Matriz de correlação
display(df_standard.corr())


# A matriz de correlação traz as principais variáveis que afetam o preço. A idade do veículo (`vehicle_age_year`) e a quilometragem (`odometer`) possuem as maiores correlações com preço, porém correlações negativas — como realmente deveria ser, pois veículos com mais anos e maiores quilometragens normalmente possuem os menores preços de venda. Já a quantidade de cilindros (`cylinders`) e o fato do carro ser 4x4 ou não (`is_4wd`), afetam positivamente o preço de venda do carro.
# 
# Adiante vê-se o comportamento gráfico dessas variáveis.

# In[62]:


# Gráfico de dispersão 'price' e 'odometer' com 'condition'
plt.figure(figsize = ((16, 8)))
sns.scatterplot(data=df_standard, x="odometer", y="price", hue='condition', legend="full")
plt.title(f'Dispersão do Preço e Quilometragem', fontsize = 20)
plt.ylabel('Preço')
plt.xlabel('Quilometragem')
plt.xticks(rotation = 0);


# Conforme a matriz de correlação, temos correlação negativa relevante entre o preço do veículo e a quantidade de sua quilometragem. No gráfico de dispersão é possível ver a massa de dados decaíndo conforme há o aumento da quilometragem dos veículos.
# 
# Veículos tidos como novos (new), condição 5, estão concentrados próximos do eixo Y, com baixas quilometragens e com variação no preço ao longo do eixo Y. Já os veículos com excelentes condições (condição 3 e 4) estão distribuídos, em sua maioria, na zona que abrange os intervalos até a quilometragem de 125000km e o preço de 35 mil dólares. Apesar de existir veículos com condições inferiores (condições 1 e 2) por todo o gráfico de dispersão, é visível uma maior concentração deles quando a quilometragem passa dos 125000km, principalmente a condição 1, concentrada ao longo do eixo X, no qual possui os menores preços e as maiores quilometragens.

# In[63]:


# Gráfico de dispersão 'price' e 'vehicle_age_year' com 'transmission'
plt.figure(figsize = ((16, 8)))
sns.scatterplot(data=df_standard, x="vehicle_age_year", y="price", hue='transmission', legend="full")
plt.title(f'Dispersão do Preço e Idade do Veículo', fontsize = 20)
plt.ylabel('Preço')
plt.xlabel('Transmissão')
plt.xticks(rotation = 0);


# Como a idade do veículo (`vehicle_age_year`) em anos possui uma correlação negativa com o preço do veículo, temos que para grandes valores na idade do veículo encontremos também baixos valores na variável preço. Veículos mais antigos, tendem a serem mais baratos. Há uma predominância de veículos com transmissão automática nos anúncios publicados, bem como se revela uma concentração maior de transmissão manual em veículos mais antigos — um reflexo do mercado de automóveis na região de estudo.

# In[64]:


# Gráfico de dispersão 'price' e 'cylinders' com 'is_4wd'
plt.figure(figsize = ((16, 8)))
sns.boxplot(data=df_standard, x="cylinders", y="price", hue='is_4wd', showmeans=True)
plt.title(f'Boxplot do Preço e Cilindros', fontsize = 20)
plt.ylabel('Preço')
plt.xlabel('Cilindros')
plt.xticks(rotation = 0);


# O gráfico de boxplot acima revela que veículos com a característica 4x4 possuem em média maiores preços de venda que os veículos sem essa característica. Os veículos com quantidade de cilindros típicos, 6 ou 8, possuem maiores intervalos de preço entre preços mínimos e máximos.

# In[65]:


# Gráfico de dispersão 'price' e 'paint_color'
plt.figure(figsize = ((16, 8)))
sns.boxplot(data=df_standard, x="paint_color", y="price", showmeans=True)
plt.title(f'Boxplot do Preço e Cor', fontsize = 20)
plt.ylabel('Preço')
plt.xlabel('Cor')
plt.xticks(rotation = 0);


# Conforme estudo de 2017 e reestudo de 2022 realizado pelo site de anúncio de vendas de carros *iSeeCars*, as cores mais neutras costumam ser mais demandadas pelos consumidores, logo acabam por afetar o preço dos carros. O estudo também ressalta que a cor amarela (yellow) é bem procurada em carros de luxo e carros *premiums*.
# 
# Percebam que a cor roxa (purple) possui a menor mediana em relação ao preço, em contrapartida as cores branca (white) e preto (black) com um das maiores médias. Atenção para a cor laranja (orange), essa cor pode sugerir uma similaridade com a cor amarela (yellow) e ter seus preços acrescido pela procura dos consumidores, ou até mesmo ser a cor predominante no tipo de veículo ônibus (bus) que tipicamente possui preços bem mais elevados que os outros tipos de veículos.

# In[66]:


# Gráfico de dispersão 'price' e 'type'
plt.figure(figsize = ((18, 8)))
sns.boxplot(data=df_standard, x="type", y="price", showmeans=True)
plt.title(f'Boxplot do Preço e Tipo', fontsize = 20)
plt.ylabel('Preço')
plt.xlabel('Tipo')
plt.xticks(rotation = 90);


# Os maiores preços médios estão com o tipo de veículo ônibus (bus), algo comum por se tratarem de veículos de maior porte e de caráter comercial. Muitos veículos anunciados com preços atípicos, acabam por puxar quase todas as médias de preço dos tipos de veículos para acima das suas respectivas medianas.

# ## Conclusão geral
# 
# Após as análises iniciais do DataFrame, foram feitas correções ao nível de duplicatas implícitas e de tipo dos dados.
# 
# A existência de valores ausentes levou a procura por preenchê-los da melhor maneira possível. Após verificar que nenhuma característica era responsável por dominar a existência de valores ausentes nos dados, foi iniciado o preenchimento da variável `cylinders` utilizando o modelo do veículo, uma vez que a fabricação do veículo define a quantidade de cilindros que aquele modelo de motor vai ter. O ano do modelo, variável `model_year`, foi preenchido com auxílio da variável `model`, já que os modelos dos veículos definem, com bastante precisão, o ano em que aqueles veículos foram fabricados.
# 
# Os valores ausentes na quilometragem, variável `odometer`, foram preenchidos de acordo com o estado de conservação do veículo, uma vez que veículos mal conservados costumam ter alta quilometragem, ao nível que veículos mais bem conservados possuem os menores valores de quilometragens.
# 
# A variável `is_4wd` foi identificada como *boolean* com valores zero (0) ausentes, assim foi relativamente simples preencher/trocar os valores faltantes por zero.
# 
# Já a variável da cor do veículo, `paint_color`, foi a mais complexa para realizar seu preenchimento, uma vez que estudos comprovam que a cor do veículo afeta o seu preço de venda — principal objetivo desse estudo. Nesse sentido, e de forma a ser razoável com o preenchimento, foi escolhido a cor que mais se repetia entre os mesmo modelos de veículos, a moda (frequência).
# 
# Uma outra análise que foi realizada foi o tratamento dos valores atípicos. A criação dos intervalos interquartis (IQR) foram imprescindíveis para identificar e tratar esses valores da base de dados.
# 
# Em seguida foram analisados o novo DataFrame através de gráficos de histograma e bloxpot, com e sem sobreposição, e criação de linhas de limites inferiores e superiores. Nessa etapa os gráficos se mostraram mais claros e perceptíveis, com a ausência dos valores extremos.
# 
# Verificou-se o tempo médio de existência da publicação dos anúncios, que são de 39.5 dias. Além de identificarmos os anúncios que foram removidos em menos de um dia de publicados. Já por outro lado, os anúncios mais demorados foram os que superaram 104 dias de publicação.
# 
# Foi identificado também que as categorias truck e SUV são as duas com maiores montantes de preço anunciados pela plataforma, com mais de 167 e 124 milhões de dólares, respectivamente. O preço médio da categoria truck ultrapassa 15 mil dólares, enquanto a categoria SUV possui um preço médio superior a 10 mil dólares.
# 
# Por fim, a matriz de correlação lançou luz sobre as principais variáveis que afetam o preço dos veículos nos anúncios. Nas quais, as principais foram a idade do veículo, quilometragem, quantidade de cilindros e se o carro possui ou não a característica 4x4.
# 
# Com a utilização de gráficos de dispersão, bem como boxplots, foi possível corroborar coms os estudos da iSeeCars que identificam que veículos com certas cores são mais caros que outros. Além de reforçar que veículos em melhores condições de conservação tendem a atingirem maiores preços nos anúncios.
# 
# ### Referência
# 
# * iSeeCars — acesso em 20 de dezembro de 2022, em: https://www.iseecars.com/most-popular-car-colors-study#v=2022.
