import ctypes
import time
import random
import MySQLdb
from MySQLdb.constants.CLIENT import MULTI_STATEMENTS
import flet as ft

from read_settings import JSON_DATA
from global_variables import QUESTIONS_LIST
import sqls


def get_screen_size():
    """画面のサイズを取得する。

    Returns:
        screen_width (int): 画面の幅。
        screen_height (int): 画面の高さ。
    """
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height


class Timer():
    """タイマークラス

    Attributes:
        minutes (int): タイマーの分数
        seconds (int): タイマーの秒数
        timer_text (obj): タイマーを表示するTextオブジェクト
        data_table (obj): データテーブル
        result_table (obj): 結果テーブル
        correct_answer_number (str): 正解数
        is_stop (bool): タイマー停止フラグ
    """
    # タイマー停止フラグ
    is_stop = False

    def __init__(self, minutes, seconds, timer_text, display_word, data_table, result_table, correct_answer_number, page):
        """コンストラクタ"""
        self.minutes = minutes
        self.seconds = seconds
        self.timer_text = timer_text
        self.display_word = display_word
        self.data_table = data_table
        self.result_table = result_table
        self.correct_answer_number = correct_answer_number
        self.page = page

    def start_timer(self):
        """指定した分数と秒数のタイマーを開始する。"""
        total_seconds = self.minutes * 60 + self.seconds

        while total_seconds >= 0:
            if Timer.is_stop:
                return
            mins, secs = divmod(total_seconds, 60)
            self.timer_text.value = f"{mins:02}:{secs:02}"
            if self.timer_text.page:
                self.timer_text.update()
            time.sleep(1)
            total_seconds -= 1

        self._timer_stopped()

    def _timer_stopped(self):
        """タイマーが停止した時の処理"""
        global QUESTIONS_LIST

        # 最後に表示された単語をリストに追加
        if not self.display_word.value == "No anymore.":
            QUESTIONS_LIST.append([self.display_word.value, self.display_word.data, ""])

        # タイマー終了メッセージを表示
        self.timer_text.value = "終了！"
        self.timer_text.update()

        # データテーブルを更新する
        self.data_table.rows = get_data_table_rows(QUESTIONS_LIST)
        if self.data_table.page:
            self.data_table.update()
        if self.result_table.page:
            self.result_table.update()

        # 正解数を更新
        correct_count = sum(1 for word in QUESTIONS_LIST if word[2] == "✓")
        self.correct_answer_number.value = str(correct_count)
        if self.correct_answer_number.page:
            self.correct_answer_number.update()

        Timer.is_stop = True

        self.page.go("/result")


def get_english_words(level):
    """データベースから指定した難易度の英単語を取得する。

    Args:
        level (str): 単語の難易度。

    Returns:
        List[List[str, str]]: 英単語と日本語訳のリスト。
    """
    words_tuple = _exe_sql_sel(sqls.SelectStatement.get_words, [level])

    en_ja_words_list = []
    for word_row in words_tuple:
        en_ja_words_list.append([word_row[1], word_row[2]])

    return en_ja_words_list


def show_english_words(en_ja_words_list, display_word):
    """英単語を画面に表示する。

    Args:
        en_ja_words_list (list[List[str, str]]): 英単語と日本語訳のリスト。
        display_word (obj): 単語を表示するTextオブジェクト。

    Returns:
        str: 表示された単語。
    """
    # 表示する単語がない場合
    if len(en_ja_words_list) == 0:
        display_word.value = "No anymore."
        if display_word.page:
            display_word.update()
        return "No anymore."

    # ランダムに単語を選択
    randint = random.randint(0, len(en_ja_words_list))

    # 単語を表示
    display_word.value = f"{en_ja_words_list[randint][0]}"
    display_word.data  = f"{en_ja_words_list[randint][1]}"
    if display_word.page:
        display_word.update()

    return display_word.value


def increment_used_count(displayed_word):
    """英単語が使用された回数を更新する。

    Args:
        displayed_word (str): 表示された英単語。

    Raises:
        Exception: 使用回数の更新に失敗した場合。
    """
    return  # TODO: Debug用
    is_succeeded = _exe_sql_upd(sqls.UpdateStatement.update_used_count, [displayed_word])
    if is_succeeded:
        return

    raise Exception("Failed to update used count.")


def get_data_table_columns(header):
    """DataTableのcolumns向けにリストを整形する関数

    Args:
        header (list[str]): テーブルのヘッダー。

    Returns:
        List[DataColumn]: ヘッダーのリスト。
    """
    return [ft.DataColumn(ft.Text(t)) for t in header]


def get_data_table_rows(data):
    """DataTableのrows向けに2次元リストを整形する関数

    Args:
        data (list[list[any]]): テーブルのデータ。

    Returns:
        List[DataRow]: データのリスト。
    """
    converted_rows = []
    for row in data:
        cells = [ft.DataCell(ft.Text(str(t))) for t in row]
        converted_rows.append(ft.DataRow(cells=cells))
    return converted_rows


def _exe_sql_sel(sql, prm=None) :
    """Selectクエリを実行する関数。

    Args:
        sql (str): SELECTクエリ。
        prm (list[any], optional): クエリのパラメータ。デフォルトはNone。

    Returns:
        Tuple(Tuple(any)): クエリの結果行。
    """
    try :
        # DBコネクション確立(トランザクション開始)
        conn = MySQLdb.connect(
            host    = JSON_DATA['db_connect_info']['host'],
            port    = JSON_DATA['db_connect_info']['port'],
            user    = JSON_DATA['db_connect_info']['user'],
            passwd  = JSON_DATA['db_connect_info']['passwd'],
            charset = JSON_DATA['db_connect_info']['charset'],
            db      = JSON_DATA['db_connect_info']['db_name'])

        with conn.cursor() as cur :
            cur.execute(sql, prm) if prm else cur.execute(sql)
            res = cur.fetchall()

        return res
    except Exception :
        raise
    finally :
        conn.close()


def _exe_sql_upd(sql, prm) :
    """UpdateまたはInsertクエリを実行する関数。

    Args:
        sql (str): UpdateまたはInsertクエリ。
        prm (list[any]): クエリのパラメータ。

    Returns:
        bool: クエリの実行結果。成功した場合はTrue。
    """
    try :
        # DBコネクション確立(トランザクション開始)
        conn = MySQLdb.connect(
            host        = JSON_DATA['db_connect_info']['host'],
            port        = JSON_DATA['db_connect_info']['port'],
            user        = JSON_DATA['db_connect_info']['user'],
            passwd      = JSON_DATA['db_connect_info']['passwd'],
            charset     = JSON_DATA['db_connect_info']['charset'],
            db          = JSON_DATA['db_connect_info']['db_name'],
            client_flag = MULTI_STATEMENTS,
            autocommit  = False)

        with conn.cursor() as cur :
            cur.execute(sql, prm)
        conn.commit()

        return True
    except Exception :
        return False
    finally :
        conn.close()