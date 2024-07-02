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

        result = [0]

        cursor = conn.cursor()
        query = """select distinct g1.Chromosome, g2.Chromosome, i.GeneID1, i.GeneID2 , i.Expression_Corr as ec
                from genes g1, genes g2, interactions i  
                where g1.Chromosome = %s and g2.Chromosome = %s and
                g2.GeneID = i.GeneID2 and g1.GeneID = i.GeneID1 """

        cursor.execute(query, (node1, node2))

        for row in cursor:
            result[0] += row[4]

        cursor.close()
        conn.close()

        return result

    # OPPURE CREO DIRETTAMENTE LISTA DI TUPLE ARCO CON PESO
    @staticmethod
    def getWeightedEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = """select c1,c2, sum(p) as peso
                    from(
                        select g.chromosome as c1, g2.Chromosome as c2, i.GeneID1, i.GeneID2, i.Expression_Corr as p
                        from genes g , genes g2 , interactions i 
                        where g.chromosome != g2.Chromosome 
                            and g.geneid=i.GeneID1 
                            and g2.geneid=i.GeneID2  
                            and g.chromosome!=0 
                            and g2.chromosome!=0
                        group by g.chromosome, g2.Chromosome, i.GeneID1, i.GeneID2) as gruppi
                    group by c1,c2"""

        cursor.execute(query, )

        for row in cursor:
            result.append((row[0],row[1],row[2]))

        cursor.close()
        conn.close()

        return result
