import { useEffect, useState } from "react";
import {
  uploadExcel,
  getExcels,
  deleteExcel,
} from "../../services/excelAnalyzerService";

export default function ExcelAnalyzer() {
  const [files, setFiles] = useState([]);
  const [selected, setSelected] = useState(null);
  const [workbook, setWorkbook] = useState(null);
  const [selectedSheet, setSelectedSheet] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadFiles();
  }, []);

  async function loadFiles() {
    try {
      const data = await getExcels();

      setFiles(data);

      if (data.length > 0) {
        selectWorkbook(data[0]);
      }
    } catch (err) {
      toast.error(
      err.response?.data?.detail ||
      "Something went wrong."
    );
    }
  }

  function selectWorkbook(file) {
    setSelected(file);

    if (file.workbook_json) {
      const wb = JSON.parse(file.workbook_json);

      setWorkbook(wb);

      if (wb.sheets.length > 0) {
        setSelectedSheet(wb.sheets[0]);
      } else {
        setSelectedSheet(null);
      }
    } else {
      setWorkbook(null);
      setSelectedSheet(null);
    }
  }

  async function handleUpload(e) {
    const file = e.target.files[0];

    if (!file) return;

    setLoading(true);

    try {
      const uploaded = await uploadExcel(file);

      const updated = [uploaded, ...files];

      setFiles(updated);

      selectWorkbook(uploaded);

      alert("Workbook uploaded.");
    } catch (err) {
      toast.error(
      err.response?.data?.detail ||
      "Something went wrong."
    );
    }

    setLoading(false);

    e.target.value = "";
  }

  async function handleDelete() {
    if (!selected) return;

    if (!window.confirm("Delete workbook?"))
      return;

    try {
      await deleteExcel(selected.id);

      const updated = files.filter(
        (x) => x.id !== selected.id
      );

      setFiles(updated);

      if (updated.length > 0) {
        selectWorkbook(updated[0]);
      } else {
        setSelected(null);
        setWorkbook(null);
        setSelectedSheet(null);
      }
    } catch (err) {
      toast.error(
      err.response?.data?.detail ||
      "Something went wrong."
    );
    }
  }

  return (
    <div className="space-y-8">

      <h1 className="text-3xl font-bold">
        Excel Analyzer
      </h1>

      <div className="bg-white rounded-xl shadow p-6 flex justify-between">

        <label className="cursor-pointer bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg">

          {loading
            ? "Uploading..."
            : "Upload Excel"}

          <input
            hidden
            type="file"
            accept=".xlsx,.xls"
            onChange={handleUpload}
          />

        </label>

        {selected && (
          <button
            onClick={handleDelete}
            className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg"
          >
            Delete
          </button>
        )}

      </div>

      <div className="grid grid-cols-4 gap-6">

        <div className="bg-white rounded-xl shadow p-5">

          <h2 className="font-semibold text-lg mb-4">
            Workbooks
          </h2>

          {files.map((file) => (
            <div
              key={file.id}
              onClick={() =>
                selectWorkbook(file)
              }
              className={`cursor-pointer border rounded-lg p-3 mb-3 ${
                selected?.id === file.id
                  ? "border-green-600 bg-green-50"
                  : "border-gray-200"
              }`}
            >
              📊 {file.filename}
            </div>
          ))}

        </div>

        <div className="col-span-3 space-y-6">

          {selected && workbook && (

            <>
              <div className="bg-white rounded-xl shadow p-6">

                <h2 className="text-2xl font-bold">
                  {selected.filename}
                </h2>

                <p className="text-gray-500 mt-2">
                  Uploaded{" "}
                  {new Date(
                    selected.uploaded_at
                  ).toLocaleString()}
                </p>

              </div>

              <div className="bg-white rounded-xl shadow p-6">

                <h2 className="font-semibold text-xl mb-4">
                  Sheets
                </h2>

                <div className="flex gap-3 flex-wrap">

                  {workbook.sheets.map(
                    (sheet) => (

                      <button
                        key={sheet.name}
                        onClick={() =>
                          setSelectedSheet(
                            sheet
                          )
                        }
                        className={`px-4 py-2 rounded-lg ${
                          selectedSheet?.name ===
                          sheet.name
                            ? "bg-green-600 text-white"
                            : "bg-gray-200"
                        }`}
                      >
                        {sheet.name}
                      </button>

                    )
                  )}

                </div>

              </div>

              {selectedSheet && (

                <div className="bg-white rounded-xl shadow p-6">

                  <h2 className="font-semibold text-xl mb-4">
                    Sheet Details
                  </h2>

                  <p>
                    <strong>Rows:</strong>{" "}
                    {selectedSheet.rows}
                  </p>

                  <p className="mt-3">
                    <strong>Columns</strong>
                  </p>

                  <div className="flex flex-wrap gap-2 mt-2">

                    {selectedSheet.columns.map(
                      (column) => (
                        <span
                          key={column}
                          className="bg-green-100 px-3 py-1 rounded-full"
                        >
                          {column}
                        </span>
                      )
                    )}

                  </div>

                </div>

              )}

              <div className="bg-white rounded-xl shadow p-6">

                <h2 className="font-semibold text-xl mb-4">
                  AI Summary
                </h2>

                <div className="whitespace-pre-wrap leading-8">

                  {selected.summary}

                </div>

              </div>

            </>

          )}

        </div>

      </div>

    </div>
  );
}