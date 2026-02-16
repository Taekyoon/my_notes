"""
방명록 이미지에서 이름을 추출하는 스크립트
Usage: python extract_names.py <image_path> [--lang kor+eng]
"""

import argparse
import sys
import re
from pathlib import Path

import cv2
import pytesseract
from PIL import Image


def preprocess_image(image_path: str):
    """OCR 정확도를 높이기 위해 이미지를 전처리한다."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"이미지를 열 수 없습니다: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 노이즈 제거
    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    # 이진화 (adaptive threshold)
    binary = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    return binary


def extract_text(image_path: str, lang: str = "kor+eng") -> str:
    """이미지에서 텍스트를 추출한다."""
    processed = preprocess_image(image_path)
    pil_image = Image.fromarray(processed)

    custom_config = r"--oem 3 --psm 6"
    text = pytesseract.image_to_string(pil_image, lang=lang, config=custom_config)
    return text


def parse_names(raw_text: str) -> list[str]:
    """추출된 텍스트에서 이름을 파싱한다."""
    lines = raw_text.strip().splitlines()
    names = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 한글 이름 패턴 (2~4글자)
        korean_names = re.findall(r"[가-힣]{2,4}", line)
        # 영문 이름 패턴 (대문자로 시작하는 단어)
        english_names = re.findall(r"[A-Z][a-z]+(?:\s[A-Z][a-z]+)*", line)

        names.extend(korean_names)
        names.extend(english_names)

    # 중복 제거, 순서 유지
    seen = set()
    unique_names = []
    for name in names:
        if name not in seen:
            seen.add(name)
            unique_names.append(name)

    return unique_names


def main():
    parser = argparse.ArgumentParser(description="방명록 이미지에서 이름을 추출합니다.")
    parser.add_argument("image", help="방명록 이미지 파일 경로")
    parser.add_argument(
        "--lang",
        default="kor+eng",
        help="OCR 언어 (기본값: kor+eng)",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="전처리 없이 원본 텍스트도 함께 출력",
    )
    args = parser.parse_args()

    image_path = args.image
    if not Path(image_path).exists():
        print(f"파일을 찾을 수 없습니다: {image_path}", file=sys.stderr)
        sys.exit(1)

    raw_text = extract_text(image_path, lang=args.lang)

    if args.raw:
        print("=== 원본 OCR 텍스트 ===")
        print(raw_text)
        print()

    names = parse_names(raw_text)

    print(f"=== 추출된 이름 ({len(names)}명) ===")
    for i, name in enumerate(names, 1):
        print(f"  {i}. {name}")


if __name__ == "__main__":
    main()
