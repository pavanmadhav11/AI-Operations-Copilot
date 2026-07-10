import { useEffect } from "react";
import { RouterProvider } from "react-router-dom";

import { router } from "./routes/AppRoutes";
import useAuthStore from "./store/authStore";

function App() {
  const { loadUser, token } = useAuthStore();

  useEffect(() => {
    if (token) {
      loadUser();
    }
  }, []);

  return <RouterProvider router={router} />;
}

export default App;