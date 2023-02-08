from blockchain.utils.get_w3 import get_w3
from blockchain.utils.contract_tools import get_sensor_contract, load_sensor_contract_address

if __name__ == "__main__":
    w3 = get_w3()
    contract_address = load_sensor_contract_address()
    contract, w3 = get_sensor_contract(w3, contract_address)
    event_filter = contract.events.AddedData.create_filter(fromBlock='latest')


    def handle_event(event):
        msg = event['args']['message']
        sensor_data = event['args']['sensor_data'].decode()
        index = event['args']['index']
        print(index, msg + ':', sensor_data)


    print('Running event-handler for "AddedData" events...')
    while True:
        events = event_filter.get_new_entries()
        for e in events:
            handle_event(e)
