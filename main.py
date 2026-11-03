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


def print_menu():
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


def play_quiz(quizzes):
    """저장된 퀴즈를 순서대로 출제하고, 맞힌 개수를 반환한다."""
    if not quizzes:  # 퀴즈가 없는 경우
        print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
        return None

    total = len(quizzes)
    correct = 0
    print(f"📝 퀴즈를 시작합니다! (총 {total}문제)")
    print()

    for number, quiz in enumerate(quizzes, start=1):
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
    return correct


def main():
    quizzes = get_default_quizzes()

    while True:
        print_menu()
        choice = input_number("선택: ", 1, 5)

        if choice == 1:
            play_quiz(quizzes)
        elif choice == 2:
            print("퀴즈 추가 기능은 준비 중입니다.")
        elif choice == 3:
            print("퀴즈 목록 기능은 준비 중입니다.")
        elif choice == 4:
            print("점수 확인 기능은 준비 중입니다.")
        elif choice == 5:
            print("프로그램을 종료합니다. 👋")
            break

        print()  # 메뉴 사이 빈 줄


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):  # Ctrl+C 또는 입력 스트림 종료
        print("\n\n⚠️ 입력이 중단되어 프로그램을 안전하게 종료합니다.")