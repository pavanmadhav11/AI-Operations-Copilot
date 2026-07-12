import { useNavigate } from "react-router-dom";

export default function ForgotPassword() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100 dark:bg-slate-900">
      <div className="bg-white dark:bg-slate-800 shadow-xl rounded-xl p-10 w-[450px] text-center">

        <div className="text-6xl mb-6">🚧</div>

        <h1 className="text-3xl font-bold mb-4 text-gray-800 dark:text-white">
          Coming Soon
        </h1>

        <p className="text-gray-600 dark:text-gray-300 leading-7 mb-8">
          The <strong>Forgot Password</strong> feature is currently under
          development and will be available in a future update.
        </p>

        <button
          onClick={() => navigate("/login")}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition"
        >
          Back to Login
        </button>

      </div>
    </div>
  );
}