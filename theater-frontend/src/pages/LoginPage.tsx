import React from "react";
import { Button, Container, Paper, Typography } from "@mui/material";
import LoginIcon from "@mui/icons-material/Login";
import SecurityIcon from "@mui/icons-material/Security";
import { useAuth } from "../auth/AuthContext";

const LoginPage: React.FC = () => {
  const { login } = useAuth();

  return (
    <Container maxWidth="sm" sx={{ py: 8 }}>
      <Paper elevation={3} sx={{ p: 4, textAlign: "center" }}>
        <SecurityIcon color="primary" sx={{ fontSize: 60, mb: 2 }} />

        <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
          Welcome to MVL Theater
        </Typography>

        <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
          Sign in with Keycloak to continue.
        </Typography>

        <Button
          variant="contained"
          size="large"
          startIcon={<LoginIcon />}
          onClick={login}
        >
          Sign in with Keycloak
        </Button>
      </Paper>
    </Container>
  );
};

export default LoginPage;
