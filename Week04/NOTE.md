[TOC]

### Pandas dtype mapping

| Pandas dtype   | Python type   | NumPy type   |usage   |
|---|---|---|---|
| object |str or mixed |string_, unicode_, mixed types | 字符串|
| int64 |int |	int_, int8, int16, int32, int64, uint8, uint16, uint32, uint64 |整型 |
| float64 |float |float_, float16, float32, float64 |浮点数 |
| bool |bool | bool| |
| datetime64 |NA |datetime64[ns] | 日期和时间 |
| timedelta[ns] |NA |NA | 时间差 |

### 如何查看Pandas的数据类型?
1. df.dtypes
2. df.info()
```
>>> import pandas as pd
>>> df = pd.read_csv("example.csv")
>>> df
   Customer Number     Customer Name         2016          2017 Percent Growth Jan Units  Month  Day  Year Active
0          10002.0  Quest Industries  $125,000.00    $162500.00         30.00%       500      1   10  2015      Y
1         552278.0    Smith Plumbing  $920,000.00  $101,2000.00         10.00%       700      6   15  2014      Y
2          23477.0   ACME Industrial   $50,000.00     $62500.00         25.00%       125      3   29  2016      Y
3          24900.0        Brekke LTD  $350,000.00    $490000.00          4.00%        75     10   27  2015      Y
4         651029.0         Harbor Co   $15,000.00     $12750.00        -15.00%    Closed      2    2  2014      N

>>> df.dtypes
Customer Number    float64
Customer Name       object
2016                object
2017                object
Percent Growth      object
Jan Units           object
Month                int64
Day                  int64
Year                 int64
Active              object

>>> df.info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5 entries, 0 to 4
Data columns (total 10 columns):
 #   Column           Non-Null Count  Dtype
---  ------           --------------  -----
 0   Customer Number  5 non-null      float64
 1   Customer Name    5 non-null      object
 2   2016             5 non-null      object
 3   2017             5 non-null      object
 4   Percent Growth   5 non-null      object
 5   Jan Units        5 non-null      object
 6   Month            5 non-null      int64
 7   Day              5 non-null      int64
 8   Year             5 non-null      int64
 9   Active           5 non-null      object
dtypes: float64(1), int64(3), object(6)
memory usage: 528.0+ bytes

```
### 如何转换Pandas数据类型

为了在 Pandas 中转换数据类型，有三个基本选项：
1. 使用 astype() 来强制转换到合适的 dtype. 但是需要注意astype() 只能针对数据类型很干净的情况，如果源数据中
有不同类型数据，或者含有特殊字符则无法进行转换。
例如：
1). 上表中Customer Number可以从Object转换为int
2). 但同样的方法无法把2016列数据从object转换为数字，因为其中包含着￥符号
```
>>>> df["Customer Number"] = df['Customer Number'].astype('int')

>>>> df['2016'].astype('float')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "D:\05_Tools\Python37\lib\site-packages\pandas\core\generic.py", line 5698, in astype
    new_data = self._data.astype(dtype=dtype, copy=copy, errors=errors)
  File "D:\05_Tools\Python37\lib\site-packages\pandas\core\internals\managers.py", line 582, in astype
    return self.apply("astype", dtype=dtype, copy=copy, errors=errors)
  File "D:\05_Tools\Python37\lib\site-packages\pandas\core\internals\managers.py", line 442, in apply
    applied = getattr(b, f)(**kwargs)
  File "D:\05_Tools\Python37\lib\site-packages\pandas\core\internals\blocks.py", line 625, in astype
    values = astype_nansafe(vals1d, dtype, copy=True)
  File "D:\05_Tools\Python37\lib\site-packages\pandas\core\dtypes\cast.py", line 897, in astype_nansafe
    return arr.astype(dtype, copy=True)
ValueError: could not convert string to float: '$125,000.00'
```
2. 创建一个自定义函数来转换数据
Pandas支持自定义转换函数。当然如果转换方法简单，也可以直接使用lambda函数进行。


对于货币转换（这个特定的数据集），可以自定义一个转换函数：
```
def convert_currency(val):
    # input: $125,000.00
    # expect output: 12500000.0
    new_val = val.replace(',', '').replace('$','')
    return float(new_val)

df = pd.read_csv("example.csv")
print(df['2016'].head())
df['2016'] = df['2016'].apply(convert_currency)
print(df['2016'].head())

output:
    0    $125,000.00
    1    $920,000.00
    2     $50,000.00
    3    $350,000.00
    4     $15,000.00
    Name: 2016, dtype: object
    0    125000.0
    1    920000.0
    2     50000.0
    3    350000.0
    4     15000.0
    Name: 2016, dtype: float64
```
直接使用lambda进行转换：
```
df['2016'].apply(lambda x: x.replace('$', '').replace(',', '')).astype('float')
```
3. 使用 Pandas 的函数，例如 to_numeric() 或 to_datetime()

使用Pandas自带的to_datatime()函数可以方便地把日期整理成合适的格式
```
>>> pd.to_datetime(df[['Month', 'Day', 'Year']])
0   2015-01-10
1   2014-06-15
2   2016-03-29
3   2015-10-27
4   2014-02-02
dtype: datetime64[ns]

```
结合numpy.where() 函数可以对数据进行映射转换，例如把上表中的Active中的Y/N转换为bool类型
```
df["Active"] = np.where(df["Active"] == "Y", True, False)
```

### 使用Pandas中的map, apply, applymap函数逐行逐列对数据进行转换
1. Pandas中的map、apply和applymap可以实现对一个DataFrame进行逐行、逐列和逐元素的操作。
2. map和apply函数可以对一列或一行进行操作
2. applymap函数会对DataFrame中的每个单元格执行指定函数的操作
3. DataFrame中axis=0代表操作对列columns进行，axis=1代表操作对行row进行

例子：
```
import numpy as np
import pandas as pd

boolean = [True, False]
gender = ["男", "女"]
color = ["white", "black", "yellow"]
data = pd.DataFrame( {
    "height": np.random.randint( 150, 190, 100 ),
    "weight": np.random.randint( 40, 90, 100 ),
    "smoker": [boolean[x] for x in np.random.randint( 0, 2, 100 )],
    "gender": [gender[x] for x in np.random.randint( 0, 2, 100 )],
    "age": np.random.randint( 15, 90, 100 ),
    "color": [color[x] for x in np.random.randint( 0, len( color ), 100 )]
}
)
print("Before: ", data.head())
# 1. 使用map函数把gender中的数据映射为bool类型
data["gender"] = data["gender"].map({"男":True, "女":False})
print("After: ", data.head())

# 2. 使用自定义的转换函数
def convert(val):
    gender = "男" if val == True else "女"
    return gender

data["gender"] = data["gender"].map(convert)
print( "After: ", data.head() )

```

### 参考
1. Pandas 数据类型概览 https://juejin.im/post/6844903589341560839
2. Pandas 数据转换函数 https://zhuanlan.zhihu.com/p/100064394


### Pandas可以读取excel表格
```
data = pd.read_excel(io, sheet_name = 'test', usecols = [0, 1, 3])
```
### Pandas可以读取SQL
```
conn=create_engine('mysql+pymysql://root:root@localhost:3306/test')
sql = "select * from test.student"
df1 = pd.read_sql(sql, conn)
print(df1)

# save DataFrame to MySQL
pd.to_sql()
```

## 4.4 Pandas 数据预处理

### 常见的预处理步骤：清洗数据

1. 查看数据维度以及数据类型
```
data = pd.read_csv('example.csv')
print(data.head())
print(data.info())
print(data.shape)
print(data.describe())
```
1. 去除重复项
```
data = pd.DataFrame(data=[['a',1],['a',2],['b',1],['b',2],['a',1]],columns=['label','num'])
print(data)
# get the duplicated items
print(data[data.duplicated(keep=False)])
# get the duplicated items
print(data.drop_duplicates(keep=False))
```
1. 处理缺失值
根据数据的不同会做出不同的选择，有用均值填充的，中位数填充的，用0填充的，甚至直接去除的。
```
# 用均值填充
hr.fillna(hr.mean())
# 用中位数填充
hr.fillna(hr.median())
# 用0填充
hr.fillna(0)
```