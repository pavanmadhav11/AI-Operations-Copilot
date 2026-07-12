import { useEffect, useState } from "react";

import useThemeStore from "../../store/themeStore";

import {
  getProfile,
  updateProfile,
  changePassword,
} from "../../services/settingsService";

export default function Settings() {
  const { theme, toggleTheme } = useThemeStore();

  const [profile, setProfile] = useState({
    name: "",
    email: "",
  });

  const [password, setPassword] = useState({
    current_password: "",
    new_password: "",
  });

  useEffect(() => {
    loadProfile();
  }, []);

  async function loadProfile() {
    try {
      const data = await getProfile();
      setProfile(data);
    } catch (err) {
      toast.error(
    err.response?.data?.detail ||
    "Something went wrong."
);
    }
  }

  async function handleProfile(e) {
    e.preventDefault();

    try {
      await updateProfile(profile);
      alert("Profile updated successfully.");
    } catch (err) {
      toast.error(
      err.response?.data?.detail ||
      "Something went wrong."
    );
    }
  }

  async function handlePassword(e) {
    e.preventDefault();

    try {
      await changePassword(password);

      alert("Password changed successfully.");

      setPassword({
        current_password: "",
        new_password: "",
      });
    } catch (err) {
      toast.error(
      err.response?.data?.detail ||
      "Something went wrong."
    );
    }
  }

  return (
    <div className="max-w-3xl mx-auto space-y-8 bg-gray-100 dark:bg-slate-900 min-h-screen p-6">

      <h1 className="text-3xl font-bold text-black dark:text-white">
        Settings
      </h1>

      {/* Profile */}

      <div className="bg-white dark:bg-slate-800 shadow rounded-xl p-6">

        <h2 className="text-xl font-semibold text-black dark:text-white mb-5">
          Profile
        </h2>

        <form
          onSubmit={handleProfile}
          className="space-y-4"
        >

          <input
            className="w-full border rounded-lg p-3 bg-white dark:bg-slate-700 dark:text-white dark:border-slate-600"
            value={profile.name}
            onChange={(e) =>
              setProfile({
                ...profile,
                name: e.target.value,
              })
            }
            placeholder="Name"
          />

          <input
            className="w-full border rounded-lg p-3 bg-white dark:bg-slate-700 dark:text-white dark:border-slate-600"
            value={profile.email}
            onChange={(e) =>
              setProfile({
                ...profile,
                email: e.target.value,
              })
            }
            placeholder="Email"
          />

          <button
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg"
          >
            Save Profile
          </button>

        </form>

      </div>

      {/* Password */}

      <div className="bg-white dark:bg-slate-800 shadow rounded-xl p-6">

        <h2 className="text-xl font-semibold text-black dark:text-white mb-5">
          Change Password
        </h2>

        <form
          onSubmit={handlePassword}
          className="space-y-4"
        >

          <input
            type="password"
            className="w-full border rounded-lg p-3 bg-white dark:bg-slate-700 dark:text-white dark:border-slate-600"
            placeholder="Current Password"
            value={password.current_password}
            onChange={(e) =>
              setPassword({
                ...password,
                current_password: e.target.value,
              })
            }
          />

          <input
            type="password"
            className="w-full border rounded-lg p-3 bg-white dark:bg-slate-700 dark:text-white dark:border-slate-600"
            placeholder="New Password"
            value={password.new_password}
            onChange={(e) =>
              setPassword({
                ...password,
                new_password: e.target.value,
              })
            }
          />

          <button
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg"
          >
            Change Password
          </button>

        </form>

      </div>

      {/* Appearance */}

      <div className="bg-white dark:bg-slate-800 shadow rounded-xl p-6">

        <h2 className="text-xl font-semibold text-black dark:text-white mb-5">
          Appearance
        </h2>

        <button
          onClick={toggleTheme}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg"
        >
          Switch to {theme === "light" ? "Dark" : "Light"} Mode
        </button>

      </div>

    </div>
  );
}