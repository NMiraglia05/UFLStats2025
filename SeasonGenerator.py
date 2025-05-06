def SeasonStats():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup
    import pandas as pd
    import time

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--log-level=3")
    options.add_argument('--ignore-certificate-errors')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)


    def load_page(url):
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        time.sleep(2)
        return driver.page_source


    def extract_data(html):
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        all_data = []
        for table in tables:
            rows = table.find_all("tr")[1:]
            for row in rows:
                row_data = [td.text.strip() for td in row.find_all("td")]
                if row_data and row_data[0] not in ["Team", "Opponents"]:
                    all_data.append(row_data)

        return all_data


    def get_headers(url):
        html_content = load_page(url)
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table")
        if table:
            thead = table.find("thead")
            if thead:
                rows = thead.find_all("tr")
                if len(rows) > 1:
                    return [th.text.strip() for th in rows[1].find_all("th")]
                return [th.text.strip() for th in rows[0].find_all("th")]

        return []

    def cleandf(df):
        df=pd.DataFrame(df)
        dropcolumns=['#']
        for col in dropcolumns:
            try:
                df=df.drop(columns=col,axis=1)
            except KeyError:
                pass
        return df
    
    def convertdf(df):
        df=pd.DataFrame(df)
        for col in df.columns:
            try:
                df=pd.to_numeric(col,errors='raise')
            except (ValueError,TypeError):
                pass
        return df


    teams = [
        'arlington', 'birmingham', 'dc', 'houston',
        'memphis', 'michigan', 'san-antonio', 'st-louis'
    ]

    pages = [
        #'passing', 'rushing', 'receiving', 'defense',
        'field-goals', #'punt-returns', 'kick-returns'
    ]

    baseurl = 'https://www.theufl.com/teams/'
    statsurl = '/stats/individual?stats-category='
    all_results = []

    with pd.ExcelWriter('C:\\Users\\miragn\\Python\\UFL\\SeasonStats.xlsx',mode='a',if_sheet_exists='replace') as writer:
        for page in pages:
            headers = []
            for team in teams:
                pageurl = baseurl + team + statsurl + page
                headers = get_headers(pageurl)

                try:
                    html_content = load_page(pageurl)
                    extracted_data = extract_data(html_content)
                    all_results.extend(extracted_data)
                except Exception:
                    pass

            df = pd.DataFrame(all_results, columns=headers)

            df=cleandf(df)

            if page in ['passing', 'rushing', 'receiving']:
                split_cols = df['FUM-LST'].str.split('-', expand=True)
                split_cols.columns = ['Fum', 'Lst']
                df = pd.concat([df, split_cols], axis=1)
                df.drop(columns='FUM-LST', inplace=True)
                if page == 'passing':
                    split_cols = df['C-A-I'].str.split('-', expand=True)
                    split_cols.columns = ['C', 'A', 'I']
                    df = pd.concat([df, split_cols], axis=1)
                    cols = df.columns.tolist()
                    for col in ['C', 'A', 'I']:
                        cols.remove(col)
                    insert_at = cols.index('C-A-I') + 1
                    for i, col in enumerate(['C', 'A', 'I']):
                        cols.insert(insert_at + i, col)
                    df = df[cols]
                    df.drop(columns='C-A-I', inplace=True)

            elif page == 'defense':
                split_cols = df['TFL - Yds'].str.split('-', expand=True)
                split_cols.columns = ['TFL', 'Yds(TFL)']
                df = pd.concat([df, split_cols], axis=1)
                cols = df.columns.tolist()
                for col in ['TFL', 'Yds(TFL)']:
                    cols.remove(col)
                insert_at = cols.index('TFL - Yds') + 1
                for i, col in enumerate(['TFL', 'Yds(TFL)']):
                    cols.insert(insert_at + i, col)
                df = df[cols]
                df.drop(columns='TFL - Yds', inplace=True)

            elif page == 'field-goals':
                newcolumns=['Name','Distance','Category','Value']
                df=pd.DataFrame(df)
                df1=pd.DataFrame(columns=newcolumns)
                for col in df.columns:
                    if not '-' in col:
                        pass
                    else:
                        df2=pd.DataFrame(columns=newcolumns)
                        df2['Name']=df['Name']
                        if col=='Made-Att':
                            distance='Total'
                        else:
                            distance=col
                        df2['Distance']=distance
                        split_cols = df[col].str.split('-', expand=True)
                        split_cols.columns=['Made','Att']
                        for subcol in split_cols:
                            df2['Category']=subcol
                            df2['Value']=split_cols[subcol]
                            df1 = pd.concat([df1, df2], ignore_index=True)
            
                df=df1

            df=convertdf(df)

            try:
                df.to_excel(writer,sheet_name=page,index=False)
            except FileNotFoundError:
                df.to_excel('SeasonStats.xlsx',index=False,sheet_name=page)
            all_results = []

    driver.quit()
