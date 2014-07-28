taxon = """
    SELECT t1.taxonid, t1.name, t1.fullname, t1.nodenumber, t1.highestchildnodenumber,
    (
        SELECT COUNT(t.taxonid) FROM taxon t WHERE t.parentid = t1.taxonid
    ) AS children,
    (
        SELECT COUNT(DISTINCT det.collectionobjectid)
        FROM determination det, taxon t
        WHERE det.taxonid = t.taxonid
        AND t.nodenumber BETWEEN t1.nodenumber AND t1.highestchildnodenumber
        AND det.collectionmemberid = %s AND det.iscurrent
    ) AS allcos,
    (
        SELECT COUNT(DISTINCT det.collectionobjectid)
        FROM determination det
        WHERE det.taxonid = t1.taxonid
        AND det.collectionmemberid = %s AND det.iscurrent
    ) AS directcos
    FROM taxon t1
    WHERE t1.parentid = %s
    ORDER BY t1.name
"""

geography = """
    SELECT g1.geographyid, g1.name, g1.fullname, g1.nodenumber, g1.highestchildnodenumber,
    (
        SELECT COUNT(g.geographyid) FROM geography g WHERE g.parentid = g1.geographyid
    ) AS children,
    (
        SELECT COUNT(DISTINCT co.collectionobjectid)
        FROM collectionobject co, collectingevent ce, locality l, geography g
        WHERE co.collectingeventid = ce.collectingeventid
        AND ce.localityid = l.localityid
        AND l.geographyid = g.geographyid
        AND g.nodenumber BETWEEN g1.nodenumber AND g1.highestchildnodenumber
        AND co.collectionmemberid = %s
    ) AS allcos,
    (
        SELECT COUNT(DISTINCT co.collectionobjectid)
        FROM collectionobject co, collectingevent ce, locality l
        WHERE co.collectingeventid = ce.collectingeventid
        AND ce.localityid = l.localityid
        AND l.geographyid = g1.geographyid
        AND co.collectionmemberid = %s
    ) AS directcos
    FROM geography g1
    WHERE g1.parentid = %s
    ORDER BY g1.name
"""

storage = """
    SELECT s1.storageid, s1.name, s1.fullname, s1.nodenumber, s1.highestchildnodenumber,
    (
        SELECT COUNT(s.storageid) FROM storage s WHERE s.parentid = s1.storageid
    ) AS children,
    (
        SELECT COUNT(DISTINCT prep.collectionobjectid)
        FROM preparation prep, storage s
        WHERE prep.storageid = s.storageid
        AND s.nodenumber BETWEEN s1.nodenumber AND s1.highestchildnodenumber
        AND prep.collectionmemberid = %s
    ) AS allcos,
    (
        SELECT COUNT(DISTINCT prep.collectionobjectid)
        FROM preparation prep
        WHERE prep.storageid = s1.storageid
        AND prep.collectionmemberid = %s
    ) AS directcos
    FROM storage s1
    WHERE s1.parentid = %s
    ORDER BY s1.name
"""

geologictimeperiod = """
    SELECT g1.geologictimeperiodid, g1.name, g1.fullname, g1.nodenumber, g1.highestchildnodenumber,
    (
        SELECT COUNT(g.geologictimeperiodid) FROM geologictimeperiod g WHERE g.parentid = g1.geologictimeperiodid
    ) AS children,
    (
        SELECT COUNT(DISTINCT co.collectionobjectid)
        FROM collectionobject co, paleocontext pc, geologictimeperiod g
        WHERE co.paleocontextid = pc.paleocontextid
        AND pc.chronosstratid = g.geologictimeperiodid
        AND g.nodenumber BETWEEN g1.nodenumber AND g1.highestchildnodenumber
        AND co.collectionmemberid = %s
    ) AS allcos,
    (
        SELECT COUNT(DISTINCT co.collectionobjectid)
        FROM collectionobject co, paleocontext pc
        WHERE co.paleocontextid = pc.paleocontextid
        AND pc.chronosstratid = g1.geologictimeperiodid
        AND co.collectionmemberid = %s
    ) AS directcos
    FROM geologictimeperiod g1
    WHERE g1.parentid = %s
    ORDER BY g1.name
"""

lithostrat = """
    SELECT ls1.lithostratid, ls1.name, ls1.fullname, ls1.nodenumber, ls1.highestchildnodenumber,
    (
        SELECT COUNT(ls.lithostratid) FROM lithostrat ls WHERE ls.parentid = ls1.lithostratid
    ) AS children,
    (
        SELECT COUNT(DISTINCT co.collectionobjectid)
        FROM collectionobject co, paleocontext pc, lithostrat ls
        WHERE co.paleocontextid = pc.paleocontextid
        AND pc.chronosstratid = ls.lithostratid
        AND ls.nodenumber BETWEEN ls1.nodenumber AND ls1.highestchildnodenumber
        AND co.collectionmemberid = %s
    ) AS allcos,
    (
        SELECT COUNT(DISTINCT co.collectionobjectid)
        FROM collectionobject co, paleocontext pc
        WHERE co.paleocontextid = pc.paleocontextid
        AND pc.chronosstratid = ls1.lithostratid
        AND co.collectionmemberid = %s
    ) AS directcos
    FROM lithostrat ls1
    WHERE ls1.parentid = %s
    ORDER BY ls1.name
"""
