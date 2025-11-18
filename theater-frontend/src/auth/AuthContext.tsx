import React, { createContext, useContext, useEffect, useState } from "react";
import keycloak from "../keycloak";

type AuthContextType = {
  initialized: boolean;
  authenticated: boolean;
  username?: string;
  token?: string;
  login: () => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [initialized, setInitialized] = useState(false);
  const [authenticated, setAuthenticated] = useState(false);
  const [username, setUsername] = useState<string | undefined>(undefined);
  const [token, setToken] = useState<string | undefined>(undefined);

  useEffect(() => {
    keycloak
      .init({
        onLoad: "check-sso", // don't force login on load
        silentCheckSsoRedirectUri:
          window.location.origin + "/silent-check-sso.html",
      })
      .then((auth) => {
        setAuthenticated(!!auth);
        if (auth) {
          setToken(keycloak.token || undefined);
          const parsed = keycloak.tokenParsed as { preferred_username?: string } | undefined;
          setUsername(parsed?.preferred_username);
        }
      })
      .finally(() => setInitialized(true));
  }, []);

  const login = () => {
    keycloak.login();
  };

  const logout = () => {
    keycloak.logout({ redirectUri: window.location.origin });
  };

  const value: AuthContextType = {
    initialized,
    authenticated,
    username,
    token,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
};
