import os
import logging
import cloudflare


def create_tld_policy(tld_list: str):
        
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("main")

    # Define file paths
    name_prefix = f"[CFPihole] Block TLDs"
       
    # delete the policy
    cf_policies = cloudflare.get_firewall_policies(name_prefix)

    if len(cf_policies) > 0:
        cloudflare.delete_firewall_policy(cf_policies[0]["id"])

    if len(tld_list) != 0:
        # get the gateway policies
        cf_policies = cloudflare.get_firewall_policies(name_prefix)

        logger.info(f"Number of policies in Cloudflare: {len(cf_policies)}")

        regex_tld = (
            "[.]("
            + tld_list.replace(".", "|").lstrip("|").replace("\n", "")
            + ")$"
        )

        # setup the gateway policy
        if len(cf_policies) == 0:
            logger.info("Creating firewall policy")

            cf_policies = cloudflare.create_gateway_policy_tld(
                f"{name_prefix}", regex_tld
            )

        elif len(cf_policies) != 1:
            logger.error("More than one firewall policy found")

            raise Exception("More than one firewall policy found")

        else:
            logger.info("Updating firewall policy")

            cloudflare.update_gateway_policy_tld(
                f"{name_prefix}", cf_policies[0]["id"], regex_tld
            )

        logger.info(f"\033[92m Done\033[0;0m")

    else:
        logger.info(f"033[0;31;97m tldlist.txt is empty, deleting\033[0;0m")
