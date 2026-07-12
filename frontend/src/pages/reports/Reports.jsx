import {
  downloadDashboardReport,
  downloadChatReport,
  downloadDocumentReport,
  downloadSQLReport,
} from "../../services/reportService";

export default function Reports() {
  return (
    <div className="space-y-8">

      <h1 className="text-3xl font-bold">
        Reports
      </h1>

      <div className="grid grid-cols-2 gap-6">

        {/* Dashboard */}

        <div className="bg-white rounded-xl shadow p-6">

          <h2 className="text-xl font-semibold">
            Dashboard Report
          </h2>

          <p className="text-gray-500 mt-3 mb-6">
            Download dashboard statistics and analytics.
          </p>

          <button
            onClick={downloadDashboardReport}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-lg"
          >
            Download PDF
          </button>

        </div>

        {/* Chat */}

        <div className="bg-white rounded-xl shadow p-6">

          <h2 className="text-xl font-semibold">
            Chat History Report
          </h2>

          <p className="text-gray-500 mt-3 mb-6">
            Download complete AI conversation history.
          </p>

          <button
            onClick={downloadChatReport}
            className="bg-green-600 hover:bg-green-700 text-white px-5 py-3 rounded-lg"
          >
            Download PDF
          </button>

        </div>

        {/* Documents */}

        <div className="bg-white rounded-xl shadow p-6">

          <h2 className="text-xl font-semibold">
            Documents Report
          </h2>

          <p className="text-gray-500 mt-3 mb-6">
            Download uploaded documents summary.
          </p>

          <button
            onClick={downloadDocumentReport}
            className="bg-purple-600 hover:bg-purple-700 text-white px-5 py-3 rounded-lg"
          >
            Download PDF
          </button>

        </div>

        {/* SQL */}

        <div className="bg-white rounded-xl shadow p-6">

          <h2 className="text-xl font-semibold">
            SQL Report
          </h2>

          <p className="text-gray-500 mt-3 mb-6">
            Download SQL questions history.
          </p>

          <button
            onClick={downloadSQLReport}
            className="bg-orange-600 hover:bg-orange-700 text-white px-5 py-3 rounded-lg"
          >
            Download PDF
          </button>

        </div>

      </div>

    </div>
  );
}