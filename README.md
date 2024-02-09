# TODO

1. 개별의 파일들에 TODO 항목작성된 것 정리해 둘 수단 확보.
  * 전체 프로젝트를 읽고, TodoList 생성하는 스크립트 생성 등
2. 디버깅 용도로 프로그램 중간 중간에 작성한 print() 메시지들 중, 로그 형태로 남길 필요가 있는지 중요도 구분 후 로그화.


## 서버 실행 방법

myapp과 동일한 위치에서 다음 명령어를 실행합니다.

py -m uvicorn myapp.main:app --reload

---

## bcrypt version error

bcrypt 4.0.1 사용
(https://github.com/logspace-ai/langflow/issues/1173)

(trapped) error reading bcrypt version                            ApOhJXUIEvz.CdWB
Traceback (most recent call last):
  File "c:\Users\didme\Documents\CommunityBoardAPI\.venv\Lib\site-packages\passlib\handlers\bcrypt.py", line 562, in _load_backend_mixin                                                              packages\passlib
    version = _bcrypt.__about__.__version__
              ^^^^^^^^^^^^^^^^^
AttributeError: module 'bcrypt' has no attribute '__about__' 

## 테스트에 사용중인 email/pw

* email: didme07@gmail.com, didme08@gmail.com
* pw: didme07@gmail.com, didme08@gmail.com

## 테스트에 추가된 Board

* 1;"True Board";true;8
* 2;"False Board";false;8