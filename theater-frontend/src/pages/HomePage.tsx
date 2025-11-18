import React from "react";
import {
  AppBar,
  Avatar,
  Box,
  Button,
  Container,
  IconButton,
  Paper,
  Stack,
  Toolbar,
  Typography,
  Chip,
} from "@mui/material";
import LoginIcon from "@mui/icons-material/Login";
import LogoutIcon from "@mui/icons-material/Logout";
import SecurityIcon from "@mui/icons-material/Security";
import { useAuth } from "../auth/AuthContext";
import keycloak from "../keycloak";

const HomePage: React.FC = () => {
  const { initialized, authenticated, username, login, logout } = useAuth();

  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "background.default" }}>
      {/* Top AppBar */}
      <AppBar position="static" color="default" elevation={1}>
        <Toolbar>
          <SecurityIcon color="primary" sx={{ mr: 1 }} />
          <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: 600 }}>
            MVL Theater
          </Typography>

          {/* Right user icon + status */}
          <Stack direction="row" spacing={1} alignItems="center">
            <Chip
              size="small"
              label={
                !initialized
                  ? "Checking session…"
                  : authenticated
                  ? "Signed in"
                  : "Signed out"
              }
              color={authenticated ? "success" : "default"}
              variant={authenticated ? "filled" : "outlined"}
            />
            <IconButton>
              <Avatar sx={{ width: 32, height: 32 }}>
                {username ? username[0]?.toUpperCase() : "U"}
              </Avatar>
            </IconButton>
          </Stack>
        </Toolbar>
      </AppBar>

      <Container maxWidth="md" sx={{ py: 4 }}>
        <Paper
          elevation={2}
          sx={{
            p: 3,
            display: "flex",
            flexDirection: "column",
            gap: 2,
          }}
        >
          <Typography variant="h5" sx={{ fontWeight: 600 }}>
            Welcome{authenticated && username ? `, ${username}` : ""} 👋
          </Typography>

          <Typography variant="body1" color="text.secondary">
            This frontend is connected to Keycloak for authentication. Use the
            buttons below to sign in or out, and inspect your current auth
            status.
          </Typography>

          <Stack direction="row" spacing={2} sx={{ mt: 1 }}>
            {!authenticated ? (
              <Button
                variant="contained"
                startIcon={<LoginIcon />}
                onClick={login}
                disabled={!initialized}
              >
                Sign in with Keycloak
              </Button>
            ) : (
              <Button
                variant="outlined"
                color="error"
                startIcon={<LogoutIcon />}
                onClick={logout}
              >
                Sign out
              </Button>
            )}
          </Stack>

          {/* Keycloak config info */}
          <Box
            sx={{
              mt: 3,
              p: 2,
              borderRadius: 2,
              bgcolor: "background.default",
              border: "1px solid",
              borderColor: "divider",
            }}
          >
            <Typography variant="subtitle2" gutterBottom>
              Keycloak connection
            </Typography>
            <Typography variant="body2" color="text.secondary">
              <strong>Server:</strong> {keycloak.authServerUrl ?? "N/A"}
              <br />
              <strong>Realm:</strong> {keycloak.realm}
              <br />
              <strong>Client ID:</strong> {keycloak.clientId}
            </Typography>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default HomePage;
