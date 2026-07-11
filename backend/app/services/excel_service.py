import pandas as pd


def extract_excel_text(file_path: str):

    excel = pd.ExcelFile(file_path)

    final_text = ""

    final_text += f"Workbook: {file_path}\n\n"

    final_text += "Sheets:\n"

    for sheet in excel.sheet_names:
        final_text += f"- {sheet}\n"

    final_text += "\n"

    for sheet in excel.sheet_names:

        df = pd.read_excel(
            file_path,
            sheet_name=sheet,
        )

        final_text += "=" * 60 + "\n"

        final_text += f"Sheet: {sheet}\n"

        final_text += "=" * 60 + "\n"

        final_text += f"Rows: {len(df)}\n"

        final_text += f"Columns: {len(df.columns)}\n\n"

        final_text += "Column Names:\n"

        for col in df.columns:
            final_text += f"- {col}\n"

        final_text += "\n"

        final_text += "First 10 Rows:\n\n"

        final_text += df.head(10).to_string(index=False)

        final_text += "\n\n"

    return final_text