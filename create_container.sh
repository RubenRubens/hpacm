podman build -t hpacm_img .

podman pod create --name hpacm_pod \
	--publish 5432:5432 \
	--publish 8000:8000

podman run --name postgres_hpacm \
	--pod hpacm_pod \
	-e POSTGRES_USER=$(cat postgres_user) \
	-e POSTGRES_PASSWORD=$(cat postgres_psswd) \
	-e POSTGRES_DB=hpacm_db \
	-d postgres

podman run --name django_hpacm \
	--pod hpacm_pod \
	--volume $(pwd)/src:/app/src:Z \
	-it hpacm_img sh
