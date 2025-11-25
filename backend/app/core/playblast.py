
import subprocess
import json


def extract_video_metadata(path: str) -> dict:
    """
    Extract basic video metadata (resolution, fps, duration)
    using mediainfo command-line tool.
    """
    try:
        output = subprocess.check_output(["mediainfo", "--Output=JSON", path])
        data = json.loads(output)
        video = data["media"]["track"][1]  # track[1] = video

        return {
            "width": int(video.get("Width", 0)),
            "height": int(video.get("Height", 0)),
            "duration_ms": float(video.get("Duration", 0)),
            "fps": float(video.get("FrameRate", 0))
        }
    except Exception:
        return {}
        

def attach_playblast_to_version(
    db: Session,
    version_id: uuid.UUID,
    file: UploadFile
) -> Version:

    version = db.query(Version).filter(Version.id == version_id).first()
    if not version:
        raise ValueError(f"Version not found: {version_id}")

    ext = os.path.splitext(file.filename)[1].lower().lstrip(".") or "mp4"
    playblast_id = str(uuid.uuid4())
    filename = f"{playblast_id}.{ext}"
    storage_path = os.path.join(PLAYBLAST_STORAGE_ROOT, filename)

    os.makedirs(PLAYBLAST_STORAGE_ROOT, exist_ok=True)

    with open(storage_path, "wb") as out:
        out.write(file.file.read())

    # Extract metadata automatically
    metadata = extract_video_metadata(storage_path)

    version.playblast_path = storage_path
    version.playblast_ext = ext
    version.playblast_metadata = metadata

    db.add(version)
    db.commit()
    db.refresh(version)

    return version
