from __future__ import annotations

import argparse
import base64
import mimetypes
import os
from pathlib import Path

from openai import OpenAI


def encode_image_as_data_url(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    mime_type = mime_type or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a local image to the vision model server.")
    parser.add_argument("--image", required=True, help="Path to a local image file.")
    parser.add_argument(
        "--prompt",
        default="Describe the UI and identify the most important visible issues.",
        help="Prompt to send with the image.",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("VISION_MODEL_BASE_URL", "http://127.0.0.1:8081/v1"),
        help="OpenAI-compatible base URL for the vision server.",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("VISION_MODEL_NAME", "Qwen3-VL-2B-Instruct"),
        help="Served vision model name.",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("VISION_MODEL_API_KEY", "local-vision"),
        help="API key for the local vision server.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=512,
        help="Maximum response tokens.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    image_path = Path(args.image).expanduser().resolve()
    if not image_path.exists():
        raise SystemExit(f"Image file not found: {image_path}")

    client = OpenAI(base_url=args.base_url, api_key=args.api_key)
    image_url = encode_image_as_data_url(image_path)

    completion = client.chat.completions.create(
        model=args.model,
        max_tokens=args.max_tokens,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": args.prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
    )
    print(completion.choices[0].message.content or "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
