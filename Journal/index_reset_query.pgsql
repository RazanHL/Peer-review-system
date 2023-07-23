
SELECT setval(pg_get_serial_sequence('"auth_permission"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "auth_permission";
SELECT setval(pg_get_serial_sequence('"auth_group_permissions"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "auth_group_permissions";
SELECT setval(pg_get_serial_sequence('"auth_group"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "auth_group";
SELECT setval(pg_get_serial_sequence('"auth_user_groups"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "auth_user_groups";
SELECT setval(pg_get_serial_sequence('"auth_user_user_permissions"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "auth_user_user_permissions";
SELECT setval(pg_get_serial_sequence('"auth_user"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "auth_user";


SELECT setval(pg_get_serial_sequence('"articles_article"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "articles_article";
SELECT setval(pg_get_serial_sequence('"articles_article_author"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "articles_article_author";
SELECT setval(pg_get_serial_sequence('"articles_article_reviewer"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "articles_article_reviewer";
SELECT setval(pg_get_serial_sequence('"articles_article_scope"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "articles_article_scope";
SELECT setval(pg_get_serial_sequence('"articles_reviewer_publication"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "articles_reviewer_publication";
SELECT setval(pg_get_serial_sequence('"articles_reviewer_publication_scope"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "articles_reviewer_publication_scope";
SELECT setval(pg_get_serial_sequence('"articles_subject"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "articles_subject";
SELECT setval(pg_get_serial_sequence('"profiles_profiles"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "profiles_profiles";
SELECT setval(pg_get_serial_sequence('"articles_reviewer_publication"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "articles_reviewer_publication";
SELECT setval(pg_get_serial_sequence('"articles_author_order"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "articles_author_order";
