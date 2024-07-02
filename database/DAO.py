from database.DB_connect import DBConnect


class DAO():
    @staticmethod
    def getAllLocalizations():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct Localization 
                    from classification c """

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["Localization"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getWeightedEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select l1, l2, count(*) as peso
                    from (select c.localization as l1, c2.Localization as l2, i.`Type` as t
                        from classification c, classification c2, interactions i 
                        where c.GeneID != c2.GeneID 
                            and c.localization != c2.Localization 
                            and ((i.GeneID1 = c.geneID and i.GeneID2 = c2.GeneID)
                            or (i.GeneID1 = c2.geneID and i.GeneID2 = c.GeneID))
                        group by l1, l2, t) as loc
                    group by l1, l2"""

        cursor.execute(query, ())

        for row in cursor:
            result.append((row["l1"], row["l2"], row["peso"]))

        cursor.close()
        conn.close()
        return result
