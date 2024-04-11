import meraki.aio
import asyncio
import pandas as pd
import config

aiomeraki = meraki.aio.AsyncDashboardAPI(
            config.api_key,
            base_url="https://api.meraki.com/api/v1",
            log_file_prefix=__file__[:-3],
            print_console=True,
            maximum_retries=config.max_retries,
            maximum_concurrent_requests=config.max_requests,
)

async def gather_airmarshal_config(aiomeraki, net):
    air_marshal = await aiomeraki.wireless.getNetworkWirelessAirMarshal(networkId=net['id'])
    return air_marshal, net

async def air_marshal_audit(aiomeraki):
    org_networks = await aiomeraki.organizations.getOrganizationNetworks(
        organizationId=config.org_id,
        total_pages=-1
    )
    audit = []
    get_tasks = []
    for network in org_networks:
        if 'wireless' in network['productTypes']:
            get_tasks.append(gather_airmarshal_config(aiomeraki, network))
    for task in asyncio.as_completed(get_tasks):
        result, network = await task
        for entry in result:
            entry['net_id'] = network['id']
            entry['net_name'] = network['name']
            audit.append(entry)

    audit_df = pd.DataFrame(audit)
    return audit_df

async def main(aiomeraki):
    async with aiomeraki:
        audit_df = await air_marshal_audit(aiomeraki)
    return audit_df

if __name__ == "__main__":
    # -------------------Gather teleworker specific data-------------------
    loop = asyncio.get_event_loop()
    audit_df = loop.run_until_complete(main(aiomeraki))
    audit_df.to_csv(f"./{config.org_id}_air_marshal_audit.csv")
