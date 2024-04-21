import asyncio
import firebirdsql
from datetime import datetime

data_formatada_hoje = datetime.now().strftime('%d.%m.%Y')

async def connect_and_select_last_row_id():
    conn = await asyncio.to_thread(
        firebirdsql.connect,
        host='localhost',  # or '127.0.0.1'
        database='C:/Fiorilli/SIA7/SGB_DADOS/SIADADOS.FDB',
        user='fscsia',
        password='csfais'
    )
    
    try:
        cur = await asyncio.to_thread(conn.cursor)
        await asyncio.to_thread(cur.execute, "SELECT MAX(cod_lte) FROM fi_lote")
        last_row_id = await asyncio.to_thread(cur.fetchone)
        print("Ultimo ID:", last_row_id[0])
        
        novo_id = last_row_id[0] + 1        
        # Now we get the last id and insert a new id with the next number
        await asyncio.to_thread(cur.execute, "INSERT INTO fi_lote (COD_EMP_LTE, COD_LTE, DATA_LTE, QTDE_LTE, VRTOTAL_LTE, BVRTOTAL_LTE, LOGIN_INC_LTE, DTA_INC_LTE, LOGIN_ALT_LTE, DTA_ALT_LTE, SOBXMANUAL_LTE, SOCOMPENSACAO_LTE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                  (1, novo_id, data_formatada_hoje, 999, 0, 0, 'SISTEMA', data_formatada_hoje, None, None, None, None))
        # Commit the transaction
        await asyncio.to_thread(conn.commit)
        print(f"Novo ID {last_row_id[0]+1} foi criado com sucesso.")
        
    finally:
        await asyncio.to_thread(conn.close)

async def main():
    await connect_and_select_last_row_id()

asyncio.run(main())
