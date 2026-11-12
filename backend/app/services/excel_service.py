import json
import pandas as pd


def extract_excel_text(file_path: str):
    excel = pd.ExcelFile(file_path)

    workbook = {
        "sheets": [],
    }

    llm_text = ""

    for sheet in excel.sheet_names:
        df = pd.read_excel(
            file_path,
            sheet_name=sheet,
        )

        df.columns = [str(column).strip() for column in df.columns]
        unnamed_columns = [column for column in df.columns if not column or column.lower().startswith("unnamed")]
        duplicate_rows = int(df.duplicated().sum())
        empty_cells = int(df.isna().sum().sum())
        numeric_columns = df.select_dtypes(include="number")
        negative_cells = int((numeric_columns < 0).sum().sum())
        warnings = []
        errors = []
        if unnamed_columns:
            errors.append(f"Unnamed columns: {', '.join(unnamed_columns)}")
        if duplicate_rows:
            warnings.append(f"{duplicate_rows} duplicate rows found")
        if empty_cells:
            warnings.append(f"{empty_cells} empty cells found")
        if negative_cells:
            warnings.append(f"{negative_cells} negative numeric values found")

        workbook["sheets"].append(
            {
                "name": sheet,
                "rows": len(df),
                "columns": list(df.columns),
                "preview": df.head(10).fillna("").to_dict(
                    orient="records"
                ),
                "validation": {"errors": errors, "warnings": warnings},
            }
        )

        workbook.setdefault("source_chunks", []).append(
            {
                "location": f"sheet {sheet}",
                "text": df.head(100).fillna("").to_string(index=False),
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
        json.dumps(workbook, default=str),
    )
