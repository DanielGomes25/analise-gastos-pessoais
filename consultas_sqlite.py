import sqlite3

# Abre conexão com banco
conn = sqlite3.connect('gastos.db')
cur = conn.cursor()

print("=" * 60)
print("CONSULTAS COM JOINS - GASTOS E CATEGORIAS")
print("=" * 60)

# 1. INNER JOIN - mostrar gastos com categoria
print("\n1. INNER JOIN - Gastos com categoria correspondente:")
print("-" * 60)
cur.execute('''
SELECT 
    g.id,
    g.data,
    c.categoria,
    g.descricao,
    g.valor
FROM gastos g
INNER JOIN categorias c ON g.id_categoria = c.id_categoria
LIMIT 10
''')
for row in cur.fetchall():
    print(row)

# 2. LEFT JOIN - todas as despesas (mesmo sem categoria válida)
print("\n2. LEFT JOIN - Todos os gastos, categoria se existir:")
print("-" * 60)
cur.execute('''
SELECT 
    g.id,
    g.data,
    COALESCE(c.categoria, 'SEM CORRESPONDÊNCIA') AS categoria,
    g.descricao,
    g.valor
FROM gastos g
LEFT JOIN categorias c ON g.id_categoria = c.id_categoria
LIMIT 10
''')
for row in cur.fetchall():
    print(row)

# 3. INNER JOIN com GROUP BY - total por categoria
print("\n3. INNER JOIN + GROUP BY - Total de despesas por categoria:")
print("-" * 60)
cur.execute('''
SELECT 
    c.categoria,
    COUNT(*) AS quantidade,
    SUM(g.valor) AS total
FROM gastos g
INNER JOIN categorias c ON g.id_categoria = c.id_categoria
GROUP BY c.categoria
ORDER BY total ASC
''')
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]} transações | Total: R${row[2]:.2f}")

# 4. LEFT JOIN para encontrar categorias sem gastos
print("\n4. LEFT JOIN - Categorias que podem não ter gastos:")
print("-" * 60)
cur.execute('''
SELECT 
    c.categoria,
    COUNT(g.id) AS total_gastos,
    COALESCE(SUM(g.valor), 0) AS soma
FROM categorias c
LEFT JOIN gastos g ON c.id_categoria = g.id_categoria
GROUP BY c.categoria
ORDER BY total_gastos DESC
''')
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]} gastos | Soma: R${row[2]:.2f}")

# 5. BALANÇO MENSAL - Salários vs Gastos
print("\n5. BALANÇO MENSAL - Salário - Gastos = Saldo:")
print("-" * 60)
cur.execute('''
SELECT 
    SUBSTR(g.data, 1, 7) AS mes,
    SUM(CASE WHEN g.id_categoria = 1 THEN g.valor ELSE 0 END) AS total_salario,
    SUM(CASE WHEN g.id_categoria != 1 THEN g.valor ELSE 0 END) AS total_gastos,
    SUM(g.valor) AS saldo
FROM gastos g
GROUP BY SUBSTR(g.data, 1, 7)
ORDER BY mes ASC
''')
print("Mês | Salário | Gastos | Saldo")
for mes, salario, gastos, saldo in cur.fetchall():
    status = "✓ Sobrou" if saldo >= 0 else "✗ Ficou devendo"
    print(f"  {mes} | R${salario:,.2f} | R${gastos:,.2f} | R${saldo:,.2f} ({status})")

# 6. DETALHE DE JANEIRO - Todas as transações
print("\n6. DETALHE DE JANEIRO - Transações do mês:")
print("-" * 60)
cur.execute('''
SELECT 
    g.id,
    g.data,
    c.categoria,
    g.descricao,
    g.valor
FROM gastos g
INNER JOIN categorias c ON g.id_categoria = c.id_categoria
WHERE SUBSTR(g.data, 1, 7) = '2025-01'
ORDER BY g.data ASC
''')
for row in cur.fetchall():
    tipo = "ENTRADA" if row[4] > 0 else "SAÍDA"
    print(f"  {row[1]} | {row[2]:13} | {row[3]:20} | R${row[4]:>8.2f} ({tipo})")

conn.close()
