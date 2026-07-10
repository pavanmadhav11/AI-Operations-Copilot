import useChatStore from "../../store/chatStore";

export default function ChatSidebar() {
  const {
    chats,
    createChat,
    activeChatId,
    setActiveChat,
    deleteChat,
    renameChat,
  } = useChatStore();

  return (
    <aside className="w-72 bg-slate-900 text-white flex flex-col">

      <button
        onClick={createChat}
        className="m-5 bg-blue-600 p-3 rounded-lg hover:bg-blue-700"
      >
        + New Chat
      </button>

      <div className="px-5 flex-1 overflow-y-auto">

        {chats.map((chat) => (

          <div
            key={chat.id}
            className={`rounded-lg mb-2 p-3 ${
              activeChatId === chat.id
                ? "bg-blue-600"
                : "bg-slate-800"
            }`}
          >

            <div
              onClick={() => setActiveChat(chat.id)}
              className="cursor-pointer"
            >
              {chat.title}
            </div>

            <div className="flex gap-3 mt-3">

              <button
                onClick={() => {
                  const title = prompt(
                    "Rename Chat",
                    chat.title
                  );

                  if (title) {
                    renameChat(chat.id, title);
                  }
                }}
                className="text-xs text-yellow-300"
              >
                Rename
              </button>

              <button
                onClick={() => deleteChat(chat.id)}
                className="text-xs text-red-300"
              >
                Delete
              </button>

            </div>

          </div>

        ))}

      </div>

    </aside>
  );
}