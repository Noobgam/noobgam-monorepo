import asyncio
import os

import aiomysql
from tqdm import tqdm


async def insert_anki(pool, timestamp: int):
    async with pool.acquire() as connection:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            sub_query = f"""
                 WITH aggregated_reviews AS (
                  SELECT
                    nc.noteId,
                    MAX(ar.previousInterval) AS learningInterval
                  FROM anki_reviews ar
                  INNER JOIN note_cards nc ON ar.cardId = nc.cardId
                  WHERE ar.reviewId < {timestamp} DIV 300000 * 300000 AND ar.previousInterval > 0
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
                ),
                statuses AS (
                    SELECT 'DISCOVERED' AS srs_group, discovered AS count, nt.tag
                    FROM tag_aggregations nt
                    UNION ALL
                    SELECT 'LEARNING' as srs_group, learning, nt.tag
                    FROM tag_aggregations nt
                    UNION ALL
                    SELECT 'LEARNED' as srs_group, learned, nt.tag
                    FROM tag_aggregations nt
                )
                SELECT
                    ({timestamp} DIV 300000 * 300000) AS date,
                    'anki_reviews' AS origin,
                    IF(statuses.tag = 'language_japanese', 'japanese', 'german') AS language,
                    statuses.srs_group,
                    statuses.count as value
                FROM statuses
                ORDER BY language, srs_group DESC
            """
            anki_query = f"""
                INSERT INTO language_learning_view_5min (date, origin, language, srs_group, value)
                ({sub_query})
                ON DUPLICATE KEY UPDATE value = VALUES(value)
            """
            await cursor.execute(anki_query)
            return cursor.rowcount


async def insert_wanikani(pool, timestamp: int):
    async with pool.acquire() as connection:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            sub_query = f"""
            SELECT
                LL.date DIV 300000 * 300000 as date,
                LL.origin,
                LL.language,
                LL.srs_group,
                SUM(LL.`count`) as value
            FROM
                language_learning LL
            INNER JOIN (
                SELECT
                    origin,
                    language,
                    srs_group,
                    MAX(date) AS max_date
                FROM
                    language_learning
                WHERE
                    date < ({timestamp} DIV 300000 * 300000 + 300000)
                    AND date >= ({timestamp} DIV 300000 * 300000)
                GROUP BY
                    origin,
                    language,
                    srs_group
            ) AS MaxDates ON LL.origin = MaxDates.origin
                          AND LL.language = MaxDates.language
                          AND LL.srs_group = MaxDates.srs_group
                          AND LL.date = MaxDates.max_date
            WHERE
                LL.date < ({timestamp} DIV 300000 * 300000 + 300000)
                AND LL.date >= ({timestamp} DIV 300000 * 300000)
            GROUP BY
                LL.date,
                LL.origin,
                LL.language,
                LL.srs_group
            """
            wanikani_query = f"""
            INSERT INTO language_learning_view_5min (date, origin, language, srs_group, value)
            ({sub_query})
            ON DUPLICATE KEY UPDATE value = VALUES(value);
            """
            await cursor.execute(wanikani_query)
            return cursor.rowcount


async def main():
    password = os.getenv("NOOBGAM_MYSQL_PASSWORD")
    pool = await aiomysql.create_pool(
        host="mysql.noobgam.com",
        user="noobgam",
        password=password,
        db="noobgam_personal",
        autocommit=True,
    )

    async with pool.acquire() as connection:
        cursor = await connection.cursor(aiomysql.DictCursor)
        await cursor.execute(
            "SELECT MIN(date) as mn, MAX(date) as mx FROM language_learning_view"
        )
        data = await cursor.fetchone()
    l, r = data["mn"], data["mx"]
    step = 300_000
    # step = r - l

    tasks = []
    for cr in range(r, l, -step):
        tasks.append(asyncio.create_task(insert_anki(pool, cr)))
        tasks.append(asyncio.create_task(insert_wanikani(pool, cr)))

    pbar = tqdm(total=len(tasks))

    for coro in asyncio.as_completed(tasks):
        await coro
        pbar.update(1)

    pbar.close()

    pool.close()


if __name__ == "__main__":
    asyncio.run(main())
