# brdf-wrapper

# Usage
## Docker
```
docker build -t brdf:latest -f Dockerfile .
docker run --rm -itd --name=brdf -v ~/projects/brdf-wrapper:/brdf-wrapper brdf:latest
docker exec -it brdf bash
```

## Rendering sphere
```
cd /brdf-wrapper/brdf
c++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` brdf.cpp -o brdf`python3-config --extension-suffix`
cd ..
python3 download_bsdf.py --obj_file supp_info obj_isotropic.txt --out_dir ./data/isotropic
python3 render_sphere.py --brdf_dir data/isotropic/ --obj_file supp_info/obj_isotropic.txt --obj_range 0 1 --N_map_file supp_info/N_map_100.npy --mask_file supp_info/mask_100.png --L_file supp_info/L_10.txt --out_dir ./output/isotropic --n_jobs 1
```
