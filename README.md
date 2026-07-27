# 카드 가이드

신용카드 결제 가이드 PWA — 상황별 최적 카드를 아이폰 홈 화면에서 바로 확인.

- **앱**: `docs/` (GitHub Pages로 배포)
- **데이터**: [docs/data.json](docs/data.json) — 단일 소스
  - `cards`: 카드별 통일 스키마 — 기본 5슬롯(연회비/전월실적/한도/제외/유지근거) + 한도그룹(그룹·통합한도·영역) + 기타
  - `memberships`: KT·네이버 등 카드 외 혜택
  - `situations`: 상황별 추천 — `ref: "카드id/영역id"`로 카드 데이터와 연동(조건·한도 자동 표시)
- **아이콘 재생성**: `python3 make_icon.py`

## 수정 방법

data.json을 고치고 push하면 1~2분 내 반영. 새 카드 추가는 카드사 혜택 페이지를 Claude에게 주면 스키마로 분석해 추가.
