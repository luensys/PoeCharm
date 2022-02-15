# 한글 PoB

본 프로젝트는 중국어용 PoB인 PoeCharm을 한국어 버전으로 수정한 것입니다.

폰트와 번역은 PoE 네이버 카페의 겜하는아제님의 DB에서 가져왔습니다.

# 번역 정리 및 통합 방법

번역에 대한 프로그램은 공통적으로 만들 필요가 있어보여 몇 가지 기준을 정리합니다.

## 번역 Google spread sheet

https://docs.google.com/spreadsheets/d/1RCvj6xdP8Np2B1ksoYNn59WNYjdJeQaF9edUSIIKfI0/edit#gid=1352650069

## csv 각 파일명

- cn 원본 : PoeCharm/Pob/translate_cn
- tw 원본 : PoeCharm/Pob/translate_tw
- 한글 원본 : PoeCharm/Pob/translated_kr/translate_kr.csv
- 한글 번역 데이터 위치 : PoeCharm/Pob/translated_kr/
- 번역 정리 프로그램 위치 : translator/각 언어별폴더/

## 작업 방법

1. 구글 스프레드시트의 각 시트의 데이터를 csv로 저장
2. 1에서 저장한 파일과 한글 번역 데이터 위치의 번역 데이터를 읽어 옴
3. 중국어 데이터를 파일별로 읽어오면서 한글 번역 데이터와 비교해서 해당 파일로 생성
4. 3번 작업을 하면서 번역 완료 된 파일, 번역이 필요한 파일, 번역이 있지만 사용되지 않은 파일로 정리
5. 정리된 파일을 다시 구글 스프레드시트에 적용

# 아래는 기존 프로젝트에 있던 글을 그대로 남겼습니다.

---

# PoeCharm

Path of Building Chinese version
