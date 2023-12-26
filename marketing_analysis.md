Olá, visitante!

Esse projeto visa otimizar as despesas com marketing de um site de vendas.
Para isso, utilizo três arquivos que servirão como datasets:
* /datasets/visits_log_us.csv
* /datasets/orders_log_us.csv
* /datasets/costs_us.csv

Adiante crio relatórios e calculos diversas métricas para Produto, Vendas e Marketing, respondendo importantes questionamentos desses setores.
Por fim, uma conclusão é elaborada com recomendações de como e onde os investimentos deveriam ser alocados.


# 1. Carregar os dados e prepará-los para análise


```python
# Importar bibliotecas
import pandas as pd
import numpy as np
import datetime as dt
import math
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats as st

# Formatação e estilo
sns.set_style('darkgrid')
sns.set_palette('hls')
sns.set_context("notebook", font_scale = 1.5, rc={"lines.linewidth": 2})
```


```python
# Carregar os dados
visits = pd.read_csv('/datasets/visits_log_us.csv')
orders = pd.read_csv('/datasets/orders_log_us.csv')
costs = pd.read_csv('/datasets/costs_us.csv')
```


```python
# Examinar as primeiras linhas de cada conjunto de dados para entender sua estrutura
print(visits.head())
print(orders.head())
print(costs.head())
```

        Device               End Ts  Source Id             Start Ts  \
    0    touch  2017-12-20 17:38:00          4  2017-12-20 17:20:00   
    1  desktop  2018-02-19 17:21:00          2  2018-02-19 16:53:00   
    2    touch  2017-07-01 01:54:00          5  2017-07-01 01:54:00   
    3  desktop  2018-05-20 11:23:00          9  2018-05-20 10:59:00   
    4  desktop  2017-12-27 14:06:00          3  2017-12-27 14:06:00   
    
                        Uid  
    0  16879256277535980062  
    1    104060357244891740  
    2   7459035603376831527  
    3  16174680259334210214  
    4   9969694820036681168  
                    Buy Ts  Revenue                   Uid
    0  2017-06-01 00:10:00    17.00  10329302124590727494
    1  2017-06-01 00:25:00     0.55  11627257723692907447
    2  2017-06-01 00:27:00     0.37  17903680561304213844
    3  2017-06-01 00:29:00     0.55  16109239769442553005
    4  2017-06-01 07:58:00     0.37  14200605875248379450
       source_id          dt  costs
    0          1  2017-06-01  75.20
    1          1  2017-06-02  62.25
    2          1  2017-06-03  36.53
    3          1  2017-06-04  55.00
    4          1  2017-06-05  57.08


Após carregar os dados, é importante verificar o tipo de dados de cada coluna, além de realizar conversões necessárias e lidar com possíveis valores ausentes.


```python
# Verificar as informações principais dos dados
print(visits.info())
print('#'*50)
print(orders.info())
print('#'*50)
print(costs.info())
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 359400 entries, 0 to 359399
    Data columns (total 5 columns):
     #   Column     Non-Null Count   Dtype 
    ---  ------     --------------   ----- 
     0   Device     359400 non-null  object
     1   End Ts     359400 non-null  object
     2   Source Id  359400 non-null  int64 
     3   Start Ts   359400 non-null  object
     4   Uid        359400 non-null  uint64
    dtypes: int64(1), object(3), uint64(1)
    memory usage: 13.7+ MB
    None
    ##################################################
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 50415 entries, 0 to 50414
    Data columns (total 3 columns):
     #   Column   Non-Null Count  Dtype  
    ---  ------   --------------  -----  
     0   Buy Ts   50415 non-null  object 
     1   Revenue  50415 non-null  float64
     2   Uid      50415 non-null  uint64 
    dtypes: float64(1), object(1), uint64(1)
    memory usage: 1.2+ MB
    None
    ##################################################
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 2542 entries, 0 to 2541
    Data columns (total 3 columns):
     #   Column     Non-Null Count  Dtype  
    ---  ------     --------------  -----  
     0   source_id  2542 non-null   int64  
     1   dt         2542 non-null   object 
     2   costs      2542 non-null   float64
    dtypes: float64(1), int64(1), object(1)
    memory usage: 59.7+ KB
    None


Como a quantidade de linhas correspondem ao mesmo número de valores **não nulos**, em todos as três bases de dados, infere-se que a inexistência de valores ausentes. 


```python
# Verificar duplicidade nos dados
print(visits.duplicated().sum())
print('#'*50)
print(orders.duplicated().sum())
print('#'*50)
print(costs.duplicated().sum())
```

    0
    ##################################################
    0
    ##################################################
    0


A soma de linha duplicadas nos retornaria a quantidade de linhas com valores duplicados, porém não há valores duplicados nas três bases de dados.

Por fim, nessa parte exploratória dos dados iniciais, algumas considerações a serem feitas no que tange os tipos de dados e a formatação do nome das variáveis.

* Variáveis devem estar com nome em *lowercase* — verifica-se em *visits* e *orders*.
* Variáveis End Ts, Start Ts, Buy Ts e dt devem ser do tipo *datetime*.
* Variáveis com espaçamento.


```python
# Tornar o nome das variáveis no formato lowercase
visits.columns = visits.columns.str.lower()
orders.columns = orders.columns.str.lower()

# Verificar as primeiras linhas dos conjuntos de dados para confirmar as mudanças
print(visits.head())
print(orders.head())
```

        device               end ts  source id             start ts  \
    0    touch  2017-12-20 17:38:00          4  2017-12-20 17:20:00   
    1  desktop  2018-02-19 17:21:00          2  2018-02-19 16:53:00   
    2    touch  2017-07-01 01:54:00          5  2017-07-01 01:54:00   
    3  desktop  2018-05-20 11:23:00          9  2018-05-20 10:59:00   
    4  desktop  2017-12-27 14:06:00          3  2017-12-27 14:06:00   
    
                        uid  
    0  16879256277535980062  
    1    104060357244891740  
    2   7459035603376831527  
    3  16174680259334210214  
    4   9969694820036681168  
                    buy ts  revenue                   uid
    0  2017-06-01 00:10:00    17.00  10329302124590727494
    1  2017-06-01 00:25:00     0.55  11627257723692907447
    2  2017-06-01 00:27:00     0.37  17903680561304213844
    3  2017-06-01 00:29:00     0.55  16109239769442553005
    4  2017-06-01 07:58:00     0.37  14200605875248379450



```python
# Mudar o tipo de dados
visits['start ts'] = pd.to_datetime(visits['start ts'])
visits['end ts'] = pd.to_datetime(visits['end ts'])
orders['buy ts'] = pd.to_datetime(orders['buy ts'])
costs['dt'] = pd.to_datetime(costs['dt'])

# Verificar o tipo das colunas após a conversão
print(visits.dtypes)
print(orders.dtypes)
print(costs.dtypes)
```

    device               object
    end ts       datetime64[ns]
    source id             int64
    start ts     datetime64[ns]
    uid                  uint64
    dtype: object
    buy ts     datetime64[ns]
    revenue           float64
    uid                uint64
    dtype: object
    source_id             int64
    dt           datetime64[ns]
    costs               float64
    dtype: object



```python
# Substituir espaços por underscores nos nomes das colunas nos conjuntos de dados
visits.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
orders.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
costs.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)

# Verificar os nomes das colunas após a mudança
print(visits.columns)
print(orders.columns)
print(costs.columns)
```

    Index(['device', 'end_ts', 'source_id', 'start_ts', 'uid'], dtype='object')
    Index(['buy_ts', 'revenue', 'uid'], dtype='object')
    Index(['source_id', 'dt', 'costs'], dtype='object')


Agora já podemos passar para os relatórios e os cálculos das métricas.

# 2. Relatórios e Cálculo de Métricas

Vamos começar calculando as métricas relacionadas ao produto, focando em responder as seguintes perguntas:
1. Quantas pessoas usam-no cada dia, semana e mês?
2. Quantas sessões ocorrem por dia? (considerando que um usuário pode realizar várias sessões).
3. Qual a duração de cada sessão?
4. Com que frequência os usuários voltam?



```python
# Métricas de Produto
# Quantidade de pessoas que usam o produto por dia, semana e mês
daily_users = visits.resample('D', on='start_ts')['uid'].nunique()
weekly_users = visits.resample('W-Mon', on='start_ts')['uid'].nunique()
monthly_users = visits.resample('M', on='start_ts')['uid'].nunique()

# Função para imprimir as métricas
def print_metrics(label, data):
    print(f"\nMétricas para {label}:")
    print(f"Mínima: {data.min():.2f}")
    print(f"Máxima: {data.max():.2f}")
    print(f"Média: {data.mean():.2f}")
    print(f"Mediana: {data.median():.2f}")
    print(f"Desvio Padrão: {data.std():.2f}")

# Calcular e imprimir métricas para cada período
print_metrics("Dia", daily_users)
print_metrics("Semana", weekly_users)
print_metrics("Mês", monthly_users)
```

    
    Métricas para Dia:
    Mínima: 0.00
    Máxima: 3319.00
    Média: 905.50
    Mediana: 919.00
    Desvio Padrão: 373.04
    
    Métricas para Semana:
    Mínima: 2312.00
    Máxima: 10686.00
    Média: 5722.15
    Mediana: 5874.00
    Desvio Padrão: 2055.08
    
    Métricas para Mês:
    Mínima: 11631.00
    Máxima: 32797.00
    Média: 23228.42
    Mediana: 24240.50
    Desvio Padrão: 7546.38


Agora, considerando que o usuário pode realizar várias sessões, vamos identificar quantas sessões ocorrem por dia.


```python
# Calcular a quantidade de sessões por dia
sessions_per_day = visits.groupby(visits['start_ts'].dt.date)['uid'].count()

# Imprimir a quantidade de sessões por dia
print_metrics("Sessões por Dia", sessions_per_day)

# Calcular a média de sessões por usuário por dia
average_sessions_per_user_per_day = sessions_per_day.mean() / daily_users.mean()

# Imprimir a média de sessões por usuário por dia
print(f"\nMédia de sessões por usuário por dia: {average_sessions_per_user_per_day:.2f}")
```

    
    Métricas para Sessões por Dia:
    Mínima: 1.00
    Máxima: 4042.00
    Média: 987.36
    Mediana: 1003.00
    Desvio Padrão: 418.99
    
    Média de sessões por usuário por dia: 1.09


Já para identiifcar a duração de cada sessão, temos:


```python
# Calcular a duração de cada sessão em minutos
visits['session_duration_minutes'] = (visits['end_ts'] - visits['start_ts']).dt.seconds / 60

# Imprimir a duração de cada sessão em minutos usando a função
print_metrics("Duração de cada sessão", visits['session_duration_minutes'])
```

    
    Métricas para Duração de cada sessão:
    Mínima: 0.00
    Máxima: 1408.00
    Média: 10.73
    Mediana: 5.00
    Desvio Padrão: 16.94


Sabendo que 50% da duração das sessões não passam de 5 minutos, vamos identificar a frequência de retorno dos usuários (taxa de retenção).


```python
# Calcular a diferença de tempo entre as visitas consecutivas para cada usuário
visits['tempo_entre_visitas'] = visits.groupby('uid')['start_ts'].diff()
```


```python
# Converter a coluna 'tempo_entre_visitas' para segundos
visits['tempo_entre_visitas_seg'] = visits['tempo_entre_visitas'].dt.total_seconds()
```


```python
# Definir os intervalos desejados em segundos
intervalo_7_dias = 7 * 24 * 60 * 60  # 7 dias em segundos
intervalo_1_mes = 30 * 24 * 60 * 60  # 1 mês em segundos
intervalo_1_ano = 365 * 24 * 60 * 60  # 1 ano em segundos

# Calcular a frequência de retorno dentro dos intervalos desejados
frequencia_retorno_7_dias = (visits['tempo_entre_visitas_seg'] <= intervalo_7_dias).mean() * 100
frequencia_retorno_1_mes = (visits['tempo_entre_visitas_seg'] <= intervalo_1_mes).mean() * 100
frequencia_retorno_1_ano = (visits['tempo_entre_visitas_seg'] <= intervalo_1_ano).mean() * 100
```


```python
# Imprimir as frequências de retorno
print(f"Em média, apenas {frequencia_retorno_7_dias:.2f}% dos usuários retornam dentro dos próximos 7 dias.")
print(f"Em média, apenas {frequencia_retorno_1_mes:.2f}% dos usuários retornam dentro do próximo mês.")
print(f"Em média, apenas {frequencia_retorno_1_ano:.2f}% dos usuários retornam dentro do próximo ano.")
```

    Em média, apenas 23.52% dos usuários retornam dentro dos próximos 7 dias.
    Em média, apenas 27.23% dos usuários retornam dentro do próximo mês.
    Em média, apenas 36.51% dos usuários retornam dentro do próximo ano.


Agora vamos calcular as métricas relacionadas às vendas, focando em responder as seguintes perguntas:
1. Quando as pessoas começam a comprar?
2. Quantos pedidos os clientes fazem durante um determinado período de tempo?
3. Qual o volume médio de uma compra?
4. Quanto dinheiro as compras trazem para a empresa (LTV)?


```python
# Calcular a diferença de tempo entre o registro (start_ts) e a primeira ordem de compra (buy_ts) para cada usuário
time_to_first_purchase = orders.groupby('uid')['buy_ts'].min() - visits.groupby('uid')['start_ts'].min()

# Calcular as métricas para o tempo até a primeira compra
average_time = time_to_first_purchase.mean()
median_time = time_to_first_purchase.median()
min_time = time_to_first_purchase.min()
max_time = time_to_first_purchase.max()
std_time = time_to_first_purchase.std()

# Imprimir as métricas
print(f"Média do tempo até a primeira compra: {average_time}")
print(f"Mediana do tempo até a primeira compra: {median_time}")
print(f"Tempo mínimo até a primeira compra: {min_time}")
print(f"Tempo máximo até a primeira compra: {max_time}")
print(f"Desvio padrão do tempo até a primeira compra: {std_time}")
```

    Média do tempo até a primeira compra: 16 days 21:40:10.550064343
    Mediana do tempo até a primeira compra: 0 days 00:16:00
    Tempo mínimo até a primeira compra: 0 days 00:00:00
    Tempo máximo até a primeira compra: 363 days 07:04:00
    Desvio padrão do tempo até a primeira compra: 47 days 01:44:46.481416777


Apesar da média até a primeira comprar estar em 16 dias, a mediana revela que boa parte dos usuários não realizam compras (dentro do intervalo observado). Agora é importante saber quantos pedidos os clientes fazem dentro de um determinado período.


```python
# Criar colunas de coorte de semana, mês e ano para as ordens
orders['week'] = orders['buy_ts'].dt.to_period('W')
orders['month'] = orders['buy_ts'].dt.to_period('M')
orders['year'] = orders['buy_ts'].dt.to_period('Y')
```


```python
# Calcular a contagem de pedidos por coorte de semana, mês e ano
orders_per_week = orders.groupby('week')['uid'].count()
orders_per_month = orders.groupby('month')['uid'].count()
orders_per_year = orders.groupby('year')['uid'].count()
```


```python
# Imprimir métricas usando a função print_metrics
print_metrics("a contagem de pedidos por semana", orders_per_week)
print_metrics("a contagem de pedidos por mês", orders_per_month)
print_metrics("a contagem de pedidos por ano", orders_per_year)
```

    
    Métricas para a contagem de pedidos por semana:
    Mínima: 314.00
    Máxima: 1894.00
    Média: 951.23
    Mediana: 991.00
    Desvio Padrão: 396.44
    
    Métricas para a contagem de pedidos por mês:
    Mínima: 1.00
    Máxima: 6218.00
    Média: 3878.08
    Mediana: 4346.00
    Desvio Padrão: 1858.11
    
    Métricas para a contagem de pedidos por ano:
    Mínima: 22948.00
    Máxima: 27467.00
    Média: 25207.50
    Mediana: 25207.50
    Desvio Padrão: 3195.42



```python
# Calcular a média global de ordens de compra pela quantidade de clientes
average_orders_per_customer = orders['uid'].count() / orders['uid'].nunique()

# Imprimir a média global de ordens de compra pela quantidade de clientes
print(f"Média global de ordens de compra por cliente: {average_orders_per_customer:.2f}")
```

    Média global de ordens de compra por cliente: 1.38


No período analisado, a média de compras por cliente foi de 1.38. Sabemos que a cada 3 clientes há um pouco mais de 4 compras, agora é imprescindível saber o valor médio gasto nessas compras pelos clientes (ticket médio).


```python
# Calcular o ticket médio global das compras dos clientes
average_revenue_per_order_global = orders['revenue'].mean()

# Calcular o ticket médio por coorte de ano e mês
average_revenue_per_order_by_month = orders.groupby(['year', 'month'])['revenue'].mean()
average_revenue_per_order_by_year = orders.groupby('year')['revenue'].mean()

# Imprimir o ticket médio global das compras dos clientes
print(f"Ticket médio global das compras por cliente: {average_revenue_per_order_global}")

# Imprimir o ticket médio por coorte de ano e mês
print("Ticket médio das compras por cliente por mês:")
print(average_revenue_per_order_by_month)
print("\nTicket médio das compras por cliente por ano:")
print(average_revenue_per_order_by_year)
```

    Ticket médio global das compras por cliente: 4.999646930477041
    Ticket médio das compras por cliente por mês:
    year  month  
    2017  2017-06    4.060106
          2017-07    5.306589
          2017-08    4.847139
          2017-09    5.416448
          2017-10    4.928280
          2017-11    4.783518
          2017-12    5.852139
    2018  2018-01    4.112927
          2018-02    4.840095
          2018-03    5.413930
          2018-04    5.150645
          2018-05    4.771279
          2018-06    3.420000
    Name: revenue, dtype: float64
    
    Ticket médio das compras por cliente por ano:
    year
    2017    5.120599
    2018    4.854877
    Freq: A-DEC, Name: revenue, dtype: float64


Nas análises quanto às vendas, seguimos para verificar quanto dinheiro as compras dos clientes trazem para a empresa, conhecida como *LTV — Lifetime Value*: que é uma métrica utilizada em vendas para representar o valor total que um cliente traz para uma empresa.


```python
# Calcular o mês de compra para cada pedido
orders['order_month'] = orders['buy_ts'].astype('datetime64[M]')

# Encontrar a primeira compra de cada usuário
first_orders = orders.groupby('uid').agg({'order_month': 'min'}).reset_index()
first_orders.columns = ['uid', 'first_order_month']
```


```python
# Calcular o número de compradores em cada coorte
cohort_sizes = first_orders.groupby('first_order_month').agg({'uid': 'nunique'}).reset_index()
cohort_sizes.columns = ['first_order_month', 'n_buyers']

# Taxa de margem para calcular o lucro bruto
margin_rate = 0.2
```


```python
# Juntar os dados de compras com as informações de primeira compra
orders_ = pd.merge(orders, first_orders, on='uid')

# Agrupar os dados por coorte e mês de compra, somando a receita
cohorts = (
    orders_.groupby(['first_order_month', 'order_month'])
    .agg({'revenue': 'sum'})
    .reset_index()
)

# Juntar as informações da coorte com os dados de receita
report = pd.merge(cohort_sizes, cohorts, on='first_order_month')
```


```python
# Calcular o lucro bruto (gross profit) com base na receita e taxa de margem
report['gp'] = report['revenue'] * margin_rate

# Calcular a idade da coorte em meses
report['age'] = (
    report['order_month'] - report['first_order_month']
) / np.timedelta64(1, 'M')
report['age'] = report['age'].round().astype('int')

# Calcular o LTV dividindo o lucro bruto pelo número de compradores na coorte
report['ltv'] = report['gp'] / report['n_buyers']
```


```python
# Criar uma tabela pivô para mostrar a média do LTV ao longo do tempo
output = report.pivot_table(
    index='first_order_month', columns='age', values='ltv', aggfunc='mean'
).round(2)
```


```python
# Imprimir a média do LTV dos clientes agrupada por mês
print("Média do LTV dos clientes agrupada por mês:")
print(output)
```

    Média do LTV dos clientes agrupada por mês:
    age                  0     1     2     3     4     5     6     7     8     9   \
    first_order_month                                                               
    2017-06-01         0.94  0.10  0.09  0.19  0.20  0.15  0.19  0.12  0.11  0.12   
    2017-07-01         1.20  0.07  0.12  0.07  0.04  0.03  0.02  0.03  0.03  0.03   
    2017-08-01         1.06  0.09  0.09  0.08  0.10  0.06  0.04  0.08  0.06  0.04   
    2017-09-01         1.13  0.22  0.10  0.80  0.08  0.13  0.14  0.05  0.04   NaN   
    2017-10-01         1.00  0.11  0.04  0.03  0.03  0.02  0.02  0.02   NaN   NaN   
    2017-11-01         1.03  0.08  0.04  0.06  0.03  0.01  0.02   NaN   NaN   NaN   
    2017-12-01         0.95  0.05  0.19  0.21  0.06  0.07   NaN   NaN   NaN   NaN   
    2018-01-01         0.83  0.06  0.06  0.03  0.01   NaN   NaN   NaN   NaN   NaN   
    2018-02-01         0.83  0.06  0.02  0.01   NaN   NaN   NaN   NaN   NaN   NaN   
    2018-03-01         0.97  0.06  0.06   NaN   NaN   NaN   NaN   NaN   NaN   NaN   
    2018-04-01         0.93  0.11   NaN   NaN   NaN   NaN   NaN   NaN   NaN   NaN   
    2018-05-01         0.93   NaN   NaN   NaN   NaN   NaN   NaN   NaN   NaN   NaN   
    2018-06-01         0.68   NaN   NaN   NaN   NaN   NaN   NaN   NaN   NaN   NaN   
    
    age                  10    11  
    first_order_month              
    2017-06-01         0.11  0.05  
    2017-07-01         0.03   NaN  
    2017-08-01          NaN   NaN  
    2017-09-01          NaN   NaN  
    2017-10-01          NaN   NaN  
    2017-11-01          NaN   NaN  
    2017-12-01          NaN   NaN  
    2018-01-01          NaN   NaN  
    2018-02-01          NaN   NaN  
    2018-03-01          NaN   NaN  
    2018-04-01          NaN   NaN  
    2018-05-01          NaN   NaN  
    2018-06-01          NaN   NaN  



```python
# Calcular a média dos valores do Lifetime Value (LTV)
print("\nPara o tempo analisado e margem de lucro de 20%, temos que o LTV é:")
print(report['ltv'].mean())
```

    
    Para o tempo analisado e margem de lucro de 20%, temos que o LTV é:
    0.22992789840476116


Vamos calcular as métricas relacionadas ao Marketing, focando em responder as seguintes perguntas:

1. Quanto dinheiro foi gasto? No total/por origem/ao longo do tempo?
2. Quanto custou a aquisição de clientes para cada origem (CAC)?
3. Os investimentos valem a pena? (ROI)


```python
# Calcular o total gasto
total_costs = costs['costs'].sum()
print(f"Total gasto em custos: {total_costs}")
```

    Total gasto em custos: 329131.62



```python
# Calcular o custo por origem do anúncio
costs_per_source = costs.groupby('source_id')['costs'].sum()

# Plotar o gráfico de barras
plt.figure(figsize=(10, 6))
costs_per_source.plot(kind='bar')
plt.xlabel('Origem do Anúncio')
plt.ylabel('Custo')
plt.title('Custo por Origem de Anúncio')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```


    
![png](output_46_0.png)
    



```python
# Calcular o custo ao longo do tempo (mês)
costs['dt'] = pd.to_datetime(costs['dt'])
costs['month'] = costs['dt'].dt.to_period('M')
costs_per_month = costs.groupby('month')['costs'].sum()

# Plotar o gráfico de linha
plt.figure(figsize=(10, 6))
costs_per_month.plot(kind='line', marker='o')
plt.xlabel('Mês')
plt.ylabel('Custo')
plt.title('Custo ao Longo do Tempo (por Mês)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```


    
![png](output_47_0.png)
    


Conseguimos avaliar que os maiores custos com marketing se concentram nos anúncios com origem 3 e nos meses de Outubro a Março. Sabemos também que todos os custos e despesas da empresa destinados a adquirir clientes devem ser levados em conta. Nesse sentido, precisamos dividir o custo total gasto em cada origem pelo número de clientes adquiridos dessa mesma origem.


```python
# Calcular o custo total por origem
costs_per_source = costs.groupby('source_id')['costs'].sum()

# Calcular o número de clientes adquiridos por origem
customers_per_source = visits.groupby('source_id')['uid'].nunique()

# Calcular o CAC por origem
cac_per_source = costs_per_source / customers_per_source

# Imprimir o CAC por origem
print("Custo de Aquisição de Clientes (CAC) por Origem:")
print(cac_per_source)
```

    Custo de Aquisição de Clientes (CAC) por Origem:
    source_id
    1     1.096546
    2     1.631017
    3     1.890439
    4     0.731201
    5     0.908434
    6          NaN
    7          NaN
    9     0.595584
    10    0.721766
    dtype: float64



```python
# Agrupar o número de visitas por origem
visits_per_source = visits.groupby('source_id')['uid'].count()

# Relacionar as tabelas 'visits' e 'orders' pelo 'uid'
visits_with_source = visits[['uid', 'source_id']].merge(orders[['uid', 'revenue']], on='uid', how='left')

# Calcular o número de compras por origem
purchases_per_source = visits_with_source.groupby('source_id')['revenue'].count()

# Calcular o custo de aquisição de clientes por origem
cac_per_source = costs.groupby('source_id')['costs'].sum() / purchases_per_source

# Criar um DataFrame com os resultados
result_df = pd.DataFrame({
    'Visitas por Origem': visits_per_source,
    'Compras por Origem': purchases_per_source,
    'CAC por Origem': cac_per_source
})

print(result_df)
```

               Visitas por Origem  Compras por Origem  CAC por Origem
    source_id                                                        
    1                       34121              248662        0.083781
    2                       47626              238297        0.179633
    3                       85610               46766        3.021888
    4                      101794               62683        0.974325
    5                       66905              151824        0.340902
    6                           6                   0             NaN
    7                          36                   1             NaN
    9                       13277                9547        0.577929
    10                      10025                4027        1.445863



```python
# Criar um gráfico de barras com valores do CAC nas barras
plt.figure(figsize=(12, 8))
ax = sns.barplot(data=result_df.reset_index(), x='source_id', y='Visitas por Origem', color='blue', alpha=0.7, label='Visitas')
sns.barplot(data=result_df.reset_index(), x='source_id', y='Compras por Origem', color='orange', alpha=0.7, label='Compras')
sns.barplot(data=result_df.reset_index(), x='source_id', y='CAC por Origem', color='green', alpha=0.7, label='CAC')
plt.xlabel('Origem de Anúncio')
plt.ylabel('Quantidade')
plt.title('Métricas por Origem de Anúncio')
plt.legend()
plt.xticks(rotation=45)

# Adicionar valores do CAC acima das barras
for p in ax.patches:
    if p.get_height() > 0:  # Evitar valores nulos de CAC
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=10, color='black')

plt.tight_layout()
plt.show()
```


    
![png](output_51_0.png)
    

Fica evidente que os maiores custos de aquisição de clientes (CAC) se concentram na Origem 3, 10 e 4. Em contrapartida as Origens 1 e 2 possuem os menores custos com as maiores vendas. 


```python
# Calcular o ticket médio por source_id e mês
ticket_medio = orders.groupby(['uid', 'order_month'])['revenue'].mean().reset_index()

# Juntar os DataFrames ticket_medio e visits com base em uid
ltv_data = pd.merge(ticket_medio, visits[['uid', 'source_id']], on='uid')

# Agrupar por source_id e mês para calcular o LTV médio
ltv_by_source = ltv_data.groupby(['source_id', 'order_month'])['revenue'].mean().reset_index()

# Exibir o DataFrame com os valores do LTV por source_id e mês
print(ltv_by_source)
```

        source_id order_month    revenue
    0           1  2017-06-01   5.413176
    1           1  2017-07-01  10.268227
    2           1  2017-08-01   8.239024
    3           1  2017-09-01  15.303074
    4           1  2017-10-01   9.395626
    ..        ...         ...        ...
    81         10  2018-01-01   2.835136
    82         10  2018-02-01   3.224737
    83         10  2018-03-01   3.651235
    84         10  2018-04-01   2.914631
    85         10  2018-05-01   3.734177
    
    [86 rows x 3 columns]



```python
# Calcular o ROI por origem e agrupar por source_id
roi_per_source = (ltv_by_source.set_index('source_id')['revenue'] - cac_per_source) / cac_per_source
roi_per_source = roi_per_source.groupby('source_id').mean()

# Exibir o DataFrame com os valores médios de ROI por origem
print(roi_per_source)
```

    source_id
    1     120.108799
    2      51.882822
    3       0.653495
    4       5.105394
    5      16.956559
    6            NaN
    7            NaN
    9       5.253189
    10      1.326156
    dtype: float64


Percebemos que os investimentos valem muito quando se trata das origens 1, 2 e 5. Com retornos operacionais altíssimos em comparação com outras origens de marketing.

# 3. Conclusão

Na preparação dos dados tivemos:
- Carregamentod dos três arquivos .csv.
- Os tipos de dados foram alterados.
- A formatação das variáveis foram realizadas para corresponder ao estilo lowercase.
- Dados nulos e duplicados foram verificados.

Neste projeto, foi realizado uma análise dos dados de comportamento do usuário e métricas de vendas de uma plataforma de comércio eletrônico. O objetivo era compreender melhor o padrão de interações dos usuários, identificar oportunidades de melhoria e oferecer insights valiosos para as estratégias de marketing e negócios. A seguir, resumo os principais resultados e ofereço recomendações concretas para orientar decisões futuras.

#### Resultados Destacados

Observa-se uma média de 1.09 sessões por usuário, com uma duração média de 5 minutos por sessão. Essa análise nos forneceu informações cruciais sobre o engajamento dos usuários com a plataforma.

A taxa de retorno semanal é impressionante, em torno de 23.52%, indica um potencial significativo de fidelização de clientes. Isso aponta para a relevância da plataforma para os usuários e a oportunidade de explorar estratégias de retenção.

As métricas de vendas revelaram que, em média, os usuários demoram cerca de 16 dias para realizar uma compra. Essa informação é valiosa para entender o ciclo de compra do usuário e pode guiar decisões estratégicas de marketing.

A média de 1.38 ordens de compra por usuário e um ticket médio de aproximadamente 5 unidades monetárias indicam um bom envolvimento dos usuários e oportunidades de maximização das receitas por meio de estratégias de cross-selling e upselling.

A análise de LTV e CAC por Origem de Anúncio nos permitiu calcular o ROI, oferecendo uma visão clara do retorno sobre o investimento em marketing. As Origens de Anúncio 1, 2 e 5 se destacaram, demonstrando alto potencial de retorno.

#### Recomendações Estratégicas

Priorizar as Origens de Anúncio 1, 2 e 5, que apresentam o melhor ROI. Alocar mais recursos e investimentos nessas origens pode maximizar os resultados.

Investigar a falta de conversões nas Origens de Anúncio 3 e 4. Realizar pesquisas adicionais para entender os motivos por trás disso e implementar estratégias para melhorar a conversão.

Avaliar a relevância das Origens de Anúncio 6 e 7, que têm desempenho limitado. Considerar a realocação de recursos para canais mais eficazes.

#### Ações Futuras e Impacto nas Decisões

Com base nessas conclusões e recomendações, a equipe de marketing pode tomar decisões informadas e estratégicas para otimizar as estratégias de aquisição, retenção e conversão de clientes. A análise de dados fornece uma base sólida para a alocação de recursos e a criação de campanhas direcionadas, impactando positivamente os resultados de negócios.

#### Limitações e Próximos Passos

É importante observar que a análise é baseada nos dados disponíveis e em certas suposições. Para uma análise ainda mais aprofundada, pode-se considerar a inclusão de dados sazonais, a realização de testes A/B para validar nossas recomendações e a exploração de outras fontes de dados externos.

#### Conclusão Final

Em resumo, a análise abrangente dos dados proporcionou insights valiosos para direcionar estratégias de negócios. As descobertas destacaram áreas de oportunidade, bem como desafios a serem abordados. Ao seguir as recomendações e tomar medidas baseadas em dados, a plataforma de comércio eletrônico pode melhorar a experiência do usuário, aumentar a conversão e otimizar o retorno sobre o investimento em marketing, impulsionando o sucesso a longo prazo.
