import json
import pandas as pd


def extract_excel_text(file_path: str):
    excel = pd.ExcelFile(file_path)

    workbook = {
        "workbook": file_path,
        "sheets": [],
    }

    llm_text = ""

    for sheet in excel.sheet_names:
        df = pd.read_excel(
            file_path,
            sheet_name=sheet,
        )

        workbook["sheets"].append(
            {
                "name": sheet,
                "rows": len(df),
                "columns": list(df.columns),
                "preview": df.head(10).fillna("").to_dict(
                    orient="records"
                ),
            }
        )

        llm_text += f"""

Sheet: {sheet}

Columns:
{", ".join(df.columns)}

Preview:

{df.head(10).to_string(index=False)}

"""

    return (
        llm_text,
        json.dumps(workbook),
    )