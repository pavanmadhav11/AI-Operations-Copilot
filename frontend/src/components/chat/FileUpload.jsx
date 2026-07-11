import { uploadFile } from "../../services/uploadService";

import useUploadStore from "../../store/uploadStore";
import useSessionStore from "../../store/sessionStore";

export default function FileUpload() {
  const { addFile } = useUploadStore();

  const { currentSession } = useSessionStore();

  async function handleUpload(e) {
    const file = e.target.files[0];

    if (!file) return;

    if (!currentSession) {
      alert("Please create or select a chat session first.");
      return;
    }

    try {
      const uploaded = await uploadFile(
        currentSession.id,
        file
      );

      addFile(uploaded);

      e.target.value = "";
    } catch (err) {
      console.error(err);
      alert("File upload failed.");
    }
  }

  return (
    <label className="cursor-pointer bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 text-center block">
      Upload Document

      <input
        hidden
        type="file"
        accept=".pdf,.xlsx,.xls"
        onChange={handleUpload}
      />
    </label>
  );
}