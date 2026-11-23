
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(
    __name__,
    template_folder="web_pages",
    static_folder="design_assets"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "dataset_storage")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():

    data = None
    error = None

    if request.method == "POST":

        file = request.files.get("dataset")

        if not file or file.filename == "":
            error = "Please select a CSV file."

        elif not file.filename.lower().endswith(".csv"):
            error = "Only CSV files are allowed."

        else:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            try:
                file.save(filepath)

                df = pd.read_csv(filepath)

                if df.empty or len(df.columns) == 0:
                    raise ValueError("The uploaded dataset is empty.")

                # Basic information
                total_rows = len(df)
                total_columns = len(df.columns)

                # Missing values
                missing_values = df.isnull().sum().to_dict()
                total_missing = int(df.isnull().sum().sum())

                # Numeric analysis
                numeric_columns = df.select_dtypes(
                    include=np.number
                ).columns.tolist()

                statistics = {}

                for column in numeric_columns:
                    statistics[column] = {
                        "mean": round(float(df[column].mean()), 2),
                        "median": round(float(df[column].median()), 2),
                        "minimum": round(float(df[column].min()), 2),
                        "maximum": round(float(df[column].max()), 2)
                    }

                # Column information
                column_info = []

                for column in df.columns:
                    column_info.append({
                        "name": str(column),
                        "type": str(df[column].dtype),
                        "missing": int(df[column].isnull().sum())
                    })

                # Dataset preview
                preview = (
                    df.head(10)
                    .fillna("")
                    .astype(str)
                    .to_dict(orient="records")
                )

                # Chart data
                chart_labels = []
                chart_values = []
                chart_title = "Dataset Analysis"

                if numeric_columns:

                    numeric_column = numeric_columns[0]

                    categorical_columns = df.select_dtypes(
                        include=["object", "category"]
                    ).columns.tolist()

                    if categorical_columns:
                        category = categorical_columns[0]

                        grouped = (
                            df.groupby(category, dropna=True)[numeric_column]
                            .mean()
                            .head(10)
                        )

                        chart_labels = [
                            str(item) for item in grouped.index
                        ]

                        chart_values = [
                            round(float(value), 2)
                            for value in grouped.values
                        ]

                        chart_title = (
                            f"Average {numeric_column} by {category}"
                        )

                    else:
                        sample = df[numeric_column].head(10)

                        chart_labels = [
                            f"Row {i + 1}"
                            for i in range(len(sample))
                        ]

                        chart_values = [
                            float(value) if pd.notna(value) else 0
                            for value in sample
                        ]

                        chart_title = f"{numeric_column} Analysis"

                data = {
                    "filename": filename,
                    "rows": total_rows,
                    "columns": total_columns,
                    "missing": total_missing,
                    "column_info": column_info,
                    "statistics": statistics,
                    "missing_values": missing_values,
                    "preview": preview,
                    "chart_labels": chart_labels,
                    "chart_values": chart_values,
                    "chart_title": chart_title
                }

            except Exception as e:
                error = f"Unable to analyze dataset: {str(e)}"

    return render_template(
        "analytics.html",
        data=data,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
