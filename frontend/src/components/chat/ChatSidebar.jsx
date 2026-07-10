import useChatStore from "../../store/chatStore";

export default function ChatSidebar() {
  const {
    chats,
    createChat,
    activeChatId,
    setActiveChat,
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
            onClick={() => setActiveChat(chat.id)}
            className={`cursor-pointer rounded-lg p-3 mb-2 transition ${
              activeChatId === chat.id
                ? "bg-blue-600"
                : "hover:bg-slate-800"
            }`}
          >
            {chat.title}
          </div>

        ))}

      </div>

    </aside>
  );
}