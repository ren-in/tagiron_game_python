import pygame
import pygame.freetype
import random


# Pygameの初期化
pygame.init()

# freetypeを使って日本語フォントを読み込む
freetype = pygame.freetype.SysFont("Noto Sans CJK JP", 48)
button_font = pygame.freetype.SysFont("Noto Sans CJK JP", 36)
small_font = pygame.freetype.SysFont("Noto Sans CJK JP", 24)


# 画面サイズの設定
screen_width = 1300
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("タギロン")


# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
BLUE = (100, 100, 255)
YELLOW = (255, 255, 100)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 149, 237)
def draw_simple_green_background():
    screen.fill((224, 255, 224))  # ライトグリーンの背景

# ボタンの定義
button_width = 200
button_height = 50
button_margin = 20  # ボタン間の横の隙間を狭く設定
left_shift = 280  # 左に移動する量

# ボタンの座標設定
one_player_button_rect = pygame.Rect((screen_width // 2 - button_width // 2, 250), (button_width, button_height))
two_player_button_rect = pygame.Rect((screen_width // 2 - button_width // 2, 350), (button_width, button_height))
switch_turn_button_rect = pygame.Rect((screen_width // 2 - button_width // 2, screen_height - 200), (button_width, button_height))  # ターン切り替えボタン
ask_button_rect = pygame.Rect((screen_width // 2 - button_width - button_margin // 2 - left_shift, screen_height - 130), (button_width, button_height))  # 上段左
answer_button_rect = pygame.Rect((screen_width // 2 + button_margin // 2 - left_shift, screen_height - 130), (button_width, button_height))  # 上段右
history_button_rect = pygame.Rect((screen_width // 2 - button_width - button_margin // 2 - left_shift, screen_height - 70), (button_width, button_height))  # 下段左
end_button_rect = pygame.Rect((screen_width // 2 + button_margin // 2 - left_shift, screen_height - 70), (button_width, button_height))  # 下段右
back_button_rect = pygame.Rect((screen_width // 2 - button_width // 2, screen_height - 100), (button_width, button_height))

# ボタンを描画する関数
def draw_button(screen, rect, text, font):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, rect, border_radius=15)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, rect, border_radius=15)
    font.render_to(screen, (rect.x + 20, rect.y + 15), text, WHITE)


# 背景グラデーションを描画する関数
def draw_gradient_background():
    for i in range(screen_height):
        color_value = int(255 * (i / screen_height))
        pygame.draw.line(screen, (color_value, color_value, color_value), (0, i), (screen_width, i))



# タイルのセットアップ（赤と青の0〜9、黄色の5が2枚）
colors = ["red", "blue"]
numbers = list(range(0, 10))
tiles = [(color, number) for color in colors for number in numbers if number != 5] + [("yellow", 5), ("yellow", 5)]

# プレイヤーとコンピュータの手札を生成（重複なし、昇順に並べる）
def generate_hands():
    all_tiles = tiles[:]  # タイルをコピー
    player_hand = random.sample(all_tiles, 5)  # プレイヤー1の手札をランダムに選ぶ

    # プレイヤー1の手札を全体のリストから削除
    for card in player_hand:
        all_tiles.remove(card)

    opponent_hand = random.sample(all_tiles, 5)  # 残りのタイルからプレイヤー2の手札を選ぶ

    # 昇順に並べ替え。同じ数字なら赤を左にする
    player_hand.sort(key=lambda x: (x[1], x[0] != "red"))
    opponent_hand.sort(key=lambda x: (x[1], x[0] != "red"))

    return player_hand, opponent_hand


# プレイヤーと相手のカードセットアップ
player_hand, opponent_hand = generate_hands()

card_width = 100
card_height = 150
card_margin = 10


# グローバル変数の初期化
is_end_screen = False  # 終了画面のフラグを初期化
dropdown_active = [False] * 5  # 5枚のカードに対応するドロップダウンの開閉状態
dropdown_rects = [[] for _ in range(5)]  # 各カードに対応するドロップダウンの矩形リスト



# プレイヤーのカードを描画する関数
def draw_player_hand():
    for i, (color, number) in enumerate(player_hand):
        x = 100 + i * (card_width + card_margin)
        y = screen_height - card_height - 150  # プレイヤーのカードは画面下部に表示
        card_color = get_card_color(color)
        
        # カードを描画（色付き）
        pygame.draw.rect(screen, card_color, [x, y, card_width, card_height], border_radius=10)
        
        # 数字をカードの中央に大きく描画
        number_text = str(number)
        text_rect = small_font.get_rect(number_text)
        text_x = x + (card_width - text_rect.width) // 2
        text_y = y + (card_height - text_rect.height) // 2
        small_font.render_to(screen, (text_x, text_y), number_text, BLACK)


# 相手のカードを描画する関数（クリックごとに色を変える）
def draw_opponent_hand_placeholder(opponent_card_colors, selected_numbers, number_inputs):
    card_x_start = 100  # カードの表示開始位置
    card_y = 50  # カードのy位置（上部に表示）

    for i in range(5):  # 相手のカード5枚分
        card_x = card_x_start + i * (card_width + card_margin)
        # ?を表示するカードを描画（色付き）
        pygame.draw.rect(screen, opponent_card_colors[i], [card_x, card_y, card_width, card_height], border_radius=10)
        
        # 選んだ数字をカード上に表示（数字が選択されていない場合は "?" を表示）
        number_text = str(selected_numbers[i]) if selected_numbers[i] != '?' else "?"
        text_rect = small_font.get_rect(number_text)
        text_x = card_x + (card_width - text_rect.width) // 2
        text_y = card_y + (card_height - text_rect.height) // 2
        small_font.render_to(screen, (text_x, text_y), number_text, BLACK)

        # 数字入力用の小さい黒いボタンをカードの下に表示
        button_x = card_x
        button_y = card_y + card_height + 10  # カードの下にボタンを配置
        number_inputs[i] = pygame.Rect(button_x, button_y, card_width // 2, 30)  # 小さいボタンのサイズを設定
        pygame.draw.rect(screen, BLACK, number_inputs[i], border_radius=5)
        small_font.render_to(screen, (button_x + 10, button_y + 5), "n", WHITE)

        # ドロップダウンリストの描画
        options = list(range(10))  # 0〜9の選択肢
        draw_dropdown(screen, button_x, button_y - 50, card_width // 2, 30, options, dropdown_active[i], i)        


# 色の順序を定義
    color_order = [LIGHT_GRAY, RED, BLUE, YELLOW]  # 修正ポイント：定義されていなかった color_order を追加

    for i, card_rect in enumerate(card_positions):
        if card_rect.collidepoint(mouse_pos):
            current_color = opponent_card_colors[i]
            new_color_index = (color_order.index(current_color) + 1) % len(color_order)
            opponent_card_colors[i] = color_order[new_color_index]
            break        



# ドロップダウンリストを描画する関数
def draw_dropdown(screen, x, y, width, height, options, active, card_index):
    # ドロップダウンがアクティブなときのみリストを表示
    if active:
        dropdown_rects[card_index] = []  # リストを初期化して、ドロップダウン項目を保存
        for i, option in enumerate(options):
            option_rect = pygame.Rect(x, y + i * height, width, height)
            dropdown_rects[card_index].append(option_rect)  # 各項目の矩形をリストに保存
            pygame.draw.rect(screen, LIGHT_GRAY, option_rect)
            small_font.render_to(screen, (option_rect.x + 10, option_rect.y + 5), str(option), BLACK)

            # ドロップダウンが描画されているか確認するためのデバッグ出力
            print(f"Dropdown item {option} at {option_rect.x}, {option_rect.y}")

            
def handle_number_input_dropdown(mouse_pos, number_inputs, selected_numbers):
    for i, rect in enumerate(number_inputs):
        if rect.collidepoint(mouse_pos):
            # 現在の数字を1つ進める（0〜9でループする）
            if selected_numbers[i] == '?':
                selected_numbers[i] = 0  # 初期値が '?' の場合は 0 に設定
            else:
                selected_numbers[i] = (selected_numbers[i] + 1) % 10  # 0〜9でループ


            
# 相手のカードがクリックされたときに色を変更する処理
def handle_opponent_card_click(mouse_pos, opponent_card_colors):
    card_positions = [
        pygame.Rect(100, 50, card_width, card_height),  # 1枚目
        pygame.Rect(220, 50, card_width, card_height),  # 2枚目
        pygame.Rect(340, 50, card_width, card_height),  # 3枚目
        pygame.Rect(460, 50, card_width, card_height),  # 4枚目
        pygame.Rect(580, 50, card_width, card_height)   # 5枚目
    ]

    
                

# プレイヤーのカードを描画する関数
def draw_player_hand(player_hand):
    for i, (color, number) in enumerate(player_hand):
        x = 100 + i * (card_width + card_margin)
        y = screen_height - card_height - 150  # プレイヤーのカードは画面下部に表示
        card_color = get_card_color(color)
        
        # カードを描画（色付き）
        pygame.draw.rect(screen, card_color, [x, y, card_width, card_height], border_radius=10)
        
        # 数字をカードの中央に大きく描画
        number_text = str(number)
        text_rect = small_font.get_rect(number_text)
        text_x = x + (card_width - text_rect.width) // 2
        text_y = y + (card_height - text_rect.height) // 2
        small_font.render_to(screen, (text_x, text_y), number_text, BLACK)   

    
# 質問リスト (全体の質問)
all_questions = [
    "赤の数の合計数は？", "青の数の合計数は？", "赤の数字タイルは何枚ある？", "青の数字タイルは何枚ある？",
    "タイルすべての合計数は？", "数字タイルの最大の数から最小の数を引いた数は？", "大きいほうから3枚の合計数は？",
    "小さいほうから3枚の合計数は？", "中央の3枚の合計数は？", "同じ数字タイルのペアは何組ある？",
    "連番になっているタイルはどこ？", "連続して隣り合っている同じ色はどこ？", "5はどこ？",
    "1または2はどこ？", "3または4はどこ？", "6または7はどこ？", "8または9はどこ？", "0はどこ？",
    "偶数は何枚ある？", "奇数は何枚ある？", "中央の数字タイルは5以上？4以下？"
]


# 質問をランダムに選んで表示する関数
def initialize_questions():
    global current_questions
    num_questions = min(6, len(all_questions))
    current_questions = random.sample(all_questions, num_questions)


# 質問を描画する関数
def draw_questions():
    for i, question in enumerate(current_questions):
        draw_button(screen, pygame.Rect(100, 50 + i * 50, 600, 40), question, small_font)    



# プレイヤーが質問を選び、相手の手札に対して応答する関数
def answer_question(question, opponent_hand, choice=None):
    global question_count  # question_count をグローバルで扱う
    question_count += 1  # 質問が選ばれたときにカウントを増加

    
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



def draw_choose_screen(option1, option2):
    screen.fill(WHITE)
    small_font.render_to(screen, (screen_width // 2 - 100, 100), "どちらを選びますか？", BLACK)
    draw_button(screen, option1_button_rect, option1, button_font)
    draw_button(screen, option2_button_rect, option2, button_font)
           

current_questions = []  # 表示される質問のリスト
show_questions = False  # 質問を表示するかどうかのフラグ
answer_text = ""  # 質問に対する答えを表示するためのテキスト
question_screen = False  # 質問リスト画面かどうかのフラグ
question_answered = False  # 質問に答えが表示されたかどうかのフラグ
question_count = 0  # 質問回数
choose_screen = False  # 選択画面のフラグ
option1_button_rect = pygame.Rect((screen_width // 4 - button_width // 2, screen_height // 2), (button_width, button_height))
option2_button_rect = pygame.Rect((screen_width * 3 // 4 - button_width // 2, screen_height // 2), (button_width, button_height))
selected_question = ""  # 選択された質問を保存する変数


# 質問リスト画面の描画関数
def draw_question_screen():
    screen.fill(WHITE)
    draw_questions()
    if question_answered:
        small_font.render_to(screen, (100, 400), answer_text, BLACK)  # 答えを表示
    draw_button(screen, back_button_rect, "戻る", button_font)  # 戻るボタンを描画


# カードの色を取得する関数
def get_card_color(color):
    if color in ["赤", "red"]:
        return RED
    elif color in ["青", "blue"]:
        return BLUE
    elif color in ["黄", "yellow"]:
        return YELLOW
    return LIGHT_GRAY

    

# 質問と回答を履歴に追加する関数
def record_answer(question, answer):
    history.append(f"Q: {question}\nA: {answer}")

# 質問と回答の履歴を保持するリスト
history = []

# 各プレイヤーの推測情報を保持
player1_selected_numbers = ['?'] * 5
player2_selected_numbers = ['?'] * 5
player1_card_colors = [LIGHT_GRAY] * 5
player2_card_colors = [LIGHT_GRAY] * 5


# 質問履歴画面を描画する関数
def draw_history_screen(question_history):
    screen.fill(WHITE)
    small_font.render_to(screen, (screen_width // 2 - 100, 50), "質問履歴", BLACK)  # タイトル表示

    # 質問履歴を描画
    for i, (question, answer) in enumerate(question_history):
        question_text = f"{i + 1}. {question} -> {answer}"
        small_font.render_to(screen, (100, 100 + i * 40), question_text, BLACK)

    # 戻るボタンを描画
    draw_button(screen, back_button_rect, "戻る", button_font)



# 回答するボタンが押された時に、色と数字の一致を確認する処理
def handle_answer_button_click(selected_numbers, opponent_hand, opponent_card_colors):
    global question_count  # グローバル変数として宣言
    correct = True
    for i, (color, number) in enumerate(opponent_hand):
        if selected_numbers[i] != number or opponent_card_colors[i] != get_card_color(color):
            correct = False
            break
    
    if correct:
        print("正解です！ゲームを終了します。")
        return True  # 正解の場合はTrueを返して終了
    else:
        print("不正解です。質問回数が1増加します。")
        question_count += 1  # 不正解の場合、質問回数を1増やすペナルティ
        return False  # 不正解の場合はFalseを返す


# 終了画面の描画関数
def draw_end_screen(player1_hand, player2_hand):
    screen.fill(WHITE)
    small_font.render_to(screen, (screen_width // 2 - 100, 50), "ゲーム終了", BLACK)  # タイトル表示

    # 上側にplayer1のカードを表示
    for i, (color, number) in enumerate(player1_hand):
        x = 100 + i * (card_width + card_margin)
        y = 100  # player1のカードは上部に表示
        card_color = get_card_color(color)
        pygame.draw.rect(screen, card_color, [x, y, card_width, card_height], border_radius=10)
        small_font.render_to(screen, (x + 30, y + 60), str(number), BLACK)

    # 下側にplayer2のカードを表示
    for i, (color, number) in enumerate(player2_hand):
        x = 100 + i * (card_width + card_margin)
        y = 300  # player2のカードは下部に表示
        card_color = get_card_color(color)
        pygame.draw.rect(screen, card_color, [x, y, card_width, card_height], border_radius=10)
        small_font.render_to(screen, (x + 30, y + 60), str(number), BLACK)

    # ゲーム終了時のメッセージを表示
    message = f"正解です！{question_count}回の質問で当てました！"
    small_font.render_to(screen, (screen_width // 2 - 150, 500), message, BLACK)  # メッセージを表示
    
# 質問回数を表示する関数
def draw_question_count():
    small_font.render_to(screen, (screen_width - 200, 20), f"質問回数: {question_count}", BLACK)

        

    
# 2人プレイヤーのターンの切り替え    
def handle_two_player_turns(mouse_pos):
    global question_screen, question_answered, answer_text, is_end_screen, is_history_screen, question_history

    # 現在のプレイヤーの推測情報を取得
    if player_turn == 1:
        opponent_card_colors = player1_card_colors
        selected_numbers = player1_selected_numbers
    else:
        opponent_card_colors = player2_card_colors
        selected_numbers = player2_selected_numbers

    if question_screen:
        # 質問が選ばれた場合の処理
        if question_answered:
            if back_button_rect.collidepoint(mouse_pos):
                question_screen = False
                question_answered = False
                answer_text = ""
        else:
            for i, question in enumerate(current_questions):
                question_rect = pygame.Rect(100, 50 + i * 50, 600, 40)
                if question_rect.collidepoint(mouse_pos):
                    answer_text = answer_question(question, player2_hand if player_turn == 1 else player1_hand)
                    question_history.append((question, answer_text))
                    current_questions.pop(i)
                    question_answered = True
                    break
    else:
        if ask_button_rect.collidepoint(mouse_pos):
            initialize_questions()
            question_screen = True
        if end_button_rect.collidepoint(mouse_pos):
            is_end_screen = True
        if history_button_rect.collidepoint(mouse_pos):
            is_history_screen = True

        # 相手の隠されたカードがクリックされた場合、色を変更
        handle_opponent_card_click(mouse_pos, opponent_card_colors)

        # 数字入力ボタンが押されたかどうかを確認
        handle_number_input_dropdown(mouse_pos, number_inputs, selected_numbers)

        # 「回答する」ボタンが押された場合の処理
        target_hand = player2_hand if player_turn == 1 else player1_hand
        if answer_button_rect.collidepoint(mouse_pos):
            if handle_answer_button_click(selected_numbers, target_hand, opponent_card_colors):
                is_end_screen = True

        # 「相手のターンへ」ボタンが押された場合の処理
        if switch_turn_button_rect.collidepoint(mouse_pos):
            switch_turn()

# ターンの切り替え時に推測情報をリセットしない
def switch_turn():
    global player_turn
    player_turn = 2 if player_turn == 1 else 1
            


# ターンの切り替え時に相手の推測情報をリセットする
def switch_turn():
    global player_turn, player1_selected_numbers, player2_selected_numbers
    player_turn = 1 if player_turn == 2 else 2
    if player_turn == 1:
        player2_selected_numbers = ['?'] * 5  # プレイヤー2が終了したらリセット
    else:
        player1_selected_numbers = ['?'] * 5  # プレイヤー1が終了したらリセット
        
    
            
# プレイヤーのターンを表示する関数
def draw_player_turn():
    turn_text = f"Player {player_turn}のターンです"
    small_font.render_to(screen, (screen_width // 2 - 100, 20), turn_text, BLACK)


    
# 回答ボタンが押されたときの処理
def handle_answer_button_click(selected_numbers, opponent_hand, opponent_card_colors):
    correct = True
    for i, (color, number) in enumerate(opponent_hand):
        if selected_numbers[i] != number or opponent_card_colors[i] != get_card_color(color):
            correct = False
            break
    
    if correct:
        print(f"正解です！{question_count}回の質問で当てました！")  # コンソールに出力する（デバッグ用）
        return True  # 正解の場合はTrueを返して終了画面に切り替える
    else:
        print("不正解です。もう一度試してください。")
        return False  # 不正解の場合はFalseを返す
        

# 相手のカードを描画する関数（答えの表示）
def draw_opponent_hand():
    for i, (color, number) in enumerate(opponent_hand):
        x = 100 + i * (card_width + card_margin)
        y = screen_height // 2 - card_height // 2  # 相手のカードは画面中央に表示
        card_color = get_card_color(color)
        pygame.draw.rect(screen, card_color, [x, y, card_width, card_height], border_radius=10)
        small_font.render_to(screen, (x + 30, y + 60), str(number), BLACK)



# メイン画面の描画関数
def draw_main_menu():
    draw_gradient_background()
    draw_simple_green_background()  # シンプルな緑の背景を描画
    freetype.render_to(screen, (screen_width // 2 - 100, 100), "タギロン", BLACK)
    draw_button(screen, one_player_button_rect, "1人用", button_font)
    draw_button(screen, two_player_button_rect, "2人用", button_font)


# ゲームモードを開始する関数
def start_game(mode):
    global show_questions, answer_text, question_screen, question_answered, question_count, player_turn
    if mode == "1人用":
        show_questions = False
        answer_text = ""
        question_screen = False
        question_answered = False
        question_count = 0
        player_turn = 1  # プレイヤー1が開始
        return "1人用"
    elif mode == "2人用":
        show_questions = False
        answer_text = ""
        question_screen = False
        question_answered = False
        question_count = 0
        player_turn = 1  # プレイヤー1からスタート
        return "2人用"
        

    
# 1人用モードの描画
def draw_single_player_mode(opponent_card_colors, selected_numbers, number_inputs):
    draw_simple_green_background()  # 薄い緑色の背景を描画
    draw_player_hand(player_hand)
    draw_opponent_hand_placeholder(opponent_card_colors, selected_numbers, number_inputs)  # 相手のカードの?表示
    draw_button(screen, ask_button_rect, "質問する", button_font)
    draw_button(screen, answer_button_rect, "回答する", button_font)
    draw_button(screen, end_button_rect, "終了", button_font)  # 終了ボタンを追加
    draw_button(screen, history_button_rect, "履歴", button_font)  # 履歴ボタンを追加
    draw_question_count()  # 質問回数を表示


# 2人用モードの描画    
def draw_two_player_mode(player_hand, opponent_hand, opponent_card_colors, selected_numbers, number_inputs):
    """
    2人用モードの画面を描画する関数。
    player_hand: 現在のプレイヤーの手札
    opponent_hand: 相手の手札（推測対象）
    opponent_card_colors: 現在のプレイヤーが推測した相手のカードの色（推測用）
    selected_numbers: 現在のプレイヤーが推測した相手の数字
    number_inputs: 数字入力用のボタンリスト
    """
    draw_simple_green_background()  # 背景を描画
    
    # 現在のプレイヤーの手札を画面下部に描画
    draw_player_hand(player_hand)
    
    # 相手のカードを推測用に描画（現在のプレイヤーが推測した内容を表示）
    draw_opponent_hand_placeholder(opponent_card_colors, selected_numbers, number_inputs)
    
    # 質問する、回答する、終了、履歴ボタンを描画
    draw_button(screen, ask_button_rect, "質問する", button_font)
    draw_button(screen, answer_button_rect, "回答する", button_font)
    draw_button(screen, end_button_rect, "終了", button_font)
    draw_button(screen, history_button_rect, "履歴", button_font)
    
    # 現在のターンを表示
    turn_text = f"Player {player_turn}のターン"
    small_font.render_to(screen, (screen_width - 300, 20), turn_text, BLACK)
    
    # 相手のターンへ切り替えボタンを描画
    draw_button(screen, switch_turn_button_rect, "相手のターンへ", button_font)
    
    # 質問回数を表示
    draw_question_count()




# 画面のメインループ
def main():
    running = True
    game_mode = None  # 現在のゲームモード
    is_end_screen = False  # 終了画面のフラグ
    choose_screen = False  # 選択画面のフラグ
    is_history_screen = False  # 履歴画面のフラグ
    player1_card_colors = [LIGHT_GRAY] * 5  # プレイヤー1の推測用カードの色
    player2_card_colors = [LIGHT_GRAY] * 5  # プレイヤー2の推測用カードの色
    player1_selected_numbers = ['?'] * 5  # プレイヤー1の推測した数字
    player2_selected_numbers = ['?'] * 5  # プレイヤー2の推測した数字
    number_inputs = [None] * 5  # 数字入力用のボタン
    question_history = []  # 質問と回答の履歴を保持するリスト

    # プレイヤーの手札を初期化
    player1_hand, player2_hand = generate_hands()
    player_turn = 1  # 1: プレイヤー1のターン, 2: プレイヤー2のターン

    global answer_text, question_screen, question_answered, question_count, option1, option2, selected_question

    
    while running:
        screen.fill(WHITE)

        if is_end_screen:
            draw_end_screen(player1_hand, player2_hand)  # 終了画面を描画
        elif choose_screen:
            draw_choose_screen(option1, option2)  # 選択画面を描画
        elif is_history_screen:
            draw_history_screen(question_history)  # 質問履歴画面を描画
        elif game_mode == "1人用":
            if question_screen:
                draw_question_screen()  # 質問リスト画面を描画
            else:
                draw_single_player_mode(player1_card_colors, player1_selected_numbers, number_inputs)  # 1人用モードの画面を描画
        elif game_mode == "2人用":
            if question_screen:
                draw_question_screen()  # 質問リスト画面を描画
            else:
                # プレイヤーのターンに応じて異なる画面を描画
                if player_turn == 1:
                    draw_two_player_mode(player1_hand, player2_hand, player1_card_colors, player1_selected_numbers, number_inputs)
                else:
                    draw_two_player_mode(player2_hand, player1_hand, player2_card_colors, player2_selected_numbers, number_inputs)
        else:
            draw_main_menu()  # メニュー画面を描画

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if is_end_screen:
                    continue  # 終了画面では何も処理しない

                if choose_screen:
                    if option1_button_rect.collidepoint(mouse_pos):
                        answer_text = answer_question(selected_question, player2_hand if player_turn == 1 else player1_hand, choice=option1)
                        choose_screen = False
                        question_answered = True
                        question_history.append((selected_question, answer_text))  # 質問と答えを履歴に追加
                    elif option2_button_rect.collidepoint(mouse_pos):
                        answer_text = answer_question(selected_question, player2_hand if player_turn == 1 else player1_hand, choice=option2)
                        choose_screen = False
                        question_answered = True
                        question_history.append((selected_question, answer_text))  # 質問と答えを履歴に追加

                elif is_history_screen:
                    if back_button_rect.collidepoint(mouse_pos):  # 戻るボタンがクリックされた場合
                        is_history_screen = False  # 履歴画面を終了してメイン画面に戻る
                        game_mode = "2人用"  # メイン画面に戻るように設定

                elif game_mode in ["1人用", "2人用"]:
                    if question_screen:
                        if question_answered:
                            if back_button_rect.collidepoint(mouse_pos):
                                question_screen = False  # 元の画面に戻る
                                question_answered = False  # 質問の答え表示をリセット
                                answer_text = ""  # 答えをクリア
                        else:
                            # 質問がクリックされたかどうかを確認
                            for i, question in enumerate(current_questions):
                                question_rect = pygame.Rect(100, 50 + i * 50, 600, 40)
                                if question_rect.collidepoint(mouse_pos):
                                    if question in ["1または2はどこ？", "3または4はどこ？", "6または7はどこ？", "8または9はどこ？"]:
                                        choose_screen = True
                                        selected_question = question
                                        if question == "1または2はどこ？":
                                            option1, option2 = "1", "2"
                                        elif question == "3または4はどこ？":
                                            option1, option2 = "3", "4"
                                        elif question == "6または7はどこ？":
                                            option1, option2 = "6", "7"
                                        elif question == "8または9はどこ？":
                                            option1, option2 = "8", "9"
                                    else:
                                        answer_text = answer_question(question, player2_hand if player_turn == 1 else player1_hand)
                                        question_history.append((question, answer_text))  # 質問と答えを履歴に追加
                                        current_questions.pop(i)
                                        question_answered = True
                                    break
                    else:
                        if ask_button_rect.collidepoint(mouse_pos):
                            initialize_questions()
                            question_screen = True
                        if end_button_rect.collidepoint(mouse_pos):
                            is_end_screen = True
                        if history_button_rect.collidepoint(mouse_pos):  # 履歴ボタンがクリックされた場合
                            is_history_screen = True  # 履歴画面に切り替える

                        # プレイヤーごとの推測情報を使用して、カードの操作を行う
                        if player_turn == 1:
                            handle_opponent_card_click(mouse_pos, player1_card_colors)
                            handle_number_input_dropdown(mouse_pos, number_inputs, player1_selected_numbers)
                        else:
                            handle_opponent_card_click(mouse_pos, player2_card_colors)
                            handle_number_input_dropdown(mouse_pos, number_inputs, player2_selected_numbers)

                        # 「回答する」ボタンが押された場合の処理
                        if answer_button_rect.collidepoint(mouse_pos):
                            target_hand = player2_hand if player_turn == 1 else player1_hand
                            target_colors = player1_card_colors if player_turn == 1 else player2_card_colors
                            target_numbers = player1_selected_numbers if player_turn == 1 else player2_selected_numbers
                            if handle_answer_button_click(target_numbers, target_hand, target_colors):
                                is_end_screen = True

                        # 「相手のターンへ」ボタンが押された場合の処理
                        if switch_turn_button_rect.collidepoint(mouse_pos):
                            player_turn = 2 if player_turn == 1 else 1  # ターンを切り替える

                else:
                    if one_player_button_rect.collidepoint(mouse_pos):
                        game_mode = start_game("1人用")
                    if two_player_button_rect.collidepoint(mouse_pos):
                        game_mode = start_game("2人用")

        pygame.display.flip()

    pygame.quit()
# ゲームの開始
main()
    
