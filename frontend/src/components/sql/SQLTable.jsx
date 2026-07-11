export default function SQLTable({ rows }) {

  if (!rows || rows.length === 0) return null;

  const columns = Object.keys(rows[0]);

  return (
    <div className="bg-white rounded-xl shadow mt-6 overflow-auto">

      <table className="w-full">

        <thead className="bg-slate-100">

          <tr>

            {columns.map((column) => (

              <th
                key={column}
                className="text-left p-3"
              >
                {column}
              </th>

            ))}

          </tr>

        </thead>

        <tbody>

          {rows.map((row, index) => (

            <tr
              key={index}
              className="border-t"
            >

              {columns.map((column) => (

                <td
                  key={column}
                  className="p-3"
                >
                  {String(row[column])}
                </td>

              ))}

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}