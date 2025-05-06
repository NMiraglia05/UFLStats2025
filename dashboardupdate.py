def UpdateDashboard():
    import pandas as pd

    path= 'C:\\Users\\miragn\\Python\\UFL\\SeasonStats.xlsx'

    def dfconvert(df):
        df=pd.DataFrame(df)
        for col in df.columns:
            try:
                df[col]=pd.to_numeric(df[col])
            except (ValueError,TypeError):
                pass
        return df

    page1s = [
        'passing', 'rushing', 'receiving', 'defense',
        'field-goals', 'punt-returns', 'kick-returns'
    ]

    pages={
        'passing':['Eff','GP'],
        'rushing':['Gain','Loss'],
        'receiving':[],
        'defense':[],
        'field-goals':[],
        'punt-returns':[],
        'kick-returns':[]
    }

    dashboarddf=pd.DataFrame(columns=['Name'])

    with pd.ExcelWriter("C:\\Users\\miragn\\Python\\UFL\\Dashboard\\stats.xlsx",mode='a',if_sheet_exists='replace') as writer:
        for key in pages.keys():
            df=pd.read_excel(path,sheet_name=key)
            df=dfconvert(df)
            df=df.drop(columns=pages[key])
            for col in df.columns:
                if col=='Name':
                    pass
                else:
                    df.rename(columns={col:f'{key}_{col}'},inplace=True)
            dashboarddf=pd.concat([dashboarddf,df],ignore_index=True)
        dashboarddf.to_excel(writer,index=False)
