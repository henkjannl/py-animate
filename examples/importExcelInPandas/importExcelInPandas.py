import pandas as pd

for sheet in ['Script', 'Moves']:
    df = pd.read_excel (r'BulldozerTable.xls', sheet_name=sheet, header=None)
    print(sheet)
    print (df)

    print('Row count:', df.shape[0])    
    print('Col count:', df.shape[1])    
    for row, col in [ (0,3), (1,0), (1,1), (3,0) ]:
        print(df.loc[row,col], end=' > ')
        if pd.isnull(df.loc[row,col]):
            print('null')
        elif isinstance(df.loc[row,col], str):
            print('string')
        elif isinstance(df.loc[row,col], int):
            print('integer')
        elif isinstance(df.loc[row,col], float):
            print('float')
        else:
            print(type(df.loc[row,col]))
            
    
