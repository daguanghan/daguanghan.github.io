#!/bin/bash
# Cloudflare DNS Update Script for GitHub Pages

set -e

# Load credentials
source "$(dirname "$0")/.cloudflare.env"

# GitHub Pages IPs
GITHUB_IPS=(
    "185.199.108.153"
    "185.199.109.153"
    "185.199.110.153"
    "185.199.111.153"
)

echo "Updating Cloudflare DNS for $DOMAIN..."

# Function to update or create DNS record
update_record() {
    local name=$1
    local content=$2
    local type=${3:-A}
    local proxied=${4:-false}
    
    # Check if record exists
    existing=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records?name=$name" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json")
    
    record_id=$(echo "$existing" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    if [ -n "$record_id" ]; then
        # Update existing record
        curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records/$record_id" \
            -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
            -H "Content-Type: application/json" \
            --data "{\"type\":\"$type\",\"name\":\"$name\",\"content\":\"$content\",\"proxied\":$proxied}" > /dev/null
        echo "Updated $name -> $content"
    else
        # Create new record
        curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
            -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
            -H "Content-Type: application/json" \
            --data "{\"type\":\"$type\",\"name\":\"$name\",\"content\":\"$content\",\"proxied\":$proxied}" > /dev/null
        echo "Created $name -> $content"
    fi
}

# Update A records for root domain
for ip in "${GITHUB_IPS[@]}"; do
    update_record "$DOMAIN" "$ip" "A" "false"
done

# Update CNAME for www
update_record "www.$DOMAIN" "$DOMAIN" "CNAME" "false"

echo "DNS update completed!"
echo "Waiting for propagation..."
sleep 2

# Verify
echo "Current DNS records:"
dig +short $DOMAIN

echo ""
echo "Done! Your site should be accessible at https://$DOMAIN soon."