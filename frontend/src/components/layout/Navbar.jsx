export default function Navbar() {
  return (
    <header className="bg-white h-16 shadow flex justify-between items-center px-8">

      <input
        placeholder="Search..."
        className="border rounded-lg px-4 py-2 w-96"
      />

      <div className="flex items-center gap-5">

        <button>
          🔔
        </button>

        <img
          src="https://i.pravatar.cc/40"
          alt="user"
          className="rounded-full"
        />

      </div>

    </header>
  );
}