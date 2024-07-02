from database.DB_connect import DBConnect


class DAO():
    @staticmethod
    def getChromosomes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = """ select distinct Chromosome 
                    from genes where Chromosome != 0  """

        cursor.execute(query)

        for row in cursor:
            result.append(row[0])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getEdgeTo(node1, node2):
        conn = DBConnect.get_connection()

        result = [False, 0]

        cursor = conn.cursor()
        query = """select distinct g1.Chromosome, g2.Chromosome, i.GeneID1, i.GeneID2 , i.Expression_Corr as ec
                from genes g1, genes g2, interactions i  
                where g1.Chromosome = %s and g2.Chromosome = %s and
                g2.GeneID = i.GeneID2 and g1.GeneID = i.GeneID1 """

        cursor.execute(query, (node1, node2))

        for row in cursor:
            result[0] = True
            result[1] += row[4]

        cursor.close()
        conn.close()

        return result
