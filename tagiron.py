import random

# タイルのセットアップ（赤と青の0〜9、黄色の5が2枚）
colors = ["red", "blue"]
numbers = list(range(0, 10))
tiles = [(color, number) for color in colors for number in numbers if number != 5] + [("yellow", 5), ("yellow", 5)]

# プレイヤーとコンピュータの手札を生成（重複なし、昇順に並べる）
def generate_hands():
    all_tiles = tiles[:]  # タイルをコピー
    player_hand = random.sample(all_tiles, 5)  # プレイヤーの手札をランダムに選ぶ
    for card in player_hand:
        all_tiles.remove(card)
    computer_hand = random.sample(all_tiles, 5)  # 残りのタイルからコンピュータの手札を選ぶ

    # 昇順に並べ替え。同じ数字なら赤を左にする
    player_hand.sort(key=lambda x: (x[1], x[0] != "red"))
    computer_hand.sort(key=lambda x: (x[1], x[0] != "red"))

    return player_hand, computer_hand

# 質問リスト (全体の質問)
all_questions = [
    # 数の合計や枚数に関する質問
    "赤の数の合計数は？",
    "青の数の合計数は？",
    "赤の数字タイルは何枚ある？",
    "青の数字タイルは何枚ある？",
    "タイルすべての合計数は？",
    
    # 最大・最小に関する質問
    "数字タイルの最大の数から最小の数を引いた数は？",
    "大きいほうから3枚の合計数は？",
    "小さいほうから3枚の合計数は？",
    "中央の3枚の合計数は？",
    
    # 同じ数字に関する質問
    "同じ数字タイルのペアは何組ある？",
    "連番になっているタイルはどこ？",
    "連続して隣り合っている同じ色はどこ？",
    
    # 特定の数字に関する質問
    "5はどこ？",
    "1または2はどこ？",
    "3または4はどこ？",
    "6または7はどこ？",
    "8または9はどこ？",
    "0はどこ？",
    
    # 偶数・奇数に関する質問
    "偶数は何枚ある？",
    "奇数は何枚ある？",
    
    # 中央に関する質問
    "中央の数字タイルは5以上？4以下？"
]



# 初期にランダムで6つの質問をリスト1からリスト2に移動
def initialize_questions():
    current_questions = random.sample(all_questions, 6)
    for question in current_questions:
        all_questions.remove(question)
    return current_questions

# プレイヤーが質問を選び、相手の手札に対して応答する関数
def answer_question(question, opponent_hand, choice=None):
    if question == "赤の数の合計数は？":
        red_sum = sum(num for color, num in opponent_hand if color == "red")
        return f"赤の合計数は {red_sum} です。"
    
    elif question == "青の数の合計数は？":
        blue_sum = sum(num for color, num in opponent_hand if color == "blue")
        return f"青の合計数は {blue_sum} です。"

    elif question == "赤の数字タイルは何枚ある？":
        red_count = sum(1 for color, _ in opponent_hand if color == "red")
        return f"赤の数字タイルは {red_count} 枚あります。"

    elif question == "青の数字タイルは何枚ある？":
        blue_count = sum(1 for color, _ in opponent_hand if color == "blue")
        return f"青の数字タイルは {blue_count} 枚あります。"

    elif question == "タイルすべての合計数は？":
        total_sum = sum(num for _, num in opponent_hand)
        return f"タイルすべての合計数は {total_sum} です。"
    
    elif question == "数字タイルの最大の数から最小の数を引いた数は？":
        max_num = max(num for _, num in opponent_hand)
        min_num = min(num for _, num in opponent_hand)
        return f"最大の数から最小の数を引いた数は {max_num - min_num} です。"
    
    elif question == "大きいほうから3枚の合計数は？":
        top_3_sum = sum(sorted([num for _, num in opponent_hand], reverse=True)[:3])
        return f"大きいほうから3枚の合計数は {top_3_sum} です。"
    
    elif question == "小さいほうから3枚の合計数は？":
        bottom_3_sum = sum(sorted([num for _, num in opponent_hand])[:3])
        return f"小さいほうから3枚の合計数は {bottom_3_sum} です。"
    
    elif question == "中央の3枚の合計数は？":
        middle_3_sum = sum(num for _, num in opponent_hand[1:4])
        return f"中央の3枚の合計数は {middle_3_sum} です。"

    elif question == "同じ数字タイルのペアは何組ある？":
        counts = {}
        for _, num in opponent_hand:
            counts[num] = counts.get(num, 0) + 1
        pairs = sum(1 for count in counts.values() if count == 2)
        return f"同じ数字タイルのペアは {pairs} 組です。"

    elif question == "連番になっているタイルはどこ？":
        sorted_hand = sorted(opponent_hand, key=lambda x: x[1])
        consecutive_sets = []
        i = 0
        while i < len(sorted_hand) - 1:
            if sorted_hand[i][1] + 1 == sorted_hand[i + 1][1]:
                start = i + 1  # 1-based index
                end = i + 2
                while end < len(sorted_hand) and sorted_hand[end - 1][1] + 1 == sorted_hand[end][1]:
                    end += 1
                consecutive_sets.append((start, end))  # 保存: 開始と終了の範囲
                i = end - 1  # 連続が終わった位置に移動
            i += 1
        if consecutive_sets:
            result = "かつ".join([f"左から{start},{end}番目" for start, end in consecutive_sets])
            return f"連番は {result} です。"
        return "連番はありません。"

    elif question == "5はどこ？":
        positions = [i + 1 for i, (color, num) in enumerate(opponent_hand) if num == 5]
        if positions:
            return f"5は左から{', '.join(map(str, positions))}番目にあります。"
        return "5はありません。"

    elif question == "0はどこ？":
        positions = [i + 1 for i, (_, num) in enumerate(opponent_hand) if num == 0]
        if positions:
            return f"0は左から{', '.join(map(str, positions))}番目にあります。"
        return "0はありません。"

    elif question == "1または2はどこ？":
        while True:
            if choice is None:
                choice = input("1または2のどちらを選びますか？ (1/2): ").strip()
            if choice in ["1", "2"]:
                choice = int(choice)
                positions = [i + 1 for i, (_, num) in enumerate(opponent_hand) if num == choice]
                if positions:
                    return f"{choice}は左から{', '.join(map(str, positions))}番目にあります。"
                return f"{choice}はありません。"
            else:
                print("無効な選択です。もう一度選んでください。")
                choice = None  # 無効な選択をしたのでchoiceをリセットして再入力を促す

    elif question == "3または4はどこ？":
        while True:
            if choice is None:
                choice = input("3または4のどちらを選びますか？ (3/4): ").strip()
            if choice in ["3", "4"]:
                choice = int(choice)
                positions = [i + 1 for i, (_, num) in enumerate(opponent_hand) if num == choice]
                if positions:
                    return f"{choice}は左から{', '.join(map(str, positions))}番目にあります。"
                return f"{choice}はありません。"
            else:
                print("無効な選択です。もう一度選んでください。")
                choice = None  # 無効な選択をしたのでchoiceをリセットして再入力を促す

    elif question == "6または7はどこ？":
        while True:
            if choice is None:
                choice = input("6または7のどちらを選びますか？ (6/7): ").strip()
            if choice in ["6", "7"]:
                choice = int(choice)
                positions = [i + 1 for i, (_, num) in enumerate(opponent_hand) if num == choice]
                if positions:
                    return f"{choice}は左から{', '.join(map(str, positions))}番目にあります。"
                return f"{choice}はありません。"
            else:
                print("無効な選択です。もう一度選んでください。")
                choice = None  # 無効な選択をしたのでchoiceをリセットして再入力を促す

    elif question == "8または9はどこ？":
        while True:
            if choice is None:
                choice = input("8または9のどちらを選びますか？ (8/9): ").strip()
            if choice in ["8", "9"]:
                choice = int(choice)
                positions = [i + 1 for i, (_, num) in enumerate(opponent_hand) if num == choice]
                if positions:
                    return f"{choice}は左から{', '.join(map(str, positions))}番目にあります。"
                return f"{choice}はありません。"
            else:
                print("無効な選択です。もう一度選んでください。")
                choice = None  # 無効な選択をしたのでchoiceをリセットして再入力を促す

    elif question == "偶数は何枚ある？":
        even_count = sum(1 for _, num in opponent_hand if num % 2 == 0)
        return f"偶数は {even_count} 枚あります。"

    elif question == "奇数は何枚ある？":
        odd_count = sum(1 for _, num in opponent_hand if num % 2 != 0)
        return f"奇数は {odd_count} 枚あります。"
    
    elif question == "連続して隣り合っている同じ色はどこ？":
        consecutive_positions = []
        i = 0
        while i < len(opponent_hand) - 1:
            if opponent_hand[i][0] == opponent_hand[i + 1][0]:
                start = i + 1  # 1-based index
                end = i + 2
                while end < len(opponent_hand) and opponent_hand[end - 1][0] == opponent_hand[end][0]:
                    end += 1
                consecutive_positions.append((start, end))  # 保存: 開始と終了の範囲
                i = end - 1  # 連続が終わった位置に移動
            i += 1
        if consecutive_positions:
            result = "かつ".join([f"左から{start},{end}番目" for start, end in consecutive_positions])
            return f"同じ色が隣り合っているのは {result} です。"
        return "隣り合っている同じ色はありません。"

    elif question == "中央の数字タイルは5以上？4以下？":
        middle_tile = opponent_hand[2][1]
        if middle_tile >= 5:
            return "中央の数字タイルは5以上です。"
        else:
            return "中央の数字タイルは4以下です。"


    # 色を変換する関数
def convert_color(short_color):
    if short_color == 'r':
        return 'red'
    elif short_color == 'b':
        return 'blue'
    elif short_color == 'y':
        return 'yellow'
    else:
        return None

# プレイヤーが手札を推測する関数
def guess_hand():
    guess = []
    print("\n相手の手札を推測してください。")
    for i in range(5):
        while True:  # 有効な色の入力を受け取るまでループ
            short_color = input(f"{i + 1}番目のタイルの色は？ (r/b/y): ").strip().lower()
            color = convert_color(short_color)  # 色を変換する関数を呼び出す
            if color is not None:
                break  # 有効な色が入力された場合はループを抜ける
            print("無効な色です。もう一度入力してください。")

        while True:  # 有効な数字の入力を受け取るまでループ
            try:
                number = int(input(f"{i + 1}番目のタイルの数字は？: "))
                break  # 有効な数字が入力された場合はループを抜ける
            except ValueError:
                print("無効な入力です。数字を入力してください。")

        guess.append((color, number))
    return guess
    # 1人用ゲームのメインループ
def play_single_player():
    print("1人用推理ゲームを開始します！\n")
    player_hand, computer_hand = generate_hands()

    # プレイヤーの手札を表示
    print(f"あなたの手札: {player_hand}\n")

    current_questions = initialize_questions()

    while True:
        if current_questions:
            # 質問を表示
            print("以下の質問から選んで、コンピュータの手札を推理してください。")
            for i, question in enumerate(current_questions):
                print(f"{i + 1}. {question}")

            try:
                choice = int(input("\n質問を選んでください（番号で入力）：")) - 1
                if 0 <= choice < len(current_questions):
                    response = answer_question(current_questions[choice], computer_hand)
                    print(f"質問: {current_questions[choice]}")
                    print(f"答え: {response}\n")

                    # 質問をリストから削除し、新しい質問を追加
                    used_question = current_questions.pop(choice)
                    if all_questions:  # まだ質問が残っていれば補充
                        new_question = random.choice(all_questions)
                        all_questions.remove(new_question)  # リスト1から削除
                        current_questions.append(new_question)

                    # 次に行動するかどうか選ぶ
                    action = input("質問を続けますか？それとも推測しますか？あきらめますか？ (q/a/g): ").strip().lower()
                    if action == 'a':
                        guess = guess_hand()
                        if check_answer(guess, computer_hand):
                            print("あなたの勝利です！")
                            break
                        else:
                            print("不正解です。ゲームを続行します。\n")
                    elif action == 'g':
                        print("\nあなたはあきらめました。コンピュータの手札は以下の通りです：")
                        print(f"コンピュータの手札: {computer_hand}")
                        break
                else:
                    print("無効な番号です。もう一度選んでください。\n")
            except ValueError:
                print("無効な入力です。数字で質問を選んでください。\n")
        else:
            # 質問がなくなった場合は推測またはあきらめる
            action = input("質問はできません。回答しますか？あきらめますか？ (a/g): ").strip().lower()
            if action == "a":
                guess = guess_hand()
                if check_answer(guess, computer_hand):
                    print("あなたの勝利です！")
                    break
                else:
                    print("不正解です。ゲームを続行します。\n")
            elif action == "g":
                print("\nあなたはあきらめました。コンピュータの手札は以下の通りです：")
                print(f"コンピュータの手札: {computer_hand}")
                break

# 正解かどうかを判定する関数
def check_answer(guess, opponent_hand):
    return guess == opponent_hand  # 推測した手札が相手の手札と一致するかどうかを確認

# 2人用ゲームのメインループ
def play_two_player():
    print("2人用の推理ゲームを開始します！\n")

    current_player = 1  # プレイヤー1からスタート

    # 両方のプレイヤーが持つ手札を生成
    player1_hand, player2_hand = generate_hands()
    current_questions = initialize_questions()

    while True:
        print(f"プレイヤー{current_player}のターンです。\n")
        
        # プレイヤーがアクションを選択
        action = input("質問しますか？回答しますか？それともあきらめますか？ (q/a/g): ").strip().lower()

        if action == "q":
            # 質問のリストを表示
            print("以下の質問から選んで、相手の手札を推理してください。")
            for i, question in enumerate(current_questions):
                print(f"{i + 1}. {question}")

            choice = int(input("\n質問を選んでください（番号で入力）：")) - 1
            if 0 <= choice < len(current_questions):
                # プレイヤー1のターンならプレイヤー2の手札、プレイヤー2のターンならプレイヤー1の手札を使う
                if current_player == 1:
                    response = answer_question(current_questions[choice], player2_hand)
                else:
                    response = answer_question(current_questions[choice], player1_hand)
                
                print(f"質問: {current_questions[choice]}")
                print(f"答え: {response}\n")
                # 質問をリストから削除し、新しい質問を追加
                used_question = current_questions.pop(choice)
                if all_questions:  # リストにまだ質問が残っているなら補充
                    new_question = random.choice(all_questions)
                    all_questions.remove(new_question)
                    current_questions.append(new_question)

        elif action == "a":
            # 手札の推測を行う
            guess = guess_hand()
            if current_player == 1:
                if check_answer(guess, player2_hand):
                    print("プレイヤー1が勝利しました！")
                    break
            else:
                if check_answer(guess, player1_hand):
                    print("プレイヤー2が勝利しました！")
                    break
        elif action == "g":
            print(f"\nプレイヤー{current_player}があきらめました。両方の手札を表示してゲームを終了します。")
            print(f"プレイヤー1の手札: {player1_hand}")
            print(f"プレイヤー2の手札: {player2_hand}")
            break

        # プレイヤーのターンを切り替え
        current_player = 2 if current_player == 1 else 1

        
# メイン関数
def main():
    print("推理ゲームを始めます！")
    mode = input("1人用(1) か 2人用(2) を選んでください: ")

    if mode == "1":
        play_single_player()
    elif mode == "2":
        play_two_player()
    else:
        print("無効な選択です。1か2を選んでください。")

# ゲームの実行
main()
