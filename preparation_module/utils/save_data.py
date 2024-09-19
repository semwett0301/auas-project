from preparation_module.settings import USE_CSV
from common_module.db import engine


def save_data(data, csv_path, table_name):
    if USE_CSV:
        data.to_csv(csv_path)
    else:
        data.to_sql(table_name, engine, if_exists='append', index=False)