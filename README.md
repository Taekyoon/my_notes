# Guestbook Name Extractor

방명록 이미지에서 이름을 자동으로 추출하는 도구입니다.

## 요구사항

- Python 3.9+
- Tesseract OCR (`apt install tesseract-ocr tesseract-ocr-kor`)

## 설치

```bash
pip install -r requirements.txt
```

## 사용법

```bash
# 기본 사용 (한국어 + 영어)
python extract_names.py 방명록.jpg

# OCR 원본 텍스트도 함께 보기
python extract_names.py 방명록.jpg --raw

# 영어만
python extract_names.py guestbook.png --lang eng
```

## 출력 예시

```
=== 추출된 이름 (3명) ===
  1. 홍길동
  2. 김철수
  3. John Park
```
