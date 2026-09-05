"""Offline consistency checks for preserved primary-source responses.

This checks RPC-reported transaction/block/receipt relationships. It does not
claim local Ethereum consensus validation or ECDSA signature recovery.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text(encoding='utf8'))['result']
checks={}
txs={}
for label,tname,bname,rname in [
 ('r1','r1_rpc_response.json','r1_block_response.json','r1_transaction_receipt.json'),
 ('r2','r2_rpc_response.json','r2_block_verified.json','r2_receipt_verified.json'),
 ('whitehat','whitehat_rpc_response.json','whitehat_block_response.json','whitehat_transaction_receipt.json'),
 ('creation','creation_corrected_corpus_transaction.json','creation_corrected_corpus_block.json','creation_corrected_corpus_receipt.json')]:
 tx,block,receipt=read(tname),read(bname),read(rname)
 txs[label]=tx
 checks[label]={
  'transaction_hash':tx['hash'],
  'transaction_block_hash_equals_block':tx['blockHash']==block['hash'],
  'transaction_block_number_equals_block':tx['blockNumber']==block['number'],
  'transaction_listed_in_block':tx['hash'] in block['transactions'],
  'receipt_hash_equals_transaction':receipt['transactionHash']==tx['hash'],
  'receipt_block_hash_equals_transaction':receipt['blockHash']==tx['blockHash'],
  'receipt_status_success':receipt['status']=='0x1',
  'receipt_sender_equals_transaction':receipt['from']==tx['from'],
  'from':tx['from'],'to':tx['to'],'timestamp_utc':datetime.fromtimestamp(int(block['timestamp'],16),timezone.utc).isoformat(),
 }
checks['source']={'hex_sha256':hashlib.sha256((ROOT/'paste_raw.txt').read_bytes()).hexdigest(),'announcement_input_exact_slug':bytes.fromhex(txs['r2']['input'][2:])==b'zrUfKaKV','announcement_has_additional_input_bytes':len(bytes.fromhex(txs['r2']['input'][2:]))!=8}
checks['attribution']={
 'creator_receipt_contract_address':read('creation_corrected_corpus_receipt.json')['contractAddress'],
 'creator_receipt_is_caw':read('creation_corrected_corpus_receipt.json')['contractAddress']=='0xf3b9569f82b18aef890de263b84189bd33ebe452',
 'whitehat_link_sender_equals_contract_creator':txs['whitehat']['from']==txs['creation']['from'],
 'r2_sender_equals_contract_creator':txs['r2']['from']==txs['creation']['from'],
 'r1_sender_equals_r2_sender':txs['r1']['from']==txs['r2']['from'],
 'r1_input_exact_image_identifier':bytes.fromhex(txs['r1']['input'][2:])==b'58bZfQ1',
 'shared_human_controller_established':False,
 'scope':'Address equality and RPC-reported inclusion only; no inference about who controls different addresses.'
}
for label in ['r1','r2','whitehat','creation']:
 for key,value in checks[label].items():
  if key.startswith(('transaction_block_','transaction_listed_','receipt_')):assert value is True,(label,key,value)
assert checks['source']['announcement_input_exact_slug']
assert checks['attribution']['creator_receipt_is_caw']
assert checks['attribution']['whitehat_link_sender_equals_contract_creator']
assert not checks['attribution']['r2_sender_equals_contract_creator']
assert checks['attribution']['r1_sender_equals_r2_sender']
assert checks['attribution']['r1_input_exact_image_identifier']
checks['all_assertions_passed']=True
(ROOT/'endpoint_verification.json').write_text(json.dumps(checks,indent=2),encoding='utf8')
print(json.dumps(checks,indent=2))
