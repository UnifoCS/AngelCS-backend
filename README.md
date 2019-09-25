# AngelCS Backend server

## Requirements
| Module | Version |
| --- | --- |
| OS | Tensorflow, Keras, Python supported OS |
| Python  | >= 3.6 |



virtualenv, pyenv 등의 사용을 권장합니다.
## Configuration
### Release 예시
먼저 configs/release.py를 만들고 설정값을 입력합니다.
```python
import configs

#
# Put Your Release Config here!!!
# See parameters at configs/__init__.py
class ReleaseConfig(configs.DefaultConfig):
    DATABASE_URI = "mysql+pymysql:///..."

```
[doc/configuration.md]()에서 자세한 설정 방법을 안내해드립니다.

## Installation
목적에 따라 debug나 release를 선택할 수 있습니다.

```bash
# Debug 용
make debug

# Release 용
make release

# Unit Test
make test
```

## API 서버 실행
```bash
#
# --config: (release|debug)
# Default is debug.
python server.py —-config release
```