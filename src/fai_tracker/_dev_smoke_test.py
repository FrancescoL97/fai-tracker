from fai_tracker.db import init_db
from fai_tracker.settings import default_settings

if __name__ == "__main__":
    s = default_settings()
    init_db(s.db_path)
    print("DB created at:", s.db_path)
    print("Active root:", s.active_root)
    print("Archive root:", s.archive_root)
