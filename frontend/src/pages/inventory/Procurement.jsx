import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import toast from "react-hot-toast";
import { getPDFs } from "../../services/pdfAnalyzerService";
import { createPurchaseOrderDraft, extractPurchaseQuote, getPurchaseOrders } from "../../services/procurementService";

export default function Procurement() {
  const [searchParams] = useSearchParams();
  const [pdfs, setPdfs] = useState([]);
  const [orders, setOrders] = useState([]);
  const [fileId, setFileId] = useState("");
  const [quote, setQuote] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedDraft, setSelectedDraft] = useState(null);
  const inventoryId = searchParams.get("inventory_id");
  const recommendedQuantity = searchParams.get("quantity");

  async function load() {
    try {
      const [pdfList, orderList] = await Promise.all([getPDFs(), getPurchaseOrders()]);
      setPdfs(pdfList);
      setOrders(orderList);
      if (!fileId && pdfList.length) setFileId(String(pdfList[0].id));
    } catch {
      toast.error("Could not load supplier quotes or purchase orders.");
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function extractQuote() {
    if (!fileId) {
      toast.error("Choose a supplier quote PDF first.");
      return;
    }
    setLoading(true);
    try {
      setQuote(await extractPurchaseQuote(Number(fileId)));
    } catch (error) {
      toast.error(error.response?.data?.detail || "Could not extract details from this quote.");
    } finally {
      setLoading(false);
    }
  }

  function updateQuote(field, value) {
    setQuote({ ...quote, [field]: value });
  }

  function updateItem(index, field, value) {
    setQuote({
      ...quote,
      items: quote.items.map((item, itemIndex) => itemIndex === index ? { ...item, [field]: value } : item),
    });
  }

  async function saveDraft() {
    if (!quote) return;
    setLoading(true);
    try {
      const draft = await createPurchaseOrderDraft(Number(quote.file_id), {
        supplier_name: quote.supplier_name,
        supplier_email: quote.supplier_email,
        quote_reference: quote.quote_reference,
        lead_time_days: quote.lead_time_days ? Number(quote.lead_time_days) : null,
        items: quote.items.map((item) => ({
          product_name: item.product_name,
          quantity: Number(item.quantity),
          unit_price: Number(item.unit_price),
          source_page: item.source_page ? Number(item.source_page) : null,
        })),
        inventory_id: inventoryId ? Number(inventoryId) : null,
        recommended_quantity: recommendedQuantity ? Number(recommendedQuantity) : null,
      });
      setSelectedDraft(draft);
      setQuote(null);
      toast.success("Draft saved. It has not been sent to the supplier.");
      await load();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Could not save this purchase order draft.");
    } finally {
      setLoading(false);
    }
  }

  const quoteTotal = quote?.items.reduce((total, item) => total + (Number(item.quantity) * Number(item.unit_price)), 0) || 0;

  return (
    <main className="space-y-8 p-8">
      <section className="rounded-xl bg-white p-6 shadow">
        <h1 className="text-3xl font-bold">Supplier quote to purchase draft</h1>
        <p className="mt-2 text-slate-600">Upload a supplier quote in PDF Analyzer. Extracted details stay editable so you can check them against the source before saving a draft. Nothing is sent to the supplier.</p>
        {inventoryId && <p className="mt-3 rounded bg-blue-50 p-3">Reorder suggestion for inventory ID {inventoryId}: {recommendedQuantity} units.</p>}
        <div className="mt-5 flex flex-wrap gap-3">
          <select className="min-w-72 rounded border p-3" onChange={(event) => { setFileId(event.target.value); setQuote(null); }} value={fileId}>
            <option value="">Choose an uploaded PDF quote</option>
            {pdfs.map((pdf) => <option key={pdf.id} value={pdf.id}>{pdf.filename}</option>)}
          </select>
          <button className="rounded bg-blue-700 px-5 py-3 text-white disabled:opacity-50" disabled={loading || !pdfs.length} onClick={extractQuote}>
            {loading ? "Reading quote..." : "Extract quote details"}
          </button>
        </div>
        {!pdfs.length && <p className="mt-4 text-amber-700">Upload a supplier quote PDF on the PDF Analyzer page first.</p>}
      </section>

      {quote && (
        <section className="space-y-5 rounded-xl border border-amber-300 bg-amber-50 p-6">
          <div>
            <h2 className="text-xl font-semibold">Review extracted details</h2>
            <p className="mt-1 text-sm text-slate-600">Source document: {quote.source_filename}{quote.supplier_page ? ` · Supplier details on page ${quote.supplier_page}` : ""}</p>
          </div>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <label className="block"><span className="mb-1 block font-medium">Supplier name</span><input className="w-full rounded border p-3" onChange={(event) => updateQuote("supplier_name", event.target.value)} value={quote.supplier_name} /></label>
            <label className="block"><span className="mb-1 block font-medium">Supplier email</span><input className="w-full rounded border p-3" onChange={(event) => updateQuote("supplier_email", event.target.value)} value={quote.supplier_email || ""} /></label>
            <label className="block"><span className="mb-1 block font-medium">Quote reference</span><input className="w-full rounded border p-3" onChange={(event) => updateQuote("quote_reference", event.target.value)} value={quote.quote_reference || ""} /></label>
          </div>
          <div className="overflow-x-auto rounded bg-white">
            <table className="w-full text-left">
              <thead className="bg-slate-100"><tr>{["Product", "Quantity", "Unit price", "Source page"].map((heading) => <th className="p-3" key={heading}>{heading}</th>)}</tr></thead>
              <tbody>{quote.items.map((item, index) => <tr className="border-t" key={`${item.product_name}-${index}`}>
                <td className="p-3"><input className="w-full rounded border p-2" onChange={(event) => updateItem(index, "product_name", event.target.value)} value={item.product_name} /></td>
                <td className="p-3"><input className="w-28 rounded border p-2" min="1" onChange={(event) => updateItem(index, "quantity", event.target.value)} type="number" value={item.quantity} /></td>
                <td className="p-3"><input className="w-32 rounded border p-2" min="0" step="0.01" onChange={(event) => updateItem(index, "unit_price", event.target.value)} type="number" value={item.unit_price} /></td>
                <td className="p-3">{item.source_page ? `Page ${item.source_page}` : "Check PDF"}</td>
              </tr>)}</tbody>
            </table>
          </div>
          <p className="font-semibold">Estimated quote total: ${quoteTotal.toFixed(2)} · Lead time: {quote.lead_time_days ?? "Not found"} days</p>
          <button className="rounded bg-emerald-700 px-5 py-3 text-white disabled:opacity-50" disabled={loading || !quote.supplier_name || !quote.items.length} onClick={saveDraft}>
            Save reviewed draft
          </button>
        </section>
      )}

      {selectedDraft && (
        <section className="rounded-xl border border-emerald-300 bg-emerald-50 p-6">
          <h2 className="text-xl font-semibold">Draft #{selectedDraft.id} saved</h2>
          <p className="mt-2">Supplier: {selectedDraft.supplier_name} · Quote: {selectedDraft.quote_reference || "Not provided"}</p>
          <p>Source: {selectedDraft.source_filename} · Lead time: {selectedDraft.lead_time_days ?? "Not provided"} days</p>
          <p className="mt-4 font-semibold">Draft total: ${Number(selectedDraft.total_amount).toFixed(2)}</p>
        </section>
      )}

      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">Purchase order drafts</h2>
        {orders.length === 0 ? <p className="rounded bg-white p-6 shadow">No purchase order drafts yet.</p> : orders.map((order) => (
          <article className="rounded-lg bg-white p-5 shadow" key={order.id}>
            <div className="flex flex-wrap justify-between gap-2"><h3 className="font-semibold">Draft #{order.id} · {order.supplier_name}</h3><span className="rounded bg-amber-100 px-2 py-1 text-sm text-amber-800">{order.status}</span></div>
            <p className="mt-2 text-sm text-slate-600">Quote {order.quote_reference || "no reference"} · {order.source_filename} · {order.created_by}</p>
            <div className="mt-3 space-y-1">{order.items.map((item, index) => <p key={`${item.product_name}-${index}`}>{item.product_name}: {item.quantity} units at ${Number(item.unit_price).toFixed(2)}{item.source_page ? ` · PDF page ${item.source_page}` : ""}</p>)}</div>
            <p className="mt-3 font-semibold">Total ${Number(order.total_amount).toFixed(2)}</p>
          </article>
        ))}
      </section>
    </main>
  );
}
