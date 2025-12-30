import React, { useState } from "react";
import {
  Box,
  Stack,
  TextField,
  MenuItem,
  Button,
  Typography,
} from "@mui/material";
import ImageIcon from "@mui/icons-material/Image";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

interface Props {
  projectId: string;
  onClose: () => void;       // To close the add panel
  onCreated?: () => void;    // To refresh asset list
}

const AddAssetForm: React.FC<Props> = ({ projectId, onClose, onCreated }) => {
  const [assetName, setAssetName] = useState("");
  const [assetType, setAssetType] = useState("model");
  const [notes, setNotes] = useState("");
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSaveAsset = async () => {
    if (!assetName.trim()) {
      alert("Asset name is required");
      return;
    }
    if (!uploadFile) {
      alert("Please upload a file");
      return;
    }

    try {
      setLoading(true);

      // STEP 1 — Create asset in FastAPI
      const createRes = await fetch(`${API_BASE_URL}/assets`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_id: projectId,
          asset_category_id: projectId,
          asset_type_id: projectId,
          code: assetName,
          name: assetName,
          status: "new",
          meta: {},
        }),
      });

      const asset = await createRes.json();
      const assetId = asset.id;

      // STEP 2 — Get upload URL
      const uploadUrlRes = await fetch(
        `${API_BASE_URL}/assets/${assetId}/upload_url`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            filename: uploadFile.name,
            content_type: uploadFile.type,
          }),
        }
      );

      const uploadData = await uploadUrlRes.json();

      // STEP 3 — Upload to MinIO
      await fetch(uploadData.url, {
        method: "PUT",
        headers: {
          "Content-Type": uploadFile.type,
        },
        body: uploadFile,
      });

      alert("Asset saved!");

      setAssetName("");
      setNotes("");
      setUploadFile(null);

      if (onCreated) onCreated();
      onClose();

    } catch (err) {
      console.error(err);
      alert("Failed to save asset.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
        Add asset
      </Typography>

      <Stack spacing={2}>
        {/* Asset name */}
        <TextField
          label="Asset name"
          fullWidth
          value={assetName}
          onChange={(e) => setAssetName(e.target.value)}
        />

        {/* Asset type */}
        <TextField
          select
          label="Asset type"
          value={assetType}
          fullWidth
          onChange={(e) => setAssetType(e.target.value)}
        >
          <MenuItem value="model">Model</MenuItem>
          <MenuItem value="texture">Texture</MenuItem>
          <MenuItem value="hdri">HDRI</MenuItem>
          <MenuItem value="anim">Animation</MenuItem>
          <MenuItem value="vfx">VFX</MenuItem>
          <MenuItem value="other">Other</MenuItem>
        </TextField>

        {/* File upload */}
        <Button variant="outlined" startIcon={<ImageIcon />} component="label">
          Upload image / preview
          <input
            type="file"
            hidden
            accept="image/*"
            onChange={(e) => {
              if (e.target.files) setUploadFile(e.target.files[0]);
            }}
          />
        </Button>

        {/* Notes */}
        <TextField
          label="Notes"
          fullWidth
          multiline
          minRows={2}
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />

        <Stack direction="row" spacing={1}>
          <Button
            variant="contained"
            onClick={handleSaveAsset}
            disabled={loading}
          >
            {loading ? "Saving..." : "Save asset"}
          </Button>
          <Button variant="text" onClick={onClose}>
            Cancel
          </Button>
        </Stack>
      </Stack>
    </Box>
  );
};

export default AddAssetForm;
