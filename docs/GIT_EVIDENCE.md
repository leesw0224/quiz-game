# Git 작업 기록 (GIT_EVIDENCE)

- 저장소: https://github.com/leesw0224/quiz-game
- 커밋 목록: https://github.com/leesw0224/quiz-game/commits/main
- 아래 출력은 Git 명령의 실제 출력이며, 같은 내용이 `docs/` 폴더의 `.txt` 파일에 그대로 저장되어 있습니다.
  (`cmd /c "git ... > docs\파일이름.txt"` 방식으로 출력 그대로 저장)

| 증빙 | 원본 파일 | 확인 내용 |
|---|---|---|
| 커밋 그래프 | `docs/git_log_graph.txt` | 기능 단위 커밋, 브랜치 생성·병합 |
| 커밋 수 | `docs/git_commit_count.txt` | main 브랜치 커밋 16개 (요구: 10개 이상) |
| 원래 작업 폴더 기록 | `docs/git_reflog_quiz-game.txt` | clone, pull |
| 복제 폴더 기록 | `docs/git_reflog_quiz-game-clone.txt` | clone, commit (이후 push) |

## 1. 커밋 그래프 — `git log --oneline --graph --all`

```
* 3aa0233 Docs: clone 폴더에서 README 실습 기록 추가
* 3131f1e Docs: 두 번째 작업 폴더 pull 실습 준비
* e115454 Docs: clone 및 pull 실습 내용 추가
* 6a4567a Docs: README 작성 (개요, 실행 방법, 기능, 파일 구조, state.json 설명)
* 0e97407 Fix: .gitignore 줄 앞 공백 제거로 무시 규칙 적용
* a3749d8 Feat: state.json 저장/불러오기 및 손상 파일 복구 구현
* 9f529f2 Refactor: QuizGame 클래스로 게임 기능 정리
* 03bca10 Feat: 최고 점수 기록 및 확인 기능 구현
* 351c609 Feat: 퀴즈 목록 기능 구현 (목록 출력, 빈 목록 처리)
* e8afc13 Feat: 퀴즈 추가 기능 구현 (문제·선택지·정답 입력 및 검증)
*   8b2733e Merge: 퀴즈 풀기 기능 병합 (feature/play-quiz)
|\  
| * 7871165 Feat: 퀴즈 풀기 기능 구현 (출제, 정답 확인, 결과 표시)
|/  
* 2cabf43 Feat: 기본 퀴즈 데이터 작성 (파이썬 기초 6문제)
* 2718d86 Feat: Quiz 클래스 구현 (문제 출력, 정답 확인)
* af71a8c Feat: 메뉴 출력 및 입력 검증 기능 구현
* 202d9db Docs: 프로젝트 초기 설정 (.gitignore, README 뼈대 추가)
```

**읽는 법**

- 커밋마다 `Feat`/`Fix`/`Refactor`/`Docs`/`Merge` 타입과 변경 요약이 있어 기능 단위로 나뉘어 있습니다.
- `|\` 에서 갈라진 선이 `feature/play-quiz` 브랜치입니다. 이 브랜치에서 퀴즈 풀기 기능(`7871165`)을 만든 뒤,
  main으로 돌아와(`git checkout main`) `git merge --no-ff feature/play-quiz`로 병합해 병합 커밋 `8b2733e`가 생겼습니다.
- `|/` 는 브랜치가 다시 main으로 합쳐진 지점입니다.

## 2. 커밋 수 — `git rev-list --count main`

```
16
```

## 3. clone / pull 실습

같은 GitHub 저장소를 두 폴더에 clone한 뒤, 한 폴더에서 push한 변경을 다른 폴더에서 pull로 받아왔습니다.

**순서**

1. `git clone https://github.com/leesw0224/quiz-game.git` → 원래 작업 폴더 `quiz-game`
2. `git clone https://github.com/leesw0224/quiz-game.git quiz-game-clone` → 실습용 복제 폴더
3. 복제 폴더에서 README에 한 줄 추가 → `git add README.md` → `git commit` → `git push` (`3131f1e..3aa0233  main -> main`)
4. 원래 폴더 `quiz-game`에서 `git pull` → `Fast-forward`로 `3aa0233` 반영
5. 원래 폴더의 README 마지막 줄에 복제 폴더에서 추가한 문장이 나타난 것을 확인

**복제 폴더 `quiz-game-clone`의 `git reflog`** — clone 후 commit

```
3aa0233 HEAD@{0}: commit: Docs: clone 폴더에서 README 실습 기록 추가
3131f1e HEAD@{1}: clone: from https://github.com/leesw0224/quiz-game.git
```

**원래 폴더 `quiz-game`의 `git reflog`** — clone 후 pull

```
3aa0233 HEAD@{0}: pull: Fast-forward
3131f1e HEAD@{1}: clone: from https://github.com/leesw0224/quiz-game.git
```

두 폴더 모두 `3131f1e`에서 시작했고, 복제 폴더에서 만든 커밋 `3aa0233`이 원래 폴더에 `pull: Fast-forward`로 들어온 것을 확인할 수 있습니다.

## 4. 사용한 Git 명령

| 명령 | 이 저장소에서 확인할 수 있는 곳 |
|---|---|
| `add`, `commit` | 1번 그래프의 커밋 16개 |
| `checkout`, `merge` | 1번 그래프의 `feature/play-quiz` 브랜치와 병합 커밋 `8b2733e` |
| `push` | GitHub 원격 저장소에 커밋 16개가 올라가 있음, 3번의 `3131f1e..3aa0233  main -> main` |
| `clone` | 3번 두 폴더의 reflog `clone: from ...` |
| `pull` | 3번 원래 폴더의 reflog `pull: Fast-forward` |