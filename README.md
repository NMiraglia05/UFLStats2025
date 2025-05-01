## How to Run

1. Install required libraries:
   ```bash
   pip install pandas selenium beautifulsoup4

# UFLStats2025
Update repository for 2025 stats.

This project consists of 2 general compoents: the code that generates statistical spreadsheets, and the dashboard that utilizes the spreadsheets.

The components of the code are as follows:

StatController.py
  This script serves as the central controller for the UFL stats pipeline. It coordinates the following key steps to ensure data is updated and archived correctly:
  
  📅 Week Determination
  Uses weeknumber to identify the most recent completed UFL week.
  
  Designed to look backward in time, not forward.
  
  Recommended to run this script on Sunday evening after all games conclude.
  
  If run later in the week, reduce the week number by 1 to reflect the correct game week.
  
  📊 Stats Generation
  SeasonStats: Updates the season-long stats spreadsheet with current cumulative performance data for each player.
  
  WeeklyStats: Creates a new spreadsheet for weekly performance based on the identified game week.
  
  🗂 Archiving
  Uses shutil to create a copy of the season stats as an archive for the current week.
  
  Does not overwrite an existing weekly archive—consistency in run timing is important.
  
  📈 Dashboard Prep
  Appends all worksheets from the season stats file into a single fact table.
  
  This fact table powers the analytics dashboard.

SeasonGenerator.py
  This script generates the Excel file that records up-to-date season statistics.

  Extraction
  
  URL Creation:
  Lists of pages and teams are used to dynamically generate the URLs to extract data from.
  
  Scraping:
  Selenium and BeautifulSoup extract the stat tables from each webpage. For each stat category (passing, receiving, rushing, etc.), data is collected across all teams and combined into a single table per category. These       are stored in dataframes.
  
  Transformation
  
  Cleaning:
  Certain columns (e.g., FUM-Lst) contain dashes and are treated as strings. These are split into two columns (e.g., FUM and LST) to allow numeric operations. Similar logic applies to columns like C-A-I in the passing         page. Cleaning rules are applied conditionally based on the stat category.
  
  Type Conversion:
  The script attempts to convert all columns to numeric types—integers when possible, floats otherwise—skipping over non-numeric columns like player names.
  
  Loading
  An ExcelWriter object is used to save each dataframe into SeasonStats.xlsx. If the file does not exist, it is created. The ExcelWriter ensures that each sheet is updated without overwriting the others. Existing sheets       are replaced with updated data to keep the file current.

WeekGenerator.py
  Generates a weekly Excel file capturing player performance for the current week.
  
  Purpose
  To isolate and record weekly statistics by comparing the latest season totals with the previous week's totals.
  
  Process Overview
  1. Extraction
  
  df1: Pulled from the current SeasonStats.xlsx to get up-to-date cumulative stats.
  
  df2: Pulled from the archived SeasonStats file of the previous week.
  
  2. Transformation
  
  Cleaning
  Uses a dropcolumns dictionary to remove columns irrelevant to weekly analysis (varies by stat type).
  
  Combining
  Merges df1 and df2 using a left join on the "Name" column.
  
  Processing
  
  Columns from df1 have _x; from df2, _y.
  
  Weekly stats = _x minus _y.
  
  Conditional logic is applied to compute category-specific averages.
  
  3. Loading
  
  Writes the final df3 to a new Excel file named for the specific week.
  
  Uses ExcelWriter in append mode to avoid overwriting existing sheets.
  
  If the file doesn’t exist, it is created.

Dashboard Creator
  Generates a unified fact table for use in the dashboard.
  
  Purpose
  To combine all relevant stat tables into a single, wide-format table for easier data modeling and dashboard creation.
  
  Process Overview
  1. Extraction
  Each page (e.g., Passing, Rushing, Receiving) from the SeasonStats.xlsx file is read using pandas.
  
  2. Transformation
  All columns are renamed with a prefix indicating their source page. For example, columns from the "Passing" sheet become passing_Yds, passing_TD, etc. This ensures clear traceability across combined datasets.
  
  3. Loading
  Each transformed dataframe is added to a list (dashboard_df).
  Once all sheets are processed, they are concatenated horizontally (axis=1), resulting in a single wide dataframe that merges stats across all categories.
  The final dataframe is saved to Excel, overwriting any existing file.
