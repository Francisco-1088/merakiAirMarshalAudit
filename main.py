import meraki
import pandas as pd
import config

dashboard = meraki.DashboardAPI(api_key=config.api_key, maximum_retries=100)

networks = dashboard.organizations.getOrganizationNetworks(config.org_id)

audit = []

for net in networks:
    if 'wireless' in net['productTypes']:
        air_marshal = dashboard.wireless.getNetworkWirelessAirMarshal(networkId=net['id'])
        for entry in air_marshal:
            entry['net_id'] = net['id']
            entry['net_name'] = net['name']
            audit.append(entry)

audit_df = pd.DataFrame(audit)
audit_df.to_csv(f"./{config.org_id}_air_marshal_audit.csv")