import threading
import flet as ft

from utils import Timer, get_english_words, show_english_words, increment_used_count, get_data_table_columns, get_data_table_rows, get_screen_size
from global_variables import EN_JA_WORDS_LIST, QUESTIONS_LIST

def main(page: ft.Page):
    global QUESTIONS_LIST
    
    # アプリタイトル
    page.title = "Charades"
    
    # ウィンドウサイズを指定
    screen_width, screen_height = get_screen_size()
    page.window_width = screen_width - 100
    page.window_height = screen_height - 130
    
    # ウィンドウをやや中央に配置
    window_x = (screen_width - page.window_width) // 2
    window_y = (screen_height - page.window_height) // 2 - 20
    page.window_left = window_x
    page.window_top = window_y
    
    
    # #################################
    # クリックイベント定義
    # #################################
    # プレイページへ移動
    def on_play_click(e):
        # グローバル変数を使用するための宣言
        global EN_JA_WORDS_LIST
        
        # 英単語一覧を取得
        EN_JA_WORDS_LIST = get_english_words(level.value)
        
        # ページ遷移
        page.go("/play")
        
        # タイマー開始
        if Timer.is_stop:
            Timer.is_stop = False
        minutes = int(minutes_dropdown.value)
        seconds = int(seconds_dropdown.value)
        timer = Timer(minutes, seconds, timer_text, data_table, result_table, correct_answer_number, page)
        threading.Thread(target=timer.start_timer, daemon=True).start()
        
        # 最初の英単語を表示
        displayed_word = show_english_words(EN_JA_WORDS_LIST, display_word)
        
        # 英単語リストから表示した単語を削除
        EN_JA_WORDS_LIST = [row for row in EN_JA_WORDS_LIST if row[0] != displayed_word]
        increment_used_count(displayed_word)
    
    # 「SKIP」ボタンクリック
    def on_skip_click(e):
        # グローバル変数を使用するための宣言
        global EN_JA_WORDS_LIST
        
        # 出題した単語のリストに追加
        if not display_word.value == "No anymore.":
            QUESTIONS_LIST.append([display_word.value, display_word.data, ""])
        
        # 次の英単語を表示
        displayed_word = show_english_words(EN_JA_WORDS_LIST, display_word)
        
        # 英単語リストから表示した単語を削除
        EN_JA_WORDS_LIST = [row for row in EN_JA_WORDS_LIST if row[0] != displayed_word]
        increment_used_count(displayed_word)
        
        
    # 「正解」ボタンクリック
    def on_correct_click(e):
        # グローバル変数を使用するための宣言
        global EN_JA_WORDS_LIST
        
        # 出題した単語のリストに追加
        if not display_word.value == "No anymore.":
            QUESTIONS_LIST.append([display_word.value, display_word.data, "✓"])
        
        # 次の英単語を表示
        displayed_word = show_english_words(EN_JA_WORDS_LIST, display_word)
        
        # 英単語リストから表示した単語を削除
        EN_JA_WORDS_LIST = [row for row in EN_JA_WORDS_LIST if row[0] != displayed_word]
        increment_used_count(displayed_word)
        
    # 「メイン画面へ」ボタンクリック
    def on_back_click(e):
        goto_top(e)
    
    
    # #################################
    # 1. トップページのコンポーネント
    # #################################
    # 難易度選択ドロップダウン
    level_intro = ft.Text("難易度を設定してください", size=20, weight=ft.FontWeight.BOLD)
    level = ft.Dropdown(
        label="Level",
        options=[
            ft.dropdown.Option("入門"),
            ft.dropdown.Option("初級"),
            ft.dropdown.Option("中級"),
            ft.dropdown.Option("上級"),
            # ft.dropdown.Option("固有名詞"),   # TODO: 文字サイズ調整が必要
        ],
        width=400,
        value="入門"
    )
    
    # 難易度説明テキスト
    explain1 = ft.Text("入門: TOEIC 400以下、英検3級、高校入試、中学生", size=10, color='gray')
    explain2 = ft.Text("初級: TOEIC 600～400、英検2級、大学入試、高校生", size=10, color='gray')
    explain3 = ft.Text("中級: TOEIC 800～600、英検準1級、難関大学入試、高校生", size=10, color='gray')
    explain4 = ft.Text("上級: TOEIC 800以上、英検1級、最難関大学入試、高校生", size=10, color='gray')
    # explain5 = ft.Text("固有名詞: 人名、国名、ブランド名、観光名所、映画タイトルなど", size=10, color='gray') # TODO: 文字サイズ調整が必要

    # タイマー設定ドロップダウン
    timer_intro = ft.Text("タイマーを設定してください", size=20, weight=ft.FontWeight.BOLD)
    minutes_options = [ft.dropdown.Option(str(i)) for i in range(0, 6)]
    seconds_options = [ft.dropdown.Option(str(i)) for i in [0, 15, 30, 45]]
    minutes_dropdown = ft.Dropdown(label="Minutes", options=minutes_options, width=100, value=1)
    seconds_dropdown = ft.Dropdown(label="Seconds", options=seconds_options, width=100, value=0)

    # プレイボタン
    start_btn = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(name="play_arrow", size=80),
                ft.Text("PLAY", size=60, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        width=400,
        height=100,
        on_click=on_play_click,
        style=ft.ButtonStyle(
            bgcolor={"": ft.Colors.BLUE_ACCENT_700},
            color={"": ft.Colors.WHITE},
            padding={"": 10},
            shape={"": ft.RoundedRectangleBorder(radius=8)}
        )
    )
    
    
    # #################################
    # 2. プレイページのコンポーネント
    # #################################
    # 画面表示する英単語テキスト
    display_word = ft.Text("", size=200, weight=ft.FontWeight.BOLD)
    
    # タイマーアイコン
    timer_icon = ft.Icon(name="TIMER_SHARP", size=88, color=ft.Colors.BLACK)
    
    # タイマー表示テキスト
    timer_text = ft.Text("00:00", size=77, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
    
    # 「正解」ボタン
    correct_btn = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(name="CHECK", size=40),
                ft.Text("CORRECT", size=30, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        width=250,
        height=80,
        on_click=on_correct_click,
        style=ft.ButtonStyle(
            bgcolor={"": ft.Colors.GREEN_ACCENT_400},
            color={"": ft.Colors.WHITE},
            padding={"": 10},
            shape={"": ft.RoundedRectangleBorder(radius=8)}
        )
    )
    
    # 「スキップ」ボタン
    skip_btn = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(name="skip_next", size=40),
                ft.Text("SKIP", size=30, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        width=250,
        height=80,
        on_click=on_skip_click,
        style=ft.ButtonStyle(
            bgcolor={"": ft.Colors.RED_ACCENT_400},
            color={"": ft.Colors.WHITE},
            padding={"": 10},
            shape={"": ft.RoundedRectangleBorder(radius=8)}
        )
    )
    
    
    # #################################
    # 3. リザルトページのコンポーネント
    # #################################
    # 結果発表テキスト
    result_intro = ft.Stack(
        [
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "★ 結果発表 ★",
                        ft.TextStyle(
                            size=50,
                            weight=ft.FontWeight.BOLD,
                            foreground=ft.Paint(
                                color=ft.Colors.BLUE_ACCENT_400,
                                stroke_width=6,
                                stroke_join=ft.StrokeJoin.ROUND,
                                style=ft.PaintingStyle.STROKE,
                            ),
                        ),
                    ),
                ],
            ),
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "★ 結果発表 ★",
                        ft.TextStyle(
                            size=50,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.YELLOW_700,
                        ),
                    ),
                ],
            ),
        ]
    )
    
    # 正解数表示テキスト
    correct_answer_subject = ft.Text(
        "あなたの正解数は", 
        size=20, 
        weight=ft.FontWeight.BOLD, 
        color=ft.Colors.BLUE_ACCENT_400,
        style=ft.TextStyle(
            decoration=ft.TextDecoration.UNDERLINE,
            decoration_style=ft.TextDecorationStyle.DOTTED,
            decoration_color=ft.Colors.BLUE_ACCENT_400
        )
    )
    correct_answer_number  = ft.Text(
        "**", 
        size=50, 
        weight=ft.FontWeight.BOLD, 
        color=ft.Colors.RED_ACCENT_400,
        style=ft.TextStyle(
            decoration=ft.TextDecoration.UNDERLINE,
            decoration_color=ft.Colors.RED_ACCENT_400
        )
    )
    correct_answer_unit    = ft.Text(
        "個", 
        size=20, 
        weight=ft.FontWeight.BOLD, 
        color=ft.Colors.BLUE_ACCENT_400,
        style=ft.TextStyle(
            decoration=ft.TextDecoration.UNDERLINE,
            decoration_style=ft.TextDecorationStyle.DOTTED,
            decoration_color=ft.Colors.BLUE_ACCENT_400
        )
    )
    
    # 出題した英単語・日本語訳・正否の表コントロール
    result_table_header = ["English word", "Japanese word", "Correct"]
    result_table_data   = QUESTIONS_LIST    # 配置の段階ではデータ空。タイマー終了時にデータを更新する。
    data_table = ft.DataTable(
        columns=get_data_table_columns(result_table_header),
        rows=get_data_table_rows(result_table_data),    # 配置の段階ではデータ空。タイマー終了時にデータを更新する。
    )
    result_table = ft.Column(   # スクロール設定と拡大設定をするためにColumnコントロールにDataTableを配置
        controls=[data_table],
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
        height=400
    )
    
    # 「メイン画面へ」ボタン
    back_to_main_btn = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(name="ARROW_BACK", size=40),
                ft.Text("MAIN", size=30, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        width=300,
        height=75,
        on_click=on_back_click,
        style=ft.ButtonStyle(
            bgcolor={"": ft.Colors.BLUE},
            color={"": ft.Colors.WHITE},
            padding={"": 10},
            shape={"": ft.RoundedRectangleBorder(radius=8)}
        )
    )
    
    # #################################
    # 共通コンポーネント
    # #################################
    # 空白行
    blank = ft.Text("")
    
    
    # #################################
    # ページ遷移イベント
    # #################################
    # ページを更新する
    def route_change(e):
        print("Route change:", e.route)
        
        # ページクリア
        page.views.clear()

        # トップページ（常にviewに追加する）
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("ゲーム設定")),
                    ft.Column(
                        [
                            # 難易度選択
                            level_intro, level, explain1, explain2, explain3, explain4, blank,
                            # タイマー設定
                            timer_intro,
                            ft.Row(
                                [
                                    minutes_dropdown,
                                    seconds_dropdown
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            # プレイボタン
                            blank, start_btn
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ],
            )
        )
        
        # プレイページ（viewに追加する）
        if page.route == "/play":
            page.views.append(
                ft.View(
                    "/play",
                    [
                        ft.AppBar(title=ft.Text("プレイ")),
                        ft.Column(
                            [
                                ft.Row([timer_icon, timer_text], alignment=ft.MainAxisAlignment.CENTER,),
                                display_word,
                                blank, blank,
                                ft.Row([correct_btn, ft.Text("         "), skip_btn], alignment=ft.MainAxisAlignment.CENTER,),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                    ],
                )
            )
            
        # リザルトページ（viewに追加する）
        if page.route == "/result":
            page.views.append(
                ft.View(
                    "/result",
                    [
                        ft.Column(
                            [
                                blank,
                                result_intro,
                                ft.Row([
                                    correct_answer_subject, 
                                    correct_answer_number, 
                                    correct_answer_unit
                                    ], alignment=ft.MainAxisAlignment.CENTER,),
                                result_table,
                                blank,
                                back_to_main_btn
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ],
                )
            )
            
        # ページ更新
        page.update()

    # 現在のページを削除して、前のページに戻る
    def view_pop(e):
        # グローバル変数を使用するための宣言
        global EN_JA_WORDS_LIST, QUESTIONS_LIST
        
        # スレッドのタイマーを停止＆リセット
        Timer.is_stop = True
        
        # グローバル変数のリセット
        EN_JA_WORDS_LIST.clear()
        QUESTIONS_LIST.clear()
        
        # ページを削除して、前のページに戻る
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        
    # トップページに戻る
    def goto_top(e):
        # グローバル変数を使用するための宣言
        global EN_JA_WORDS_LIST, QUESTIONS_LIST
        
        # グローバル変数のリセット
        EN_JA_WORDS_LIST.clear()
        QUESTIONS_LIST.clear()
        
        # スレッドのタイマーを停止＆リセット
        Timer.is_stop = True
        
        # 全てのページをクリアしてトップページに戻る
        page.views.clear()
        page.go("/")


    # ---------------------------------
    # イベントの登録
    # ---------------------------------
    # ページ遷移イベントが発生したら、ページを更新
    page.on_route_change = route_change
    # AppBarの戻るボタンクリック時、前のページへ戻る
    page.on_view_pop = view_pop


    # ---------------------------------
    # 起動時の処理
    # ---------------------------------
    # ページ遷移を実行
    page.go(page.route)


# ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
ft.app(target=main)