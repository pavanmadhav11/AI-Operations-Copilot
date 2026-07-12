import { useEffect, useState } from "react";

import {
  getRecentDocuments,
} from "../../services/dashboardService";

export default function RecentDocuments() {
  const [docs, setDocs] = useState([]);

  useEffect(() => {
    loadDocuments();
  }, []);

  async function loadDocuments() {
    try {
      const data = await getRecentDocuments();
      setDocs(data);
    } catch (err) {
      toast.error(
      err.response?.data?.detail ||
      "Something went wrong."
    );
    }
  }

  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h2 className="text-xl font-semibold mb-5">
        Recent Documents
      </h2>

      <div className="space-y-3">
        {docs.map((doc) => (
          <div
            key={doc.id}
            className="flex justify-between border-b pb-2"
          >
            <span>{doc.filename}</span>

            <span className="text-blue-600">
              Uploaded
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}