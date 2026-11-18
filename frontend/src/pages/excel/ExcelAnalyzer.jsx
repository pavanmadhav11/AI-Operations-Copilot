import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { FileSpreadsheet } from "lucide-react";
import useAuthStore from "../../store/authStore";
import {
  uploadExcel,
  getExcels,
  deleteExcel,
  applySalesDemand,
} from "../../services/excelAnalyzerService";

export default function ExcelAnalyzer() {
  const [files, setFiles] = useState([]);
  const [selected, setSelected] = useState(null);
  const [workbook, setWorkbook] = useState(null);
  const [selectedSheet, setSelectedSheet] = useState(null);
  const [loading, setLoading] = useState(false);
  const [salesLoading, setSalesLoading] = useState(false);
  const [salesResult, setSalesResult] = useState(null);
  const user = useAuthStore((state) => state.user);
  const canImportSales = user && ["admin", "manager"].includes(user.role);

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
    setSalesResult(null);

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

  async function handleSalesImport() {
    if (!selected) return;
    setSalesLoading(true);
    try {
      const result = await applySalesDemand(selected.id);
      setSalesResult(result);
      toast.success("Sales history applied to demand estimates.");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Could not apply this workbook as sales history.");
    } finally {
      setSalesLoading(false);
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

        {selected && canImportSales && (
          <button onClick={handleSalesImport} disabled={salesLoading} className="rounded-lg bg-purple-700 px-5 py-3 text-white disabled:opacity-50">
            {salesLoading ? "Calculating..." : "Use as sales history"}
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
              <span className="flex items-center gap-2"><FileSpreadsheet size={16} className="shrink-0 text-slate-500" strokeWidth={1.7} aria-hidden="true" /><span className="truncate">{file.filename}</span></span>
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

              {selectedSheet && (
                <div className="bg-white rounded-xl shadow p-6">
                  <h2 className="mb-3 text-xl font-semibold">Import checks</h2>
                  {(selectedSheet.validation?.errors || []).length === 0 && (selectedSheet.validation?.warnings || []).length === 0 ? (
                    <p className="text-emerald-700">No common spreadsheet issues found.</p>
                  ) : (
                    <div className="space-y-2">
                      {(selectedSheet.validation?.errors || []).map((message) => <p className="text-red-700" key={message}>Error: {message}</p>)}
                      {(selectedSheet.validation?.warnings || []).map((message) => <p className="text-amber-700" key={message}>Check: {message}</p>)}
                    </div>
                  )}
                </div>
              )}

              {salesResult && (
                <div className="bg-white rounded-xl shadow p-6">
                  <h2 className="mb-3 text-xl font-semibold">Demand estimates from sales</h2>
                  {salesResult.updated.map((item) => <p className="mb-2" key={item.product_name}>{item.product_name}: {item.total_units_sold} units over {item.days_in_period} days · {item.average_daily_demand} units/day</p>)}
                  {salesResult.unmatched_products.length > 0 && <p className="mt-3 text-amber-700">Not found in inventory: {salesResult.unmatched_products.join(", ")}</p>}
                </div>
              )}

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
