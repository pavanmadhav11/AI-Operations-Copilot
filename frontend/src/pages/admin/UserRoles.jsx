import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { getUsers, updateUserRole } from "../../services/userService";

export default function UserRoles() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getUsers()
      .then(setUsers)
      .catch(() => toast.error("Could not load users."))
      .finally(() => setLoading(false));
  }, []);

  async function changeRole(userId, role) {
    try {
      const updated = await updateUserRole(userId, role);
      setUsers((current) => current.map((user) => user.id === userId ? updated : user));
      toast.success("User role updated.");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Could not update the role.");
    }
  }

  return (
    <main className="p-8">
      <h1 className="mb-2 text-3xl font-bold">User roles</h1>
      <p className="mb-6 text-slate-600">Admins can choose whether each account is an admin, manager, or employee.</p>
      {loading ? <p>Loading users...</p> : (
        <div className="max-w-3xl overflow-hidden rounded-lg bg-white shadow">
          {users.map((user) => (
            <div className="flex items-center justify-between border-b p-4" key={user.id}>
              <div>
                <p className="font-semibold">{user.name}</p>
                <p className="text-sm text-slate-600">{user.email}</p>
              </div>
              <select aria-label={`Role for ${user.email}`} className="rounded border border-slate-300 p-2" onChange={(event) => changeRole(user.id, event.target.value)} value={user.role}>
                <option value="employee">Employee</option>
                <option value="manager">Manager</option>
                <option value="admin">Admin</option>
              </select>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
