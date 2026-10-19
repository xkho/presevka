# 소스에서 빌드하기

완성된 폰트는 [릴리스](https://github.com/xkho/presevka/releases/latest)에서 받을
수 있습니다. 이 문서는 직접 빌드해야 하는 경우를 위한 것입니다.

- 라틴 글자꼴을 바꾸고 싶은데 사용하는 앱이 OpenType 피처를 지원하지 않을 때
- 힌팅을 끄거나 한글에만 다르게 적용하고 싶을 때
- 업스트림 Iosevka·Pretendard 버전을 바꿔 시험할 때

## 1. 의존성

| 도구 | 버전 |
| --- | --- |
| Node.js | 16 이상 (Iosevka가 요구하는 최소값), **22 권장** |
| npm | Node.js에 포함 |
| Python | 3.11 이상 |
| [uv](https://docs.astral.sh/uv/) | 최신 |

Node.js는 Iosevka를 빌드할 때만 쓰입니다. 16 이상이면 Iosevka가 요구하는
조건은 만족하지만, 실제로 빌드를 검증하는 CI는 22에서 돌리므로 22 이상을
권합니다. Python 쪽 의존성은 uv가 알아서 가져오므로 따로 설치할 것이 없습니다.

## 2. 빌드

```sh
git clone https://github.com/xkho/presevka.git
cd presevka

make doctor
make build
```

`make doctor`는 도구가 갖춰졌는지, 버전 표기가 어긋나지 않았는지, 워크플로
설정이 유효한지 먼저 확인합니다. 여기서 멈추면 빌드를 시작하지 않습니다.

`make build`는 Iosevka를 내려받아 라틴 베이스를 만들고, Pretendard에서 한글을
준비해 합친 뒤, 힌팅과 검사를 거칩니다. 아홉 가지 weight의 Upright와 Italic,
**총 18개 TTF가 `dist/`에 생성**됩니다. 처음 빌드는 Iosevka를 통째로 컴파일하므로
오래 걸립니다.

```sh
IOSEVKA_JOBS=4 make build     # 병렬도 지정. 기본값 2
```

기본값이 2인 것은 CI의 메모리 사용을 예측 가능하게 하기 위해서입니다. 메모리가
넉넉한 로컬에서는 올리면 눈에 띄게 빨라집니다.

## 3. 배포용 묶음

```sh
make package
```

`dist/`에 `Presevka-<version>-ttf.zip`과 `Presevka-<version>-woff2.zip`이
만들어지고, 각 아카이브에는 라이선스 문서가 함께 들어갑니다. WOFF2 변환은 brotli
최고 압축을 쓰기 때문에 페이스당 수 분이 걸립니다. 기본적으로 코어 수만큼 병렬로
처리하며 `PRESEVKA_PACKAGE_JOBS`로 조정할 수 있습니다.

## 4. 라틴 글자꼴 바꾸기

> [!TIP]
> 대부분의 경우 빌드할 필요가 없습니다. stylistic set과 character variant는
> 배포되는 폰트에 이미 들어 있어 에디터 설정만으로 켤 수 있습니다.
> [README의 Iosevka Features](../README.md#iosevka-features)를 먼저 보세요.
> 사용하는 앱이 OpenType 피처를 지원하지 않을 때만 아래가 필요합니다.

### 미리 만들어진 프리셋

[`config/presets/`](../config/presets/)에 있는 프리셋을 환경변수로 고릅니다.
한글과 셀 너비는 그대로 유지됩니다.

```sh
PRESEVKA_PRESET=adwaita-mono make build
```

`adwaita-mono`는 GNOME Adwaita Mono가 고르는 글자꼴을 따릅니다. Adwaita Mono는
Inter를 향해 다듬은 Iosevka 빌드이고 Pretendard의 라틴도 Inter 계열이라, 한글과
설계 혈통을 공유합니다. 다만 Adwaita Mono의 600-unit 셀이 아니라 Presevka의
500-unit 셀을 그대로 쓰므로 비율까지 같지는 않습니다.

### 직접 고르기

[`config/private-build-plans.toml`](../config/private-build-plans.toml)을
편집합니다. 기본값은 stock Iosevka이며 어떤 character variant도 덮어쓰지
않습니다.

```toml
[buildPlans.PresevkaBase500.variants]
inherits = "ss14"          # JetBrains Mono 스타일

[buildPlans.PresevkaBase500.variants.design]
zero = "slashed"           # 개별 글자만 바꾸기
i = "serifed-asymmetric"
```

쓸 수 있는 이름은
[Iosevka custom-build 문서](https://github.com/be5invis/Iosevka/blob/v34.9.0/doc/custom-build.md)에
있습니다. `[weights]`, `[slopes]`, `[widths]` 섹션은 한글 맞춤과 직결되므로
그대로 두는 편이 좋습니다.

## 5. 힌팅

`PRESEVKA_HINT` 환경변수로 고릅니다. 기본값은 `full`이며 릴리스도 `full`로
빌드됩니다.

| 값 | 동작 | Regular 크기 |
| --- | --- | --- |
| `full` (기본) | 병합된 폰트 전체에 ttfautohint 적용. 한글도 힌팅됨 | 14.7 MB |
| `latin` | Iosevka 베이스에만 적용. 한글은 Pretendard 원본 렌더링 유지 | 11.8 MB |
| `gasp` | ttfautohint 없이 gasp 스무딩과 dropout control만 | 8.8 MB |
| `none` | 힌팅 없는 원본 윤곽 | 8.8 MB |

```sh
PRESEVKA_HINT=latin make build
make build-fast                # PRESEVKA_HINT=none 과 동일. 반복 빌드용
```

11–13px 같은 작은 크기에서는 `full`이 한글 가로획을 픽셀 그리드에 맞춰 눈에 띄게
또렷합니다. 한글을 Pretendard가 의도한 렌더링 그대로 두고 싶다면 `latin`을
쓰세요.

## 6. 업스트림 버전 바꾸기

```sh
IOSEVKA_REF=v34.9.0 PRETENDARD_REF=v1.3.9 make build
```

기본값은 [`scripts/build_iosevka.sh`](../scripts/build_iosevka.sh)와
[`scripts/build_pretendard.sh`](../scripts/build_pretendard.sh)에 고정되어
있습니다. 같은 커밋에서 언제 빌드하든 같은 결과가 나오도록 핀으로 묶어 둔
것이므로, 바꿔 빌드한 결과는 릴리스와 다를 수 있습니다.

## 7. 정리

```sh
make clean       # build/ 와 dist/ 를 비움. 내려받은 소스는 유지
make distclean   # .cache/ 와 .venv/ 까지 삭제
```
