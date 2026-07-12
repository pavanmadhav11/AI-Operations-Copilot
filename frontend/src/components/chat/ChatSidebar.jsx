import { useEffect } from "react";

import {
  createSession,
  getSessions,
  deleteSession,
} from "../../services/sessionService";

import {
  getFiles,
  deleteFile,
} from "../../services/uploadService";

import useSessionStore from "../../store/sessionStore";
import useUploadStore from "../../store/uploadStore";

import FileUpload from "./FileUpload";

export default function ChatSidebar() {
  const {
    sessions,
    currentSession,
    setSessions,
    setCurrentSession,
    addSession,
  } = useSessionStore();

  const {
    files,
    setFiles,
    deleteFile: removeFile,
  } = useUploadStore();

  useEffect(() => {
    loadSessions();
  }, []);

  useEffect(() => {
    if (currentSession) {
      loadFiles(currentSession.id);
    } else {
      setFiles([]);
    }
  }, [currentSession]);

  async function loadSessions() {
    try {
      const data = await getSessions();

      setSessions(data);

      if (data.length > 0) {
        setCurrentSession(data[0]);
      } else {
        setCurrentSession(null);
      }
    } catch (err) {
      toast.error(
        err.response?.data?.detail ||
        "Something went wrong."
      );
    }
  }

  async function loadFiles(sessionId) {
    try {
      const data = await getFiles(sessionId);

      setFiles(data);
    } catch (err) {
      toast.error(
        err.response?.data?.detail ||
        "Something went wrong."
      );
    }
  }

  async function handleNewChat() {
    try {
      const session = await createSession();

      addSession(session);

      setCurrentSession(session);
    } catch (err) {
      toast.error(
        err.response?.data?.detail ||
        "Something went wrong."
      );
    }
  }

  async function handleDelete(id) {
    try {
      await deleteSession(id);

      await loadSessions();
    } catch (err) {
      toast.error(
        err.response?.data?.detail ||
        "Something went wrong."
      );
    }
  }

  async function handleDeleteFile(id) {
    try {
      await deleteFile(id);

      removeFile(id);
    } catch (err) {
      toast.error(
        err.response?.data?.detail ||
        "Something went wrong."
      );
    }
  }

  return (
    <aside className="w-72 bg-slate-900 text-white flex flex-col">

      <div className="p-5 border-b border-slate-700">
        <h1 className="text-xl font-bold">
          AI Operations Copilot
        </h1>
      </div>

      <div className="p-5">
        <button
          onClick={handleNewChat}
          className="w-full bg-blue-600 p-3 rounded-lg hover:bg-blue-700"
        >
          + New Chat
        </button>
      </div>

      <div className="px-5">
        <h3 className="text-sm text-slate-400 mb-3">
          Chat Sessions
        </h3>

        {sessions.map((session) => (
          <div
            key={session.id}
            className={`rounded-lg mb-2 p-3 ${
              currentSession?.id === session.id
                ? "bg-blue-600"
                : "bg-slate-800"
            }`}
          >
            <div
              className="cursor-pointer"
              onClick={() => setCurrentSession(session)}
            >
              {session.title}
            </div>

            <button
              onClick={() => handleDelete(session.id)}
              className="text-xs text-red-300 mt-2"
            >
              Delete
            </button>
          </div>
        ))}
      </div>

      <div className="px-5 mt-6">
        <h3 className="text-sm text-slate-400 mb-3">
          Documents
        </h3>

        <FileUpload />
      </div>

      <div className="flex-1 overflow-y-auto px-5 mt-4">
        {files.map((file) => (
          <div
            key={file.id}
            className="bg-slate-800 rounded-lg p-3 mb-2"
          >
            <p className="font-medium truncate">
              {file.filename}
            </p>

            <p className="text-xs text-slate-400">
              {file.file_type}
            </p>

            <button
              onClick={() => handleDeleteFile(file.id)}
              className="text-xs text-red-400 mt-2"
            >
              Delete
            </button>
          </div>
        ))}
      </div>

    </aside>
  );
}