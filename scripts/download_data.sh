set -euo pipefail

mkdir -p data/raw
uv run kaggle competitions download -c home-credit-default-risk -p data/raw
cd data/raw
unzip -o home-credit-default-risk.zip
rm home-credit-default-risk.zip
