count=0
while [ $count -le 50 ]; do
  kiss_icp_pipeline /home/ohmpr/data/datasets/av2/train-006/ --config config/basic.yaml --dataloader argoverse2 --log_id $count -v
  ((count++))
done