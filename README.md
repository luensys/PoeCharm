# 한글 PoB

본 프로젝트는 중국어용 PoB인 PoeCharm을 한국어 버전으로 수정한 것입니다.

폰트와 번역은 PoE 네이버 카페의 겜하는아제님의 DB에서 가져왔습니다.

# 번역 정리 및 통합 방법

번역에 대한 프로그램은 공통적으로 만들 필요가 있어보여 몇 가지 기준을 정리합니다.

## csv 각 파일명

- cn 또는 tw 원본 : PoeCharm/Pob
- 한국어 원본 : PoeCharm/Pob/translate_kr.csv
- 구글 스프레드시트의 번역 완료 시트 csv 파일 : translator/translated.csv
- 구글 스프레드시트의 번역 필요 시트 csv 파일 : translator/non_translated.csv

## 작업 방법

1. 구글 스프레드시트의 번역 완료 시트 csv 파일과 한국어 원본 파일을 merge
   1. 새로운 구글 스프레드시트의 csv 파일과 기존 csv의 다를 부분을 비교해 새로운 번역으로 대체
   2. 결과는 translator/merged.csv
2. 구글 스프레드시트의 번역 필요 시트 csv 파일과 1번의 파일을 merge
   1. 합쳐진 결과는 translator/merged_kr.csv
3. 원본 csv 파일과 merge 완료된 파일을 비교하여 정리
   1. 원본 csv 파일에는 없지만 merge 완료된 파일에는 있는 것은 삭제 (이제 필요 없는 번역이므로)
      1. 이렇게 완료된 파일의 결과는 translator/translate_kr.csv로 완성
      2. 구글 스프레드시트 업로드용으로 쓰기 위해 Delimiter를 tab으로 한 csv 생성 결과는 translator/completed_translate.csv
   2. 원본 csv 파일에는 있지만 merge 완료된 파일에는 없는 것은 번역 필요 시트에 업데이트할 파일 생성
      1. 이렇게 완료된 파일의 결과는 translator/need_translate.csv
      2. delimiter는 tab으로 해야 함

# 아래는 기존 프로젝트에 있던 글을 그대로 남겼습니다.

---

# PoeCharm

Path of Building Chinese version
