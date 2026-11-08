#!/bin/sh
# Runs inside the "tests" container. Each file gets its own pytest process:
# Playwright's sync API leaves an event loop running, and the channels test is
# order-sensitive under pytest-django's DB blocker (see README "Known caveats").
set -e
python manage.py migrate -v0
python - <<'PY'
import boto3
s3 = boto3.client("s3", endpoint_url="http://s3:8333", aws_access_key_id="check",
                  aws_secret_access_key="check", region_name="us-east-1")
if "check" not in [b["Name"] for b in s3.list_buckets().get("Buckets", [])]:
    s3.create_bucket(Bucket="check")
PY
for f in tests/test_core.py tests/test_services.py tests/test_browser.py; do
  echo "== $f (broker: $BROKER_URL)"
  pytest -q -p no:cacheprovider "$f"
done
