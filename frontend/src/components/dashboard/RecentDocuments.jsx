const docs = [
  "Invoice.pdf",
  "Report.xlsx",
  "Meeting.pdf",
  "Budget.xlsx",
  "Shipment.pdf",
];

export default function RecentDocuments() {
  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h2 className="text-xl font-semibold mb-5">
        Recent Documents
      </h2>

      <div className="space-y-3">
        {docs.map((doc) => (
          <div
            key={doc}
            className="flex justify-between border-b pb-2"
          >
            <span>{doc}</span>

            <span className="text-blue-600">
              View
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}