import pandas as pd
import os.path


def save_data_to_excel(heading_dict, post_dict, file_name):
    # change dictionary to dataframe object
    heading_df = pd.DataFrame(heading_dict)
    post_df = pd.DataFrame(post_dict)

    sheets = {"post_details": post_df, "heading_details": heading_df}

    excel_file = '{}.xlsx'.format(file_name)

    # Check if the file exist or not
    if os.path.isfile(excel_file):
        with pd.ExcelWriter(excel_file, mode='a', if_sheet_exists='overlay') as file:
            for sheet in file.sheets:
                sheet_rows_num = file.sheets[sheet].max_row
                sheets[sheet].to_excel(file, startrow=sheet_rows_num, index=False, header=False, sheet_name=sheet)
    else:
        with pd.ExcelWriter(excel_file) as file:
            for sheetname, df_name in sheets.items():
                df_name.to_excel(file, index=False, sheet_name=sheetname)