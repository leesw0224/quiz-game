import json
from pathlib import Path

STATE_FILE = Path(__file__).with_name("state.json")  # 프로젝트 루트의 데이터 파일


class Quiz:
    """퀴즈 한 문제를 표현하는 클래스."""

    def __init__(self, question, choices, answer):
        self.question = question  # 문제 (str)
        self.choices = choices    # 선택지 4개 (list[str])
        self.answer = answer      # 정답 번호 1~4 (int)

    def display(self, number):
        """문제 번호와 함께 문제와 선택지를 출력한다."""
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 입력한 번호가 정답인지 확인한다."""
        return user_answer == self.answer

    def to_dict(self):
        """JSON으로 저장할 수 있도록 딕셔너리로 바꾼다."""
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data):
        """딕셔너리에서 Quiz 객체를 만든다. 형식이 잘못되면 ValueError를 일으킨다."""
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제가 비어 있습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개여야 합니다.")
        if not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("정답 번호는 1~4여야 합니다.")
        return cls(question, choices, answer)


def get_default_quizzes():
    """파이썬 기초 주제의 기본 퀴즈 목록을 Quiz 인스턴스로 만들어 반환한다."""
    return [
        Quiz("Python에서 정수(integer)를 나타내는 자료형은?",
             ["int", "str", "bool", "list"], 1),
        Quiz("print(type(\"3\"))를 실행하면 어떤 자료형이 출력될까?",
             ["int", "float", "str", "bool"], 3),
        Quiz("a = [10, 20, 30] 일 때 a[1]의 값은?",
             ["10", "20", "30", "오류 발생"], 2),
        Quiz("if 조건이 거짓일 때 다른 조건을 이어서 검사하는 키워드는?",
             ["else", "then", "elif", "case"], 3),
        Quiz("for i in range(3): 에서 i가 차례로 가지는 값은?",
             ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "1, 2"], 2),
        Quiz("{\"name\": \"Kim\"}처럼 키와 값을 짝지어 저장하는 자료형은?",
             ["list", "tuple", "set", "dict"], 4),
    ]


def input_number(prompt, min_value, max_value):
    """min_value~max_value 범위의 정수를 입력받을 때까지 반복한다."""
    while True:
        text = input(prompt).strip()  # 앞뒤 공백 제거

        if text == "":  # 빈 입력 (그냥 Enter)
            print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
            continue

        try:
            number = int(text)
        except ValueError:  # 숫자 변환 실패 (예: abc)
            print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        if number < min_value or number > max_value:  # 범위 밖 숫자 (예: 9)
            print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        return number


def input_text(prompt):
    """빈 칸이 아닌 글자를 입력받을 때까지 반복한다."""
    while True:
        text = input(prompt).strip()  # 앞뒤 공백 제거
        if text:
            return text
        print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")


class QuizGame:
    """퀴즈 게임 전체(퀴즈 목록, 최고 점수, 메뉴 흐름)를 관리하는 클래스."""

    def __init__(self):
        self.quizzes = []  # 퀴즈 목록 (Quiz 객체 리스트)
        self.best = None   # 최고 기록 (아직 없음)
        self.load_state()

    def load_state(self):
        """state.json에서 퀴즈와 최고 점수를 불러온다. 없거나 손상되면 기본 데이터를 쓴다."""
        if not STATE_FILE.exists():  # 첫 실행: 파일 없음
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            self.quizzes = get_default_quizzes()
            self.best = None
            return

        try:
            # utf-8-sig: 메모장 등에서 저장해 BOM이 붙은 UTF-8 파일도 읽을 수 있다
            with open(STATE_FILE, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best = None
            if data.get("best_score") is not None:
                best = {"score": int(data["best_score"]),
                        "correct": int(data["best_correct"]),
                        "total": int(data["best_total"])}
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다.")
            self.quizzes = get_default_quizzes()
            self.best = None
            self.save_state()  # 손상된 파일을 기본 데이터로 덮어써 복구
            return

        self.quizzes = quizzes
        self.best = best
        best_text = f"{best['score']}점" if best else "없음"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {best_text})")

    def save_state(self):
        """퀴즈와 최고 점수를 state.json에 UTF-8로 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best["score"] if self.best else None,
            "best_correct": self.best["correct"] if self.best else None,
            "best_total": self.best["total"] if self.best else None,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            print("⚠️ 데이터를 저장하지 못했습니다. (파일 쓰기 오류)")

    def show_menu(self):
        """메뉴 화면을 출력한다."""
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def play(self):
        """퀴즈를 순서대로 출제하고, 결과(점수·정답 수·문제 수)를 반환한다."""
        if not self.quizzes:  # 퀴즈가 없는 경우
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return None

        total = len(self.quizzes)
        correct = 0
        print(f"📝 퀴즈를 시작합니다! (총 {total}문제)")
        print()

        for number, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            quiz.display(number)
            user_answer = input_number("정답 입력: ", 1, len(quiz.choices))

            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
            print()

        score = round(correct / total * 100)  # 100점 만점 환산
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        print("=" * 40)
        return {"score": score, "correct": correct, "total": total}

    def update_best_score(self, result):
        """이번 결과가 최고 점수보다 높으면 최고 기록을 갱신한다."""
        if result is None:  # 퀴즈를 풀지 못한 경우 (퀴즈 없음)
            return

        if self.best is None or result["score"] > self.best["score"]:
            print("🎉 새로운 최고 점수입니다!")
            self.best = result
            self.save_state()

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 새 퀴즈를 추가한다."""
        print("📌 새로운 퀴즈를 추가합니다.")
        print()

        question = input_text("문제를 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choices.append(input_text(f"선택지 {i}: "))
        answer = input_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print()
        print("✅ 퀴즈가 추가되었습니다!")

    def show_quiz_list(self):
        """등록된 퀴즈의 문제 목록을 출력한다."""
        if not self.quizzes:  # 퀴즈가 없는 경우
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print()
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def show_best_score(self):
        """최고 점수를 출력한다."""
        if self.best is None:  # 아직 퀴즈를 풀지 않은 경우
            print("📭 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어 주세요.")
            return

        print(f"🏆 최고 점수: {self.best['score']}점 "
              f"({self.best['total']}문제 중 {self.best['correct']}문제 정답)")

    def run(self):
        """메뉴를 반복해서 보여주고, 선택한 기능을 실행한다."""
        while True:
            self.show_menu()
            choice = input_number("선택: ", 1, 5)

            if choice == 1:
                result = self.play()
                self.update_best_score(result)
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                self.save_state()
                print("프로그램을 종료합니다. 👋")
                break

            print()  # 메뉴 사이 빈 줄


if __name__ == "__main__":
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):  # Ctrl+C 또는 입력 스트림 종료
        print("\n\n⚠️ 입력이 중단되었습니다. 데이터를 저장하고 안전하게 종료합니다.")
        game.save_state()