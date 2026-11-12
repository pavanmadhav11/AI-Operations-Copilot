import { useEffect } from "react";
import toast from "react-hot-toast";

import {
  createSession,
  getSessions,
  deleteSession,
  renameSession,
} from "../../services/sessionService";

import {
  getFiles,
  deleteFile,
} from "../../services/uploadService";

import useSessionStore from "../../store/sessionStore";
import useUploadStore from "../../store/uploadStore";

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
        const selected = data.find((session) => session.id === currentSession?.id) || data[0];
        setCurrentSession(selected);
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
    const session = sessions.find((item) => item.id === id);
    if (!window.confirm(`Delete "${session?.title || "this chat"}" and its messages?`)) return;
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

  async function handleRename(session) {
    const title = window.prompt("Enter a name for this chat", session.title);
    if (title === null || !title.trim() || title.trim() === session.title) return;
    try {
      const updated = await renameSession(session.id, title.trim());
      setSessions(sessions.map((item) => item.id === session.id ? updated : item));
      if (currentSession?.id === session.id) setCurrentSession(updated);
    } catch (err) {
      toast.error(err.response?.data?.detail || "Could not rename this chat.");
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

      <div className="min-h-0 flex-1 overflow-y-auto px-4">
        <h3 className="text-sm text-slate-400 mb-3">
          Chat Sessions
        </h3>

        {sessions.map((session) => (
          <div
            key={session.id}
            className={`group mb-2 rounded-lg p-3 ${
              currentSession?.id === session.id
                ? "bg-blue-600"
                : "bg-slate-800"
            }`}
          >
            <button className="w-full truncate text-left" onClick={() => setCurrentSession(session)} title={session.title}>
              {session.title}
            </button>
            <div className="mt-2 flex gap-3 text-xs">
              <button onClick={() => handleRename(session)} className="text-slate-200 hover:text-white">Rename</button>
              <button onClick={() => handleDelete(session.id)} className="text-rose-200 hover:text-white">Delete</button>
            </div>
          </div>
        ))}
      </div>

      <div className="px-5 pt-4">
        <h3 className="text-sm text-slate-400 mb-3">
          Documents
        </h3>
      </div>

      <div className="max-h-48 overflow-y-auto px-5 pb-4">
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
