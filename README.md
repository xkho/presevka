# Presevka

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/presevka-banner-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="./assets/presevka-banner-light.png">
    <img alt="Presevka — 프리텐다드 × Iosevka" src="./assets/presevka-banner-light.png" width="100%">
  </picture>
</p>

<p align="center">
<span style="font-style: italic;">
  Iosevka에 Pretendard의 한글을 결합한 고정폭 글꼴<br>
</span>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/presevka-specimen-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/presevka-specimen-light.svg">
    <img alt="Presevka 굵기별 견본" src="./assets/presevka-specimen-light.svg" width="100%">
  </picture>
</p>

---

> [!NOTE]
> [Presevka](https://github.com/xkho/presevka)는 Iosevka 또는 Pretendard의 공식 배포판이 아니며,
> [Iosevka](https://github.com/be5invis/Iosevka)를 코드와 라틴 문자의 기반으로,
> [Pretendard](https://github.com/orioncactus/pretendard)를 한글 글리프의 기반으로 삼는
> 독립적인 폰트입니다.


## 다운로드

[최신 버전 다운로드](https://github.com/xkho/presevka/releases/latest)

## 글꼴 변형

Iosevka의 stylistic set 19종과 character variant 99종이 그대로 들어 있습니다.
폰트를 다시 받지 않고 에디터 설정으로 켭니다.

```jsonc
"editor.fontLigatures": "'ss14'"   // JetBrains Mono 스타일
```

미리보기는 [Iosevka의 stylistic set 문서](https://github.com/be5invis/Iosevka/blob/v34.9.0/doc/stylistic-sets.md)에
있습니다. Presevka는 Iosevka의 라틴 글자를 그대로 쓰므로 그 그림이 곧 이 글꼴의
모습입니다.

<details>
<summary>stylistic set 목록</summary>

`ss01` Andale Mono · `ss02` Anonymous Pro · `ss03` Consolas · `ss04` Menlo ·
`ss05` Fira Mono · `ss06` Liberation Mono · `ss07` Monaco · `ss08` Pragmata
Pro · `ss09` Source Code Pro · `ss10` Envy Code R · `ss11` X Window · `ss12`
Ubuntu Mono · `ss13` Lucida · `ss14` JetBrains Mono · `ss15` IBM Plex Mono ·
`ss16` PT Mono · `ss17` Recursive Mono · `ss18` Input Mono · `ss20` Curly

</details>

<details>
<summary>GNOME Adwaita Mono 스타일</summary>

`config/presets/adwaita-mono.toml`이 고르는 글자꼴을 OpenType 피처로 옮긴
것입니다. 직접 빌드하지 않아도 같은 모습이 됩니다.

```jsonc
"editor.fontLigatures": "'VAAB' 4, 'VAAC' 4, 'VLAC' 2, 'VLAD' 2, 'VSAB' 7, 'VSAH' 1, 'VSAI' 1, 'VSAJ' 2, 'VSAL' 7, 'VSAO' 3, 'VSAS' 5, 'cv02' 1, 'cv04' 1, 'cv06' 1, 'cv08' 2, 'cv09' 1, 'cv10' 6, 'cv14' 4, 'cv17' 20, 'cv19' 3, 'cv23' 4, 'cv26' 4, 'cv32' 7, 'cv41' 11, 'cv44' 6, 'cv45' 6, 'cv47' 10, 'cv52' 9, 'cv54' 7, 'cv57' 7, 'cv59' 4, 'cv62' 16, 'cv70' 1, 'cv76' 3, 'cv82' 1, 'cv84' 9"
```

</details>

> [!NOTE]
> OpenType 피처 지원은 앱마다 다릅니다. VS Code, kitty, WezTerm, Ghostty에서
> 동작하며, 일부 터미널은 지원하지 않습니다. 그런 경우에는
> `PRESEVKA_PRESET`으로 직접 빌드하세요.

## 소스에서 빌드

### 의존성

- Node.js 18 이상과 npm
- Python 3.11 이상
- [uv](https://docs.astral.sh/uv/)

### 빌드

```sh
git clone https://github.com/xkho/presevka.git
cd presevka

make doctor
make build
```

아홉 가지 weight의 Upright와 Italic, 총 18개 TTF가 `dist/`에 생성됩니다.
`make package`를 실행하면 `Presevka-<version>-ttf.zip`과 `Presevka-<version>-woff2.zip`이 만들어집니다.

라틴 글자꼴을 바꾸는 프리셋이 [`config/presets/`](./config/presets/)에 있습니다.
예를 들어 GNOME Adwaita Mono의 글자꼴 선택을 따르려면 다음과 같이 빌드합니다.
한글과 셀 너비는 그대로입니다.

```sh
PRESEVKA_PRESET=adwaita-mono make build
```

## 라이선스

- 완성 폰트와 폰트 수정물: [SIL Open Font License 1.1](./LICENSE)
- Presevka의 Python/shell 빌더: [MIT](./LICENSE-CODE)
- 원본 저작권·Reserved Font Name: [OFL.txt](./OFL.txt)
- 원본 출처: [THIRD_PARTY.md](./THIRD_PARTY.md)
- 변경 이력: [FONTLOG.md](./FONTLOG.md)

## 크레딧

- [Iosevka](https://github.com/be5invis/Iosevka) — Renzhi Li / The Iosevka Project Authors
- [Pretendard](https://github.com/orioncactus/pretendard) — Kil Hyung-jin and upstream authors
