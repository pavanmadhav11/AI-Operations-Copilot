import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import useAuthStore from "../../store/authStore";

export default function Login() {
  const navigate = useNavigate();

  const { login, token } = useAuthStore();

  const [error, setError] = useState("");

  const {
    register,
    handleSubmit,
  } = useForm();

  useEffect(() => {
    if (token) {
      navigate("/", {
        replace: true,
      });
    }
  }, [token, navigate]);

  const onSubmit = async (data) => {
    try {
      setError("");

      await login(
        data.email,
        data.password
      );

      navigate("/", {
        replace: true,
      });
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Login failed"
      );
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100 dark:bg-slate-900">

      <form
        onSubmit={handleSubmit(onSubmit)}
        className="bg-white dark:bg-slate-800 shadow-xl rounded-xl p-10 w-[420px]"
      >

        <h1 className="text-3xl font-bold mb-8 text-center dark:text-white">
          Login
        </h1>

        {error && (
          <div className="bg-red-100 text-red-700 rounded-lg p-3 mb-5">
            {error}
          </div>
        )}

        <input
          {...register("email")}
          type="email"
          placeholder="Email"
          className="border dark:border-slate-600 dark:bg-slate-700 dark:text-white rounded-lg p-3 w-full mb-5"
        />

        <input
          {...register("password")}
          type="password"
          placeholder="Password"
          className="border dark:border-slate-600 dark:bg-slate-700 dark:text-white rounded-lg p-3 w-full mb-3"
        />

        <div className="flex justify-end mb-6">
          <button
            type="button"
            onClick={() => navigate("/forgot-password")}
            className="text-blue-600 hover:underline text-sm"
          >
            Forgot Password?
          </button>
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg p-3 font-semibold"
        >
          Login
        </button>

        <p className="text-center mt-6 text-gray-600 dark:text-gray-300">
          Don't have an account?{" "}
          <button
            type="button"
            onClick={() => navigate("/register")}
            className="text-blue-600 hover:underline font-medium"
          >
            Register
          </button>
        </p>

      </form>

    </div>
  );
}