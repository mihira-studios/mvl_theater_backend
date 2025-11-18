import React, { useState } from "react";
import {
  Avatar,
  Box,
  Button,
  Chip,
  Divider,
  IconButton,
  MenuItem,
  Paper,
  Stack,
  Switch,
  TextField,
  Typography,
  Grid,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import ViewListIcon from "@mui/icons-material/ViewList";
import LogoutIcon from "@mui/icons-material/Logout";
import ImageIcon from "@mui/icons-material/Image";
import { useAuth } from "../auth/AuthContext";

// Temporary mock assets – later you’ll fetch from backend
const mockAssets = [
  {
    id: "a1",
    name: "hero_character_rig",
    type: "model",
    thumbColor: "#6366f1",
    tags: ["character", "rig", "hero"],
  },
  {
    id: "a2",
    name: "city_alley_hdri",
    type: "hdri",
    thumbColor: "#f59e0b",
    tags: ["environment", "night", "alley"],
  },
  {
    id: "a3",
    name: "fx_dust_burst",
    type: "vfx",
    thumbColor: "#10b981",
    tags: ["fx", "dust", "burst"],
  },
  {
    id: "a4",
    name: "prop_sci-fi_crate",
    type: "model",
    thumbColor: "#ec4899",
    tags: ["prop", "sci-fi"],
  },
];

const UsersPage: React.FC = () => {
  const { username, logout } = useAuth();
  const [showAddPanel, setShowAddPanel] = useState(false);
  const [aiTaggingEnabled, setAiTaggingEnabled] = useState(true);

  const handleToggleAddPanel = () => {
    setShowAddPanel((prev) => !prev);
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        bgcolor: "background.default",
        p: 2,
      }}
    >
      {/* Left side navigation panel */}
      <Paper
        elevation={2}
        sx={{
          width: 220,
          p: 2,
          display: "flex",
          flexDirection: "column",
          gap: 2,
          mr: 2,
        }}
      >
        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          Assets
        </Typography>

        <Stack spacing={1}>
          <Button
            variant={showAddPanel ? "outlined" : "contained"}
            startIcon={<AddIcon />}
            fullWidth
            onClick={handleToggleAddPanel}
          >
            {showAddPanel ? "Close" : "Add"}
          </Button>
          <Button variant="outlined" startIcon={<ViewListIcon />} fullWidth>
            Catalog
          </Button>
        </Stack>

        <Divider sx={{ my: 2 }} />

        <Typography variant="body2" color="text.secondary">
          Use “Add” to attach new assets with AI-assisted image tagging. The
          catalog shows all asset thumbnails.
        </Typography>
      </Paper>

      {/* Main content */}
      <Box sx={{ flex: 1, display: "flex", flexDirection: "column", gap: 2 }}>
        {/* Top bar: search + avatar + logout */}
        <Paper
          elevation={1}
          sx={{
            p: 1.5,
            display: "flex",
            alignItems: "center",
            gap: 1.5,
          }}
        >
          <TextField
            placeholder="Search assets"
            variant="outlined"
            size="small"
            fullWidth
          />

          <IconButton>
            <Avatar sx={{ bgcolor: "primary.main" }}>
              {username ? username[0].toUpperCase() : "U"}
            </Avatar>
          </IconButton>

          <Button
            color="error"
            variant="outlined"
            startIcon={<LogoutIcon />}
            onClick={logout}
          >
            Logout
          </Button>
        </Paper>

        {/* Add panel: asset loading + AI tagging */}
        {showAddPanel && (
          <Paper
            elevation={2}
            sx={{
              p: 2,
              display: "grid",
              gridTemplateColumns: { xs: "1fr", md: "2fr 1.3fr" },
              gap: 2,
            }}
          >
            {/* Asset loading info */}
            <Box>
              <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                Add asset
              </Typography>

              <Stack spacing={2}>
                <TextField
                  label="Asset name"
                  placeholder="e.g. hero_character_rig"
                  fullWidth
                />

                <TextField
                  select
                  label="Asset type"
                  defaultValue="model"
                  fullWidth
                >
                  <MenuItem value="model">Model</MenuItem>
                  <MenuItem value="texture">Texture</MenuItem>
                  <MenuItem value="hdri">HDRI</MenuItem>
                  <MenuItem value="anim">Animation</MenuItem>
                  <MenuItem value="vfx">VFX</MenuItem>
                  <MenuItem value="other">Other</MenuItem>
                </TextField>

                <Button
                  variant="outlined"
                  startIcon={<ImageIcon />}
                  component="label"
                >
                  Upload image / preview
                  <input type="file" hidden accept="image/*" />
                </Button>

                <TextField
                  label="Notes"
                  placeholder="Optional notes about this asset…"
                  fullWidth
                  multiline
                  minRows={2}
                />

                <Stack direction="row" spacing={1}>
                  <Button variant="contained">Save asset</Button>
                  <Button variant="text">Cancel</Button>
                </Stack>
              </Stack>
            </Box>

            {/* AI image tagging */}
            <Box
              sx={{
                borderLeft: { md: "1px solid", xs: "none" },
                borderColor: { md: "divider" },
                pl: { md: 2 },
              }}
            >
              <Stack
                direction="row"
                alignItems="center"
                justifyContent="space-between"
              >
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                  AI image tagging
                </Typography>
                <Stack direction="row" spacing={1} alignItems="center">
                  <Typography variant="caption" color="text.secondary">
                    Auto-tag
                  </Typography>
                  <Switch
                    checked={aiTaggingEnabled}
                    onChange={(e) => setAiTaggingEnabled(e.target.checked)}
                    size="small"
                  />
                </Stack>
              </Stack>

              <Typography
                variant="body2"
                color="text.secondary"
                sx={{ mt: 1, mb: 2 }}
              >
                When enabled, the system will analyze the uploaded image and
                suggest tags like character, props, location, lighting style,
                mood, etc.
              </Typography>

              <Typography variant="caption" color="text.secondary">
                Suggested tags (mocked for now):
              </Typography>

              <Stack
                direction="row"
                spacing={1}
                sx={{ mt: 1, flexWrap: "wrap" }}
              >
                {aiTaggingEnabled ? (
                  <>
                    <Chip size="small" label="character" />
                    <Chip size="small" label="hero" />
                    <Chip size="small" label="cinematic" />
                    <Chip size="small" label="studio_light" />
                    <Chip size="small" label="vfx-ready" />
                  </>
                ) : (
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ mt: 0.5 }}
                  >
                    Enable auto-tagging to see AI suggestions here.
                  </Typography>
                )}
              </Stack>
            </Box>
          </Paper>
        )}

        {/* Asset thumbnail catalog */}
        <Paper elevation={1} sx={{ flex: 1, p: 2 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Asset Catalog
          </Typography>

          <Grid container spacing={2}>
            {mockAssets.map((asset) => (
              <Grid item xs={12} sm={6} md={3} key={asset.id}>
                <Paper
                  elevation={2}
                  sx={{
                    p: 1.5,
                    borderRadius: 2,
                    display: "flex",
                    flexDirection: "column",
                    gap: 1,
                    cursor: "pointer",
                    transition: "transform 0.1s ease, box-shadow 0.1s ease",
                    "&:hover": {
                      transform: "translateY(-2px)",
                      boxShadow: 4,
                    },
                  }}
                >
                  {/* Thumbnail box */}
                  <Box
                    sx={{
                      height: 120,
                      borderRadius: 1.5,
                      mb: 0.5,
                      bgcolor: asset.thumbColor,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      color: "white",
                      fontWeight: 600,
                      fontSize: 12,
                      textTransform: "uppercase",
                      letterSpacing: 0.08,
                    }}
                  >
                    {asset.type}
                  </Box>

                  <Typography
                    variant="body2"
                    sx={{
                      fontWeight: 600,
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                    }}
                    title={asset.name}
                  >
                    {asset.name}
                  </Typography>

                  <Stack
                    direction="row"
                    spacing={0.5}
                    sx={{ flexWrap: "wrap", mt: 0.5 }}
                  >
                    {asset.tags.map((tag) => (
                      <Chip key={tag} size="small" label={tag} />
                    ))}
                  </Stack>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Paper>
      </Box>
    </Box>
  );
};

export default UsersPage;
