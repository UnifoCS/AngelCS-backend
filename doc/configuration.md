# How to change configurations?

[configs/__init__.py]() 에서 설정값을 바꿀 수 있으며 주석으로 자세한 설명이 있습니다.
```python
# configs/__init__.py
import os
import argparse

#
# release, debug 외에 다른 config를 여기에 추가
def from_arg_module():
    config = get_config_from_argument()

    if config == "release":
        import release
        return release.ReleaseConfig()
    elif config == "debug":
        import debug
        return debug.DebugConfig()
    else:
        return DefaultConfig()

class DefaultConfig(dict):
    ...

```

디버그 버전의 configurations는 여기에 추가해주세요.

```python
# configs/debug.py
import configs

#
# Put Your Debug Config here!!!
# See parameters at configs/__init__.py
class DebugConfig(configs.DefaultConfig):
    ...

```

릴리즈 버전의 configurations는 여기에 추가해주세요.<br>
릴리즈 버전은 gitignore에 추가해서 기록에 남지 않게 해야합니다.

```python
# configs/release.py
import configs

#
# Put Your Release Config here!!!
# See parameters at configs/__init__.py
class ReleaseConfig(configs.DefaultConfig):
    pass
```

### Configuration을 가져오는 방법
```python
import configs

config = configs.from_arg_module()
```