def WeeklyStats(week):
    import pandas as pd
    from pathlib import Path

    pages = [
        'passing', 'rushing', 'receiving',
        'punt-returns', 'kick-returns'
    ]

    tfcolumns = {
        'passing':{
            'dropcolumns':['#', 'GP', 'Eff', 'Pct', 'Lng', 'Avg/Gm'],
            'avgcolumns':{
                'Pct':('Pct','C','A'),
                'Avg/C':('Avg/C','Yds','C')
            }
        },
        'rushing':{
            'dropcolumns':['#', 'GP', 'Gain', 'Loss', 'Avg', 'Lng', 'Avg/Gm'],
            'avgcolumns':('Avg','Net','Att')
        },
        'receiving':{
            'dropcolumns':['#', 'GP', 'Avg', 'Lng', 'Avg/Gm'],
            'avgcolumns':('Avg','Yds','REC')
        },
        'punt-returns':{
            'dropcolumns':['#', 'GP', 'Avg', 'Lng'],
            'avgcolumns':('Avg','Yds','No.')
        },
        'kick-returns':{
            'dropcolumns':['#', 'GP', 'Avg', 'Lng'],
            'avgcolumns':('Avg','Yds','No.')
        }
    }

    def dfclean(df,page):
        df=pd.DataFrame(df)
        for col in tfcolumns[page]['dropcolumns']:
            try:
                df=df.drop(columns=col,axis=1)
            except Exception:
                pass
        return df

    lastweek = week - 1 #takes the current week, and sets it back 1. This is so that the conversion logic below is working on the correct file. Without this line, you will get all 0.
    file=Path(f'C:\\Users\\miragn\\Python\\UFL\\WeekStats\\Week {week}.xlsx')

    if not file.exists():
        df=pd.DataFrame()
        df.to_excel(file,index=False)
    else:
        pass

    with pd.ExcelWriter(file, mode='a', if_sheet_exists='replace') as writer:
        for page in pages:
            df1 = pd.DataFrame(dfclean(pd.read_excel("C:\\Users\\miragn\\Python\\UFL\\SeasonStats.xlsx", sheet_name=page),page))
            df2 = pd.DataFrame(dfclean(pd.read_excel(f"C:\\Users\\miragn\\Python\\UFL\\SeasonStats\\Week{lastweek}.xlsx", sheet_name=page),page))
            merged = pd.merge(df1, df2, how='left', on='Name').fillna(0)
            
            df3 = pd.DataFrame()
            df3['Name'] = df1['Name']
            
            for col in df1.columns: #this will subtract the seasonal stats from the seasonal stats for the previous week. This calculates the difference, which functions to show the performance for a given week.
                try:
                    df3[col] = merged[f'{col}_x'] - merged[f'{col}_y']
                except KeyError:
                    pass

            try:
                checker=tfcolumns[page]['avgcolumns']
                if isinstance(checker,dict):
                    for key in tfcolumns[page]['avgcolumns'].keys():
                        if key=='Pct':
                            df3[key]=(tfcolumns[page]['avgcolumns'][1]/tfcolumns[page]['avgcolumns'][2])*100
                        else:
                            df3[key]=tfcolumns[page]['avgcolumns'][1]/tfcolumns[page]['avgcolumns'][2]
                else:
                    df3[tfcolumns[page]['avgcolumns'][0]]=df3[page]['avgcolumns'][1]/df3[page]['avgcolumns'][2]
            except KeyError:
                pass

            try:
                df3.to_excel(writer, sheet_name=page, index=False)
            except ValueError:
                pass
            except FileNotFoundError:
                df3.to_excel(f'C:\\Users\\miragn\\Python\\UFL\\WeekStats\\Week {week}.xlsx', sheet_name=page, index=False)
