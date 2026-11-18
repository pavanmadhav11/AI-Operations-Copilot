import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { FileText } from "lucide-react";

import {
  uploadPDF,
  getPDFs,
  deletePDF,
} from "../../services/pdfAnalyzerService";

export default function PDFAnalyzer() {
  const [pdfs, setPDFs] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadPDFs();
  }, []);

  async function loadPDFs() {
    try {
      const data = await getPDFs();

      setPDFs(data);

      if (data.length > 0) {
        setSelected(data[0]);
      } else {
        setSelected(null);
      }
    } catch (err) {
      toast.error(
    err.response?.data?.detail ||
    "Something went wrong."
);
    }
  }

  async function handleUpload(e) {
    const file = e.target.files[0];

    if (!file) return;

    setLoading(true);

    try {
      const uploaded = await uploadPDF(file);

      setPDFs((prev) => [uploaded, ...prev]);

      setSelected(uploaded);

      toast.success("PDF uploaded successfully.");
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

    const ok = window.confirm(
      "Delete this PDF?"
    );

    if (!ok) return;

    try {
      await deletePDF(selected.id);

      const updated = pdfs.filter(
        (pdf) => pdf.id !== selected.id
      );

      setPDFs(updated);

      if (updated.length > 0) {
        setSelected(updated[0]);
      } else {
        setSelected(null);
      }

      toast.success("PDF deleted successfully.");
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
        PDF Analyzer
      </h1>

      <div className="bg-white rounded-xl shadow p-6 flex justify-between items-center">

        <label className="cursor-pointer bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg">

          {loading
            ? "Uploading..."
            : "Upload PDF"}

          <input
            hidden
            type="file"
            accept=".pdf"
            onChange={handleUpload}
          />

        </label>

        {selected && (
          <button
            onClick={handleDelete}
            className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg"
          >
            Delete PDF
          </button>
        )}

      </div>

      <div className="grid grid-cols-3 gap-6">

        <div className="bg-white rounded-xl shadow p-6">

          <h2 className="text-xl font-semibold mb-4">
            Uploaded PDFs
          </h2>

          {pdfs.length === 0 && (
            <div className="text-center py-10 text-gray-500">
              <FileText className="mx-auto mb-4 text-slate-400" size={34} strokeWidth={1.6} aria-hidden="true" />
              <p>No PDFs uploaded yet.</p>
              <p className="text-sm mt-2">
                Upload a PDF to generate an AI summary.
              </p>
            </div>
          )}

          {pdfs.map((pdf) => (
            <div
              key={pdf.id}
              onClick={() => setSelected(pdf)}
              className={`cursor-pointer rounded-lg border p-3 mb-3 transition ${
                selected?.id === pdf.id
                  ? "border-blue-600 bg-blue-50"
                  : "border-gray-200 hover:bg-gray-50"
              }`}
            >
              <div>
                <p className="flex items-center gap-2 truncate font-semibold">
                  <FileText className="shrink-0 text-slate-500" size={16} strokeWidth={1.7} aria-hidden="true" />
                  <span className="truncate">{pdf.filename}</span>
                </p>

                <p className="text-xs text-gray-500">
                  {new Date(pdf.uploaded_at).toLocaleDateString()}
                </p>
              </div>
            </div>
          ))}

        </div>

        <div className="col-span-2 bg-white rounded-xl shadow p-6">

          {!selected ? (
            <div className="text-gray-500">
              Upload a PDF to begin.
            </div>
          ) : (
            <>
              <h2 className="text-2xl font-bold">
                {selected.filename}
              </h2>

              <p className="text-gray-500 mt-2">
                Uploaded{" "}
                {new Date(
                  selected.uploaded_at
                ).toLocaleString()}
              </p>

              <hr className="my-6" />

              <h3 className="text-xl font-semibold mb-4">
                AI Summary
              </h3>

              <div className="bg-gray-100 rounded-lg p-5 whitespace-pre-wrap leading-8 min-h-[300px]">

                {selected.summary ||
                  "Summary not available."}

              </div>

            </>
          )}

        </div>

      </div>

    </div>
  );
}