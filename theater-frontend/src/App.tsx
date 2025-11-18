import React from "react";
import LoginPage from "./pages/LoginPage";
import UsersPage from "./pages/UsersPage";
import { useAuth } from "./auth/AuthContext";

const App: React.FC = () => {
  const { initialized, authenticated } = useAuth();

  if (!initialized) return <div>Loading auth…</div>;

  return authenticated ? <UsersPage /> : <LoginPage />;
};

export default App;
