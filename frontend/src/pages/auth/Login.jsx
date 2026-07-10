import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import useAuthStore from "../../store/authStore";

export default function Login() {
  const navigate = useNavigate();

  const { login } = useAuthStore();

  const [error, setError] = useState("");

  const {
    register,
    handleSubmit,
  } = useForm();

  const onSubmit = async (data) => {
    try {
      setError("");

      await login(
        data.email,
        data.password
      );

      navigate("/");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Login failed"
      );
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="bg-white p-10 rounded-xl shadow-lg w-[420px]"
      >
        <h1 className="text-3xl font-bold mb-8">
          Login
        </h1>

        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded-lg mb-5">
            {error}
          </div>
        )}

        <input
          {...register("email")}
          placeholder="Email"
          className="border p-3 rounded-lg w-full mb-5"
        />

        <input
          {...register("password")}
          type="password"
          placeholder="Password"
          className="border p-3 rounded-lg w-full mb-6"
        />

        <button
          className="w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700"
        >
          Login
        </button>
      </form>
    </div>
  );
}