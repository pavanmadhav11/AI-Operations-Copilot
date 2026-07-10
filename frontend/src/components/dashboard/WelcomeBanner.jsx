export default function WelcomeBanner() {
  const hour = new Date().getHours();

  let greeting = "Good Evening";

  if (hour < 12) greeting = "Good Morning";
  else if (hour < 17) greeting = "Good Afternoon";

  return (
    <div className="bg-linear-to-r from-blue-600 to-indigo-700 text-white rounded-xl p-8">

      <h1 className="text-3xl font-bold">
        {greeting}, Admin 👋
      </h1>

      <p className="mt-2 text-blue-100">
        Welcome back to AI Operations Copilot.
      </p>

    </div>
  );
}