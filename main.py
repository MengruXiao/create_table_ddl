import streamlit as st
import pandas as pd
import io

def parse_excel(file):
    # 读取Excel文件
    df = pd.read_excel(file, header=None)

    tables = []
    current_table = None

    for index, row in df.iterrows():
        if pd.isna(row[0]):
            continue  # 跳过空行

        if row[0].startswith('目标表:'):
            if current_table:
                tables.append(current_table)
            current_table = {'table_name': row[0].split(":")[1], 'columns': []}
        else:
            column_name = row[0]
            column_type = row[1]
            current_table['columns'].append((column_name, column_type))

    if current_table:  # 添加最后一个表
        tables.append(current_table)

    return tables


def generate_sql(tables):
    sql_statements = []
    for table in tables:
        columns = ',\n'.join([f"  {col} {typ}" for col, typ in table['columns']])
        sql = f"CREATE TABLE {table['table_name']} (\n{columns}\n);"
        sql_statements.append(sql)
    return sql_statements


def main():
    st.title("Excel to SQL Create Table Statements")
    file = st.file_uploader("Upload your Excel file", type=["xlsx"])

    if file is not None:
        tables = parse_excel(file)
        sql_statements = generate_sql(tables)

        st.header("Generated SQL Statements")
        for sql in sql_statements:
            st.code(sql, language='sql')

        sql_content = '\n'.join(sql_statements)

        # 创建一个文本文件并提供下载链接
        st.download_button(
            label="Download SQL File",
            data=io.StringIO(sql_content).read(),
            file_name="create_tables.sql",
            mime="text/plain"
        )







if __name__ == "__main__":
    main()