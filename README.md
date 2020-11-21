# Project : REPORTING AFTER DATA CLEANSING
- Bibtext files have huge amount of data, which can be advantageous to the users ( publisher, researchers, organisers, etc.)
- This project aims at providing Visualizations of such important metrics of the bibtext file at a glance.

Assumption: The user provides the file in IEEE bibtext format.

- Description:
  - Pre-processing Step : First the Bibtext files were Analyzed manually and the co-relation between different fields was found and noted.
  - Input : The user uploads a bibtext file.
  - Output: Appropriate graphs are plotted and the final Output/Visualisation will be presented on an HTML page.
 
- Visualization:
  - Using the co-relation found between different fields in the Pre-processing Step, the following visualisations were plotted:
    - Page Count
    - Month Vs Paper Published In Month
    - Year Vs Paper
    - Year Vs Paper Per Month
    - Month Vs Paper Per Year
    - Historical trend for keyword
    - Overall Keyword Count
    - Wordcloud Visulization
    - Author Vs Number of Paper


- Description:
  - Matploilib
  - Pandas
  - bibtexparser
  - wordcloud
  - django
 
- Installation:
  - pip install matploilib
  - pip install django
  - pip install wordcloud
  - pip install pandas
  - pip install bibtexparser 
  - pip install OrderedDict

- Build And Run:
  - Change Directory to SSD26 manage.py and run it using : python manage.py runserver



    
      


