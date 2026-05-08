#!/usr/bin/env python3
"""
MiniMax Image Generation Script for 骗了吗 project
Based on: https://platform.minimaxi.com/docs/api-reference/image-generation-t2i

Usage:
    python3 generate_image.py --prompt "描述" [--aspect-ratio 16:9] [--n 1] [--api-key xxx]
"""

import argparse
import requests
import sys
import json
import os

DEFAULT_API_KEY = os.environ.get("MINIMAX_API_KEY", "")

def generate_image(prompt: str, api_key: str, aspect_ratio: str = "16:9", n: int = 1, model: str = "image-01"):
    url = "https://api.minimaxi.com/v1/image_generation"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": "url",
        "n": n
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()

    result = resp.json()

    if result.get("base_resp", {}).get("status_code") != 0:
        print(f"Error: {result}", file=sys.stderr)
        sys.exit(1)

    image_urls = result.get("data", {}).get("image_urls", [])
    return image_urls


def main():
    parser = argparse.ArgumentParser(description="MiniMax Image Generation")
    parser.add_argument("--prompt", "-p", required=True, help="Image prompt")
    parser.add_argument("--aspect-ratio", "-r", default="16:9",
                        choices=["1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16", "21:9"],
                        help="Aspect ratio (default: 16:9)")
    parser.add_argument("--n", type=int, default=1, choices=range(1, 10),
                        help="Number of images to generate (1-9)")
    parser.add_argument("--model", "-m", default="image-01",
                        choices=["image-01", "image-01-live"],
                        help="Model to use")
    parser.add_argument("--api-key", "-k", default=DEFAULT_API_KEY,
                        help="MiniMax API Key (or set MINIMAX_API_KEY env)")
    parser.add_argument("--style", "-s", choices=["漫画", "元气", "中世纪", "水彩"],
                        help="Style type (only for image-01-live)")

    args = parser.parse_args()

    if not args.api_key:
        print("Error: API key required. Set MINIMAX_API_KEY env or use --api-key", file=sys.stderr)
        sys.exit(1)

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "aspect_ratio": args.aspect_ratio,
        "response_format": "url",
        "n": args.n
    }

    if args.style and args.model == "image-01-live":
        payload["style"] = {
            "style_type": args.style,
            "style_weight": 0.8
        }

    try:
        urls = generate_image(
            prompt=args.prompt,
            api_key=args.api_key,
            aspect_ratio=args.aspect_ratio,
            n=args.n,
            model=args.model
        )

        for i, url in enumerate(urls):
            print(f"IMAGE_URL_{i+1}: {url}")

        if urls:
            print(f"MEDIA_URL: {urls[0]}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()