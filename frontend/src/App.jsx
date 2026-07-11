import { useEffect } from "react";
import { RouterProvider } from "react-router-dom";

import { router } from "./routes/AppRoutes";
import useAuthStore from "./store/authStore";

function App() {
  const { token, loadUser } = useAuthStore();

  useEffect(() => {
    if (token) {
      loadUser();
    }
  }, [token]);

  return <RouterProvider router={router} />;
}

export default App;