import pandas as pd
import sqlite3

# 1. ler o CSV para um DataFrame
df = pd.read_csv('dados/gastos.csv')
categorias_df = pd.read_csv('dados/categorias.csv')

# 2. abrir/criar um banco SQLite chamado gastos.db
conn = sqlite3.connect('gastos.db')

# 3. gravar o DataFrame como tabela 'gastos'
#    if_exists='replace' apaga qualquer tabela anterior
df.to_sql('gastos', conn, if_exists='replace', index=False)

categorias_df.to_sql('categorias', conn, if_exists='replace', index=False)

conn.close()