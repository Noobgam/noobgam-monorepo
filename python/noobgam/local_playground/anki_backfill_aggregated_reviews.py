import os
import random

import mysql.connector

if __name__ == "__main__":
    m = mysql.connector.connect(
        host="mysql.noobgam.com",
        user="noobgam",
        password=os.environ["NOOBGAM_MYSQL_PASSWORD"],
        database="noobgam_personal",
    )
    cursor = m.cursor(dictionary=True)
    cursor.execute("SELECT distinct date FROM language_learning_view")
    dates = [c["date"] for c in cursor.fetchall()]
    random.shuffle(dates)
    for ts_seconds in dates:
        # see grafana
        query = f"""
            WITH aggregated_reviews AS (
              SELECT
                nc.noteId,
                MAX(ar.previousInterval) AS learningInterval
              FROM anki_reviews ar
              INNER JOIN note_cards nc ON ar.cardId = nc.cardId
              WHERE ar.reviewId < 1 AND ar.previousInterval > 0
              GROUP BY nc.noteId
            ),
            tag_aggregations AS (
              SELECT
                nt.tag,
                SUM(IF(learningInterval > 200, 1, 0)) AS learned,
                SUM(IF(learningInterval > 10 AND learningInterval <= 200, 1, 0)) AS learning,
                SUM(IF(learningInterval > 0 AND learningInterval <= 10, 1, 0)) AS discovered
              FROM aggregated_reviews
              INNER JOIN note_tags nt ON aggregated_reviews.noteId = nt.noteId
              WHERE nt.tag IN ('language_german', 'language_japanese')
              GROUP BY nt.tag
            )
            SELECT
              ta.tag,
              ta.learned,
              ta.learning,
              ta.discovered
            FROM tag_aggregations ta;
        """
        cursor.execute(query)
        print(cursor.fetchall())
