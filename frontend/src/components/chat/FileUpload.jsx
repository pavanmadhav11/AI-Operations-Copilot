import { uploadFile } from "../../services/uploadService";
import toast from "react-hot-toast";
import { Paperclip } from "lucide-react";

import useUploadStore from "../../store/uploadStore";
import useSessionStore from "../../store/sessionStore";

export default function FileUpload() {
  const { addFile } = useUploadStore();

  const { currentSession } = useSessionStore();

  async function handleUpload(e) {
    const input = e.currentTarget;
    const file = input.files[0];

    if (!file) return;

    if (!currentSession) {
      toast.error("Create or select a chat before uploading a document.");
      return;
    }

    try {
      const uploaded = await uploadFile(
        currentSession.id,
        file
      );

      addFile(uploaded);

      input.value = "";
    } catch (err) {
      toast.error(
        err.response?.data?.detail ||
        "Could not upload this document. Check the file and try again."
      );
    } finally {
      input.value = "";
    }
  }

  return (
    <label className="flex h-11 w-11 shrink-0 cursor-pointer items-center justify-center rounded-xl text-slate-600 transition hover:bg-slate-100 hover:text-blue-700" title="Attach a PDF or spreadsheet">
      <Paperclip size={19} />

      <input
        hidden
        type="file"
        accept=".pdf,.xlsx,.xls"
        onChange={handleUpload}
        aria-label="Attach a PDF or spreadsheet"
      />
    </label>
  );
}
