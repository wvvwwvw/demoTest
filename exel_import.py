import pandas as pd
from connect_to_database import connect_db

# file_path1 = "exel_data/partners_types.xlsx"
#
# data_file1 = pd.read_excel(file_path1)
#
# cursor = connect_db.cursor()
#
# query1 = "insert into Types (name) values (%s)"
#
# data1 = list(data_file1.itertuples(index=False, name=None))
#
# cursor.executemany(query1, data1)
# connect_db.commit()
# cursor.close()


# file_path2 = "exel_data/Product_type_import.xlsx"
#
# data_file2 = pd.read_excel(file_path2)
#
# cursor = connect_db.cursor()
#
# query2 = "insert into ProductsTypes (name, types_rate) values (%s, %s)"
#
# data2 = list(data_file2.itertuples(index=False, name=None))
#
# cursor.executemany(query2, data2)
# connect_db.commit()
# cursor.close()


# file_path3 = "exel_data/Partners_import.xlsx"
#
# data_file3 = pd.read_excel(file_path3)
#
# cursor = connect_db.cursor()
#
# query3 = "insert into Partners (type_id, name, address, inn, FIO, email, phone, rating) values (%s, %s, %s, %s, %s, %s, %s, %s)"
#
# data3 = list(data_file3.itertuples(index=False, name=None))
#
# cursor.executemany(query3, data3)
# connect_db.commit()
# cursor.close()


# file_path4 = "exel_data/Products_import.xlsx"
#
# data_file4 = pd.read_excel(file_path4)
#
# cursor = connect_db.cursor()
#
# query4 = "insert into Products (type_id, name, article, min_price) values (%s, %s, %s, %s)"
#
# data4 = list(data_file4.itertuples(index=False, name=None))
#
# cursor.executemany(query4, data4)
# connect_db.commit()
# cursor.close()



# file_path5 = "exel_data/Partner_products_import.xlsx"
#
# data_file5 = pd.read_excel(file_path5)
#
# query = "insert into Sales (product_id, partner_id, quantity, date_sale) values (%s, %s, %s, %s)"
#
# cursor = connect_db.cursor()
#
# data5 = list(data_file5.itertuples(index=False, name=None))
#
# cursor.executemany(query, data5)
# connect_db.commit()
# cursor.close()
