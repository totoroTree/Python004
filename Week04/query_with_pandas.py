"""
 * Project        Python-Geek-Training
 * (c) copyright  2020
 * Author: Alice Wang

Convert the followed SQL queries to Pandas:
1. SELECT * FROM data;
2. SELECT * FROM data LIMIT 10;
3. SELECT id FROM data;  //id 是 data 表的特定一列
4. SELECT COUNT(id) FROM data;
5. SELECT * FROM data WHERE id<1000 AND age>30;
6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
8. SELECT * FROM table1 UNION SELECT * FROM table2;
9. DELETE FROM table1 WHERE id=10;
10. ALTER TABLE table1 DROP COLUMN column_name;
"""

import numpy as np
import pandas as pd

data_size = 2000
df_0 = pd.DataFrame({
    "age": np.random.randint(18, 80, data_size)
})
df_0['id'] = range(1, len(df_0)+1)

# 初始化 table1 数据
df_1 = pd.DataFrame({
    "order_id": np.random.randint(1, 100, data_size)
})
df_1['id'] = range(1, len(df_1)+1)

df_2 = pd.DataFrame({
    "age": np.random.randint(20, 60, data_size)
})
df_2['id'] = range(1, len(df_0)+1)

print('SQL 1. SELECT * FROM data')
print(df_0)

print('SQL 2. SELECT * FROM data LIMIT 10')
print(df_0.head(10))

print('SQL 3. SELECT id FROM data')
print(df_0['id'])

print('SQL 4. SELECT COUNT(id) FROM data')
print(df_0['id'].size)

print('SQL 5. SELECT * FROM data WHERE id<1000 AND age>30')
print(df_0[(df_0['id'] < 1000) & (df_0['age'] > 30)])

print('SQL 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id')
print(df_1.groupby('id').agg({'order_id': pd.Series.nunique}))

print('SQL 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;')
print(pd.merge(df_1, df_2, on='id'))

print('SQL 8. SELECT * FROM table1 UNION SELECT * FROM table2')
print(pd.concat([df_1, df_2]).drop_duplicates())

print('SQL 9. DELETE FROM table1 WHERE id=10;')
print(df_1.drop(df_1.query('id==10').index, axis=0))

print('SQL 10. ALTER TABLE table1 DROP COLUMN column_name')
print(df_1.drop('id', axis=1))