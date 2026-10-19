# Presevka

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/presevka-banner-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="./assets/presevka-banner-light.png">
    <img alt="Presevka — 프리텐다드 × Iosevka" src="./assets/presevka-banner-light.png" width="100%">
  </picture>
</p>

---

<p align="center">
<span style="font-style: italic;">
  Iosevka에 Pretendard의 한글을 결합한 고정폭 글꼴<br>
</span>
</p>


[Presevka](https://github.com/xkho/presevka)는 Iosevka 또는 Pretendard의 공식 배포판이 아니며, [Iosevka](https://github.com/be5invis/Iosevka)를 코드와 라틴 문자의 기반으로, [Pretendard](https://github.com/orioncactus/pretendard)를 한글 글리프의 기반으로 삼는 독립적인 폰트입니다. 한글 글리프가 포함된 Iosevka 스타일 폰트를 찾는다면,
[Sarasa Gothic](https://github.com/be5invis/Sarasa-Gothic)도 찾아보세요!

## 다운로드

1. [Github release 에서 다운받기](https://github.com/xkho/presevka/releases/latest)
2. [Source 에서 빌드하는 방법 보기](./docs/build_from_source_instruction.md)

## 특징

- **한글 한 칸이 라틴 두 칸에 정확히 맞물립니다.** 표와 주석 정렬이 한글이
  섞여도 무너지지 않습니다.
- **현대 한글 음절 11,172자 전체**와 호환 자모 53자를 담았습니다.
- **9 weight × Upright/Italic, 18개 페이스.** Italic에서도 한글은 기울이지 않은
  Pretendard 윤곽을 유지합니다.
- **힌팅이 적용되어 있습니다.** 11–13px처럼 작은 크기에서 한글 가로획이 픽셀
  그리드에 맞아 또렷합니다.
- Pretendard 한글 윤곽은 원본 비율을 유지한 채 가로로 2%만 확대하고, 나머지
  폭은 좌우 여백으로 둡니다.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/presevka-specimen-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/presevka-specimen-light.svg">
    <img alt="Presevka 굵기별 견본" src="./assets/presevka-specimen-light.svg" width="100%">
  </picture>
</p>



## Iosevka Features

Presevka의 라틴 글자는 [Iosevka](https://github.com/be5invis/Iosevka)를 손대지
않고 그대로 씁니다. Iosevka는 글자 하나하나에 대안 모양을 마련해 두고 그것을
OpenType 피처로 골라 쓰게 만든 고정폭 글꼴입니다. `0`에 점을 넣을지 사선을
그을지, `l`에 꼬리를 달지, `g`를 한 층으로 그릴지를 쓰는 사람이 정합니다.

그 선택지가 **stylistic set 19종과 character variant 99종**으로 Presevka에
그대로 들어 있습니다. 폰트를 다시 받거나 빌드할 필요 없이 에디터 설정만으로
켜집니다.

### Stylistic sets

한 번에 글꼴 전체의 인상을 바꾸는 묶음입니다. 널리 쓰이는 고정폭 글꼴의 분위기를
흉내 내도록 미리 조합해 둔 것으로, `ss14`는 JetBrains Mono, `ss05`는 Fira Mono,
`ss09`는 Source Code Pro 스타일입니다.

```jsonc
"editor.fontLigatures": "'ss14'"
```

아래 문서의 미리보기가 곧 이 글꼴의 모습입니다. Presevka가 Iosevka의 라틴을
그대로 쓰기 때문입니다.

<table>
  <tr>
    <td>
      <h3>
        <a href="https://github.com/be5invis/Iosevka/blob/v34.9.0/doc/stylistic-sets.md"> 
          List of stylistic sets of Iosevka
        </a>
      </h3>
    </td>

  </tr>
</table>

### Character variants

글자 하나씩 따로 고르는 방식입니다. stylistic set이 통째로 바꾸는 것과 달리 `0`만
점 있는 모양으로 바꾸거나 `i`에만 세리프를 더하는 식으로 쓸 수 있고, 여러 개를
함께 적으면 그대로 겹쳐 적용됩니다.

```jsonc
"editor.fontLigatures": "'cv10' 6, 'cv17' 20"
```

아래 문서에서 글자별 선택지와 그 코드를 찾을 수 있습니다.

<table>
  <tr>
    <td>
      <h3>
      <a href="https://github.com/be5invis/Iosevka/blob/v34.9.0/doc/character-variants.md">
        List of character variants of Iosevka
      </a>
      </h3>
    </td>
  </tr>
</table>

> [!NOTE]
> OpenType 피처 지원은 앱마다 다릅니다. VS Code, kitty, WezTerm, Ghostty에서
> 동작하며 일부 터미널은 지원하지 않습니다. 그런 앱을 쓴다면 원하는 글자꼴이
> 기본값으로 박힌 TTF를 직접 만들 수 있습니다.
> [소스에서 빌드하는 방법](./docs/build_from_source_instruction.md)을 참고하세요.

## 라이선스

- 완성 폰트와 폰트 수정물: [SIL Open Font License 1.1](./LICENSE)
- Presevka의 Python/shell 빌더: [MIT](./LICENSE-CODE)
- 원본 저작권·Reserved Font Name: [OFL.txt](./OFL.txt)
- 원본 출처: [THIRD_PARTY.md](./THIRD_PARTY.md)
- 변경 이력: [FONTLOG.md](./FONTLOG.md)

## 크레딧

- [Iosevka](https://github.com/be5invis/Iosevka) — Renzhi Li / The Iosevka Project Authors
- [Pretendard](https://github.com/orioncactus/pretendard) — Kil Hyung-jin and upstream authors
