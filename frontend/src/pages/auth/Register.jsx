import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import { register as registerUser } from "../../services/authService";

export default function Register() {
  const navigate = useNavigate();

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const {
    register,
    handleSubmit,
    reset,
  } = useForm();

  const onSubmit = async (data) => {
    try {
      setError("");
      setSuccess("");

      await registerUser(data);

      setSuccess("Account created successfully.");

      reset();

      setTimeout(() => {
        navigate("/login");
      }, 1500);

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Registration failed."
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
          Register
        </h1>

        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        {success && (
          <div className="bg-green-100 text-green-700 p-3 rounded-lg mb-4">
            {success}
          </div>
        )}

        <input
          {...register("name")}
          placeholder="Full Name"
          className="border p-3 rounded-lg w-full mb-4"
        />

        <input
          {...register("email")}
          placeholder="Email"
          className="border p-3 rounded-lg w-full mb-4"
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
          Register
        </button>
      </form>
    </div>
  );
}