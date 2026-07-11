import { useEffect } from "react";

import {
  getFiles,
  deleteFile,
} from "../../services/uploadService";

import useUploadStore from "../../store/uploadStore";

export default function UploadedFiles() {
  const {
    files,
    setFiles,
    deleteFile: removeFile,
  } = useUploadStore();

  useEffect(() => {
    loadFiles();
  }, []);

  async function loadFiles() {
    const data = await getFiles();

    setFiles(data);
  }

  async function handleDelete(id) {
    await deleteFile(id);

    removeFile(id);
  }

  return (
    <div className="mt-6">

      <h3 className="font-semibold mb-3">
        Uploaded Files
      </h3>

      {files.map((file) => (
        <div
          key={file.id}
          className="flex justify-between items-center bg-slate-100 rounded-lg p-3 mb-2"
        >
          <div>
            <p className="font-medium">
              {file.filename}
            </p>

            <p className="text-xs text-gray-500">
              {file.file_type}
            </p>
          </div>

          <button
            onClick={() =>
              handleDelete(file.id)
            }
            className="text-red-500"
          >
            Delete
          </button>
        </div>
      ))}

    </div>
  );
}