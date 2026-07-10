export default function Input({
  label,
  ...props
}) {
  return (
    <div className="flex flex-col gap-2">

      <label className="font-medium">
        {label}
      </label>

      <input
        {...props}
        className="border rounded-lg p-3 outline-none focus:ring-2 focus:ring-blue-500"
      />

    </div>
  );
}