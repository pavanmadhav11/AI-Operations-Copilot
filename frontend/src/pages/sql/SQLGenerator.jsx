import { useState } from "react";

import SQLInput from "../../components/sql/SQLInput";
import SQLResult from "../../components/sql/SQLResult";
import SQLTable from "../../components/sql/SQLTable";

import { generateSQL } from "../../services/sqlService";

export default function SQLGenerator() {

  const [loading, setLoading] = useState(false);

  const [sql, setSql] = useState("");

  const [rows, setRows] = useState([]);

  async function handleGenerate(question) {

    setLoading(true);

    try {

      const response = await generateSQL(question);

      if (response.success) {

        setSql(response.sql);

        setRows(response.result);

      } else {

        alert(response.message);

      }

    } catch {

      alert("Something went wrong.");

    }

    setLoading(false);
  }

  return (

    <div className="p-8">

      <h1 className="text-3xl font-bold mb-8">

        SQL Generator

      </h1>

      <SQLInput
        onGenerate={handleGenerate}
        loading={loading}
      />

      <SQLResult
        sql={sql}
      />

      <SQLTable
        rows={rows}
      />

    </div>

  );
}