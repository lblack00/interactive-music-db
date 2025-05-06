from db_utils import db_utils

class forum:
    db = db_utils(dbname='test_users_db', user='postgres', 
                  password='postgres', host='users_db', port='5434')

    @staticmethod
    def get_all_threads(category=None, limit=20, offset=0):
        if category:
            query = """
                SELECT 
                    t.id, 
                    t.title, 
                    t.category,
                    t.created_at, 
                    t.updated_at,
                    t.is_edited,
                    u.id as author_id, 
                    u.username as author_name,
                        (SELECT COUNT(*)
                         FROM forum_replies r
                         WHERE r.thread_id = t.id AND r.is_deleted = FALSE) as reply_count
                FROM forum_threads t
                JOIN users u ON t.user_id = u.id
                WHERE t.is_deleted = FALSE AND t.category = %s
                ORDER BY t.created_at DESC
                LIMIT %s OFFSET %s;
            """
            return forum.db.read_data(query, (category, limit, offset))
        else:
            query = """
                SELECT 
                    t.id, 
                    t.title,
                    t.category,
                    t.created_at, 
                    t.updated_at,
                    t.is_edited,
                    u.id as author_id, 
                    u.username as author_name,
                        (SELECT COUNT(*)
                         FROM forum_replies r
                         WHERE r.thread_id = t.id AND r.is_deleted = FALSE) as reply_count
                FROM forum_threads t
                JOIN users u ON t.user_id = u.id
                WHERE t.is_deleted = FALSE
                ORDER BY t.created_at DESC
                LIMIT %s OFFSET %s;
            """
            return forum.db.read_data(query, (limit, offset))
    
    @staticmethod
    def get_categories():
        query = """
            SELECT DISTINCT category FROM forum_threads
            WHERE is_deleted = FALSE
            ORDER BY category;
        """
        return forum.db.read_data(query)
    
    @staticmethod
    def create_thread(user_id, title, content, category):
        query = """
            INSERT INTO forum_threads (user_id, title, content, category, created_at)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING id;
        """
        return forum.db.mutate_data(query, (user_id, title, content, category))
    
    @staticmethod
    def get_thread(thread_id):
        query = """
            SELECT 
                t.id,
                t.title,
                t.content,
                t.category,
                t.created_at,
                t.updated_at,
                t.is_deleted,
                u.id as author_id, 
                u.username as author_name
            FROM forum_threads t
            JOIN users u ON t.user_id = u.id
            WHERE t.id = %s AND t.is_deleted = FALSE;
        """
        return forum.db.read_data(query, (thread_id,))
    
    @staticmethod
    def get_thread_replies(thread_id):
        query = """
            SELECT 
                r.id, 
                r.content, 
                r.created_at, 
                r.updated_at,
                r.parent_id,
                r.is_edited,
                r.is_deleted,
                u.id as author_id, 
                u.username as author_name
            FROM forum_replies r
            JOIN users u ON r.user_id = u.id
            WHERE r.thread_id = %s
            ORDER BY r.created_at ASC;
        """
        return forum.db.read_data(query, (thread_id,))

    @staticmethod
    def get_thread_reply(reply_id):
        query = """
            SELECT
                r.id,
                r.thread_id,
                r.content,
                r.parent_id,
                r.created_at,
                r.is_edited,
                r.is_deleted,
                u.username as author_name,
                t.title
            FROM forum_replies r
            JOIN users u
            ON r.user_id = u.id
            JOIN forum_threads t
            ON r.thread_id = t.id
            WHERE r.id = %s;
        """
        return forum.db.read_data(query, (reply_id,))
    
    @staticmethod
    def add_reply(user_id, thread_id, content, parent_id=None):
        query = """
            INSERT INTO forum_replies (user_id, thread_id, content, parent_id, created_at)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING id;
        """
        return forum.db.mutate_data(query, (user_id, thread_id, content, parent_id))
    
    @staticmethod
    def update_reply(reply_id, content, user_id):
        query = """
            UPDATE forum_replies
            SET content = %s, updated_at = CURRENT_TIMESTAMP, is_edited = TRUE
            WHERE id = %s AND user_id = %s
            RETURNING id;
        """
        return forum.db.mutate_data(query, (content, reply_id, user_id))
    
    @staticmethod
    def delete_reply(reply_id, user_id):
        query = """
            UPDATE forum_replies
            SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND user_id = %s
            RETURNING id;
        """
        return forum.db.mutate_data(query, (reply_id, user_id))
    
    @staticmethod
    def update_thread(thread_id, content, user_id):
        query = """
            UPDATE forum_threads
            SET content = %s, updated_at = CURRENT_TIMESTAMP, is_edited = TRUE
            WHERE id = %s AND user_id = %s
            RETURNING id;
        """
        return forum.db.mutate_data(query, (content, thread_id, user_id))
    
    @staticmethod
    def delete_thread(thread_id, user_id):
        query = """
            UPDATE forum_threads
            SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND user_id = %s
            RETURNING id;
        """
        return forum.db.mutate_data(query, (thread_id, user_id))
    
    @staticmethod
    def report_item(user_id, item_type, item_id, reason):
        query = """
            INSERT INTO forum_reports (user_id, item_type, item_id, reason, created_at)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING id;
        """
        return forum.db.mutate_data(query, (user_id, item_type, item_id, reason))

    @staticmethod
    def get_reports():
        query = """
            SELECT *
            FROM forum_reports
            ORDER BY created_at DESC;
        """
        reports = forum.db.read_data(query)
        content = []
        for report in reports:
            if report['item_type'] == 'thread':
                thread_query = """
                    SELECT 
                        t.id,
                        t.title,
                        t.content,
                        t.category,
                        t.created_at,
                        t.updated_at,
                        t.is_deleted,
                        u.id as author_id, 
                        u.username as author_name
                    FROM forum_threads t
                    JOIN users u ON t.user_id = u.id
                    WHERE t.id = %s;
                """
                thread_content = forum.db.read_data(thread_query, (report['item_id'],))
                if thread_content and len(thread_content) > 0:
                    content.append(thread_content[0])
            else:
                reply_content = forum.get_thread_reply(report['item_id'])
                if reply_content and len(reply_content) > 0:
                    content.append(reply_content[0])

        return {
            'reports': reports,
            'content': content
        }

    @staticmethod
    def resolve_report(report_id, is_resolved):
        query = """
            UPDATE forum_reports fr
            SET resolved = %s, resolved_by = %s, resolved_at = CURRENT_TIMESTAMP
            WHERE id = %s;
        """
        return forum.db.mutate_data(query, (is_resolved, session['user']['id'], report_id))

    @staticmethod
    def delete_report_reply(reply_id, is_deleted):
        query = """
            UPDATE forum_replies
            SET is_deleted = %s
            WHERE id = %s;
        """
        return forum.db.mutate_data(query, (is_deleted, reply_id))

    @staticmethod
    def delete_report_thread(thread_id, is_deleted):
        query = """
            UPDATE forum_threads
            SET is_deleted = %s
            WHERE id = %s;
        """
        return forum.db.mutate_data(query, (is_deleted, thread_id))

    @staticmethod
    def add_reference(item_type, item_id, reference_type, reference_id, name):
        query = """
            INSERT INTO forum_references(item_type, item_id, reference_type, reference_id, created_at, name)
            VALUES(%s, %s, %s, %s, CURRENT_TIMESTAMP, %s)
            RETURNING id;
        """
        return forum.db.mutate_data(query, (item_type, item_id, reference_type, reference_id, name,))

    @staticmethod
    def delete_reference(_id, reference_id):
        query = """
            DELETE FROM forum_references fr
            WHERE id=%s AND reference_id=%s
            RETURNING id;
        """
        return forum.db.mutate_data(query, (_id, reference_id,))

    @staticmethod
    def get_thread_references(item_id):
        query = """
            SELECT
                *
            FROM forum_references fr
            WHERE fr.item_id = %s;
        """
        return forum.db.read_data(query, (item_id,))

    @staticmethod
    def get_reference(reference_id):
        query = "SELECT * FROM forum_references WHERE id=%s;"
        return forum.db.read_data(query, (reference_id,))

    @classmethod
    def set_db_for_testing(cls, dbname='test_users_db', user='postgres', 
                         password='postgres', host='localhost', port='5434'):
        cls.db = db_utils(dbname=dbname, user=user, password=password, 
                         host=host, port=port)
        
    @classmethod
    def reset_db(cls):
        cls.db = db_utils(dbname='discogs_db', user='postgres')