export default function Button({
  children,
  type = "button",
  variant = "primary",
  onClick,
  className = "",
}) {
  const styles = {
    primary:
      "bg-blue-600 hover:bg-blue-700 text-white",
    secondary:
      "bg-slate-700 hover:bg-slate-800 text-white",
    danger:
      "bg-red-600 hover:bg-red-700 text-white",
    outline:
      "border border-gray-300 hover:bg-gray-100 text-black",
  };

  return (
    <button
      type={type}
      onClick={onClick}
      className={`px-5 py-2 rounded-lg transition font-medium ${styles[variant]} ${className}`}
    >
      {children}
    </button>
  );
}