import pandas as pd
import input_downloader
from utils import VARIABLES


BOOKS_CSV_PATH = '_input/BX-Books.csv'
SITE_DATA_CSV_PATH = '_input/SITE_DATA.CSV'
BOOKS_FINAL_PATH = '_output/BOOKS.CSV'
AUTHORS_FINAL_PATH = '_output/AUTHORS.CSV'
BOOKS_AUTHORS_FINAL_PATH = '_output/BOOKS_AUTHORS.CSV'

_input_downloader = input_downloader.InputDownloader(VARIABLES['raw_zip'])
_input_downloader.run()

books_data_rough_df = pd.read_csv(BOOKS_CSV_PATH,
                                      sep=';',
                                      encoding='ISO-8859-14',
                                      quotechar='"',
                                      escapechar='\\')
books_data_rough_df['Book-Author'] = (books_data_rough_df['Book-Author']
                                          .str.title())

books_data_rough_df['Book-Author_old'] = books_data_rough_df['Book-Author']
books_data_rough_df['Book-Author'] = (books_data_rough_df['Book-Author']
                                      .str.split('&'))
books_data_rough_df = books_data_rough_df.explode('Book-Author')

authors_series = books_data_rough_df['Book-Author']
authors_df = (authors_series.drop_duplicates()
              .reset_index(drop=True)
              .reset_index()
              .rename(columns={'index': 'id'}))

books_df = pd.DataFrame({
    'ISBN': books_data_rough_df['ISBN'],
    'Book-Title': books_data_rough_df['Book-Title'],
    'Year-Of-Publication': books_data_rough_df['Year-Of-Publication'],
    'Image-URL-S': books_data_rough_df['Image-URL-S'],
    'Image-URL-M': books_data_rough_df['Image-URL-M'],
    'Image-URL-L': books_data_rough_df['Image-URL-L']
}).drop_duplicates(subset='ISBN')

books_authors_df = (books_data_rough_df.merge(authors_df,
                                              on='Book-Author')[['ISBN', 'id']]
                    .rename(columns={'ISBN': 'books_id',
                                     'id': 'authors_id'}))

books_df.to_csv(BOOKS_FINAL_PATH, index=False)
authors_df.to_csv(AUTHORS_FINAL_PATH, index=False)
books_authors_df.to_csv(BOOKS_AUTHORS_FINAL_PATH, index=False)
