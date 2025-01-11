class SelectStatement() :
    get_words = '''
        SELECT
            id,
            word_en,
            word_ja,
            level,
            used_count
        FROM mst_words
        WHERE level = %s
            AND used_count = 0
            AND delete_flag = 0;
        '''


class UpdateStatement() :
    update_used_count = '''
        UPDATE mst_words
        SET used_count = used_count + 1,
            update_user = "game player",
            update_datetime = CURRENT_TIMESTAMP()
        WHERE word_en = %s;
        '''
