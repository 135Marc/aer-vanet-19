import time
from adhoc_pdu import PDU
from adhoc_table import Table

def hello(zone, name, pdu, routing_table):
    # Get pdu data
    source = pdu.getSource()
    table = pdu.getTable()
    content = pdu.getDirective()

    # Timestamp do momento da receção do pdu
    timestamp = time.time()

    # Adicionar o originador do pdu aos vizinhos diretos
    routing_table.addNeighbour(source, content, timestamp)

    # Adicionar o originador do pdu na tabela geral
    routing_table.addNode(source, source, content, timestamp)

    # Juntar a tabelas geral e a tabela de vizinhos do originador do pdu 
    routing_table.mergeTable(zone, source, name,  table, timestamp)

