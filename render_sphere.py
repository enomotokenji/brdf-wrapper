import os
import sys
import argparse
import cv2
import numpy as np
import shutil
from tqdm import tqdm
from joblib import Parallel, delayed

from brdf.brdf import BRDF


def render(i, brdf, n, L, v):
    nL = L @ n
    nv = n + v
    R = nv[:, None] @ nv[None] / (1 + n[2]) - np.eye(3)
    wo = (R @ v).tolist()

    ret = np.zeros(L.shape, dtype=np.float)
    for j in range(len(L)):
        if nL[j] <= 0: continue
        wi = (R @ L[j]).tolist()

        rho = np.array(brdf.eval(wi, wo), dtype=np.float)
        rho[rho < 0] = 0
        ret[j] = rho * nL[j]

    return i, ret


def main(brdf_dir, obj_file, obj_range, N_map_file, mask_file, L_file, out_dir, save_npy, n_jobs):
    obj_names = np.loadtxt(obj_file, dtype=np.str)
    N_map = np.load(N_map_file)
    mask = cv2.imread(mask_file, 0)
    N = N_map[mask > 0] # (P, 3)
    N = N / np.linalg.norm(N, axis=1, keepdims=True)

    L = np.loadtxt(L_file) # (L, 3) 
    L = L / np.linalg.norm(L, axis=1, keepdims=True)
    v = np.array([0., 0., 1.], dtype=np.float)

    for i_obj, obj_name in enumerate(obj_names[obj_range[0]:obj_range[1]]):
        print('===== {} - {} start ====='.format(i_obj, obj_name))

        brdf = BRDF(os.path.join(brdf_dir, obj_name + '_rgb.bsdf'))

        ret = Parallel(n_jobs=n_jobs, verbose=5, prefer='threads')([delayed(render)(i, brdf, N[i], L, v) for i in range(len(N))])
        ret.sort(key=lambda x: x[0])
        M = np.array([x[1] for x in ret], dtype=np.float)
        M = M / M.max()

        imgs = np.zeros((len(L),) + N_map.shape)
        imgs[:, mask > 0] = M.transpose(1, 0, 2)

        out_path = os.path.join(out_dir, obj_name)
        if not os.path.exists(out_path):
            os.makedirs(out_path)

        print('Saving images...')
        fnames = []
        for i, img in enumerate(tqdm(imgs)):
            if save_npy:
                fname = '{:03d}.npy'.format(i + 1)
                fnames.append(fname)
                np.save(os.path.join(out_path, fname), img)
            else:
                fname = '{:03d}.png'.format(i + 1)
                fnames.append(fname)
                img = img * np.iinfo(np.uint16).max
                cv2.imwrite(os.path.join(out_path, fname), img[..., ::-1].astype(np.uint16))
        with open(os.path.join(out_path, 'filenames.txt'), 'w') as f:
            f.write('\n'.join(fnames))
        np.save(os.path.join(out_path, 'normal_gt.npy'), N_map)
        shutil.copyfile(mask_file, os.path.join(out_path, 'mask.png'))
        shutil.copyfile(L_file, os.path.join(out_path, 'light_directions.txt'))

        print('===== {} - {} done ====='.format(i_obj, obj_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--brdf_dir', type=str, required=True)
    parser.add_argument('--obj_file', type=str, required=True)
    parser.add_argument('--obj_range', type=int, nargs=2, required=True)
    parser.add_argument('--N_map_file', type=str, required=True)
    parser.add_argument('--mask_file', type=str, required=True)
    parser.add_argument('--L_file', type=str, required=True)
    parser.add_argument('--out_dir', type=str, required=True)
    parser.add_argument('--save_npy', action='store_true')
    parser.add_argument('--n_jobs', type=int, default=1)
    args = parser.parse_args()

    main(brdf_dir=args.brdf_dir,
         obj_file=args.obj_file,
         obj_range=args.obj_range,
         N_map_file=args.N_map_file,
         mask_file=args.mask_file,
         L_file=args.L_file,
         out_dir=args.out_dir,
         save_npy=args.save_npy,
         n_jobs=args.n_jobs)

