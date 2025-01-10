import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

# Carregando os dados
vendas = pd.read_excel("varejo.xlsx")
cliente = pd.read_excel("cliente_varejo.xlsx")

# Substituindo valores na coluna "idcanalvenda"
vendas["idcanalvenda"] = vendas["idcanalvenda"].replace("APP", "Aplicativo")

# Manipulando o nome do departamento para substituir espaços por "_"
vendas["Nome_Departamento"] = vendas["Nome_Departamento"].str.replace(" ", "_")

# Tratando valores nulos
vendas["estado"] = vendas["estado"].fillna("MS")
media_preco = vendas["Preço"].mean()
vendas = vendas.fillna(media_preco)

# Filtrando dados
preço_errado = vendas.query("Preço > Preço_com_frete")
preco_correto = vendas.query("Preço < Preço_com_frete")
preco_correto.query("Nome_Departamento == 'Esporte_e_Lazer' and estado == 'SP'")

# Agrupando e ordenando
valor_sort = round(preco_correto.groupby("Nome_Departamento")["Preço_com_frete"].agg("mean").reset_index(), 2)
valor_sort = valor_sort.sort_values("Preço_com_frete", ascending=False)

# Manipulando dados de data
preco_correto.groupby("Data").idcompra.nunique().sort_values(ascending=False).reset_index()

# Manipulando o DataFrame 'cliente'
cliente = cliente.astype({"renda": "float"})
vendas_clientes = preco_correto.merge(cliente, how="left", on="cliente_Log")

# Agrupando e calculando médias
agg_venda_renda = vendas_clientes.groupby("idcanalvenda")["renda"].agg("mean").reset_index()
agg_idade_bandeira = round(vendas_clientes.groupby("bandeira")["idade"].agg("mean").sort_values(ascending=False).reset_index(), 2)

# Gráfico de barras: Média de idade por bandeira usando plotly
fig1 = px.bar(agg_idade_bandeira, x='bandeira', y='idade', title="Idade Média por Bandeira", labels={'idade': 'Média de Idade'}, color='bandeira')
fig1.update_layout(showlegend=False)  # Opcional: Remover a legenda
fig1.show()

# Gráfico de barras: Média de Renda por canal de venda usando plotly
fig2 = px.bar(agg_venda_renda, x='idcanalvenda', y='renda', title="Venda por Renda", labels={'renda': 'Média de Renda'})
fig2.show()

# Gráfico de linha: Vendas por Data usando plotly
venda_por_data = preco_correto.groupby("Data").idcompra.nunique().reset_index()
fig3 = px.line(venda_por_data, x='Data', y='idcompra', title="Vendas por Data", labels={'idcompra': 'Quantidade de Vendas'})
fig3.show()

# Gráfico de barras: Preço médio por departamento (com frete) usando plotly
valor_departamento_frete = round(preco_correto.groupby("Nome_Departamento")["Preço_com_frete"].agg("mean").reset_index(), 2)
fig4 = px.bar(valor_departamento_frete, x='Nome_Departamento', y='Preço_com_frete', title="Preço Médio com Frete por Departamento", labels={'Preço_com_frete': 'Preço com Frete (Média)'})
fig4.update_layout(xaxis_tickangle=90)  # Rotaciona os rótulos do eixo X para facilitar a leitura
fig4.show()
