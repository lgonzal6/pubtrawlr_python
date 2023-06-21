import pandas as pd
import numpy as np
from pmidcite.icite.downloader import get_downloader

def upload_csv(file_path):
    '''
    Upload csv of query into a dataframe
    '''
    return pd.read_csv(file_path)

def get_pmids(query):
    '''
    Take the columns of pmid's and make them into a list
    '''
    return query['pmid'].tolist()

def get_icites(pmids):
    '''
    Call on iCite to get citation information for each pmid
    '''
    dnldr = get_downloader()
    return dnldr.get_icites(pmids)

def create_cite_table(nih_entries):
    '''
    Make and sort citation table
    '''
    cite_table = {}
    title = []
    authors = []
    year = []
    journal = []
    citation_count = []

    for i in nih_entries:
        title.append(i.dct['title'])

        author = i.dct['authors']
        authors.append(', '.join(author))

        year.append(i.dct['year'])
        journal.append(i.dct['journal'])

        citation_count.append(i.dct['num_cite'])

    cite_table['Title'] = title
    cite_table['Author(s)'] = authors
    cite_table['Year'] = year
    cite_table['Journal'] = journal
    cite_table['Total Citations'] = citation_count

    cite_df = pd.DataFrame(cite_table)
    return cite_df.sort_values(by='Total Citations', ascending=False)

def to_json(cite_df):
    '''
    Make citation table into json file
    '''
    return cite_df.to_json(orient='records')

def make_csv(df):
    df.to_csv('test_table.csv', index=False)

if __name__ == '__main__':
    ### This part here needs to change so that what we are uploading is a csv of the query
    query = upload_csv('./alz.csv')
    
    ### Calling the rest of the functions
    pmids = get_pmids(query)
    nih_entries = get_icites(pmids)
    cite_df = create_cite_table(nih_entries)
    json_table = to_json(cite_df)
    make_csv(cite_df)
