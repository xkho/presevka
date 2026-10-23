# Iosevka features

Presevka의 라틴 글자는 [Iosevka](https://github.com/be5invis/Iosevka)가 그린 것을 그대로 씁니다. 소문자 높이만 조금 올렸을 뿐 글자꼴은 손대지 않았습니다. Iosevka는 글자 하나하나에 대안 모양을 마련해 두고 그것을 OpenType 피처로 골라 쓰게 만든 고정폭 글꼴입니다. `0`에 점을 넣을지 사선을 그을지, `l`에 꼬리를 달지, `g`를 한 층으로 그릴지를 쓰는 사람이 정합니다.
그 선택지가 **stylistic set 19종과 character variant 99종**으로 Presevka에 그대로 들어 있습니다. 폰트를 다시 받거나 빌드할 필요 없이 에디터 설정만으로 켜집니다.

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

### Adwaita Mono 스타일

GNOME의 Adwaita Mono가 고르는 글자꼴을 피처로 옮긴 것입니다. Adwaita Mono는
Inter를 향해 다듬은 Iosevka 빌드이고 Pretendard의 라틴도 Inter 계열이라, 한글과
설계 혈통을 공유합니다. 아래 한 줄이면 빌드 없이 같은 글자꼴이 됩니다.

```jsonc
"editor.fontLigatures": "'VAAB' 4, 'VAAC' 4, 'VLAC' 2, 'VLAD' 2, 'VSAB' 7, 'VSAH' 1, 'VSAI' 1, 'VSAJ' 2, 'VSAL' 7, 'VSAO' 3, 'VSAS' 5, 'cv02' 1, 'cv04' 1, 'cv06' 1, 'cv08' 2, 'cv09' 1, 'cv10' 6, 'cv14' 4, 'cv17' 20, 'cv19' 3, 'cv23' 4, 'cv26' 4, 'cv32' 7, 'cv41' 11, 'cv44' 6, 'cv45' 6, 'cv47' 10, 'cv52' 9, 'cv54' 7, 'cv57' 7, 'cv59' 4, 'cv62' 16, 'cv70' 1, 'cv76' 3, 'cv82' 1, 'cv84' 9"
```

[`config/presets/adwaita-mono.toml`](../config/presets/adwaita-mono.toml)이 고르는
36개 항목을 그대로 옮긴 값입니다. 셀 너비와 한글은 달라지지
않습니다.

> [!NOTE]
> OpenType 피처 지원은 앱마다 다릅니다. VS Code, kitty, WezTerm, Ghostty에서
> 동작하며 일부 터미널은 지원하지 않습니다. 그런 앱을 쓴다면 원하는 글자꼴이
> 기본값으로 박힌 TTF를 직접 만들 수 있습니다.
> [소스에서 빌드하는 방법](./build_from_source_instruction.md)을 참고하세요.
