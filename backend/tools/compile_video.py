"""ADK Tool for compiling multimedia memories into "Reels" using FFmpeg."""

import asyncio
import subprocess
import tempfile
from pathlib import Path

import structlog

from backend.integrations.cloud_storage import upload_bytes

log = structlog.get_logger(__name__)


async def compile_reel_video(
    image_paths: list[str], audio_path: str, output_name: str = "reel.mp4"
) -> str:
    """Compiles a set of images and an audio file into a video reel using FFmpeg.

    Creates a temporal video sequence where each image is displayed for 3 seconds,
    synced with the provided audio track.

    Args:
        image_paths: List of absolute paths to local image files.
        audio_path: Absolute path to the local audio file.
        output_name: Desired filename for the resulting MP4.

    Returns:
        The public GCS URL of the uploaded video, or an empty string on failure.
    """
    with tempfile.TemporaryDirectory() as tmp_dir_str:
        tmp_dir = Path(tmp_dir_str)

    output_path = tmp_dir / output_name
    input_list = tmp_dir / "input.txt"

    try:
        log.info("compiling_reel", images=len(image_paths), audio=audio_path)

        # Create a file list for FFmpeg concat demuxer
        # Each image is shown for 3 seconds
        with open(input_list, "w") as f:
            for img in image_paths:
                f.write(f"file '{img}'\nduration 3\n")
            # Repeat the last image to avoid FFmpeg cutting it early
            if image_paths:
                f.write(f"file '{image_paths[-1]}'\n")

        # FFmpeg command:
        # -f concat: use the concat demuxer
        # -i input.txt: input file list
        # -i audio_path: audio track
        # -c:v libx264: encode video as H.264
        # -pix_fmt yuv420p: compatibility for most players
        # -vf scale: ensure even dimensions
        # -shortest: finish when the shortest track ends
        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(input_list),
            "-i",
            audio_path,
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-vf",
            "scale=trunc(iw/2)*2:trunc(ih/2)*2",
            "-shortest",
            str(output_path),
        ]

        # Run FFmpeg
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            log.error("ffmpeg_failed", error=stderr.decode())
            return ""

        # Upload to Cloud Storage
        with open(output_path, "rb") as f:
            video_bytes = f.read()

        gcs_url = await upload_bytes(video_bytes, f"reels/{output_name}", content_type="video/mp4")
        log.info("reel_uploaded", url=gcs_url)

        return gcs_url

    except Exception as e:
        log.error("error_compiling_reel", error=str(e))
        return ""
    finally:
        # Cleanup
        if input_list.exists():
            input_list.unlink()
        if output_path.exists():
            output_path.unlink()
