# 사용 방법

## github에서 다운로드
![github 에서 다운로드](https://user-images.githubusercontent.com/7742477/156355861-03025a4f-b50c-435e-a1d6-161eac963ba7.png)  

## zip 파일 압축 풀기
![zip 파일](https://user-images.githubusercontent.com/7742477/156355982-38bbd01e-65ea-4129-9877-05a66112138e.png)  
![압축 해제](https://user-images.githubusercontent.com/7742477/156355991-a609b82a-7b79-499f-9f53-8c0ffe9f8e18.png)  

## PoeCharm.exe 파일 실행
![파일 실행](https://user-images.githubusercontent.com/7742477/156356058-d921898a-6f79-41e0-a3c7-57d352a853c3.png)  

### PC 보호 화면이 나올 경우
추가 정보를 클릭 후 실행  
![pc 보호](https://user-images.githubusercontent.com/7742477/156356111-53218a5b-0c32-41d7-b376-2b08d70d2e7a.png)  
![보호 실행](https://user-images.githubusercontent.com/7742477/156356152-7f7827e1-3c38-4137-96d4-c7da8667fb33.png)  

## 아이콘 클릭
![아이콘 클릭](https://user-images.githubusercontent.com/7742477/156356181-463f1e06-e699-449b-9334-5de8cfbd9f80.png)  

### 한글이 아닐 경우
좌 하단의 번역을 translate_kr로 변경  
![하단 언어 선택](https://user-images.githubusercontent.com/7742477/156356238-51196664-da47-46e3-8d62-b9e214624a80.png)  

## 실행 화면
![실행 화면](https://user-images.githubusercontent.com/7742477/156356262-f1a2fd94-844d-451e-bea3-da502665f5ea.png)  

# FAQ
### 화면이 너무 크고 전체 화면이 나오지 않아요.
이 경우 모니터 중 하나가 화면 비율이 100%가 아닌 150% 또는 200%으로 확대 되어 있으니 찾아서 변경해야 합니다.  


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

# 작업에 필요한 정보

- search query 추출
  - https://poe-query.vercel.app/

# 아래는 기존 프로젝트에 있던 글을 그대로 남겼습니다.

---

# PoeCharm

Path of Building Chinese version
