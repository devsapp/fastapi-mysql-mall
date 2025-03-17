deploy-dev:
	s deploy -y 

deploy:
	s deploy -y -t s_hz.yaml 
	s deploy -y -t s_bj.yaml 