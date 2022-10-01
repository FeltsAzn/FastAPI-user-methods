from app.models import connection_db


class Database:
    def __init__(self,):
        self.session = connection_db()

    def add(self, table):
        try:
            self.session.add(table)

        except Exception as _ex:
            self.session.rollback()
            raise _ex
        else:
            self.session.commit()
            return True
        finally:
            self.session.close()

    def delete(self, table):
        try:
            self.session.delete(table)
        except Exception as _ex:
            self.session.rollback()
            raise _ex
        else:
            self.session.commit()
            return True
        finally:
            self.session.close()

