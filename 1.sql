INSERT INTO INPPNS_D.TB_PNPH_ACNOEN
SELECT -- 종합수익 머시기 조회 - 자체
       a.ACNO
     , b.ITG_BRNO
     , a.ACITM_BRNO
     , SUM(a.AVBAMT)
     , SUM(a.EOM_BALAMT)
     , '~'
     , '~'
     , SYSDATE
     , '~' /* 이것들은 Audit용 컬럼들 */
     , '~'
     , SYSDATE
  FROM INPPNS_D.TB_PNFH_ACNT a
     , INPPNS_D.TB_PNPH_CMPSENBRBAS b
 WHERE a.CRDT = #{CRDT}
   AND b.CRDT= a.CRDT
   AND b.CMPS_EN_MNGM_BRNO = a.CMPS_EN_MNGM_BRNO
   AND NOT b.CRDT = '20250101'
 GROUP BY a.ACNO
        , b.ITG_BRNO
        , a.ACITM_BRNO
