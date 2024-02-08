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