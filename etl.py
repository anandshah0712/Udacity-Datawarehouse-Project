import configparser
import psycopg2
from sql_queries import copy_table_queries,insert_table_queries


def load_staging_tables(cur, conn):  
    '''Function :- load_staging_tables loads the data from the files in S3 into both the staging tables on Redshift database in AWS'''    
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()
        
def load_final_tables(cur, conn):
    '''Function :- load_final_tables loads the data from the staging tables into the final dimension/fact tables on Redshift database   
       in AWS'''
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()
        
def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    print(load_staging_tables.__doc__)
    load_staging_tables(cur, conn)
    print(load_final_tables.__doc__)
    load_final_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
