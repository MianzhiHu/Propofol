from atlasTransform.atlasTransform.utils.atlas import load_shen_268
from nilearn import plotting, datasets, surface, image
import nibabel
import numpy as np
from plotting_preparation import new_df_movie_02
from make_side_by_side_surf_plots import make_side_by_side_surf_plots

# select only the first column of the new_df dataframe and save it to a list
# hurst = new_df.iloc[:, 0].tolist()
# hurst_movie_03 = new_df_movie_03.iloc[:, 0].tolist()
hurst_movie_02 = new_df_movie_02.iloc[:, 0].tolist()

# check the range of the hurst values discarding NaN values
print(min([x for x in hurst_movie_02 if str(x) != 'nan']))
print(max([x for x in hurst_movie_02 if str(x) != 'nan']))

# # convert the list to absolute values
# hurst = [abs(number) for number in hurst]

def brain_plotting (df, title, vmin, vmax, cmap):
    fsaverage = datasets.fetch_surf_fsaverage()

    atlas = load_shen_268(1)
    dr = atlas.get_data()
    dd = dr.copy().astype('float')
    labels = np.unique(dr)
    for i in np.array(list(range(268))):
        dd[dr == labels[i+1]] = df[i]
    new_image_atl = nibabel.Nifti1Image(dd, atlas.affine)
    texture = surface.vol_to_surf(new_image_atl, fsaverage.pial_right)
    make_side_by_side_surf_plots(title,texture,vmin=vmin,vmax=vmax,cmap=cmap)

# brain_plotting(hurst, 'absolute brain loadings', 0, 0.15, 'Reds')
# brain_plotting(hurst_movie_03, 'brain loadings', -0.3, 0.3, 'RdBu_r')
brain_plotting(hurst_movie_02, 'brain loadings', -0.3, 0.3, 'RdBu_r')


