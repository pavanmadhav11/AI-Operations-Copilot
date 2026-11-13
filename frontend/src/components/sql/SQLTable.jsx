export default function SQLTable({ rows }) {

  if (!rows || rows.length === 0) return null;

  const columns = Object.keys(rows[0]);
  const columnLabels = {
    id: "Inventory ID",
    product_id: "Product ID",
    warehouse_id: "Warehouse ID",
    product_name: "Item",
    warehouse_name: "Warehouse",
    quantity: "Quantity",
    reorder_level: "Reorder level",
    average_daily_demand: "Daily demand",
    supplier_lead_time_days: "Supplier lead time (days)",
  };

  return (
    <section className="mt-6 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">
        <div>
          <h2 className="font-semibold text-slate-900">Inventory results</h2>
          <p className="mt-1 text-sm text-slate-500">{rows.length} {rows.length === 1 ? "record" : "records"} found</p>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm" aria-label="Inventory query results">
          <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              {columns.map((column) => (
                <th key={column} scope="col" className="whitespace-nowrap px-5 py-3 font-semibold">
                  {columnLabels[column] || column.replaceAll("_", " ")}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {rows.map((row, index) => (
              <tr key={row.id ?? index} className="transition hover:bg-slate-50">
                {columns.map((column) => (
                  <td key={column} className="whitespace-nowrap px-5 py-3.5 text-slate-700">
                    {row[column] == null ? "—" : String(row[column])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
