#!/usr/bin/env python
# coding: utf-8

# ---
# 
# # *Calculando Free Cash Flow Yield (FCFY) para várias empresas*

# ---
# 
# *Free Cash Flow:*
# 
# 1. https://www.investopedia.com/terms/f/freecashflow.asp
# 
# 
# *Free Cash Flow Yield:*
# 
# 1. https://www.investopedia.com/articles/fundamental-analysis/09/free-cash-flow-yield.asp
# 
# 2. https://andrebona.com.br/buggpedia-o-que-e-o-free-cash-flow-to-yield/
# 
# 3. https://www.shopify.com/blog/free-cash-flow-yield
# 
# 
# *Free Cash Flow Margin:*
# 
# 1. https://www.wallstreetprep.com/knowledge/fcf-margin/
# 
# ---

# ### *Free Cash Flow*
# 
# <br>
# 
# - O dinheiro que a empresa tem disponível para repassar aos credores ou pagar dividendos e juros para investidores.
# - Representa o caixa que uma empresa gera após contabilizar as saídas de caixa para apoiar as operações e manter seus ativos de capital.
# 
# 

# ### *Free Cash Flow Yield*
# 
# <br>
# 
# - Chamado de rendimento do fluxo de caixa livre (Free Cash Flow Yield, ou FCFY), é um indicador melhor do que o índice P/L.
# 
# - O índice P/L mede quanto lucro líquido anual está disponível por ação ordinária. No entanto, a demonstração do fluxo de caixa é uma medida melhor do desempenho de uma empresa do que a demonstração do resultado.
# 
# - Existe uma ferramenta de medição comparável ao índice P/L que utiliza a demonstração do fluxo de caixa?
# 
# <br>
# 
# Felizmente, sim. Podemos usar o fluxo de caixa livre e dividi-lo pelo valor da empresa como um indicador mais confiável. Chamado de rendimento do fluxo de caixa livre, isso oferece aos investidores outra maneira de avaliar o valor de uma empresa que é comparável ao índice P/L. Como esta medida utiliza o fluxo de caixa livre, o rendimento do fluxo de caixa livre fornece uma medida melhor do desempenho de uma empresa.
# 
# A maneira mais comum de calcular o rendimento do fluxo de caixa livre é usar a capitalização de mercado como divisor.

# 
# \begin{align}
#         \text{Free Cash Flow Yield} = \frac{\text{Free Cash Flow (Fluxo de Caixa Livre) }}{\text{Market Capitalization (Valor de Mercado)}}
#     \end{align}

# ### *1. Importação das bibliotecas*

# In[92]:


import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px


# ### *2. Explorar funcionalidades básicas da yfinance*

# In[62]:


abev = yf.Ticker('ABEV3.SA')


# In[63]:


abev.basic_info


# In[64]:


abev.financials


# In[65]:


abev.quarterly_cash_flow


# In[66]:


abev.basic_info['marketCap']


# ### *3. Calcular métricas fundamentalistas derivadas*

# In[67]:


abev_fcf = abev.quarterly_cash_flow.loc['Free Cash Flow']


# In[68]:


abev_mktcap = abev.basic_info['marketCap']


# In[69]:


abev_fcfy = pd.DataFrame((abev_fcf/abev_mktcap) * 100)


# In[70]:


abev_fcfy.rename(columns = {'Free Cash Flow':'ABEV3'}, inplace = True)


# In[71]:


abev_fcfy = abev_fcfy[::-1]


# In[72]:


abev_fcfy.plot();


# In[73]:


abev_fcfy


# In[74]:


ticker = 'HYPE3'
papel = yf.Ticker(ticker + '.SA')
papel_fcf = papel.quarterly_cash_flow.loc['Free Cash Flow']
papel_mktcap = papel.basic_info['marketCap']
papel_fcfy  = pd.DataFrame((papel_fcf/papel_mktcap)*100)
papel_fcfy.columns = [ticker]
papel_fcfy = papel_fcfy[::-1]


# In[75]:


papel_fcfy


# In[76]:


papel_fcfy.plot();


# ### *4. Criando funções de generalização*

# In[77]:


ativos = ['ABEV3', 'B3SA3', 'PRIO3', 'FLRY3', 'ODPV3', 'WEGE3']


# In[78]:


# DataFrame vazio para popular com os dados
free_cash_flow_yield = pd.DataFrame()
# Loop
for i in ativos:
    # Formatando a String para obtenção dos dados
    papel = yf.Ticker(i + '.SA')
    # Obtendo os dados do FCF
    papel_fcf = papel.quarterly_cash_flow.loc['Free Cash Flow']
    # Obtendo os dados do MArket cap
    papel_mktcap = papel.basic_info['marketCap']
    # Relizando a operação
    papel_fcfy  = (papel_fcf/papel_mktcap)*100
    # Garantindo que o dado seja do tipo float
    papel_fcfy = papel_fcfy.astype(float)
    # Arredondando os valores para 2 casas decimais
    papel_fcfy = round(papel_fcfy, 2)
    # Adicionando o resultado no DatafRame vazio
    free_cash_flow_yield[i] = papel_fcfy
    
# Invertendo o DataFrame
free_cash_flow_yield = free_cash_flow_yield[::-1]


# In[79]:


free_cash_flow_yield


# Criando a função

# In[82]:


def fcfy(stocks):
    
    import pandas as pd
    import yfinance as yf
    
    free_cash_flow_yield = pd.DataFrame()

    for i in stocks:
        # Formatando a String para obtenção dos dados
        papel = yf.Ticker(i + '.SA')
        # Obtendo os dados do FCF
        papel_fcf = papel.quarterly_cash_flow.loc['Free Cash Flow']
        # Obtendo os dados do MArket cap
        papel_mktcap = papel.basic_info['marketCap']
        # Relizando a operação
        papel_fcfy  = (papel_fcf/papel_mktcap)*100
        # Garantindo que o dado seja do tipo float
        papel_fcfy = papel_fcfy.astype(float)
        # Arredondando os valores para 2 casas decimais
        papel_fcfy = round(papel_fcfy, 2)
        # Adicionando o resultado no DatafRame vazio
        free_cash_flow_yield[i] = papel_fcfy

    # Invertendo o DataFrame
    free_cash_flow_yield = free_cash_flow_yield[::-1]
    
    return free_cash_flow_yield;
    


# In[86]:


fcfy(['PETR4','ITUB3','B3SA3','RADL3'])


# ### *5. Plotagem*

# In[87]:


data = fcfy(['PETR4','ITUB3','B3SA3','RADL3'])


# In[90]:


data.index = data.index.strftime('%m/%Y')


# In[91]:


data.plot();


# In[96]:


fig = go.Figure(data=[
    go.Bar(name='PETR4', x=data.index, y=data['PETR4'],marker_color=px.colors.qualitative.Safe[0]),
    go.Bar(name='ITUB3', x=data.index, y=data['ITUB3'],marker_color=px.colors.qualitative.Safe[9]),
    go.Bar(name='B3SA3', x=data.index, y=data['B3SA3'],marker_color=px.colors.qualitative.Safe[4]),
    go.Bar(name='RADL3', x=data.index, y=data['RADL3'],marker_color=px.colors.qualitative.Safe[3]),
], layout=go.Layout(xaxis = {"type": "category"} ))

# Modificar o 'barmode' para agrupar as barras
fig.update_layout(title_text='Free Cash Flow Yield')
fig.update_layout(barmode='group')
fig.show()


# In[ ]:




